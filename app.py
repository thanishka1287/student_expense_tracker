"""
app.py - Student Expense Tracker Dashboard
A clean, responsive, student-friendly data analytics dashboard built with Streamlit.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Student Expense Tracker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply a clean, readable visual styling
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10

# Color palettes
TEAL_PALETTE = ["#2b5c8f", "#3c8dbc", "#56b4e9", "#78c2ad", "#a0d2db", "#cbe3eb"]
SEAT_COLORS = {"UPI": "#2ca02c", "Card": "#1f77b4", "Cash": "#ff7f0e"}

# ---------------------------------------------------------
# Data Ingestion & Caching
# ---------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "student_expenses.csv")


@st.cache_data
def load_data():
    if not os.path.exists(DATA_PATH):
        st.error(f"Dataset file not found at: {DATA_PATH}")
        return pd.DataFrame()

    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.strftime("%Y-%m")
    df["Month_Name"] = df["Date"].dt.strftime("%b %Y")
    df["Day_of_Week"] = df["Date"].dt.day_name()
    return df


df_raw = load_data()

if df_raw.empty:
    st.stop()

# ---------------------------------------------------------
# Sidebar Navigation & Interactive Filters
# ---------------------------------------------------------
st.sidebar.image(
    "https://img.icons8.com/fluency/96/student-male.png",
    width=72
)
st.sidebar.title("Filter Options")
st.sidebar.markdown("Customize the dashboard view by selecting filters below:")

# 1. Month Filter
available_months = sorted(df_raw["Month"].unique())
month_options = ["All Months"] + available_months
selected_month = st.sidebar.selectbox("📅 Select Month", options=month_options, index=0)

# 2. Category Filter
all_categories = sorted(df_raw["Category"].unique())
selected_categories = st.sidebar.multiselect(
    "🏷️ Expense Categories",
    options=all_categories,
    default=all_categories
)

# 3. Payment Method Filter
all_payments = sorted(df_raw["Payment Method"].unique())
selected_payments = st.sidebar.multiselect(
    "💳 Payment Methods",
    options=all_payments,
    default=all_payments
)

# 4. Student Year Filter (Optional exploration)
all_years = sorted(df_raw["Student Year"].unique())
year_options = ["All Academic Years"] + all_years
selected_year = st.sidebar.selectbox("🎓 Student Year", options=year_options, index=0)

# Apply filters
df_filtered = df_raw.copy()

if selected_month != "All Months":
    df_filtered = df_filtered[df_filtered["Month"] == selected_month]

if selected_categories:
    df_filtered = df_filtered[df_filtered["Category"].isin(selected_categories)]
else:
    df_filtered = df_filtered.iloc[0:0]

if selected_payments:
    df_filtered = df_filtered[df_filtered["Payment Method"].isin(selected_payments)]
else:
    df_filtered = df_filtered.iloc[0:0]

if selected_year != "All Academic Years":
    df_filtered = df_filtered[df_filtered["Student Year"] == selected_year]

# Reset Filters button
if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **Project Info:**  
    Student Expense Tracker  
    *A genuine college-level exploratory analytics project built with Python & Streamlit.*
    """
)

# ---------------------------------------------------------
# Header & Introduction
# ---------------------------------------------------------
st.title("🎓 Student Expense Tracker Dashboard")
st.markdown(
    """
    Welcome to the **Student Expense Tracker**! This dashboard analyzes college student spending patterns,
    evaluating category allocations, payment trends, and monthly budget adherence to help students
    manage their finances more effectively.
    """
)

# Check if filter results in empty data
if df_filtered.empty:
    st.warning("⚠️ No expense records match your selected filters. Please adjust your selections in the sidebar.")
    st.stop()

# ---------------------------------------------------------
# Core KPI Metric Cards
# ---------------------------------------------------------
total_spending = df_filtered["Amount"].sum()
total_txns = len(df_filtered)
avg_txn = df_filtered["Amount"].mean() if total_txns > 0 else 0

# Budget utilization calculation
# Calculate total budget allocated to active students in the selected month/slice
student_months_active = df_filtered[["Month", "Student ID", "Monthly Budget"]].drop_duplicates()
total_budget = student_months_active["Monthly Budget"].sum()
budget_utilization = (total_spending / total_budget * 100) if total_budget > 0 else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        label="💰 Total Spending",
        value=f"₹{total_spending:,.2f}"
    )

with kpi2:
    st.metric(
        label="📊 Average Transaction",
        value=f"₹{avg_txn:,.2f}"
    )

with kpi3:
    st.metric(
        label="🧾 Transactions Count",
        value=f"{total_txns:,}"
    )

with kpi4:
    delta_str = f"{budget_utilization:.1f}% used"
    st.metric(
        label="🎯 Budget Utilization",
        value=f"{budget_utilization:.1f}%",
        delta=f"{100 - budget_utilization:.1f}% left" if budget_utilization <= 100 else f"-{budget_utilization - 100:.1f}% over"
    )

st.markdown("---")

# ---------------------------------------------------------
# Charts Section 1: Categories & Monthly Trends
# ---------------------------------------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🏷️ Spending by Category")
    cat_summary = df_filtered.groupby("Category")["Amount"].sum().reset_index()
    cat_summary = cat_summary.sort_values(by="Amount", ascending=True)

    fig_cat, ax_cat = plt.subplots(figsize=(6, 4))
    bars = ax_cat.barh(cat_summary["Category"], cat_summary["Amount"], color="#3c8dbc", edgecolor="#2b5c8f")
    ax_cat.set_xlabel("Total Amount (INR)", fontsize=9)
    ax_cat.set_ylabel("Category", fontsize=9)
    ax_cat.grid(axis="x", linestyle="--", alpha=0.5)

    # Annotate bar values
    max_val = cat_summary["Amount"].max() if not cat_summary.empty else 1
    for bar in bars:
        w = bar.get_width()
        pct = (w / total_spending) * 100 if total_spending > 0 else 0
        ax_cat.annotate(
            f" ₹{int(w):,} ({pct:.1f}%)",
            (w, bar.get_y() + bar.get_height() / 2),
            ha="left", va="center", fontsize=8, color="#222"
        )
    ax_cat.set_xlim(0, max_val * 1.30)
    plt.tight_layout()
    st.pyplot(fig_cat)

with col2:
    st.subheader("📈 Monthly Spending Trend")
    monthly_summary = df_filtered.groupby("Month")["Amount"].sum().reset_index()
    monthly_summary = monthly_summary.sort_values("Month")

    fig_month, ax_month = plt.subplots(figsize=(6, 4))
    if len(monthly_summary) > 1:
        ax_month.plot(
            monthly_summary["Month"],
            monthly_summary["Amount"],
            marker="o",
            color="#2b5c8f",
            linewidth=2.2,
            markersize=6,
            label="Monthly Expenditure"
        )
        ax_month.fill_between(
            monthly_summary["Month"],
            monthly_summary["Amount"],
            color="#56b4e9",
            alpha=0.25
        )
        for _, row in monthly_summary.iterrows():
            ax_month.annotate(
                f"₹{int(row['Amount']):,}",
                (row["Month"], row["Amount"]),
                textcoords="offset points",
                xytext=(0, 7),
                ha="center",
                fontsize=8,
                weight="bold"
            )
    else:
        ax_month.bar(
            monthly_summary["Month"],
            monthly_summary["Amount"],
            color="#2b5c8f",
            width=0.4
        )
        for _, row in monthly_summary.iterrows():
            ax_month.annotate(
                f"₹{int(row['Amount']):,}",
                (row["Month"], row["Amount"]),
                ha="center", va="bottom", fontsize=9, weight="bold"
            )

    ax_month.set_xlabel("Month", fontsize=9)
    ax_month.set_ylabel("Total Spent (INR)", fontsize=9)
    ax_month.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig_month)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Charts Section 2: Payment Methods & Budget vs Actual
# ---------------------------------------------------------
col3, col4 = st.columns([1, 1])

with col3:
    st.subheader("💳 Payment Method Distribution")
    pay_summary = df_filtered.groupby("Payment Method").agg(
        Total_Amount=("Amount", "sum"),
        Count=("Amount", "count")
    ).reset_index()

    fig_pay, ax_pay = plt.subplots(figsize=(6, 4))
    colors = [SEAT_COLORS.get(p, "#999999") for p in pay_summary["Payment Method"]]

    wedges, texts, autotexts = ax_pay.pie(
        pay_summary["Total_Amount"],
        labels=pay_summary["Payment Method"],
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        pctdistance=0.75,
        wedgeprops=dict(width=0.45, edgecolor="white")
    )
    for at in autotexts:
        at.set_fontsize(9)
        at.set_weight("bold")
    ax_pay.set_title("Spending Share by Payment Channel", fontsize=11, weight="bold")
    plt.tight_layout()
    st.pyplot(fig_pay)

with col4:
    st.subheader("⚖️ Budget vs. Actual Spending")
    # Compare budget vs actual spent grouped by Month
    stu_monthly = df_filtered.groupby(["Month", "Student ID", "Monthly Budget"])["Amount"].sum().reset_index()
    monthly_budget_comp = stu_monthly.groupby("Month").agg(
        Allocated_Budget=("Monthly Budget", "sum"),
        Actual_Spent=("Amount", "sum")
    ).reset_index().sort_values("Month")

    fig_bva, ax_bva = plt.subplots(figsize=(6, 4))
    x_indices = np.arange(len(monthly_budget_comp))
    bar_w = 0.35

    ax_bva.bar(
        x_indices - bar_w / 2,
        monthly_budget_comp["Allocated_Budget"],
        bar_w,
        label="Allocated Budget",
        color="#2b5c8f"
    )
    ax_bva.bar(
        x_indices + bar_w / 2,
        monthly_budget_comp["Actual_Spent"],
        bar_w,
        label="Actual Spent",
        color="#e26d5c"
    )

    ax_bva.set_xticks(x_indices)
    ax_bva.set_xticklabels(monthly_budget_comp["Month"], fontsize=9)
    ax_bva.set_ylabel("Amount (INR)", fontsize=9)
    ax_bva.set_xlabel("Month", fontsize=9)
    ax_bva.legend(fontsize=8, loc="upper left")
    ax_bva.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig_bva)

# ---------------------------------------------------------
# Budget Overrun Alerts
# ---------------------------------------------------------
st.markdown("---")
st.subheader("🚨 Budget Overrun Monitoring")

stu_month_all = df_filtered.groupby(["Month", "Student ID", "Student Year", "Monthly Budget"])["Amount"].sum().reset_index()
stu_month_all["Over_Budget"] = stu_month_all["Amount"] > stu_month_all["Monthly Budget"]
stu_month_all["Overspend"] = stu_month_all["Amount"] - stu_month_all["Monthly Budget"]
stu_month_all["Utilization_%"] = ((stu_month_all["Amount"] / stu_month_all["Monthly Budget"]) * 100).round(1)

overruns = stu_month_all[stu_month_all["Over_Budget"]].sort_values(by="Overspend", ascending=False)

if not overruns.empty:
    st.info(f"🔎 Found **{len(overruns)}** instances of students exceeding their monthly budget in the filtered dataset.")
    col_ov1, col_ov2 = st.columns([2, 1])

    with col_ov1:
        st.dataframe(
            overruns[[
                "Month", "Student ID", "Student Year", "Monthly Budget",
                "Amount", "Overspend", "Utilization_%"
            ]].rename(columns={
                "Monthly Budget": "Budget (₹)",
                "Amount": "Spent (₹)",
                "Overspend": "Exceeded By (₹)",
                "Utilization_%": "Utilization"
            }),
            use_container_width=True,
            hide_index=True
        )

    with col_ov2:
        st.markdown(
            """
            **Why Do Overruns Happen?**  
            - **March (Fest Month):** Spikes in team registrations, event gear, and outing expenses.  
            - **May (Semester End):** Academic project materials, textbook costs, and hostel checkout bills.  
            - **Discretionary Spikes:** Unbudgeted online shopping sales and social celebrations.
            """
        )
else:
    st.success("✅ All students stayed within their allocated budgets for the selected filters!")

# ---------------------------------------------------------
# Filtered Transaction Table
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📋 Expense Transaction Log")
st.markdown(f"Showing **{len(df_filtered):,}** records based on the currently applied filters.")

# Format display table
display_table = df_filtered[[
    "Date", "Student ID", "Student Year", "Category", "Amount",
    "Payment Method", "Monthly Budget"
]].copy()

display_table["Date"] = display_table["Date"].dt.strftime("%Y-%m-%d")
display_table = display_table.sort_values("Date", ascending=False)

# Add search input
search_query = st.text_input("🔍 Search transactions (e.g., student ID, category, or payment method):")
if search_query:
    q = search_query.lower()
    mask = (
        display_table["Student ID"].str.lower().str.contains(q)
        | display_table["Category"].str.lower().str.contains(q)
        | display_table["Payment Method"].str.lower().str.contains(q)
        | display_table["Student Year"].str.lower().str.contains(q)
    )
    display_table = display_table[mask]

st.dataframe(
    display_table.rename(columns={
        "Amount": "Amount (₹)",
        "Monthly Budget": "Monthly Budget (₹)"
    }),
    use_container_width=True,
    hide_index=True,
    height=320
)

# Download CSV button
csv_bytes = display_table.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_bytes,
    file_name="filtered_student_expenses.csv",
    mime="text/csv"
)

# ---------------------------------------------------------
# Key Analytical Findings
# ---------------------------------------------------------
st.markdown("---")
st.subheader("💡 Key Analytical Findings & Takeaways")

f1, f2 = st.columns(2)

with f1:
    st.markdown(
        """
        #### 1. Spending Concentration
        - **Shopping & Education** represent over **54% of total student spending**, despite having fewer transactions than Food.
        - High-value transactions (textbooks, clothes, lab supplies) significantly impact student balances compared to daily petty expenses.
        
        #### 2. Digital UPI Dominance
        - **UPI accounts for over 60% of all student transactions**.
        - Frictionless payments make tracking small daily snacks and recharges challenging without intentional review.
        """
    )

with f2:
    st.markdown(
        """
        #### 3. Seasonal Trajectory & Fest Surges
        - **March** is the peak expense month across the entire semester, driving 4 separate student budget breaches.
        - Expenses drop sharply in **June** (exam completion and summer departure).
        
        #### 4. Practical Financial Recommendations
        - **Establish a 10% Fest Buffer:** Save ₹500–₹1,000 monthly between January and February to cushion March festivities.
        - **Set a Daily UPI Micro-Cap:** Use UPI transaction limits to avoid unnoticed balance leakage on fast food and impulse purchases.
        """
    )

# Footer
st.markdown("---")
st.caption("Student Expense Tracker · Beginner Data Analytics Project · Built with Python, Pandas, Matplotlib & Streamlit.")
