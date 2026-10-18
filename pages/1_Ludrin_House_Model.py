import pandas as pd
import streamlit as st

st.title("Ludrin House Business Model")
st.write(
    "Two-floor, 3,000 sq ft TCG shop and internet cafe with a full kitchen, a play hall, "
    "a 16-PC gaming room and a small beer and wine program. Defaults match the stabilized "
    "month 12 plan from the business model doc. Edit any number in the tables or sidebar."
)


def money(x):
    if x is None or x == float("inf"):
        return "n/a"
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


# ---------------- Defaults from the business model doc ----------------
DEFAULT_STREAMS = pd.DataFrame(
    [
        ["Sealed TCG product", 30000, 25],
        ["Singles and buylist", 25000, 50],
        ["Kitchen and drinks", 24000, 68],
        ["PC and console time", 9500, 95],
        ["Event entries (net of prizes)", 7500, 50],
        ["Accessories", 6000, 50],
        ["Board games, RPGs, minis", 5000, 40],
        ["Memberships and day passes", 4000, 95],
        ["Beer and wine", 4000, 70],
        ["Parties and private events", 3000, 70],
    ],
    columns=["Stream", "Monthly revenue ($)", "Gross margin (%)"],
)

DEFAULT_OPEX = pd.DataFrame(
    [
        ["Payroll and payroll taxes, including two cooks", 26300],
        ["Rent (1,500 sq ft ground at ~$67, 1,500 sq ft second floor at ~$34 per sq ft per year)", 12600],
        ["Utilities, internet and kitchen gas", 2400],
        ["PC room: power, fiber, software, licenses", 1530],
        ["Insurance, including kitchen and liquor liability", 1500],
        ["Marketing", 1500],
        ["PC hardware replacement reserve", 1000],
        ["Store supplies", 800],
        ["Kitchen services: hood cleaning, pest control, grease trap, carting", 800],
        ["Software subscriptions, including kitchen display and QR ordering", 650],
        ["Accounting and legal", 600],
    ],
    columns=["Cost", "Monthly ($)"],
)

DEFAULT_STARTUP = pd.DataFrame(
    [
        ["Kitchen build-out and equipment", 180000],
        ["Working capital reserve (about 2 months of fixed costs)", 90000],
        ["Opening inventory: sealed, accessories, board games", 70000],
        ["Build-out for both floors: flooring, lighting, electrical, stairs, two ADA restrooms", 70000],
        ["PC and console room", 68900],
        ["Lease security deposit and first month", 50400],
        ["Singles seed buying", 25000],
        ["Display cases and shelving", 15000],
        ["Licenses, permits, legal, first insurance payment", 15000],
        ["Play hall tables and chairs (20 tables, 80 seats)", 13000],
        ["Beer and wine: license, equipment and opening stock", 12000],
        ["Board game library wall and starter game library", 8000],
        ["Signage and grand opening marketing", 7000],
        ["POS, inventory software, cameras", 6000],
    ],
    columns=["Item", "Cost ($)"],
)

# ---------------- Sidebar: financing and growth ----------------
sb = st.sidebar
sb.header("Financing")
loan_amount = sb.number_input("SBA 7(a) loan ($)", 0, 5_000_000, 375_000, 5_000)
loan_rate = sb.number_input("Interest rate (%)", 0.0, 30.0, 10.5, 0.25)
loan_years = sb.number_input("Term (years)", 1, 30, 10)

sb.header("Variable costs")
processing_pct = sb.slider("Card processing (% of revenue)", 0.0, 10.0, 3.6, 0.1)
shrink_pct = sb.slider("Shrink (% of revenue)", 0.0, 5.0, 1.0, 0.1)

sb.header("Growth")
start_level = sb.slider("Month 1 revenue (% of month 12)", 10, 100, 50)
year2_growth = sb.slider("Growth from month 12 to month 24 (%)", 0, 100, 27)
payroll_growth = sb.slider("Payroll increase in year 2 (%)", 0, 50, 0)

if sb.button("Reset all tables to the doc's numbers"):
    for k in ("streams", "opex", "startup"):
        st.session_state.pop(k, None)
    st.rerun()

# ---------------- Editable tables ----------------
tab_rev, tab_cost, tab_start = st.tabs(["Revenue streams", "Monthly operating costs", "Startup costs"])
with tab_rev:
    streams = st.data_editor(
        DEFAULT_STREAMS, key="streams", hide_index=True, num_rows="dynamic",
        column_config={
            "Monthly revenue ($)": st.column_config.NumberColumn(format="$%d", min_value=0),
            "Gross margin (%)": st.column_config.NumberColumn(format="%d%%", min_value=0, max_value=100),
        },
    )
with tab_cost:
    opex = st.data_editor(
        DEFAULT_OPEX, key="opex", hide_index=True, num_rows="dynamic",
        column_config={"Monthly ($)": st.column_config.NumberColumn(format="$%d", min_value=0)},
    )
with tab_start:
    startup = st.data_editor(
        DEFAULT_STARTUP, key="startup", hide_index=True, num_rows="dynamic",
        column_config={"Cost ($)": st.column_config.NumberColumn(format="$%d", min_value=0)},
    )

streams = streams.fillna(0)
opex = opex.fillna(0)
startup = startup.fillna(0)

# ---------------- Calculations (month 12, stabilized) ----------------
streams["Gross profit ($)"] = streams["Monthly revenue ($)"] * streams["Gross margin (%)"] / 100
revenue = streams["Monthly revenue ($)"].sum()
gross_profit = streams["Gross profit ($)"].sum()
cogs = revenue - gross_profit
gm = gross_profit / revenue if revenue else 0
var_pct = (processing_pct + shrink_pct) / 100
variable = revenue * var_pct
fixed = opex["Monthly ($)"].sum()
payroll = opex.loc[opex["Cost"].astype(str).str.contains("Payroll", case=False), "Monthly ($)"].sum()
ebitda = gross_profit - variable - fixed

r = loan_rate / 100 / 12
n = loan_years * 12
loan_payment = loan_amount * r / (1 - (1 + r) ** -n) if r > 0 else loan_amount / n
cash_flow = ebitda - loan_payment

startup_total = startup["Cost ($)"].sum()
equity = max(startup_total - loan_amount, 0)

contrib = gm - var_pct
be_operating = fixed / contrib if contrib > 0 else float("inf")
be_debt = (fixed + loan_payment) / contrib if contrib > 0 else float("inf")

# ---------------- 60-month projection ----------------
rows, cum, payback = [], -equity, None
for m in range(1, 61):
    if m <= 12:
        level = start_level / 100 + (1 - start_level / 100) * (m - 1) / 11
    elif m <= 24:
        level = 1 + (year2_growth / 100) * (m - 12) / 12
    else:
        level = 1 + year2_growth / 100
    m_rev = revenue * level
    m_fixed = fixed + (payroll * payroll_growth / 100 if m > 12 else 0)
    m_cf = m_rev * contrib - m_fixed - loan_payment
    cum += m_cf
    if payback is None and cum >= 0:
        payback = m
    rows.append({"Month": m, "Revenue": m_rev, "Cash flow after debt": m_cf, "Owner equity recovered": cum})
proj = pd.DataFrame(rows).set_index("Month")
m24 = proj.loc[24]

# ---------------- Headline ----------------
st.subheader("Month 12 at a glance")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Monthly revenue", money(revenue))
c2.metric("Operating profit (EBITDA)", money(ebitda))
c3.metric("Cash flow after loan", money(cash_flow))
c4.metric("Startup cost", money(startup_total))
c5, c6, c7, c8 = st.columns(4)
c5.metric("Gross margin", f"{gm:.0%}")
c6.metric("Break-even before loan", money(be_operating))
c7.metric("Break-even after loan", money(be_debt))
c8.metric("Owner equity needed", money(equity))

st.caption(
    f"Loan payment {money(loan_payment)} a month. By month 24, revenue reaches "
    f"{money(m24['Revenue'])} and cash flow after debt is {money(m24['Cash flow after debt'])} a month."
)

if payback:
    st.success(f"Owner equity of {money(equity)} is earned back in month {payback} ({payback / 12:.1f} years).")
else:
    st.warning(f"Owner equity of {money(equity)} is not earned back within 5 years under these assumptions.")

# ---------------- Charts ----------------
left, right = st.columns(2)
with left:
    st.subheader("Where gross profit comes from")
    gp_chart = streams.set_index("Stream")[["Gross profit ($)"]]
    st.bar_chart(gp_chart, horizontal=True)
with right:
    st.subheader("Monthly operating costs")
    oc = opex.copy()
    oc["Short name"] = oc["Cost"].astype(str).str.split(r"[,(:]").str[0].str.strip()
    st.bar_chart(oc.set_index("Short name")[["Monthly ($)"]], horizontal=True)

st.subheader("5-year cash projection")
st.line_chart(proj[["Owner equity recovered"]])
with st.expander("Monthly projection table"):
    st.dataframe(proj.style.format(money))

st.subheader("Monthly P&L at month 12")
pnl = pd.DataFrame(
    {"Amount": [revenue, -cogs, gross_profit, -variable, -fixed, ebitda, -loan_payment, cash_flow]},
    index=[
        "Revenue", "Cost of goods, food, drinks and prize support", f"Gross profit ({gm:.0%})",
        f"Card processing and shrink ({var_pct:.1%})", "Operating costs", "Operating profit (EBITDA)",
        "SBA loan payment", "Cash flow to owner",
    ],
)
st.dataframe(pnl.style.format({"Amount": money}))

st.caption("Planning estimates only. Not financial advice.")
