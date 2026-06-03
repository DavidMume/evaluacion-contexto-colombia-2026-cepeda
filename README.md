# evaluacion-contexto-colombia-2026-cepeda

**Evaluación del plan de gobierno de Iván Cepeda frente a las necesidades actuales de Colombia, 2026**

---

## Descripción del proyecto

El proyecto anterior ([analisis-plan-gobierno-ivan-cepeda-2026](https://github.com/DavidMume/analisis-plan-gobierno-ivan-cepeda-2026)) analizó *qué dice* el programa de gobierno de Iván Cepeda Castro mediante NLP y análisis de discurso: frecuencias léxicas, modelado de tópicos, análisis de sentimiento, redes semánticas, reconocimiento de entidades nombradas y métricas retóricas.

**Este segundo proyecto evalúa si esas prioridades responden a las necesidades actuales de Colombia en 2026.**

---

## Pregunta de investigación

> ¿El plan de gobierno de Iván Cepeda responde a las necesidades estructurales e inmediatas de Colombia en 2026, especialmente en inflación, sostenibilidad fiscal, productividad, formalización laboral, seguridad, desigualdad territorial, desarrollo rural, salud, educación y paz?

---

## Diferencia respecto al repositorio original

| Dimensión | Proyecto 1 (NLP) | Proyecto 2 (este repositorio) |
|---|---|---|
| Objeto de análisis | Texto del programa de gobierno | Contexto nacional vs. prioridades del plan |
| Método principal | Procesamiento de lenguaje natural | Evaluación de política pública con indicadores |
| Pregunta central | ¿Qué dice el plan? | ¿El plan responde a lo que Colombia necesita? |
| Datos | Texto del programa | Indicadores macroeconómicos y sociales |
| Salida | Frecuencias, tópicos, redes semánticas | Puntajes de alineación, riesgos, gráficos |

---

## Metodología

1. Se extraen los énfasis discursivos del programa mediante el análisis NLP del proyecto original.
2. Se recopilan indicadores contextuales de Colombia 2026 (inflación, crecimiento, empleo, pobreza, seguridad, desigualdad territorial).
3. Se construye una matriz de alineación (escala 1–5) entre las prioridades del plan y las necesidades nacionales.
4. Se evalúa el riesgo de implementación por área de política pública.
5. Se generan visualizaciones para comparar alineación y riesgo.

**Sistema de citación:** Harvard autor-fecha. Ver [`docs/referencias_harvard.md`](docs/referencias_harvard.md).

---

## Estructura del proyecto

```text
evaluacion-contexto-colombia-2026-cepeda/
│
├── README.md
│
├── docs/
│   ├── evaluacion_contexto_colombia_2026.md   ← análisis principal
│   └── referencias_harvard.md                 ← fuentes completas
│
├── data/
│   ├── alineacion_plan_necesidades_2026.csv   ← matriz de alineación y riesgo
│   └── indicadores_contexto_colombia_2026.csv ← indicadores de contexto
│
├── scripts/
│   └── graficar_alineacion.py                 ← genera todos los gráficos
│
├── outputs/
│   └── charts/
│       ├── alineacion_plan_necesidades.png
│       ├── riesgo_implementacion.png
│       ├── alineacion_vs_riesgo.png
│       └── indicadores_contexto.png
│
├── requirements.txt
└── .gitignore
```

---

## Fuentes de datos

| Fuente | Tipo | Área |
|---|---|---|
| Banco de la República (2026) | Informe de Política Monetaria | Inflación, crecimiento, tasa de interés |
| World Bank (2026) | Country Overview | Crecimiento, productividad, desigualdad territorial |
| El País (2026a-d) | Prensa internacional | Empleo, pobreza, déficit fiscal |
| Reuters (2026) | Prensa internacional | Seguridad, conflicto armado |
| Associated Press (2026) | Prensa internacional | Crimen organizado, extorsión |
| Muñoz (2026) | Repositorio GitHub | Análisis NLP del programa de gobierno |

---

## Cómo ejecutar el análisis

### 1. Requisitos

```bash
pip install -r requirements.txt
```

### 2. Generar todos los gráficos

Desde la raíz del repositorio:

```bash
python scripts/graficar_alineacion.py
```

Los gráficos se guardan automáticamente en `outputs/charts/`.

### 3. Explorar los datos

```python
import pandas as pd

df = pd.read_csv("data/alineacion_plan_necesidades_2026.csv")
print(df[["area", "alineacion_1_5", "riesgo_implementacion"]])

df_ind = pd.read_csv("data/indicadores_contexto_colombia_2026.csv")
print(df_ind[["indicador", "valor", "unidad"]])
```

---

## Gráficos generados

| Archivo | Descripción |
|---|---|
| `alineacion_plan_necesidades.png` | Barras horizontales: puntaje de alineación por área de política pública |
| `riesgo_implementacion.png` | Barras horizontales: riesgo de implementación por área |
| `alineacion_vs_riesgo.png` | Scatter: alineación vs. riesgo (posiciona cada área en un cuadrante) |
| `indicadores_contexto.png` | Panel de indicadores macroeconómicos y sociales de Colombia 2026 |

---

## Conexión con el proyecto NLP original

Este proyecto consume los resultados del repositorio [`analisis-plan-gobierno-ivan-cepeda-2026`](https://github.com/DavidMume/analisis-plan-gobierno-ivan-cepeda-2026). Los énfasis discursivos identificados mediante NLP (frecuencias, bigramas, tópicos) se traducen aquí en puntajes de alineación frente a indicadores empíricos de Colombia.

El flujo analítico completo es:

```text
Texto del programa → NLP (repo 1) → Énfasis discursivos
                                            ↓
Indicadores de contexto Colombia 2026 → Matriz de alineación (este repo)
                                            ↓
                               Gráficos + análisis interpretativo
```

---

## Contribución analítica principal

El plan de Cepeda es fuerte como agenda de justicia histórica y transformación social (derechos humanos, reforma agraria, inclusión). Sin embargo, muestra menor centralidad discursiva en áreas que Colombia necesita urgentemente en 2026: estabilidad fiscal, productividad, inversión privada y formalización laboral. Esta brecha entre el énfasis redistributivo y los retos macroeconómicos constituye el hallazgo central de este proyecto.

---

## Cómo inicializar y publicar en GitHub

```bash
cd evaluacion-contexto-colombia-2026-cepeda
git init
git add .
git commit -m "Initial commit: evaluacion-contexto-colombia-2026-cepeda"
git remote add origin https://github.com/DavidMume/evaluacion-contexto-colombia-2026-cepeda.git
git branch -M main
git push -u origin main
```

---

## Autor

David Muñoz  
Proyecto: `evaluacion-contexto-colombia-2026-cepeda`  
Fecha: Junio 2026  
Citación del proyecto original: Muñoz, D. (2026) *Análisis computacional del programa de gobierno de Iván Cepeda Castro*. GitHub. Available at: https://github.com/DavidMume/analisis-plan-gobierno-ivan-cepeda-2026
