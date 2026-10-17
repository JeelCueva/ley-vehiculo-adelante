"""
Genera las figuras del artículo como archivos PNG independientes
(300 dpi, 16 cm de ancho), según las normas de las revistas de la UNI.

Uso: python figuras.py   (requiere numpy, matplotlib; lee el CSV de datos)
"""
import csv
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import FuncFormatter

CM = 1 / 2.54
ANCHO = 16 * CM
DPI = 300
ACENTO = "#1F5EAA"
GRIS = "#8C8C8C"
GRIS_CLARO = "#C8C8C8"
os.makedirs("figuras", exist_ok=True)

# Tipografía tipo Palatino (TeX Gyre Pagella si está disponible)
for f in font_manager.findSystemFonts():
    if "texgyrepagella" in f.lower():
        font_manager.fontManager.addfont(f)
fam = "TeX Gyre Pagella" if any("Pagella" in f.name for f in font_manager.fontManager.ttflist) else "serif"
plt.rcParams.update({
    "font.family": fam, "font.size": 10, "axes.spines.top": False,
    "axes.spines.right": False, "axes.edgecolor": "#444444",
    "axes.grid": True, "grid.color": "#E6E6E6", "grid.linewidth": 0.6,
    "axes.axisbelow": True, "legend.frameon": False,
    "mathtext.fontset": "custom", "mathtext.rm": fam, "mathtext.it": f"{fam}:italic",
})

coma = lambda dec: FuncFormatter(lambda v, _: f"{v:.{dec}f}".replace(".", ",").replace("-", "\u2212"))
pct = FuncFormatter(lambda v, _: f"{v * 100:.0f} %")


def cargar(ruta="datos_crecimiento_bm_2023_2025.csv"):
    d = {}
    with open(ruta, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d.setdefault(int(r["anio"]), {})[r["iso3"]] = float(r["crecimiento_pbi_real"])
    return d


def referencia(g, lam):
    w = np.exp(lam * (g - g.max()))
    return float((w * g).sum() / w.sum())


def winsor(g):
    a, b = np.percentile(g, [2.5, 97.5])
    return np.clip(g, a, b)


datos = cargar()

# ---------------- Figura 1: Ley del Vehículo de Adelante ----------------
N = np.arange(2, 201)
fig, ax = plt.subplots(figsize=(ANCHO, 8.5 * CM))
for p, c, lw, lab in [(0.90, GRIS_CLARO, 1.6, "Percentil 90"),
                      (0.95, GRIS, 1.6, "Percentil 95"),
                      (0.99, ACENTO, 2.4, "Percentil 99")]:
    ax.plot(N, 1 - p ** (N - 1), color=c, lw=lw, label=lab)
ax.axhline(0.5, color="#555555", lw=0.9, ls="--")
ax.text(198, 0.515, "50 %", ha="right", va="bottom", fontsize=9, color="#555555")
ax.plot(70, 0.5, "o", mfc="white", mec=ACENTO, ms=7, mew=1.5)
ax.annotate("N = 70: 50 %", (70, 0.5), xytext=(80, 0.38), fontsize=9,
            arrowprops=dict(arrowstyle="-", color="#555555", lw=0.7))
p190 = 1 - 0.99 ** 189
ax.plot(190, p190, "o", color=ACENTO, ms=5)
ax.annotate(f"{p190 * 100:.0f} % con N = 190".replace(".", ","), (190, p190),
            xytext=(150, 0.95), fontsize=9, color=ACENTO,
            arrowprops=dict(arrowstyle="-", color=ACENTO, lw=0.7))
ax.set_xlim(0, 200)
ax.set_ylim(0, 1.04)
ax.yaxis.set_major_formatter(pct)
ax.set_xlabel("Número de economías comparadas (N)")
ax.set_ylabel("Probabilidad de tener al menos\nuna economía adelante")
ax.legend(loc="lower right", fontsize=9)
fig.tight_layout()
fig.savefig("figuras/figura1.png", dpi=DPI)
plt.close(fig)

# ---------------- Figura 2: distribución 2024 ----------------
g = np.array(list(datos[2024].values()))
gp = datos[2024]["PER"]
gw = winsor(g)
mu = gw.mean()
r10, r20 = referencia(gw, 0.10), referencia(gw, 0.20)
fig, ax = plt.subplots(figsize=(ANCHO, 8.5 * CM))
dentro = g[(g >= -6) & (g < 12)]
ax.hist(dentro, bins=np.arange(-6, 13, 1), color=GRIS_CLARO, edgecolor="white", lw=0.8)
ymax = 50
ax.axvline(mu, color="#555555", ls="--", lw=1.1)
ax.text(mu - 0.15, ymax * 0.99, f"Promedio {mu:.2f}".replace(".", ","), ha="right", va="top",
        fontsize=9, color="#555555")
ax.axvline(gp, color=ACENTO, lw=2.2)
ax.text(gp + 0.15, ymax * 0.99, f"Perú {gp:.2f}".replace(".", ","), ha="left", va="top",
        fontsize=9.5, color=ACENTO, fontweight="bold")
for val, y, ls, lab in [(r10, 41, "-", "λ = 0,10"), (r20, 34, ":", "λ = 0,20")]:
    ax.plot([val, val], [0, y], color="black", lw=1.2, ls=ls)
    ax.plot([val, 6.0], [y, y], color="black", lw=0.6)
    ax.text(6.1, y, f"r({lab.split('= ')[1]}) = {val:.2f}".replace(".", ","), va="center", fontsize=9,
            bbox=dict(fc="white", ec="none", pad=1))
ax.set_xlim(-6, 12)
ax.set_ylim(0, 52)
ax.set_xticks(range(-6, 13, 2))
ax.set_xlabel("Crecimiento del PBI real en 2024 (%)")
ax.set_ylabel("Número de economías")
ax.grid(axis="x", visible=False)
fig.tight_layout()
fig.savefig("figuras/figura2.png", dpi=DPI)
plt.close(fig)

# ---------------- Figura 3: IRP del Perú según lambda ----------------
lams = np.linspace(0, 0.30, 61)
fig, ax = plt.subplots(figsize=(ANCHO, 8.0 * CM))
estilos = {2024: dict(color=ACENTO, lw=2.4), 2025: dict(color=GRIS, lw=1.6)}
for anio in (2024, 2025):
    g = np.array(list(datos[anio].values()))
    gw = winsor(g)
    sd = gw.std(ddof=1)
    gj = datos[anio]["PER"]
    irp = [(referencia(gw, L) - gj) / sd for L in lams]
    ax.plot(lams, irp, label=str(anio), **estilos[anio])
ax.axhline(0, color="#555555", lw=0.9, ls="--")
lstar = 0.055
ax.plot(lstar, 0, "o", mfc="white", mec=ACENTO, ms=7, mew=1.5)
ax.annotate("λ* (2024) = 0,055", (lstar, 0), xytext=(0.075, -0.17), fontsize=9, color=ACENTO,
            arrowprops=dict(arrowstyle="-", color=ACENTO, lw=0.7))
ax.text(0.297, 0.03, "Se percibe detrás", ha="right", va="bottom", fontsize=8.5, color="#555555")
ax.text(0.297, -0.03, "Se percibe adelante", ha="right", va="top", fontsize=8.5, color="#555555")
ax.set_xlim(0, 0.30)
ax.set_ylim(-0.3, 0.9)
ax.xaxis.set_major_formatter(coma(2))
ax.yaxis.set_major_formatter(coma(1))
ax.set_xlabel("Sesgo de saliencia (λ)")
ax.set_ylabel("IRP del Perú (desv. est.)")
ax.legend(loc="upper left", fontsize=9)
fig.tight_layout()
fig.savefig("figuras/figura3.png", dpi=DPI)
plt.close(fig)
print("Figuras guardadas en ./figuras con", fam)
