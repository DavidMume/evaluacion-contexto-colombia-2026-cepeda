"""Genera visualizaciones para el proyecto evaluacion-contexto-colombia-2026-cepeda.

Graficos producidos:
    1. alineacion_plan_necesidades.png  — puntaje de alineacion por area
    2. riesgo_implementacion.png        — riesgo de implementacion por area
    3. alineacion_vs_riesgo.png         — scatter: alineacion vs riesgo
    4. indicadores_contexto.png         — panel de indicadores contextuales de Colombia

Uso:
    cd evaluacion-contexto-colombia-2026-cepeda
    python scripts/graficar_alineacion.py

Requiere: pandas matplotlib numpy
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs" / "charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PALETTE_BLUE = "#2166ac"
PALETTE_RED = "#d6604d"
PALETTE_GREEN = "#4dac26"
FONT_TITLE = {"fontsize": 13, "fontweight": "bold"}
FONT_AXIS = {"fontsize": 10}
DPI = 200

# ── helpers ──────────────────────────────────────────────────────────────────

def bar_colors(values, low_thresh=2.5, high_thresh=3.5):
    colors = []
    for v in values:
        if v >= high_thresh:
            colors.append(PALETTE_GREEN)
        elif v >= low_thresh:
            colors.append("#f4a582")
        else:
            colors.append(PALETTE_RED)
    return colors


def risk_colors(values, low_thresh=2.5, high_thresh=3.5):
    colors = []
    for v in values:
        if v <= low_thresh:
            colors.append(PALETTE_GREEN)
        elif v <= high_thresh:
            colors.append("#f4a582")
        else:
            colors.append(PALETTE_RED)
    return colors


# ── 1. Alineacion por area ───────────────────────────────────────────────────

def chart_alineacion(df: pd.DataFrame) -> None:
    df_s = df.sort_values("alineacion_1_5", ascending=True).copy()
    colors = bar_colors(df_s["alineacion_1_5"])

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(df_s["area"], df_s["alineacion_1_5"], color=colors, edgecolor="white", height=0.6)

    for bar, val in zip(bars, df_s["alineacion_1_5"]):
        ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}", va="center", ha="left", fontsize=9)

    ax.set_xlim(0, 5.5)
    ax.set_xlabel("Puntaje de alineacion (1 = minimo, 5 = maximo)", **FONT_AXIS)
    ax.set_title("Alineacion del plan de Cepeda con las necesidades de Colombia, 2026",
                 **FONT_TITLE, pad=12)
    ax.axvline(3, color="gray", linestyle="--", linewidth=0.8, alpha=0.6, label="Umbral medio (3)")

    legend_patches = [
        mpatches.Patch(color=PALETTE_GREEN, label="Alta alineacion (>= 3.5)"),
        mpatches.Patch(color="#f4a582", label="Alineacion parcial (2.5-3.5)"),
        mpatches.Patch(color=PALETTE_RED, label="Baja alineacion (< 2.5)"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=8)
    ax.tick_params(axis="y", labelsize=9)

    plt.tight_layout()
    path = OUT_DIR / "alineacion_plan_necesidades.png"
    plt.savefig(path, dpi=DPI)
    plt.close()
    print(f"[OK] {path.relative_to(ROOT)}")


# ── 2. Riesgo de implementacion ──────────────────────────────────────────────

def chart_riesgo(df: pd.DataFrame) -> None:
    df_s = df.sort_values("riesgo_implementacion", ascending=True).copy()
    colors = risk_colors(df_s["riesgo_implementacion"])

    fig, ax = plt.subplots(figsize=(11, 6))
    bars = ax.barh(df_s["area"], df_s["riesgo_implementacion"], color=colors, edgecolor="white", height=0.6)

    for bar, val in zip(bars, df_s["riesgo_implementacion"]):
        ax.text(val + 0.05, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}", va="center", ha="left", fontsize=9)

    ax.set_xlim(0, 5.5)
    ax.set_xlabel("Riesgo de implementacion (1 = bajo, 5 = muy alto)", **FONT_AXIS)
    ax.set_title("Riesgo de implementacion por area de politica publica — Plan Cepeda 2026",
                 **FONT_TITLE, pad=12)
    ax.axvline(3, color="gray", linestyle="--", linewidth=0.8, alpha=0.6, label="Umbral medio (3)")

    legend_patches = [
        mpatches.Patch(color=PALETTE_GREEN, label="Riesgo bajo (<= 2.5)"),
        mpatches.Patch(color="#f4a582", label="Riesgo medio (2.5-3.5)"),
        mpatches.Patch(color=PALETTE_RED, label="Riesgo alto (> 3.5)"),
    ]
    ax.legend(handles=legend_patches, loc="lower right", fontsize=8)
    ax.tick_params(axis="y", labelsize=9)

    plt.tight_layout()
    path = OUT_DIR / "riesgo_implementacion.png"
    plt.savefig(path, dpi=DPI)
    plt.close()
    print(f"[OK] {path.relative_to(ROOT)}")


# ── 3. Scatter: alineacion vs riesgo ────────────────────────────────────────

def chart_scatter(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 7))

    scatter = ax.scatter(
        df["alineacion_1_5"],
        df["riesgo_implementacion"],
        s=120,
        c=df["alineacion_1_5"],
        cmap="RdYlGn",
        vmin=1,
        vmax=5,
        edgecolors="gray",
        linewidths=0.5,
        zorder=3,
    )
    plt.colorbar(scatter, ax=ax, label="Puntaje de alineacion")

    for _, row in df.iterrows():
        label = row["area"]
        x, y = row["alineacion_1_5"], row["riesgo_implementacion"]
        ax.annotate(
            label,
            xy=(x, y),
            xytext=(6, 3),
            textcoords="offset points",
            fontsize=7.5,
            ha="left",
        )

    ax.axhline(3, color="gray", linestyle="--", linewidth=0.7, alpha=0.5)
    ax.axvline(3, color="gray", linestyle="--", linewidth=0.7, alpha=0.5)

    ax.set_xlabel("Alineacion con necesidades nacionales (1-5)", **FONT_AXIS)
    ax.set_ylabel("Riesgo de implementacion (1-5)", **FONT_AXIS)
    ax.set_title("Alineacion vs Riesgo de implementacion — Plan Cepeda 2026",
                 **FONT_TITLE, pad=12)
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)

    ax.text(4.2, 4.6, "Alta alineacion\nAlto riesgo", fontsize=7, color="gray", ha="center")
    ax.text(1.2, 4.6, "Baja alineacion\nAlto riesgo", fontsize=7, color="gray", ha="center")
    ax.text(4.2, 1.1, "Alta alineacion\nBajo riesgo", fontsize=7, color="gray", ha="center")
    ax.text(1.2, 1.1, "Baja alineacion\nBajo riesgo", fontsize=7, color="gray", ha="center")

    plt.tight_layout()
    path = OUT_DIR / "alineacion_vs_riesgo.png"
    plt.savefig(path, dpi=DPI)
    plt.close()
    print(f"[OK] {path.relative_to(ROOT)}")


# ── 4. Panel de indicadores contextuales ────────────────────────────────────

def chart_indicadores(df_ind: pd.DataFrame) -> None:
    subset = df_ind[df_ind["indicador"].isin([
        "inflacion_total",
        "inflacion_basica",
        "proyeccion_inflacion_dic_2026",
        "crecimiento_pib_2025",
        "crecimiento_pib_2026_banrep",
        "crecimiento_pib_2026_banco_mundial",
        "pobreza_multidimensional",
        "desempleo_abril_2026",
        "informalidad_laboral",
        "deficit_fiscal_pib",
    ])].copy()

    labels = {
        "inflacion_total": "Inflacion total Q1 2026",
        "inflacion_basica": "Inflacion basica Q1 2026",
        "proyeccion_inflacion_dic_2026": "Proyeccion inflacion Dic 2026",
        "crecimiento_pib_2025": "Crecimiento PIB 2025",
        "crecimiento_pib_2026_banrep": "Crecimiento PIB 2026 (BanRep)",
        "crecimiento_pib_2026_banco_mundial": "Crecimiento PIB 2026 (BM)",
        "pobreza_multidimensional": "Pobreza multidimensional 2025",
        "desempleo_abril_2026": "Desempleo Abr 2026",
        "informalidad_laboral": "Informalidad laboral 2025",
        "deficit_fiscal_pib": "Deficit fiscal / PIB",
    }
    subset["etiqueta"] = subset["indicador"].map(labels)

    fig, ax = plt.subplots(figsize=(11, 6))
    colors_ind = [
        "#d6604d", "#d6604d", "#d6604d",
        "#4dac26", "#4dac26", "#4dac26",
        "#2166ac", "#2166ac",
        "#f4a582",
        "#d6604d",
    ]
    bars = ax.barh(subset["etiqueta"], subset["valor"], color=colors_ind[:len(subset)],
                   edgecolor="white", height=0.6)

    for bar, val in zip(bars, subset["valor"]):
        ax.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                f"{val:.1f}%", va="center", ha="left", fontsize=9)

    ax.set_xlabel("Valor (%)", **FONT_AXIS)
    ax.set_title("Indicadores de contexto — Colombia 2026", **FONT_TITLE, pad=12)
    ax.tick_params(axis="y", labelsize=9)
    ax.set_xlim(0, 65)

    legend_patches = [
        mpatches.Patch(color="#d6604d", label="Presiones / riesgos"),
        mpatches.Patch(color="#4dac26", label="Crecimiento economico"),
        mpatches.Patch(color="#2166ac", label="Mercado laboral"),
        mpatches.Patch(color="#f4a582", label="Informalidad"),
    ]
    ax.legend(handles=legend_patches, fontsize=8, loc="lower right")

    plt.tight_layout()
    path = OUT_DIR / "indicadores_contexto.png"
    plt.savefig(path, dpi=DPI)
    plt.close()
    print(f"[OK] {path.relative_to(ROOT)}")


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    df = pd.read_csv(DATA_DIR / "alineacion_plan_necesidades_2026.csv")
    df_ind = pd.read_csv(DATA_DIR / "indicadores_contexto_colombia_2026.csv")

    print("Generando graficos...")
    chart_alineacion(df)
    chart_riesgo(df)
    chart_scatter(df)
    chart_indicadores(df_ind)
    print(f"\nTodos los graficos guardados en: outputs/charts/")


if __name__ == "__main__":
    main()
