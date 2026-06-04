"""
Genera visualizaciones de verificabilidad de las cifras del plan de gobierno Cepeda 2026-2030.

Salida:
    outputs/charts/verificabilidad_resumen.png
    outputs/charts/verificabilidad_por_tema.png
    outputs/charts/cifras_clave_comparacion.png

Uso:
    python scripts/graficar_verificabilidad.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

ROOT    = Path(__file__).resolve().parent.parent
DATA    = ROOT / "data" / "verificabilidad_cifras_plan_cepeda.csv"
OUT_DIR = ROOT / "outputs" / "charts"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DPI = 200

COLORES_ESTADO = {
    "Consistente":         "#27ae60",
    "Con matices":         "#f39c12",
    "Plausible":           "#2980b9",
    "Ambicioso":           "#8e44ad",
    "Sobreestimado":       "#e74c3c",
    "Requiere contexto":   "#e67e22",
}

COLORES_VERIF = {
    "VERIFICABLE":                "#27ae60",
    "PARCIALMENTE VERIFICABLE":   "#f39c12",
    "NO CONSISTENTE":             "#e74c3c",
    "CON MATICES":                "#e67e22",
}


def donut_verificabilidad(df):
    """Dona: distribucion por tipo de verificabilidad."""
    conteo = df["verificabilidad"].value_counts()
    colores = [COLORES_VERIF.get(k, "#95a5a6") for k in conteo.index]

    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(
        conteo.values,
        labels=None,
        colors=colores,
        autopct="%1.0f%%",
        pctdistance=0.75,
        startangle=90,
        wedgeprops=dict(width=0.55, edgecolor="white", linewidth=2),
    )
    for at in autotexts:
        at.set_fontsize(11)
        at.set_fontweight("bold")
        at.set_color("white")

    leyenda = [mpatches.Patch(color=COLORES_VERIF.get(k, "#95a5a6"), label=f"{k} ({v})")
               for k, v in conteo.items()]
    ax.legend(handles=leyenda, loc="lower center", bbox_to_anchor=(0.5, -0.15),
              fontsize=9, ncol=2, frameon=False)

    ax.set_title("Verificabilidad de las cifras del plan de Cepeda 2026",
                 fontsize=12, fontweight="bold", pad=20)
    ax.text(0, 0, f"{len(df)}\ncifras", ha="center", va="center",
            fontsize=13, fontweight="bold", color="#1a1a1a")

    plt.tight_layout()
    path = OUT_DIR / "verificabilidad_resumen.png"
    plt.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"[OK] {path.relative_to(ROOT)}")


def barras_por_tema(df):
    """Barras apiladas: verificabilidad por tema."""
    estados  = ["Consistente", "Con matices", "Plausible", "Ambicioso",
                "Sobreestimado", "Requiere contexto"]
    temas    = df["tema"].unique()
    pivot    = df.groupby(["tema", "estado"]).size().unstack(fill_value=0)
    for e in estados:
        if e not in pivot.columns:
            pivot[e] = 0
    pivot = pivot[estados]
    pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=True).index]

    fig, ax = plt.subplots(figsize=(11, 6))
    left = np.zeros(len(pivot))
    for estado in estados:
        vals = pivot[estado].values
        bars = ax.barh(pivot.index, vals, left=left,
                       color=COLORES_ESTADO.get(estado, "#95a5a6"),
                       label=estado, edgecolor="white", height=0.6)
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_y() + bar.get_height() / 2,
                        str(int(val)), ha="center", va="center",
                        fontsize=8, color="white", fontweight="bold")
        left += vals

    ax.set_xlabel("Número de cifras", fontsize=10)
    ax.set_title("Verificabilidad de cifras del plan de Cepeda por tema", fontsize=12, fontweight="bold", pad=12)
    ax.legend(loc="lower right", fontsize=8, frameon=True, ncol=2)
    ax.tick_params(axis="y", labelsize=9)
    ax.set_xlim(0, left.max() + 1)
    plt.tight_layout()
    path = OUT_DIR / "verificabilidad_por_tema.png"
    plt.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"[OK] {path.relative_to(ROOT)}")


def comparacion_cifras_clave(df):
    """Gráfico de barras comparando cifra del plan vs indicador real."""
    # Seleccion manual de cifras con comparacion numerica disponible
    casos = [
        ("Crecimiento PIB 2025 (%)",         3.6,  2.6,  "Plan vs BanRep"),
        ("Inflacion (%) — nivel actual",      5.3,  5.6,  "Plan vs BanRep Q1-2026"),
        ("Desempleo (%)",                     8.2,  8.8,  "Plan vs DANE Abr-2026"),
        ("Desempleo mujeres (%)",             9.0, 10.5,  "Plan vs DANE 2025"),
        ("Desempleo hombres (%)",             5.0,  7.1,  "Plan vs DANE 2025"),
        ("Pobreza monetaria (%)",            29.0, 29.0,  "Plan vs DANE 2024"),
        ("Energias limpias matriz (%)",      15.0, 14.0,  "Plan vs UPME 2025"),
    ]

    etiquetas = [c[0] for c in casos]
    vals_plan = [c[1] for c in casos]
    vals_real = [c[2] for c in casos]
    fuentes   = [c[3] for c in casos]

    x      = np.arange(len(etiquetas))
    ancho  = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))

    b1 = ax.bar(x - ancho/2, vals_plan, ancho, label="Cifra en el plan de Cepeda",
                color="#2c5f8a", edgecolor="white")
    b2 = ax.bar(x + ancho/2, vals_real, ancho, label="Indicador real 2025-2026",
                color="#e74c3c", edgecolor="white", alpha=0.85)

    for bar in b1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=8, color="#2c5f8a", fontweight="bold")
    for bar in b2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=8, color="#c0392b", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(etiquetas, rotation=22, ha="right", fontsize=9)
    ax.set_ylabel("Valor (%)", fontsize=10)
    ax.set_title("Comparación: cifras del plan de Cepeda vs. indicadores reales (2025-2026)",
                 fontsize=12, fontweight="bold", pad=12)
    ax.legend(fontsize=10)
    ax.set_ylim(0, max(max(vals_plan), max(vals_real)) * 1.25)
    plt.tight_layout()
    path = OUT_DIR / "cifras_clave_comparacion.png"
    plt.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"[OK] {path.relative_to(ROOT)}")


def main():
    df = pd.read_csv(DATA)
    print(f"Cifras cargadas: {len(df)}")
    print("Generando visualizaciones de verificabilidad...\n")
    donut_verificabilidad(df)
    barras_por_tema(df)
    comparacion_cifras_clave(df)
    print(f"\nTodos los graficos guardados en: outputs/charts/")


if __name__ == "__main__":
    main()
