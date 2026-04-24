#  Grafica nueva con % de captuira referente al mercado

# ------------------------------------------------------ Captura de los Instrumentos -----------------------------------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ===========================================================================================================================
# Returns (Esto son los retornos que tuvieron los instrumentos de nuestro portafolio en la semana de 20-03-2026 al 2703-2026)
# ===========================================================================================================================
retorno = {
    "VXM": 11.63, "V2TX": 5.42, "TSR20": 4.32, "MCL": 3.19, "MHG": 3.07,
    "SMI": 1.97, "W": 1.60, "MNTPX": 0.74, "HO": 0.57, "DX": 0.53,
    "SI": 0.49, "M2K": 0.37, "RY": 0.29, "ESTX50": 0.04, "EBM": 0.00,
    "ZT": -0.02, "MGC": -0.03, "R": -0.03, "ZAR": -0.13, "ZB": -0.19,
    "N225M": -0.21, "ZN": -0.31, "UB": -0.38, "DAX": -0.39,
    "TN": -0.42, "GBP": -0.59, "EUR": -0.59, "GBL": -0.62, "JPY": -0.73,
    "GBX": -0.75, "OAT": -0.87, "SCI": -0.92, "MYM": -1.02, "RB": -1.04,
    "BTP": -1.05, "CHF": -1.46, "NZD": -1.50, "QG": -1.78, "MCA": -1.91,
    "D": -1.94, "M6A": -1.96, "PA": -2.12, "MES": -2.24, "CC": -2.76,
    "MNQ": -3.21, "PL": -3.74, "ZM": -3.87, "MBT": -5.60, "K200": -6.52,
    "GOIL": -10.81
}

# ==========================================================================================================================================
# Data (De aqui se lee la data utilizada en el codigo y sus variables, el excel "Posicion Optima Futuros 1" estara disponible en el archivo)
# ==========================================================================================================================================
file_path = r"C:\Users\Irama Mendoza\Documents\AAGA Proyecto\Posicion Optima Futuros 1.xlsx"
df = pd.read_excel(file_path, header=1)
df.columns = df.columns.str.strip().str.upper()

# =========================================================
# Clean (Limpieza de datos numéricos provenientes de Excel)
# =========================================================

# GANANCIAS = Profit del portafolio (Realized + Unrealized).
df["GANANCIAS"] = (
    df["GANANCIAS"].astype(str)
    .str.replace(",", "")
    .str.replace("(", "-")
    .str.replace(")", "")
)
df["GANANCIAS"] = pd.to_numeric(df["GANANCIAS"], errors="coerce")

# MERCADO = Profit teórico del mercado.
df["MERCADO"] = (
    df["DIFERENCIA"].astype(str)
    .str.replace(",", "")
    .str.replace("(", "-")
    .str.replace(")", "")
)
df["MERCADO"] = pd.to_numeric(df["MERCADO"], errors="coerce")

# CAPTURA = Qué porcentaje del movimiento del mercado capturó el portafolio.
df["CAPTURA"] = df["GANANCIAS"] / df["MERCADO"]
df["RETURN"] = df["INSTRUMENTO"].map(retorno)

df = df.dropna(subset=["RETURN", "CAPTURA"])

df["CAPTURA"] = np.where(df["MERCADO"] != 0,
                         df["GANANCIAS"] / df["MERCADO"],
                         np.nan)

df = df.set_index("INSTRUMENTO").loc[
    [i for i in retorno.keys() if i in df["INSTRUMENTO"].values]
].reset_index()

# ==============================================
# PLOT (Grafica - captura del mercado)
# ==============================================
def plot(df, title):

    df = df.copy()
    y = np.arange(len(df))

    market = df["RETURN"]
    pnl = market * df["CAPTURA"]

    colors = np.where(df["CAPTURA"] >= 0, "#2E7D32", "#B71C1C")

    # Figura Base.
    fig, ax = plt.subplots(figsize=(12, max(10, len(df) * 0.4)))

    xmax = np.nanmax(np.abs([market.max(), pnl.max(), market.min(), pnl.min()])) * 1.3

    gap = xmax * 0.03
    left = -gap
    right = gap

    # Gap Central.
    ax.axvline(left, color="black", linewidth=1, zorder=10)
    ax.axvline(right, color="black", linewidth=1, zorder=10)
    ax.axvspan(left, right, color="white", zorder=3)

    # Barras de mercado (Retuns de los instrumentos en base al mercado).
    ax.barh(y, market.clip(upper=0), left=left, color="#4C78A8", alpha=0.25)
    ax.barh(y, market.clip(lower=0), left=right, color="#4C78A8", alpha=0.25)

    # La captura sale directamente desde el Gap y no desde el valor 0. 
    ax.barh(
        y,
        pnl.clip(upper=0),
        left=left,
        color=colors,
        height=0.3,
        edgecolor="black",
        linewidth=0.3,
        zorder=5
    )

    ax.barh(
        y,
        pnl.clip(lower=0),
        left=right,
        color=colors,
        height=0.3,
        edgecolor="black",
        linewidth=0.3,
        zorder=5
    )

    # Nombres de los instrumentos dentro del Gap creado. 
    ax.set_yticks(y)
    ax.set_yticklabels([""] * len(df))

    for i in range(len(df)):
        ax.text(
            0,
            y[i],
            df.iloc[i]["INSTRUMENTO"],
            ha="center",
            va="center",
            fontsize=7,
            fontweight="bold",
            bbox=dict(facecolor="white", alpha=0.95, edgecolor="none", pad=1),
            zorder=6
        )

    ax.invert_yaxis()

    # Cuadros de informacion al finalizar las barras (M: representa el return del mercado y C: la captura que tuvimos).
    for i in range(len(df)):

        m = market.iloc[i]
        c = df.iloc[i]["CAPTURA"]
        val = pnl.iloc[i]

        ax.text(
            (right + val + 0.2) if val > 0 else (left + val - 0.2),
            y[i],
            f"M:{m:.2f}% | C:{c*100:.0f}%",
            fontsize=6,
            va="center",
            ha="left" if val > 0 else "right",
            bbox=dict(facecolor="white", alpha=0.85),
            zorder=6
        )

    # Fecha indicando el periodo analizado.
    ax.set_xlim(-xmax, xmax)
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.2) 
    ax.text(0.18, 0.98, "Periodo 2026-03-20 al 2026-03-27", transform=ax.transAxes,
        ha="left", va="bottom", fontsize=10, fontweight="bold") 

    # Leyenda informativa.
    market_patch = mpatches.Patch(color="#4C78A8", alpha=0.25, label="M = Movimiento de Mercado")
    capture_pos = mpatches.Patch(color="#2E7D32", label="C ≥ 0 (Captura positiva)")
    capture_neg = mpatches.Patch(color="#B71C1C", label="C < 0 (Captura negativa)")
    ax.legend(handles=[market_patch, capture_pos, capture_neg], 
              loc="lower right",
              bbox_to_anchor=(0.82, 0.02))

    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    plt.show()


plot(df, "Zenit Portafolio Captura de Instrumentos (%)")

