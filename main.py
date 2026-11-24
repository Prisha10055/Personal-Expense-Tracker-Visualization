"""End-to-end runner for Personal Expense Tracker with Data Visualization."""

from pathlib import Path
from src.models import init_db
from src.data_generator import generate_synthetic_expenses
from src.ingest import read_expense_csv, upsert_transactions
from src.categorize import categorize_transactions
from src.analyze import (
    fetch_transactions,
    compute_kpis,
    category_analysis,
    monthly_analysis,
    payment_method_analysis,
    daily_analysis,
)
from src.budget import seed_default_budgets, check_budget
from src.visualize import generate_all_charts
from src.report import export_outputs


def main() -> None:
    csv_path = Path("data/synthetic_expenses.csv")
    db_path = "db/expenses.db"

    print("1. Initializing SQLite database...")
    init_db(db_path)

    if not csv_path.exists():
        print("2. Generating synthetic expense dataset...")
        generate_synthetic_expenses(str(csv_path), months=6, seed=42)
    else:
        print("2. Using existing dataset:", csv_path)

    print("3. Loading and cleaning CSV data...")
    cleaned_df, clean_stats = read_expense_csv(str(csv_path))
    inserted = upsert_transactions(cleaned_df, db_path)
    print(f"   Cleaned {clean_stats['clean_rows']} rows (dropped {clean_stats['dropped_invalid']} invalid, {clean_stats['dropped_duplicates']} duplicates); inserted {inserted} new rows.")

    print("4. Auto-categorizing transactions...")
    updated = categorize_transactions(db_path)
    print(f"   Categorized {updated} transactions.")

    print("5. Running analytics...")
    df = fetch_transactions(db_path)
    kpis = compute_kpis(df)
    cat_df = category_analysis(df)
    monthly_df = monthly_analysis(df)
    pm_df = payment_method_analysis(df)
    daily_df = daily_analysis(df)

    latest_month = monthly_df.iloc[-1]["month"]
    seed_default_budgets(latest_month, db_path)
    budget_df = check_budget(latest_month, db_path)

    print("6. Generating visualization charts...")
    charts = generate_all_charts(cat_df, monthly_df, pm_df, daily_df, output_dir="images")
    for ch in charts:
        print(f"   Saved chart: {ch}")

    print("7. Exporting CSV, TXT, and Excel reports...")
    exported = export_outputs(df, kpis, cat_df, monthly_df, pm_df, budget_df, outputs_dir="outputs", reports_dir="reports")
    for label, path in exported.items():
        print(f"   Saved {label}: {path}")

    print("\n=== SUMMARY INSIGHTS ===")
    print(f"Total Income             : INR {kpis['total_income']:,.2f}")
    print(f"Total Spending           : INR {kpis['total_spend']:,.2f}")
    print(f"Net Savings              : INR {kpis['net_savings']:,.2f} ({kpis['savings_rate_pct']:.1f}%)")
    print(f"Highest Spend Category   : {kpis['highest_spending_category']} (INR {kpis['highest_category_spend']:,.2f})")
    print(f"Average Daily Spending   : INR {kpis['avg_daily_spend']:,.2f}")
    print(f"Average Monthly Spending : INR {kpis['avg_monthly_spend']:,.2f}")
    print("\nPipeline completed successfully!")


if __name__ == "__main__":
    main()
