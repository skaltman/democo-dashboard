# This file generated by Quarto; do not edit by hand.

from __future__ import annotations

from pathlib import Path
from shiny import App, Inputs, Outputs, Session, ui




def server(input: Inputs, output: Outputs, session: Session) -> None:
    import pandas as pd
    from helpers import plot_churn_reason, plot_contract_type, table_purchases
    from matplotlib import rcParams
    from shiny import render, reactive, ui

    rcParams.update({"savefig.bbox": "tight"})

    churn = pd.read_csv("data/churn.csv")
    churn_reason = pd.read_csv("data/churn_reason.csv")
    purchase_characteristics = pd.read_csv("data/purchase_characteristics.csv")

    # ========================================================================

    reasons=['Competitor', 'Price', 'Dissatisfaction', 'Other']
    years=[2022, 2023]

    ui.input_checkbox_group(
      "reasons", 
      "Churn reason",
      reasons,
      selected=reasons
    )

    ui.input_checkbox_group(
      "years", 
      "Year",
      years,
      selected=years
    )

    @reactive.Calc
    def filtered_churn_reason():
        data = churn_reason[churn_reason["year"].isin(input.years())]
        data = data[data["reason"].isin(input.reasons())]
        return data

    # ========================================================================

    # @render.plot
    # def churn_years():
    #   return plot_churn_reason(churn_reason, "Standard", [2022, 2023])

    @render.plot
    def depth():
        return plot_churn_reason(
            filtered_churn_reason(), "Standard"
        )

    # ========================================================================

    table_purchases(purchase_characteristics, "Standard")

    # ========================================================================

    plot_contract_type(churn, "Standard")

    # ========================================================================

    plot_churn_reason(churn_reason, "Premium")

    # ========================================================================

    table_purchases(purchase_characteristics, "Premium")

    # ========================================================================

    plot_contract_type(churn, "Premium")

    # ========================================================================

    plot_churn_reason(churn_reason, "Professional")

    # ========================================================================

    table_purchases(purchase_characteristics, "Professional")

    # ========================================================================

    plot_contract_type(churn, "Professional")

    # ========================================================================




_static_assets = ["dashboard_files","images/logo.png"]
_static_assets = {"/" + sa: Path(__file__).parent / sa for sa in _static_assets}

app = App(
    Path(__file__).parent / "dashboard.html",
    server,
    static_assets=_static_assets,
)
