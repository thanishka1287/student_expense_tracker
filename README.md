# 🎓 Student Expense Tracker

A simple, beginner-friendly data analytics project that analyzes college students' spending habits, category breakdowns, payment channels, and monthly budget discipline.

---

## 📌 Project Overview

Managing personal finances as a college student can be tricky. Between canteen meals, shared autos, textbooks, weekend hangouts, and online shopping, monthly allowances often disappear without students knowing where the money actually went.

This project was built to explore and visualize actual student expenditure data. It tracks expenses across multiple students, compares actual expenditures against allocated monthly budgets, identifies spending spikes (such as during college fest season), and provides a clean interactive dashboard to explore the data.

---

## 🎯 Objectives

1. **Track Student Spending:** Aggregate and analyze daily student expenses across six core categories (*Food, Transport, Education, Shopping, Entertainment, Bills and Other*).
2. **Evaluate Budget Adherence:** Identify which students stayed within their monthly budgets, which exceeded them, and by how much.
3. **Analyze Payment Behavior:** Examine how students pay for transactions (UPI, Debit/Credit Cards, or Cash).
4. **Identify Seasonal Trends:** Spot monthly spending patterns, especially during exam times and campus cultural events.
5. **Interactive Exploration:** Provide an intuitive Streamlit dashboard that lets users filter by month, category, payment mode, and academic year in real time.

---

## 📁 Dataset Source & Description

- **Source:** Synthetically generated realistic dataset (`data/student_expenses.csv`).
- **Transparency Note:** To protect personal student financial privacy while maintaining realistic student behavior, this dataset was synthetically generated using authentic college expense ranges and probability distributions. It is explicitly synthetic and not scraped from an external personal bank account.
- **Size:** 520 transaction records across 15 students spanning 6 months (January 1, 2024 to June 30, 2024).

### Dataset Schema:

| Column | Type | Description | Example Values |
| :--- | :--- | :--- | :--- |
| `Student ID` | Text | Unique identifier for each student | `STU101`, `STU102` ... `STU115` |
| `Date` | Date | Date of expense (YYYY-MM-DD) | `2024-03-14` |
| `Category` | Text | Classification of expenditure | `Food`, `Transport`, `Education`, `Shopping`, `Entertainment`, `Bills and Other` |
| `Amount` | Integer | Transaction value in Indian Rupees (₹) | `250`, `1200` |
| `Payment Method` | Text | Mode of payment | `UPI`, `Cash`, `Card` |
| `Monthly Budget` | Integer | Fixed monthly budget for the student (₹) | `7000` to `13000` |
| `Student Year` | Text | Academic seniority | `1st Year`, `2nd Year`, `3rd Year`, `4th Year` |

---

## 🛠️ Technologies Used

- **Python 3.10+**: Core programming language
- **Pandas**: Data manipulation, cleaning, and aggregations
- **NumPy**: Numerical operations and array calculations
- **Matplotlib & Seaborn**: Data visualizations and statistical plots
- **Streamlit**: Interactive web dashboard
- **Jupyter Notebook**: Step-by-step exploratory data analysis document
- **Git & GitHub**: Version control and project collaboration

---

## 📂 Project Structure

```text
student_expense_tracker/
├── app.py                             # Streamlit interactive web dashboard
├── requirements.txt                   # Project Python dependencies
├── README.md                          # Project documentation
├── .gitignore                         # Ignored files (venv, caches, etc.)
├── data/
│   └── student_expenses.csv           # Cleaned expense dataset (520 rows)
├── notebooks/
│   └── student_expense_analysis.ipynb # Fully executed Jupyter notebook with EDA
└── analysis/
    └── analysis.py                    # Standalone modular analysis script
```

---

## 🚀 Installation & Setup

### Prerequisites
Make sure you have Python 3.10 or later installed on your system.

### 1. Clone the Repository
```bash
git clone https://github.com/thanishka1287/student_expense_tracker.git
cd student_expense_tracker
```

### 2. Set Up a Virtual Environment (Recommended)
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows (Command Prompt / PowerShell):
```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 💻 How to Run

### Run the Interactive Dashboard
Launch the Streamlit app from the project root:
```bash
streamlit run app.py
```
After running, open your web browser and navigate to:
```text
http://localhost:8501
```

### Run the Command-Line Analysis Report
To quickly view all summary statistics and tabular metrics in your terminal:
```bash
python analysis/analysis.py
```

### Open the Jupyter Notebook
To inspect the exploratory data analysis, step-by-step charts, and markdown commentary:
```bash
jupyter notebook notebooks/student_expense_analysis.ipynb
```
*(Or simply open `notebooks/student_expense_analysis.ipynb` directly in VS Code or GitHub to view the pre-rendered outputs and charts!)*

---

## 📊 Key Analytical Findings

Based on analysis of the 520 student records:

1. **Top Expense Drivers:**
   - **Shopping (33.7%)** and **Education (20.3%)** make up over **54% of all spending** (₹222,358 combined), primarily driven by semester book purchases, tech accessories, and clothing sales.
   - **Food** is the most frequent category (**165 transactions**, ~32% of all expenses), but maintains a manageable average ticket size of **₹337.39**.

2. **The "Fest Month" Surge:**
   - **March 2024** was the single highest spending month (₹115,284), nearly doubling normal monthly averages.
   - 4 out of 7 total budget overruns occurred in March due to annual campus fests, team events, and social gatherings.
   - **June 2024** was the lowest spending month (₹55,899), as exams wrapped up and students headed home.

3. **Cashless Campus Adoption:**
   - **UPI** is the dominant payment channel, handling **62.5% of all transactions** and **60.2% of total expenditure**.
   - **Card** payments accounted for only 16.35% of transactions but had the highest average ticket size (**₹1,203.75**), typically used for high-value shopping and tuition fees.
   - **Cash** was used for 21.15% of transactions (small snacks, local autos, and printing/xerox).

4. **Budget Adherence:**
   - Overall cohort budget utilization was healthy at **47.96%**.
   - However, **7 individual student-month overruns** took place. The largest overspend was by student `STU110` in March, who spent ₹15,477 against a ₹7,000 monthly allowance (221.1% utilization).

---

## 🖼️ Dashboard Features & Screenshots

The Streamlit dashboard includes:
- **Header & Metric Cards:** Real-time updates for Total Spend, Average Transaction, Transaction Count, and Budget Utilization.
- **Interactive Sidebar Filters:** Filter by Month, Category, Payment Method, and Academic Year.
- **Visual Analytics:**
  - Category breakdown (horizontal bar chart with percentages)
  - Monthly spending trajectory (line chart with area fill)
  - Payment method distribution (donut chart)
  - Budget vs. Actual comparison (grouped bar chart)
- **Budget Overrun Alert Table:** Instantly flags students who exceeded their monthly limits.
- **Transaction Table with Search & CSV Export:** Search records in real-time and export filtered logs.

*To add your own screenshots:*
1. Run `streamlit run app.py` and take a screenshot of the dashboard.
2. Save the image in `screenshots/dashboard_preview.png`.
3. Reference it in markdown:
   ```markdown
   ![Dashboard Preview](screenshots/dashboard_preview.png)
   ```

---

## 🔮 Future Improvements

- [ ] Add an automatic SMS/email expense parser to auto-log transactions.
- [ ] Implement monthly savings goal tracking with custom progress bars.
- [ ] Add multi-currency support ($ USD, € EUR, £ GBP, ₹ INR).
- [ ] Include receipt upload and OCR text extraction for paper bills.
- [ ] Export automated PDF monthly spending summaries.

---

## 👤 Author

Developed by **Thanishka** as a college data analytics portfolio project.  
Feel free to open an issue or pull request if you have ideas or suggestions!
