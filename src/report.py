"""Export CSV, plain-text summary, and Excel reports."""

from pathlib import Path
import pandas as pd


def export_outputs(
    df: pd.DataFrame,
    kpis: dict,
    cat_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
    pm_df: pd.DataFrame,
    budget_df: pd.DataFrame,
    outputs_dir: str = "outputs",
    reports_dir: str = "reports",
) -> dict[str, str]:
    """Save CSV summaries, text insight report, and multi-sheet Excel workbook."""
    out_p = Path(outputs_dir)
    rep_p = Path(reports_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    rep_p.mkdir(parents=True, exist_ok=True)

    cat_csv = out_p / "category_summary.csv"
    monthly_csv = out_p / "monthly_summary.csv"
    pm_csv = out_p / "payment_method_summary.csv"

    cat_df.to_csv(cat_csv, index=False)
    monthly_df.to_csv(monthly_csv, index=False)
    pm_df.to_csv(pm_csv, index=False)

    # Text summary report
    txt_report = rep_p / "monthly_summary_report.txt"
    latest_month = monthly_df.iloc[-1]["month"] if not monthly_df.empty else "N/A"
    lines = [
        "============================================================",
        "       PERSONAL EXPENSE TRACKER - ANALYTICAL REPORT         ",
        "============================================================",
        f"Total Transactions Analyzed : {kpis['total_transactions']}",
        f"Total Income                : INR {kpis['total_income']:,.2f}",
        f"Total Spending              : INR {kpis['total_spend']:,.2f}",
        f"Net Savings                 : INR {kpis['net_savings']:,.2f}",
        f"Savings Rate                : {kpis['savings_rate_pct']:.2f}%",
        f"Average Daily Spending      : INR {kpis['avg_daily_spend']:,.2f}",
        f"Average Monthly Spending    : INR {kpis['avg_monthly_spend']:,.2f}",
        f"Highest Spending Category   : {kpis['highest_spending_category']} (INR {kpis['highest_category_spend']:,.2f})",
        "",
        "--- Category-Wise Breakdown ---",
        cat_df.to_string(index=False),
        "",
        "--- Monthly Trend ---",
        monthly_df.to_string(index=False),
        "",
        f"--- Budget Check ({latest_month}) ---",
        budget_df.to_string(index=False) if not budget_df.empty else "No budgets configured.",
        "============================================================",
    ]
    txt_report.write_text("\n".join(lines), encoding="utf-8")

    # Excel multi-sheet report
    xlsx_report = rep_p / "monthly_report.xlsx"
    with pd.ExcelWriter(xlsx_report, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Transactions", index=False)
        cat_df.to_excel(writer, sheet_name="Category Summary", index=False)
        monthly_df.to_excel(writer, sheet_name="Monthly Trend", index=False)
        pm_df.to_excel(writer, sheet_name="Payment Methods", index=False)
        if not budget_df.empty:
            budget_df.to_excel(writer, sheet_name="Budget Check", index=False)

    return {
        "category_csv": str(cat_csv),
        "monthly_csv": str(monthly_csv),
        "payment_method_csv": str(pm_csv),
        "text_report": str(txt_report),
        "excel_report": str(xlsx_report),
    }
