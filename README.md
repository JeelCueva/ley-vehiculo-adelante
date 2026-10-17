# La Ley del Vehículo de Adelante: saliencia y percepción del crecimiento económico

Datos y código de replicación del artículo:

> Cueva Laguna, J. E. (2026). *La Ley del Vehículo de Adelante: saliencia y percepción del crecimiento económico*. Manuscrito enviado a la revista IECOS, Universidad Nacional de Ingeniería.

**Autor:** Jeel Elvis Cueva Laguna. Facultad de Ingeniería Económica, Estadística y Ciencias Sociales, Universidad Nacional de Ingeniería, Lima, Perú.

## Contenido

| Archivo | Descripción |
|---|---|
| `datos_crecimiento_bm_2023_2025.csv` | Crecimiento anual del PBI real (%) de 186 a 204 economías, 2023-2025 (590 observaciones). |
| `replicacion.py` | Reproduce las tablas 1 a 5 del artículo: posición del Perú, Índice de Rezago Percibido, umbral de saliencia, robustez y simulación de Monte Carlo. |
| `figuras.py` | Genera las figuras 1 a 3 en PNG a 300 dpi y 16 cm de ancho. |
| `figuras/` | Figuras del artículo. |
| `requirements.txt` | Bibliotecas de Python necesarias. |

## Fuente de los datos

Banco Mundial, *World Development Indicators*, indicador `NY.GDP.MKTP.KD.ZG` (crecimiento del PIB real, % anual). Página pública: https://data.worldbank.org/indicator/NY.GDP.MKTP.KD.ZG. Descargado mediante la API v2 (https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.KD.ZG) el 16 de octubre de 2026. Las series de 2023 y 2024 corresponden a la actualización del 8 de octubre de 2026 y la de 2025 a la del 13 de julio de 2026. Se excluyeron los agregados regionales y por nivel de ingreso.

Columnas del CSV: `iso3` (código de país ISO 3166-1 alfa-3), `anio`, `crecimiento_pbi_real` (en %).

## Cómo reproducir los resultados

Requiere Python 3.9 o superior.

```bash
pip install -r requirements.txt
python replicacion.py   # imprime las cifras de las tablas
python figuras.py       # regenera las figuras en ./figuras
```

La simulación usa la semilla 1, por lo que los resultados son idénticos en cada ejecución.

## Licencias

- Código (`*.py`): licencia MIT (ver `LICENSE`).
- Datos: provienen del Banco Mundial y se redistribuyen bajo la licencia [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), con atribución a la fuente original.
- Figuras: CC BY 4.0.

## Cómo citar

Ver `CITATION.cff`. Tras el archivo en Zenodo, citar con el DOI asignado.
