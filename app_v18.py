
# APP V7 - Finance OS
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="Surojit Finance OS", layout="wide")

st.markdown("""
<style>
.block-container{padding-top:2rem;padding-bottom:1rem;}

.main-title{font-size:48px;font-weight:800;letter-spacing:2px;}
.subtitle{font-size:18px;color:#bdbdbd;}
.tagline{font-size:13px;color:#808080;margin-bottom:15px;}

.expense-summary,.savings-summary,.category-card{
transition:all .25s ease;
}

.expense-summary:hover,.savings-summary:hover,.category-card:hover{
transform:translateY(-6px);
}

.expense-summary,.savings-summary{
border-radius:24px;
padding:24px;
height:220px;
display:flex;
flex-direction:column;
justify-content:space-between;
}

.expense-summary{
background:linear-gradient(135deg, rgba(255,75,75,.18), rgba(255,75,75,.04));
border:1px solid rgba(255,75,75,.25);
box-shadow:0 4px 10px rgba(255,75,75,.14);
}

.savings-summary{
background:linear-gradient(135deg, rgba(0,210,106,.18), rgba(0,210,106,.04));
border:1px solid rgba(0,210,106,.25);
box-shadow:0 4px 10px rgba(0,210,106,.14);
}

.category-card{
background:linear-gradient(180deg,#232b38,#171c24);
border:1px solid #374151;
border-radius:18px;
padding:22px;
text-align:center;
min-height:145px;
margin:18px 12px;
box-shadow:0 8px 18px rgba(0,0,0,.28);
}

.section-title{
font-size:26px;
font-weight:700;
margin-top:18px;
margin-bottom:12px;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_excel("Expense Tracker.xlsx", sheet_name="Database", header=3)
    df.columns = df.columns.str.strip()
    return df.dropna(subset=["Year"])

df = load_data()

years = sorted(df["Year"].dropna().unique())
current_year = datetime.now().year
default_year = current_year if current_year in years else max(years)

c1,c2 = st.columns([8,2])

with c1:
    st.markdown('<div class="main-title">PERSONAL FINANCE DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">Expense Analytics • Savings Tracking • Financial Monitoring</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div style="text-align:right;color:#cbd5e1;font-weight:600;font-size:15px;margin-top:10px;">👤 Surojit Nath</div>', unsafe_allow_html=True)
    year = st.selectbox("Year", years, index=years.index(default_year))
    month = st.selectbox("Month", ["All"] + list(df["Month"].dropna().unique()))

filtered = df[df["Year"] == year]

if month != "All":
    filtered = filtered[filtered["Month"] == month]

filtered = filtered[pd.to_numeric(filtered["Total Spent"], errors="coerce").fillna(0) != 0]

total_expense = pd.to_numeric(filtered["Total Spent"], errors="coerce").fillna(0).sum()
investment = pd.to_numeric(filtered["Investments"], errors="coerce").fillna(0).sum()
personal = pd.to_numeric(filtered["Personal"], errors="coerce").fillna(0).sum()
total_savings = pd.to_numeric(filtered["Total Savings"], errors="coerce").fillna(0).sum()

monthly_avg = total_expense / len(filtered) if len(filtered) else 0

cashflow = total_expense + total_savings
expense_pct = (total_expense/cashflow*100) if cashflow else 0
savings_pct = (total_savings/cashflow*100) if cashflow else 0

expense_alpha = 0.15 + (expense_pct/100)*0.45
savings_alpha = 0.15 + (savings_pct/100)*0.45


left,right = st.columns(2)

with left:
    st.markdown(f"""
    <div style="border-radius:24px;padding:24px;height:220px;
    background:linear-gradient(135deg, rgba(255,75,75,{expense_alpha}), rgba(255,75,75,.05));
    border:1px solid rgba(255,75,75,.35);position:relative;">
    <div style="position:absolute;right:20px;top:18px;background:rgba(255,75,75,.30);padding:8px 16px;border-radius:999px;font-weight:800;">{expense_pct:.1f}%</div>
    <div style="font-size:30px;font-weight:800;">Total Expense</div>
    <div style="font-size:48px;font-weight:800;color:#ff5a5a;margin-top:18px;">₹ {total_expense:,.0f}</div>
    <div style="margin-top:22px;font-size:16px;">Monthly Avg ₹ {monthly_avg:,.0f}</div>
<div style="margin-top:12px;background:rgba(255,255,255,.08);height:10px;border-radius:999px;overflow:hidden">
<div style="width:{expense_pct:.1f}%;height:10px;background:rgba(255,75,75,.85)"></div>
</div>

    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div style="border-radius:24px;padding:24px;height:220px;background:linear-gradient(135deg, rgba(0,210,106,{savings_alpha}), rgba(0,210,106,.05));border:1px solid rgba(0,210,106,.35);position:relative;">
    <div style="position:absolute;right:20px;top:18px;background:rgba(0,210,106,.30);padding:8px 16px;border-radius:999px;font-weight:800;">{savings_pct:.1f}%</div><div style="font-size:30px;font-weight:800;">Total Savings</div>
    <div style="font-size:48px;font-weight:800;color:#00d26a;margin-top:12px;">₹ {total_savings:,.0f}</div>
    <div style="margin-top:22px;">Personal ₹ {personal:,.0f} | Investment ₹ {investment:,.0f}</div>
<div style="margin-top:12px;background:rgba(255,255,255,.08);height:10px;border-radius:999px;overflow:hidden">
<div style="width:{savings_pct:.1f}%;height:10px;background:rgba(0,210,106,.85)"></div>
</div>
</div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:25px'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Expense Breakdown</div>', unsafe_allow_html=True)

expense_cols=["Home Rent","Transport","Shopping","Office","Bills","Insurance","Medical","Fitness","Travel","Misc"]
icons={"Home Rent":"🏠","Transport":"🚌","Shopping":"🛒","Office":"💼","Bills":"📄","Insurance":"🛡️","Medical":"🏥","Fitness":"💪","Travel":"✈️","Misc":"🎁"}

rows=[st.columns(5,gap="large"),st.columns(5,gap="large")]

for i,col in enumerate(expense_cols):
    val=pd.to_numeric(filtered[col],errors="coerce").fillna(0).sum()
    pct=(val/total_expense*100) if total_expense else 0

    with rows[0][i] if i<5 else rows[1][i-5]:
        st.markdown(f"""
        <div class="category-card">
        <div style="font-size:26px;font-weight:700;">{icons[col]} {col}</div><div style="height:34px"></div><div style="font-size:24px;">₹ {val:,.0f}</div><div style="height:24px"></div><div style="color:#aaa;">{pct:.1f}% of expense</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="section-title">Expense Analytics</div>', unsafe_allow_html=True)

a,b=st.columns(2)

with a:
    fig=go.Figure()
    fig.add_bar(name="Expense",x=filtered["Month"],y=filtered["Total Spent"],marker_color="#ff4b4b")
    fig.add_bar(name="Savings",x=filtered["Month"],y=filtered["Total Savings"],marker_color="#00d26a")
    fig.update_layout(height=430,barmode="group")
    st.plotly_chart(fig,use_container_width=True)

with b:
    pie_df=pd.DataFrame({
    "Category":expense_cols,
    "Amount":[pd.to_numeric(filtered[c],errors="coerce").fillna(0).sum() for c in expense_cols]
    })

    fig2=px.pie(pie_df,names='Category',values='Amount',hole=0.45)
    fig2.update_layout(
        legend=dict(font=dict(size=16))
    )
    st.plotly_chart(fig2,use_container_width=True)

st.markdown('<div class="section-title">Database</div>', unsafe_allow_html=True)


table_df = filtered[[
"Month","Home Rent","Transport","Shopping","Office","Bills",
"Insurance","Medical","Fitness","Travel","Misc",
"Total Spent","Investments","Personal","Total Savings"
]].copy()

for col in table_df.columns:
    if col != "Month":
        table_df[col] = pd.to_numeric(table_df[col], errors="coerce").fillna(0).round(0).astype(int).map(lambda x:f"{x:,}")

st.markdown("""
<div style="display:grid;grid-template-columns:74% 26%;gap:10px;margin-bottom:10px">
<div style="background:#4a2020;padding:12px;border-radius:8px;text-align:center;font-weight:bold;letter-spacing:1px">EXPENSES</div>
<div style="background:#124128;padding:12px;border-radius:8px;text-align:center;font-weight:bold;letter-spacing:1px">SAVINGS</div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<style>
[data-testid="stDataFrame"] table th:nth-child(14),
[data-testid="stDataFrame"] table td:nth-child(14){
border-left:4px solid #1f8b4c !important;
}
</style>
""", unsafe_allow_html=True)

st.dataframe(table_df.reset_index(drop=True), hide_index=True, use_container_width=True)


