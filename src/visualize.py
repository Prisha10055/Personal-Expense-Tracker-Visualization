"""Matplotlib and Seaborn chart generators for Personal Expense Tracker."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid", palette="muted")


def generate_all_charts(
    cat_df: pd.DataFrame,
    monthly_df: pd.DataFrame,
    pm_df: pd.DataFrame,
    daily_df: pd.DataFrame,
    output_dir: str = "images",
) -> list[str]:
    """Generate and save all 4 core visualization charts. Returns list of saved file paths."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    saved = []

    # 1. Category-wise Bar Chart
    p1 = out / "category_spending_bar.png"
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.barplot(data=cat_df, x="total_spend", y="category", hue="category", legend=False, palette="viridis", ax=ax)
    ax.set_title("Total Spending by Category (INR)", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Total Spend (INR)")
    ax.set_ylabel("Category")
    for container in ax.containers:
        ax.bar_label(container, fmt="₹%.0f", padding=4, fontsize=9)
    ax.set_xlim(0, cat_df["total_spend"].max() * 1.18 if not cat_df.empty else 100)
    plt.tight_layout()
    plt.savefig(p1, dpi=150)
    plt.close(fig)
    saved.append(str(p1))

    # 2. Monthly Spending & Income Line Chart
    p2 = out / "monthly_spending_line.png"
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly_df["month"], monthly_df["total_spend"], marker="o", linewidth=2.5, color="#D9534F", label="Total Spend")
    ax.plot(monthly_df["month"], monthly_df["total_income"], marker="s", linewidth=2.0, linestyle="--", color="#2E8B57", label="Total Income")
    for x, y in zip(monthly_df["month"], monthly_df["total_spend"]):
        ax.annotate(f"₹{y:,.0f}", (x, y), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8.5)
    ax.set_title("Monthly Income vs. Spending Trend", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (INR)")
    ax.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(p2, dpi=150)
    plt.close(fig)
    saved.append(str(p2))

    # 3. Payment Method Pie Chart
    p3 = out / "payment_method_pie.png"
    fig, ax = plt.subplots(figsize=(7, 6))
    colors = sns.color_palette("Set2", len(pm_df))
    ax.pie(
        pm_df["total_spend"],
        labels=pm_df["payment_method"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    ax.set_title("Spending Share by Payment Method", fontsize=14, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(p3, dpi=150)
    plt.close(fig)
    saved.append(str(p3))

    # 4. Daily Spending Trend Chart
    p4 = out / "daily_spending_trend.png"
    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.bar(daily_df["tx_date"], daily_df["daily_spend"], alpha=0.35, color="#4A90E2", label="Daily Spend")
    ax.plot(daily_df["tx_date"], daily_df["rolling_7d"], color="#1B4F72", linewidth=2.2, label="7-Day Rolling Avg")
    ax.set_title("Daily Spending & 7-Day Rolling Average", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date")
    ax.set_ylabel("Spend (INR)")
    ax.legend()
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(p4, dpi=150)
    plt.close(fig)
    saved.append(str(p4))

    return saved
