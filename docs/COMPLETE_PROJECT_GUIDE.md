# Personal Expense Tracker with Data Visualization — Complete 14-Part Project Guide

---

## 1. Project Explanation

### Simple Explanation
A **Personal Expense Tracker** is a digital tool that records every rupee you spend or earn, groups your spending into meaningful categories (like *Food & Dining*, *Groceries*, *Transport*, *Bills*), and turns raw numbers into easy-to-read charts and monthly reports. Instead of guessing why your bank balance dropped at the end of the month, you can immediately see your biggest spending habits and stay within budget.

### Technical Explanation
This project is an end-to-end **ETL (Extract, Transform, Load) and Analytics Pipeline** written in Python:
1. **Extract**: Reads raw CSV transaction exports (or synthetic/manual entries).
2. **Transform**: Cleans malformed dates, strips whitespace, coerces numeric amounts, drops duplicates, and applies regex-based merchant categorization.
3. **Load**: Persists normalized records into a relational **SQLite** database (`categories`, `transactions`, `budgets`) with foreign-key and uniqueness constraints.
4. **Analyze & Visualize**: Uses **Pandas** for multi-dimensional grouping (category, month, payment method, daily rolling average), **Matplotlib/Seaborn** for static PNG charts, **XlsxWriter** for multi-sheet Excel reports, and **Streamlit** for an interactive dashboard.

### Why It Matters & Who Benefits
- **Students**: Manage monthly allowances/stipends and spot food-delivery or impulse spending.
- **Employees & Families**: Track recurring bills, groceries, and savings rate (`(Income - Spend) / Income`).
- **Freelancers & Small Businesses**: Separate operating categories, monitor cash flow, and export clean Excel/CSV records for tax or reimbursement prep.

### End-to-End Workflow
`Expense Data Entry (CSV / Synthetic)` -> `Data Storage (SQLite)` -> `Data Cleaning (Pandas)` -> `Auto-Categorization (Regex)` -> `Category & Monthly Analysis` -> `Visualization (4 Charts + Streamlit)` -> `Report Generation (CSV, TXT, XLSX)`

---

## 2. Tech Stack Options

| Option | Tools & Libraries | Difficulty | Expected Output |
| :--- | :--- | :--- | :--- |
| **Option A: Easy** | Python, `csv`, `pandas`, `matplotlib` | Beginner | Single script reading a CSV, printing totals, and saving 2–3 basic PNG charts. |
| **Option B: Intermediate (Recommended)** | Python 3.11, `pandas`, `numpy`, `sqlite3`, `matplotlib`, `seaborn`, `xlsxwriter`, `streamlit` | Intermediate | Modular ETL package, SQLite database, 4 polished charts, budget alerts, Excel/TXT/CSV reports, and an interactive Streamlit dashboard. |
| **Option C: Advanced** | Option B + `scikit-learn` (Naive Bayes classifier), `FastAPI`, `PostgreSQL`, `Docker`, `Tesseract OCR` | Advanced | Full-stack web app with receipt OCR, ML-based categorization, REST APIs, and containerized deployment. |

**Best Option for Students:** **Option B (Intermediate)** is the sweet spot. It demonstrates real industry skills—SQLite schema design, modular Python code, Pandas analytics, automated reporting, and a Streamlit UI—without requiring paid cloud infrastructure or complex DevOps setup.

---

## 3. Project Architecture

### Text-Based Architecture Diagram
```text
+-------------------------------------------------------------------+
|                        INPUT LAYER                                |
|  [Synthetic CSV Generator]  OR  [User / Bank CSV Upload]          |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                   INGESTION & CLEANING (src/ingest.py)            |
|  - Parse dates (YYYY-MM-DD)      - Coerce numeric amounts         |
|  - Strip whitespace              - Drop nulls & duplicates        |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|              STORAGE & CATEGORIZATION (SQLite + Regex)            |
|  - db/expenses.db (categories, transactions, budgets)             |
|  - src/categorize.py: Auto-tag merchants -> category_id           |
+-------------------------------------------------------------------+
                                  |
                                  v
+-------------------------------------------------------------------+
|                  ANALYTICS ENGINE (src/analyze.py & budget.py)    |
|  - Category Totals   - Monthly Trends   - Payment Method Share    |
|  - Daily 7d Avg      - KPIs & Savings   - Budget Overspend Check  |
+-------------------------------------------------------------------+
                                  |
                 +----------------+----------------+
                 v                                 v
+---------------------------------+ +-------------------------------+
|    VISUALIZATION (images/)      | |   REPORTS & UI (reports/)     |
|  - Category Bar Chart           | |  - category_summary.csv       |
|  - Monthly Line Chart           | |  - monthly_summary_report.txt |
|  - Payment Method Pie Chart     | |  - monthly_report.xlsx        |
|  - Daily Spending Trend         | |  - Streamlit Dashboard        |
+---------------------------------+ +-------------------------------+
```

### Data Flow Explanation
1. **Input**: `src/data_generator.py` creates `data/synthetic_expenses.csv` (or you upload a real bank CSV).
2. **Cleaning**: `src/ingest.py` standardizes column names, removes invalid dates/amounts, and inserts unique rows into SQLite.
3. **Categorization**: `src/categorize.py` inspects `description` and `amount` to assign a `category_id`.
4. **Aggregation**: `src/analyze.py` and `src/budget.py` compute KPIs, category splits, monthly trends, and budget variances.
5. **Output**: `src/visualize.py` writes 4 charts to `images/`, `src/report.py` writes CSV/TXT/XLSX files to `outputs/` and `reports/`, and `src/app_streamlit.py` serves live interactive views.

---

## 4. Implementation Plan (10 Phases)

1. **Phase 1: Setup** — Install Python 3.11+, create a virtual environment (`venv`), and install libraries. *Mistake to avoid:* installing packages globally instead of inside `venv`.
2. **Phase 2: Project Folder Creation** — Set up `data/`, `db/`, `src/`, `outputs/`, `images/`, `reports/`, `docs/`, `tests/`. *Mistake to avoid:* putting all code and outputs in one flat folder.
3. **Phase 3: Expense CSV Creation** — Generate 6 months of realistic synthetic transactions (`src/data_generator.py`). *Mistake to avoid:* using only 5–10 rows, which makes monthly trend charts look empty.
4. **Phase 4: Expense Data Loading** — Build `src/models.py` (SQLite tables) and `src/ingest.py`. *Mistake to avoid:* inserting duplicate rows on repeated script runs (solved with `UNIQUE` constraint + `INSERT OR IGNORE`).
5. **Phase 5: Data Cleaning** — Parse dates with `errors="coerce"`, strip strings, drop NaNs. *Mistake to avoid:* assuming bank CSV dates are always valid.
6. **Phase 6: Category-Wise Analysis** — Group negative amounts by `category` and compute share %. *Mistake to avoid:* mixing positive income rows into expense totals.
7. **Phase 7: Monthly Trend Analysis** — Group by `YYYY-MM` to compare income vs. spend and net savings. *Mistake to avoid:* sorting months alphabetically instead of chronologically.
8. **Phase 8: Data Visualization** — Generate bar, line, pie, and daily trend charts (`src/visualize.py`). *Mistake to avoid:* overlapping x-axis labels or missing currency units.
9. **Phase 9: Report Generation** — Export CSV summaries, a TXT executive summary, and a multi-sheet Excel workbook (`src/report.py`). *Mistake to avoid:* overwriting raw data files with summary outputs.
10. **Phase 10: GitHub Upload** — Initialize Git, write `README.md`, commit cleanly, and push with screenshots. *Mistake to avoid:* committing `venv/` or `__pycache__/`.

---

## 5. Folder Structure
- `data/`: Stores raw or synthetic input CSV files (`synthetic_expenses.csv`).
- `db/`: Stores the SQLite database (`expenses.db`).
- `notebooks/`: Jupyter notebooks for exploratory analysis (`expense_analysis_walkthrough.ipynb`).
- `src/`: Modular Python source files (`models.py`, `ingest.py`, `categorize.py`, `analyze.py`, `budget.py`, `visualize.py`, `report.py`, `app_streamlit.py`).
- `outputs/`: Clean aggregated CSV tables (`category_summary.csv`, `monthly_summary.csv`, `payment_method_summary.csv`).
- `images/`: High-resolution PNG charts generated by Matplotlib/Seaborn.
- `reports/`: Formatted `.txt` and `.xlsx` reports ready for sharing.
- `docs/`: Documentation, 14-part guide, and interview preparation notes.
- `tests/`: Automated unit tests (`test_tracker.py`).

---

## 6. Installation Guide

### Windows (PowerShell / CMD)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 7. Full Project Code
All executable, commented, modular Python files are included in this repository:
- `main.py` — End-to-end pipeline orchestrator
- `src/models.py` — SQLite schema
- `src/data_generator.py` — Synthetic dataset generator
- `src/ingest.py` — CSV loader & data cleaner
- `src/categorize.py` — Regex auto-categorizer
- `src/analyze.py` — KPIs & grouped analytics
- `src/budget.py` — Monthly budget tracker
- `src/visualize.py` — 4 Matplotlib/Seaborn charts
- `src/report.py` — CSV, TXT, and Excel exporter
- `src/app_streamlit.py` — Interactive Streamlit dashboard
- `tests/test_tracker.py` — Unit tests

---

## 8. Virtual Simulation
Because students rarely have direct bank API access, `src/data_generator.py` simulates a real 6-month personal finance ledger:
1. **Income & Fixed Bills**: Credits a monthly stipend/salary (INR 35,000–40,000) and deducts recurring bills (JioFiber, MSEDCL Electricity, Netflix).
2. **Daily Variable Spending**: Simulates 0–3 daily transactions across realistic Indian merchants (Swiggy, Zomato, D-Mart, Uber, Ola, Amazon, Apollo Pharmacy) and payment methods (UPI, Debit Card, Credit Card, Net Banking, Cash).
3. **Intentional Dirty Data**: Adds 2 corrupted rows (`invalid-date` and missing `Amount`) so you can prove your cleaning pipeline catches and drops bad records.
4. **Overspending Detection**: `src/budget.py` compares the latest month's actual spend against category limits and flags `OVER BUDGET` categories.

---

## 9. How to Run Project
```bash
# Run the complete ETL + Visualization + Reporting pipeline
python main.py

# Run the interactive Streamlit dashboard
streamlit run src/app_streamlit.py

# Run unit tests
pytest -v
```

### Expected Terminal Output
```text
1. Initializing SQLite database...
2. Generating synthetic expense dataset...
3. Loading and cleaning CSV data...
   Cleaned 266 rows (dropped 2 invalid, 0 duplicates); inserted 266 new rows.
4. Auto-categorizing transactions...
   Categorized 266 transactions.
5. Running analytics...
6. Generating visualization charts...
   Saved chart: images/category_spending_bar.png
   Saved chart: images/monthly_spending_line.png
   Saved chart: images/payment_method_pie.png
   Saved chart: images/daily_spending_trend.png
7. Exporting CSV, TXT, and Excel reports...
...
Pipeline completed successfully!
```

---

## 10. GitHub Upload Steps

- **Recommended Repo Name**: `Personal-Expense-Tracker-Visualization`
- **Recommended Description**: `End-to-end Python & SQLite Personal Expense Tracker with automated data cleaning, regex categorization, budget alerts, Matplotlib/Seaborn charts, Excel reporting, and a Streamlit dashboard.`
- **GitHub Tags/Topics**: `python`, `pandas`, `sqlite`, `data-visualization`, `matplotlib`, `seaborn`, `streamlit`, `personal-finance`, `data-analytics`, `etl-pipeline`

```bash
git init
git add .
git commit -m "feat: initial commit with modular ETL, SQLite schema, charts, and Streamlit app"
git branch -M main
git remote add origin https://github.com/<your-username>/Personal-Expense-Tracker-Visualization.git
git push -u origin main
```

---

## 11. README.md
The complete, GitHub-ready `README.md` is located at the root of this project.

---

## 12. Proof Building Strategy (6-Day Commit Plan)

| Day | Focus | What to Commit | Commit Message | Screenshot to Save |
| :--- | :--- | :--- | :--- | :--- |
| **Day 1** | Setup & Schema | `requirements.txt`, `.gitignore`, `src/models.py` | `chore: initialize project structure and SQLite schema` | Folder tree |
| **Day 2** | Synthetic Data | `src/data_generator.py`, `data/synthetic_expenses.csv` | `feat: add 6-month synthetic expense dataset generator` | CSV preview |
| **Day 3** | Cleaning & Categorization | `src/ingest.py`, `src/categorize.py` | `feat: implement CSV cleaning and regex auto-categorization` | Terminal cleaning log |
| **Day 4** | Category & Payment Charts | `src/analyze.py`, `src/visualize.py` | `feat: add category bar and payment method pie charts` | `category_spending_bar.png` |
| **Day 5** | Monthly & Daily Trends | `src/budget.py`, `monthly_spending_line.png`, `daily_spending_trend.png` | `feat: add monthly trend, daily rolling avg, and budget alerts` | `monthly_spending_line.png` |
| **Day 6** | Reports, Streamlit & Docs | `src/report.py`, `src/app_streamlit.py`, `README.md`, `tests/` | `docs: add Excel/TXT reporting, Streamlit UI, tests, and README` | Streamlit & GitHub repo |

---

## 13. Screenshots / Outputs Checklist
Capture and verify these 9 items for your portfolio and README:
1. Project folder structure screenshot
2. `data/synthetic_expenses.csv` preview
3. Terminal output from `python main.py`
4. `images/category_spending_bar.png`
5. `images/monthly_spending_line.png`
6. `images/payment_method_pie.png`
7. `images/daily_spending_trend.png`
8. `reports/monthly_summary_report.txt` & `reports/monthly_report.xlsx`
9. Live GitHub repository & Streamlit dashboard screenshot

---

## 14. Interview Preparation (10 Questions & Answers)

### Q1. Explain your project.
- **HR / 30-Second Pitch**: "I built a Personal Expense Tracker in Python that takes raw transaction CSVs, automatically cleans and categorizes them into a SQLite database, checks monthly budgets, and generates visual charts, Excel reports, and a Streamlit dashboard so users can control overspending."
- **Technical Explanation**: "It's a modular ETL and analytics pipeline. `ingest.py` normalizes CSVs and drops invalid/duplicate rows, `categorize.py` applies regex rules to classify merchants, `models.py` stores normalized tables in SQLite with foreign keys, `analyze.py` computes KPIs and rolling averages, and `visualize.py`/`report.py`/`app_streamlit.py` deliver the outputs."

### Q2. Why did you use SQLite instead of keeping everything in CSVs?
SQLite gives relational integrity (foreign keys between `transactions` and `categories`), prevents duplicate imports using `UNIQUE` constraints with `INSERT OR IGNORE`, and supports fast SQL aggregations without loading every file into memory.

### Q3. How did you handle dirty or inconsistent data in CSVs?
In `src/ingest.py`, I used `pd.to_datetime(..., errors="coerce")` to catch invalid dates, `pd.to_numeric(..., errors="coerce")` for amounts, `.str.strip()` for whitespace, and `drop_duplicates()` on key transaction columns.

### Q4. How does your auto-categorization work, and how would you improve it?
It uses regex pattern matching on merchant descriptions (e.g., `swiggy|zomato` -> `Food & Dining`) and checks the sign of the amount for `Income`. To scale it, I would train a `MultinomialNB` or TF-IDF + Logistic Regression model on user-corrected historical labels.

### Q5. How do you prevent duplicate transactions if the same CSV is uploaded twice?
The `transactions` table has a composite `UNIQUE(tx_date, description, amount, payment_method, account)` constraint, and `upsert_transactions()` uses `INSERT OR IGNORE` alongside Pandas deduplication.

### Q6. What KPIs did you calculate and why?
Total Income, Total Spend, Net Savings, Savings Rate %, Average Daily Spend, Average Monthly Spend, and Highest Spending Category—because these directly answer whether a user is living within their means and where to cut costs.

### Q7. Why did you include a 7-day rolling average on the daily spending chart?
Daily spending is noisy (some days have ₹0, others have a ₹3,000 grocery run). A 7-day rolling average smooths out spikes so the underlying spending trend is immediately visible.

### Q8. How does budget tracking work in your system?
`src/budget.py` stores monthly category limits in the `budgets` table and performs a SQL `LEFT JOIN` against aggregated monthly spend to compute `variance = limit_amount - actual_spend` and flag `OVER BUDGET` items.

### Q9. How did you ensure code quality and maintainability?
I separated concerns into single-responsibility modules under `src/`, added docstrings and type hints, and wrote unit tests in `tests/test_tracker.py` to verify cleaning, categorization, KPIs, and budget alerts.

### Q10. What real-world extensions would you add next?
Receipt OCR with Tesseract, scheduled email/Telegram alerts when a category crosses 80% of its budget, recurring transaction detection (rent/EMI), and multi-currency FX conversion.
