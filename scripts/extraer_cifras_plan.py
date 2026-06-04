"""
Extrae todas las cifras cuantitativas del programa de gobierno de Ivan Cepeda 2026-2030
y las estructura para verificabilidad frente a indicadores reales de Colombia.

Uso:
    python scripts/extraer_cifras_plan.py

Salida:
    data/cifras_plan_cepeda_2026.csv
    data/texto_completo_plan.txt
"""

import re
import sys
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("Instalando pdfplumber...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pdfplumber"], check=True)
    import pdfplumber

import csv

PDF_PATH = Path(r"C:\Users\David.Munoz\Downloads\programa-gobierno-2026-2030.pdf")
ROOT = Path(__file__).resolve().parent.parent
OUT_TXT  = ROOT / "data" / "texto_completo_plan.txt"
OUT_CSV  = ROOT / "data" / "cifras_plan_cepeda_2026.csv"

# ── Patrones de cifras ──────────────────────────────────────────────────────
# Captura: porcentajes, millones, billones, cantidades con unidades, años-meta
PATRONES = [
    # porcentajes: 8%, 8,5%, 8.5%
    r'\b\d{1,3}[.,]?\d*\s*%',
    # billones / millones de pesos o dolares
    r'\b\d{1,4}[.,]?\d*\s*(?:billones?|millones?|mil millones?)\s*(?:de\s+)?(?:pesos?|dolares?|USD|COP)?',
    # cifras absolutas con unidades (empleos, hectareas, viviendas, etc.)
    r'\b\d[\d.,]*\s*(?:empleos?|puestos? de trabajo|hectareas?|viviendas?|familias?|hogares?|personas?|estudiantes?|escuelas?|hospitales?|municipios?|kilometros?|km)',
    # metas tipo "de X a Y"
    r'de\s+\d[\d.,]*\s*%?\s+a\s+\d[\d.,]*\s*%',
    # PIB porcentaje
    r'\d[.,]?\d*\s*%\s*del\s*PIB',
    # años con meta asociada
    r'(?:en|para|al?)\s+20[23]\d[^,;]{0,60}(?:%|millones?|billones?|empleos?|hectareas?)',
]

PATRON_COMBINADO = re.compile('|'.join(PATRONES), re.IGNORECASE)

# Ventana de contexto (caracteres antes y después de la cifra)
VENTANA = 180

def limpiar(texto):
    texto = re.sub(r'\s+', ' ', texto)
    return texto.strip()

def extraer_contexto(texto_pagina, match):
    inicio = max(0, match.start() - VENTANA)
    fin    = min(len(texto_pagina), match.end() + VENTANA)
    fragmento = texto_pagina[inicio:fin]
    return limpiar(fragmento)

def clasificar_tema(contexto):
    ctx = contexto.lower()
    temas = {
        "Empleo / trabajo":       ["empleo", "trabajo", "desempleo", "ocupacion", "laboral", "formaliz"],
        "Salud":                  ["salud", "hospital", "clinica", "medic", "eps", "sgsss"],
        "Educacion":              ["educacion", "escuela", "colegio", "universidad", "estudiante", "maestro"],
        "Vivienda":               ["vivienda", "hogar", "habitacion", "deficit habitacional"],
        "Reforma agraria / tierra":["tierra", "agrari", "rural", "campesino", "hectarea", "catastro"],
        "Paz / seguridad":        ["paz", "conflicto", "armad", "victima", "guerrill", "crimen"],
        "Economia / fiscal":      ["pib", "fiscal", "deficit", "deuda", "presupuesto", "inversion", "crecimiento"],
        "Inflacion / precios":    ["inflacion", "precio", "ipc", "costo de vida"],
        "Infraestructura":        ["via", "carretera", "km", "infraestructura", "acueducto", "alcantarillado"],
        "Medio ambiente":         ["ambiente", "clima", "carbon", "bosque", "agua", "energia"],
        "Pobreza / inclusion":    ["pobreza", "desigualdad", "gini", "vulnerab", "exclusion"],
        "Mujer / genero":         ["mujer", "genero", "femicidio", "feminicidio", "paridad"],
    }
    for tema, palabras in temas.items():
        if any(p in ctx for p in palabras):
            return tema
    return "General / otro"

def main():
    print(f"Leyendo PDF: {PDF_PATH}")
    print(f"Total de paginas esperadas: 209\n")

    todos_textos = []
    registros    = []
    paginas_leidas = 0

    with pdfplumber.open(PDF_PATH) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            num = i + 1
            texto = page.extract_text() or ""
            todos_textos.append(f"\n\n=== PAGINA {num} ===\n{texto}")
            paginas_leidas += 1

            matches = list(PATRON_COMBINADO.finditer(texto))
            for m in matches:
                cifra    = limpiar(m.group())
                contexto = extraer_contexto(texto, m)
                tema     = clasificar_tema(contexto)
                registros.append({
                    "pagina":    num,
                    "cifra":     cifra,
                    "contexto":  contexto,
                    "tema":      tema,
                    "verificabilidad": "",   # se llena en siguiente fase
                    "indicador_real":  "",
                    "fuente_real":     "",
                    "notas":           "",
                })

            if num % 20 == 0:
                print(f"  Procesadas {num}/{total} paginas — cifras encontradas hasta ahora: {len(registros)}")

    # Guardar texto completo
    OUT_TXT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("".join(todos_textos))
    print(f"\nTexto completo guardado en: {OUT_TXT.relative_to(ROOT)}")

    # Guardar CSV de cifras
    campos = ["pagina","cifra","contexto","tema","verificabilidad","indicador_real","fuente_real","notas"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        w.writerows(registros)

    print(f"CSV de cifras guardado en:  {OUT_CSV.relative_to(ROOT)}")
    print(f"\nRESUMEN")
    print(f"  Paginas procesadas : {paginas_leidas}")
    print(f"  Cifras encontradas : {len(registros)}")

    # Conteo por tema
    from collections import Counter
    conteo = Counter(r["tema"] for r in registros)
    print("\n  Cifras por tema:")
    for tema, n in sorted(conteo.items(), key=lambda x: -x[1]):
        print(f"    {n:4d}  {tema}")

if __name__ == "__main__":
    main()
