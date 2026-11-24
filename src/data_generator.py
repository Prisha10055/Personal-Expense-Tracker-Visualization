"""Synthetic personal expense dataset generator for realistic simulation."""

from pathlib import Path
import numpy as np
import pandas as pd


def generate_synthetic_expenses(
    output_path: str = "data/synthetic_expenses.csv",
    months: int = 6,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a realistic 6-month synthetic personal finance CSV dataset (INR).
    Includes intentional minor formatting quirks (extra spaces, a few invalid rows)
    to demonstrate data cleaning in the ingestion pipeline.
    """
    rng = np.random.default_rng(seed)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    end_date = pd.Timestamp("2026-10-31")
    start_date = (end_date - pd.DateOffset(months=months - 1)).replace(day=1)
    all_days = pd.date_range(start_date, end_date, freq="D")

    merchants = {
        "Groceries": [
            ("D-Mart Supermarket", 450, 2400),
            ("Reliance Fresh", 300, 1800),
            ("BigBasket Order", 500, 2600),
            ("Local Kirana Store", 120, 650),
        ],
        "Food & Dining": [
            ("Swiggy Food Delivery", 180, 650),
            ("Zomato Order", 200, 750),
            ("Cafe Coffee Day", 150, 480),
            ("College Canteen Lunch", 80, 220),
        ],
        "Transport": [
            ("Uber Ride", 120, 480),
            ("Ola Auto", 60, 280),
            ("Metro Card Recharge", 200, 600),
            ("HP Petrol Pump", 500, 1800),
        ],
        "Bills & Utilities": [
            ("JioFiber Broadband", 799, 999),
            ("MSEDCL Electricity Bill", 900, 2400),
            ("Airtel Mobile Recharge", 299, 599),
        ],
        "Shopping": [
            ("Amazon India", 450, 3500),
            ("Flipkart Order", 500, 3200),
            ("Myntra Apparel", 700, 2800),
        ],
        "Entertainment": [
            ("Netflix Subscription", 199, 649),
            ("Spotify Premium", 119, 119),
            ("BookMyShow Movie", 280, 750),
        ],
        "Health & Fitness": [
            ("Apollo Pharmacy", 150, 950),
            ("Cult.fit Membership", 1200, 1800),
        ],
    }

    payment_methods = ["UPI", "Debit Card", "Credit Card", "Net Banking", "Cash"]
    method_weights = [0.52, 0.18, 0.16, 0.08, 0.06]

    rows = []

    # Monthly salary / stipend + fixed bills
    month_starts = pd.date_range(start_date, end_date, freq="MS")
    for ms in month_starts:
        rows.append(
            {
                "Date": ms.strftime("%Y-%m-%d"),
                "Description": "Monthly Stipend / Salary Credit",
                "Amount": float(rng.choice([35000, 38000, 40000])),
                "Payment_Method": "Net Banking",
                "Account": "HDFC",
                "Note": "Monthly income",
            }
        )
        rows.append(
            {
                "Date": (ms + pd.Timedelta(days=4)).strftime("%Y-%m-%d"),
                "Description": "JioFiber Broadband",
                "Amount": -849.0,
                "Payment_Method": "UPI",
                "Account": "HDFC",
                "Note": "Wi-Fi monthly plan",
            }
        )
        rows.append(
            {
                "Date": (ms + pd.Timedelta(days=9)).strftime("%Y-%m-%d"),
                "Description": "MSEDCL Electricity Bill",
                "Amount": -float(rng.integers(1100, 2200)),
                "Payment_Method": "UPI",
                "Account": "HDFC",
                "Note": "Monthly power bill",
            }
        )
        rows.append(
            {
                "Date": (ms + pd.Timedelta(days=14)).strftime("%Y-%m-%d"),
                "Description": "Netflix Subscription",
                "Amount": -499.0,
                "Payment_Method": "Credit Card",
                "Account": "ICICI",
                "Note": "OTT plan",
            }
        )

    # Daily variable spending
    for day in all_days:
        n_tx = int(rng.choice([0, 1, 1, 2, 2, 3], p=[0.12, 0.28, 0.25, 0.20, 0.10, 0.05]))
        for _ in range(n_tx):
            cat = str(
                rng.choice(
                    ["Groceries", "Food & Dining", "Transport", "Shopping", "Entertainment", "Health & Fitness"],
                    p=[0.24, 0.34, 0.20, 0.11, 0.06, 0.05],
                )
            )
            desc, low, high = merchants[cat][int(rng.integers(0, len(merchants[cat])))]
            amt = -round(float(rng.uniform(low, high)), 2)
            pm = str(rng.choice(payment_methods, p=method_weights))
            acct = "ICICI" if pm == "Credit Card" else ("Cash Wallet" if pm == "Cash" else "HDFC")
            rows.append(
                {
                    "Date": day.strftime("%Y-%m-%d"),
                    "Description": f"  {desc}  " if rng.random() < 0.15 else desc,
                    "Amount": amt,
                    "Payment_Method": pm,
                    "Account": acct,
                    "Note": f"{cat} expense",
                }
            )

    # Add 2 intentional dirty rows to showcase data cleaning
    rows.append(
        {
            "Date": "invalid-date",
            "Description": "Corrupted Row Test",
            "Amount": -100.0,
            "Payment_Method": "UPI",
            "Account": "HDFC",
            "Note": "Should be dropped during cleaning",
        }
    )
    rows.append(
        {
            "Date": end_date.strftime("%Y-%m-%d"),
            "Description": "Missing Amount Row",
            "Amount": None,
            "Payment_Method": "Cash",
            "Account": "Cash Wallet",
            "Note": "Should be dropped during cleaning",
        }
    )

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    generated = generate_synthetic_expenses()
    print(f"Generated {len(generated)} rows at data/synthetic_expenses.csv")
