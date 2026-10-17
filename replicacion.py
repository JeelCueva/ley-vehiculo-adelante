"""
Replicación de resultados: "La Ley del Vehículo de Adelante".

Reproduce los cuadros 1 a 4 y la simulación del Apéndice B a partir de
datos_crecimiento_bm_2023_2025.csv (Banco Mundial, WDI, NY.GDP.MKTP.KD.ZG).

Uso:  python replicacion.py
Requisitos: Python 3.9+, numpy, scipy.
"""
import csv
import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

ARCHIVO = "datos_crecimiento_bm_2023_2025.csv"
PAIS = "PER"
LATAM = ["ARG", "BOL", "BRA", "CHL", "COL", "CRI", "DOM", "ECU", "SLV",
         "GTM", "HND", "MEX", "NIC", "PAN", "PRY", "PER", "URY", "VEN"]
LAMBDAS = [0.0, 0.05, 0.10, 0.20]


def cargar(ruta=ARCHIVO):
    datos = {}
    with open(ruta, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            anio = int(fila["anio"])
            datos.setdefault(anio, {})[fila["iso3"]] = float(fila["crecimiento_pbi_real"])
    return datos


def referencia(g, lam):
    """Referencia ponderada por saliencia, ecuación (7)."""
    w = np.exp(lam * (g - g.max()))
    w /= w.sum()
    return float((w * g).sum())


def winsorizar(g, bajo=2.5, alto=97.5):
    a, b = np.percentile(g, [bajo, alto])
    return np.clip(g, a, b)


def umbral_saliencia(gw, gj):
    """Menor lambda con r(lambda) >= g_j (raíz empírica)."""
    f = lambda lam: referencia(gw, lam) - gj
    if f(0.0) >= 0:
        return 0.0
    return brentq(f, 0.0, 5.0)


def main():
    datos = cargar()
    for anio in sorted(datos):
        d = datos[anio]
        g = np.array(list(d.values()))
        gj = d[PAIS]
        gw = winsorizar(g)
        mu, sd = gw.mean(), gw.std(ddof=1)
        A = int((g > gj).sum())
        lat = {c: d[c] for c in LATAM if c in d}
        print(f"\n===== {anio} =====")
        print(f"N = {len(g)}, crecimiento {PAIS} = {gj:.2f} %")
        print(f"Promedio = {g.mean():.2f}, mediana = {np.median(g):.2f}")
        print(f"Economías adelante A = {A}, PA = {A / (len(g) - 1):.3f}, percentil = {100 * (g < gj).mean():.1f}")
        lider = max(d, key=d.get)
        print(f"Líder mundial: {lider} ({d[lider]:.1f} %)")
        print(f"Adelante en América Latina: {sum(v > gj for v in lat.values())} de {len(lat) - 1}")
        print(f"Media y desv. est. winsorizadas: {mu:.2f}, {sd:.2f}")
        for lam in LAMBDAS:
            r = referencia(gw, lam)
            print(f"  lambda = {lam:.2f}: r = {r:.2f}, IRP = {(r - gj) / sd:+.2f}")
        r10 = referencia(gw, 0.10)
        print(f"Fracción rezagada (lambda = 0,10): predicha {norm.cdf(0.10 * sd):.3f}, observada {(gw < r10).mean():.3f}")
        print(f"Umbral de saliencia: empírico {umbral_saliencia(gw, gj):.3f}, normal {max(0.0, (gj - mu) / sd ** 2):.3f}")
        gl = np.array(list(lat.values()))
        print(f"Referencia latinoamericana: IRP(0,10) = {(referencia(gl, 0.10) - gj) / gl.std(ddof=1):+.2f}")
        # Cuadro de robustez
        for bajo, alto in [(1, 99), (2.5, 97.5), (5, 95)]:
            gv = winsorizar(g, bajo, alto)
            sv = gv.std(ddof=1)
            print(f"  Winsorización {bajo}-{alto}: IRP(0,10) = {(referencia(gv, 0.10) - gj) / sv:+.2f}, "
                  f"umbral = {umbral_saliencia(gv, gj):.3f}")
        a, b = np.percentile(g, [2.5, 97.5])
        gt = g[(g >= a) & (g <= b)]
        print(f"  Recorte 2,5-97,5: IRP(0,10) = {(referencia(gt, 0.10) - gj) / gt.std(ddof=1):+.2f}")
        r_bruta = referencia(g, 0.10)
        print(f"  Sin winsorizar: r(0,10) = {r_bruta:.1f} %")

    # Apéndice B: simulación de Monte Carlo
    rng = np.random.default_rng(1)
    R, N, mu, s, lam = 20000, 190, 3.0, 3.0, 0.10
    otros = rng.random((R, N - 1))
    print("\n===== Simulación =====")
    print(f"Pr(A >= 1 | p = 0,99, N = 190): fórmula {1 - 0.99 ** 189:.3f}, simulación {(otros > 0.99).any(1).mean():.3f}")
    g = rng.normal(mu, s, (R, N))
    w = np.exp(lam * g)
    w /= w.sum(1, keepdims=True)
    r = (w * g).sum(1)
    print(f"r(lambda): fórmula {mu + lam * s ** 2:.3f}, simulación {r.mean():.3f}")
    print(f"Fracción rezagada: fórmula {norm.cdf(lam * s):.3f}, simulación {(g < r[:, None]).mean():.3f}")


if __name__ == "__main__":
    main()
