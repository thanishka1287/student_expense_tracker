"""
analysis.py - Exploratory Data Analysis module for Student Expense Tracker.
Contains functions to clean data, compute core spending metrics, analyze category,
monthly, and payment trends, and evaluate budget vs actual student expenditures.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "student_expenses.csv")


def load_and_clean_data(filepath=DATA_PATH):
    """
    Load student expense dataset and perform data cleaning and validation:
    - Validate column presence
    - Check and report missing values
    - Check and report duplicate rows
    - Parse Date column into datetime
    - Derive Month (YYYY-MM), Month Name, and Day of Week
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at: {filepath}")

    df = pd.read_csv(filepath)

    # Validate essential columns
    expected_cols = [
        "Student ID", "Date", "Category", "Amount",
        "Payment Method", "Monthly Budget", "Student Year"
    ]
    for col in expected_cols:
        if col not in df.columns:
            raise ValueError(f"Missing expected column '{col}' in dataset.")

    # Data cleaning
    # Check for missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        df = df.dropna().reset_index(drop=True)

    # Check for duplicates
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)

    # Convert Date to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Feature engineering for temporal analysis
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    df["Month_Name"] = df["Date"].dt.strftime("%B %Y")
    df["Day_of_Week"] = df["Date"].dt.day_name()

    # Sort values chronologically
    df = df.sort_values(by="Date").reset_index(drop=True)

    return df


def get_summary_metrics(df):
    """
    Calculate high-level summary KPIs.
    """
    total_spending = float(df["Amount"].sum())
    total_transactions = int(len(df))
    avg_transaction = float(df["Amount"].mean()) if total_transactions > 0 else 0.0
    median_transaction = float(df["Amount"].median()) if total_transactions > 0 else 0.0
    min_transaction = float(df["Amount"].min()) if total_transactions > 0 else 0.0
    max_transaction = float(df["Amount"].max()) if total_transactions > 0 else 0.0

    # Calculate overall budget utilization across student-months
    monthly_student = df.groupby(["Month", "Student ID", "Monthly Budget"])["Amount"].sum().reset_index()
    total_budget_allocated = float(monthly_student["Monthly Budget"].sum())
    total_actual_spent = float(monthly_student["Amount"].sum())
    overall_budget_utilization = (
        (total_actual_spent / total_budget_allocated) * 100
        if total_budget_allocated > 0
        else 0.0
    )

    return {
        "total_spending": total_spending,
        "total_transactions": total_transactions,
        "avg_transaction": avg_transaction,
        "median_transaction": median_transaction,
        "min_transaction": min_transaction,
        "max_transaction": max_transaction,
        "total_budget_allocated": total_budget_allocated,
        "overall_budget_utilization": overall_budget_utilization,
    }


def analyze_by_category(df):
    """
    Aggregate spending metrics by expense category.
    """
    category_summary = df.groupby("Category").agg(
        Total_Amount=("Amount", "sum"),
        Transaction_Count=("Amount", "count"),
        Average_Amount=("Amount", "mean")
    ).reset_index()

    total_spend = df["Amount"].sum()
    category_summary["Percentage_Share"] = (
        (category_summary["Total_Amount"] / total_spend) * 100
    ).round(2)
    category_summary["Average_Amount"] = category_summary["Average_Amount"].round(2)

    category_summary = category_summary.sort_values(
        by="Total_Amount", ascending=False
    ).reset_index(drop=True)
    return category_summary


def analyze_monthly_trends(df):
    """
    Aggregate spending metrics month by month.
    """
    monthly_summary = df.groupby("Month").agg(
        Total_Amount=("Amount", "sum"),
        Transaction_Count=("Amount", "count"),
        Average_Amount=("Amount", "mean")
    ).reset_index()

    monthly_summary["Average_Amount"] = monthly_summary["Average_Amount"].round(2)
    monthly_summary = monthly_summary.sort_values("Month").reset_index(drop=True)

    # Highest and lowest spending months
    highest_month_row = monthly_summary.loc[monthly_summary["Total_Amount"].idxmax()]
    lowest_month_row = monthly_summary.loc[monthly_summary["Total_Amount"].idxmin()]

    return {
        "monthly_summary": monthly_summary,
        "highest_month": {
            "Month": highest_month_row["Month"],
            "Total_Amount": float(highest_month_row["Total_Amount"])
        },
        "lowest_month": {
            "Month": lowest_month_row["Month"],
            "Total_Amount": float(lowest_month_row["Total_Amount"])
        }
    }


def analyze_payment_methods(df):
    """
    Aggregate spending and transaction count by payment method.
    """
    payment_summary = df.groupby("Payment Method").agg(
        Total_Amount=("Amount", "sum"),
        Transaction_Count=("Amount", "count"),
        Average_Amount=("Amount", "mean")
    ).reset_index()

    total_txns = len(df)
    total_spend = df["Amount"].sum()

    payment_summary["Transaction_Share"] = (
        (payment_summary["Transaction_Count"] / total_txns) * 100
    ).round(2)
    payment_summary["Spending_Share"] = (
        (payment_summary["Total_Amount"] / total_spend) * 100
    ).round(2)
    payment_summary["Average_Amount"] = payment_summary["Average_Amount"].round(2)

    return payment_summary.sort_values(by="Total_Amount", ascending=False).reset_index(drop=True)


def analyze_budget_vs_actual(df):
    """
    Compare monthly allocated budget with actual spending.
    Identifies student-month pairs that exceeded budget.
    """
    # Group by Month, Student ID, and Monthly Budget
    student_monthly = df.groupby(["Month", "Student ID", "Monthly Budget", "Student Year"]).agg(
        Actual_Spent=("Amount", "sum"),
        Transaction_Count=("Amount", "count")
    ).reset_index()

    student_monthly["Budget_Utilization"] = (
        (student_monthly["Actual_Spent"] / student_monthly["Monthly Budget"]) * 100
    ).round(2)
    student_monthly["Over_Budget"] = (
        student_monthly["Actual_Spent"] > student_monthly["Monthly Budget"]
    )
    student_monthly["Difference"] = (
        student_monthly["Actual_Spent"] - student_monthly["Monthly Budget"]
    )

    over_budget_records = student_monthly[student_monthly["Over_Budget"]].sort_values(
        by="Difference", ascending=False
    ).reset_index(drop=True)

    # Monthly aggregated budget vs actual
    month_agg = student_monthly.groupby("Month").agg(
        Total_Budget=("Monthly Budget", "sum"),
        Total_Spent=("Actual_Spent", "sum"),
        Exceeded_Count=("Over_Budget", "sum"),
        Total_Students=("Student ID", "nunique")
    ).reset_index()

    month_agg["Utilization_Percentage"] = (
        (month_agg["Total_Spent"] / month_agg["Total_Budget"]) * 100
    ).round(2)

    return {
        "student_monthly": student_monthly,
        "over_budget_records": over_budget_records,
        "month_agg": month_agg,
        "total_over_budget_instances": int(len(over_budget_records))
    }


def analyze_by_student_year(df):
    """
    Aggregate spending across academic years.
    """
    year_summary = df.groupby("Student Year").agg(
        Total_Amount=("Amount", "sum"),
        Transaction_Count=("Amount", "count"),
        Average_Amount=("Amount", "mean")
    ).reset_index()

    total_spend = df["Amount"].sum()
    year_summary["Percentage_Share"] = (
        (year_summary["Total_Amount"] / total_spend) * 100
    ).round(2)
    year_summary["Average_Amount"] = year_summary["Average_Amount"].round(2)

    return year_summary.sort_values(by="Total_Amount", ascending=False).reset_index(drop=True)


def print_full_report():
    """
    Run full exploratory analysis and print formatted results to console.
    """
    print("=" * 65)
    print("       STUDENT EXPENSE TRACKER - DATA ANALYTICS REPORT       ")
    print("=" * 65)

    df = load_and_clean_data()
    print(f"\n[+] Dataset successfully loaded: {len(df)} records across {df['Student ID'].nunique()} students.")
    print(f"    Date span: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")

    # Summary
    metrics = get_summary_metrics(df)
    print("\n--- 1. High-Level Summary ---")
    print(f"Total Spending:              INR {metrics['total_spending']:,.2f}")
    print(f"Total Transactions:          {metrics['total_transactions']:,}")
    print(f"Average Expense / Txn:       INR {metrics['avg_transaction']:,.2f}")
    print(f"Median Expense / Txn:        INR {metrics['median_transaction']:,.2f}")
    print(f"Min / Max Expense:           INR {metrics['min_transaction']:,.2f} / INR {metrics['max_transaction']:,.2f}")
    print(f"Overall Budget Utilization:  {metrics['overall_budget_utilization']:.2f}%")

    # Categories
    cat_df = analyze_by_category(df)
    print("\n--- 2. Spending by Category ---")
    print(cat_df.to_string(index=False))

    # Monthly Trends
    month_data = analyze_monthly_trends(df)
    print("\n--- 3. Monthly Spending Trends ---")
    print(month_data["monthly_summary"].to_string(index=False))
    print(f"\n>> Highest Spending Month: {month_data['highest_month']['Month']} (INR {month_data['highest_month']['Total_Amount']:,.2f})")
    print(f">> Lowest Spending Month:  {month_data['lowest_month']['Month']} (INR {month_data['lowest_month']['Total_Amount']:,.2f})")

    # Payment Methods
    pay_df = analyze_payment_methods(df)
    print("\n--- 4. Payment Method Usage ---")
    print(pay_df.to_string(index=False))

    # Budget Analysis
    budget_data = analyze_budget_vs_actual(df)
    print("\n--- 5. Budget vs Actual Spending (Monthly) ---")
    print(budget_data["month_agg"].to_string(index=False))

    print(f"\n>> Total instances of budget overruns: {budget_data['total_over_budget_instances']}")
    if not budget_data["over_budget_records"].empty:
        print("\nTop Over-Budget Student-Month Records:")
        cols = ["Month", "Student ID", "Student Year", "Monthly Budget", "Actual_Spent", "Difference", "Budget_Utilization"]
        print(budget_data["over_budget_records"][cols].head(10).to_string(index=False))

    # Academic Year
    year_df = analyze_by_student_year(df)
    print("\n--- 6. Spending by Student Academic Year ---")
    print(year_df.to_string(index=False))

    print("\n" + "=" * 65)
    print("                      END OF REPORT                          ")
    print("=" * 65)


if __name__ == "__main__":
    print_full_report()
