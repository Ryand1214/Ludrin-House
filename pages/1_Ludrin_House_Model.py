import pandas as pd
import streamlit as st

st.set_page_config(page_title="Ludrin House Model", page_icon="📊", layout="wide")

st.title("Ludrin House Business Model")
st.write(
    "Two-floor TCG card shop and PC room with a delivery-style kitchen "
    "(food goes to tables and PCs, no dining area). All numbers below are "
    "editable placeholder assumptions. Change them in the sidebar."
)

DAYS_PER_MONTH = 30

# ---------------- Sidebar inputs ----------------
sb = st.sidebar
sb.header("Assumptions")

with sb.expander("TCG retail (singles + sealed)", expanded=True):
    retail_sales = st.number_input("Monthly retail sales ($)", 0, 1_000_000, 35_000, 1_000)
    retail_margin = st.slider("Retail gross margin (%)", 0, 80, 30)

with sb.expander("Tournaments and events"):
    events_per_week = st.number_input("Events per week", 0, 50, 6)
    players_per_event = st.number_input("Avg players per event", 0, 500, 20)
    entry_fee = st.number_input("Avg entry fee ($)", 0, 200, 10)
    prize_payout = st.slider("Share of entry fees paid out as prizes (%)", 0, 100, 40)

with sb.expander("PC room"):
    num_pcs = st.number_input("Number of PCs", 0, 200, 24)
    hourly_rate = st.number_input("Hourly rate per PC ($)", 0.0, 50.0, 6.0, 0.5)
    hours_open = st.number_input("Hours open per day", 0, 24, 12)
    utilization = st.slider("Average PC utilization (%)", 0, 100, 35)

with sb.expander("Kitchen (food)"):
    food_orders = st.number_input("Food orders per day", 0, 2_000, 60)
    food_ticket = st.number_input("Avg food ticket ($)", 0.0, 100.0, 14.0, 0.5)
    food_cost_pct = st.slider("Food cost (%)", 0, 80, 30)

with sb.expander("Drinks (incl. alcohol)"):
    drink_orders = st.number_input("Drink orders per day", 0, 2_000, 80)
    drink_ticket = st.number_input("Avg drink ticket ($)", 0.0, 50.0, 6.0, 0.5)
    drink_cost_pct = st.slider("Beverage cost (%)", 0, 80, 25)

with sb.expander("Monthly operating costs"):
    rent = st.number_input("Rent, both floors ($)", 0, 500_000, 25_000, 500)
    staff_count = st.number_input("Staff on payroll", 0, 100, 8)
    staff_wage = st.number_input("Avg hourly wage ($)", 0.0, 100.0, 19.0, 0.5)
    staff_hours = st.number_input("Hours per staff member per month", 0, 300, 140)
    payroll_burden = st.slider("Payroll taxes and benefits (% of wages)", 0, 50, 15)
    utilities = st.number_input("Utilities and internet ($)", 0, 100_000, 4_500, 100)
    software = st.number_input("Software, POS, game licenses ($)", 0, 50_000, 1_200, 100)
    insurance = st.number_input("Insurance incl. liquor liability ($)", 0, 50_000, 1_500, 100)
    marketing = st.number_input("Marketing ($)", 0, 50_000, 1_500, 100)
    other_opex = st.number_input("Other / misc ($)", 0, 50_000, 2_000, 100)

with sb.expander("Startup costs"):
    buildout = st.number_input("Buildout and renovation ($)", 0, 5_000_000, 150_000, 5_000)
    pc_unit_cost = st.number_input("Cost per gaming PC setup ($)", 0, 20_000, 2_000, 100)
    kitchen_equipment = st.number_input("Kitchen and bar equipment ($)", 0, 1_000_000, 60_000, 1_000)
    initial_inventory = st.number_input("Initial card inventory ($)", 0, 1_000_000, 50_000, 1_000)
    furniture = st.number_input("Tables, chairs, displays ($)", 0, 500_000, 30_000, 1_000)
    licenses = st.number_input("Licenses, permits, legal ($)", 0, 500_000, 20_000, 1_000)
    working_capital = st.number_input("Working capital reserve ($)", 0, 2_000_000, 75_000, 5_000)

with sb.expander("Ramp-up"):
    ramp_months = st.slider("Months to reach full volume", 1, 24, 9)
    start_level = st.slider("Opening month volume (% of full)", 10, 100, 40)

# ---------------- Calculations (monthly, at full volume) ----------------
events_rev = events_per_week * 52 / 12 * players_per_event * entry_fee
pc_rev = num_pcs * hourly_rate * hours_open * DAYS_PER_MONTH * utilization / 100
food_rev = food_orders * food_ticket * DAYS_PER_MONTH
drink_rev = drink_orders * drink_ticket * DAYS_PER_MONTH

revenue = {
    "TCG retail": retail_sales,
    "Events": events_rev,
    "PC room": pc_rev,
    "Food": food_rev,
    "Drinks": drink_rev,
}
cogs = {
    "TCG retail": retail_sales * (1 - retail_margin / 100),
    "Events": events_rev * prize_payout / 100,
    "PC room": 0.0,
    "Food": food_rev * food_cost_pct / 100,
    "Drinks": drink_rev * drink_cost_pct / 100,
}

total_rev = sum(revenue.values())
total_cogs = sum(cogs.values())
gross_profit = total_rev - total_cogs

payroll = staff_count * staff_wage * staff_hours * (1 + payroll_burden / 100)
opex = {
    "Rent": rent,
    "Payroll": payroll,
    "Utilities": utilities,
    "Software": software,
    "Insurance": insurance,
    "Marketing": marketing,
    "Other": other_opex,
}
total_opex = sum(opex.values())
net_income = gross_profit - total_opex

startup_total = (
    buildout + num_pcs * pc_unit_cost + kitchen_equipment + initial_inventory
    + furniture + licenses + working_capital
)

gross_margin_pct = gross_profit / total_rev if total_rev else 0
breakeven_rev = total_opex / gross_margin_pct if gross_margin_pct > 0 else float("inf")


def money(x):
    if x == float("inf"):
        return "n/a"
    sign = "-" if x < 0 else ""
    return f"{sign}${abs(x):,.0f}"


# ---------------- 36-month projection with ramp-up ----------------
rows = []
cumulative = -startup_total
payback_month = None
for m in range(1, 37):
    if m >= ramp_months:
        level = 1.0
    else:
        level = start_level / 100 + (1 - start_level / 100) * (m - 1) / max(ramp_months - 1, 1)
    m_rev = total_rev * level
    m_gp = gross_profit * level
    m_net = m_gp - total_opex
    cumulative += m_net
    if payback_month is None and cumulative >= 0:
        payback_month = m
    rows.append({"Month": m, "Revenue": m_rev, "Net income": m_net, "Cumulative cash": cumulative})
proj = pd.DataFrame(rows).set_index("Month")

# ---------------- Headline metrics ----------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Monthly revenue (full volume)", money(total_rev))
c2.metric("Monthly net income", money(net_income))
c3.metric("Break-even revenue / month", money(breakeven_rev))
c4.metric("Startup cost", money(startup_total))

if net_income <= 0:
    st.error("At full volume this setup loses money every month. Try raising volume or cutting costs.")
elif payback_month:
    st.success(f"Startup costs are paid back in month {payback_month}, including ramp-up.")
else:
    st.warning("Profitable at full volume, but startup costs are not paid back within 36 months.")

# ---------------- Breakdown tables and charts ----------------
left, right = st.columns(2)

with left:
    st.subheader("Revenue mix")
    mix = pd.DataFrame(
        {
            "Revenue": revenue.values(),
            "Direct costs": cogs.values(),
        },
        index=revenue.keys(),
    )
    mix["Gross profit"] = mix["Revenue"] - mix["Direct costs"]
    mix["Share of revenue"] = mix["Revenue"] / total_rev if total_rev else 0
    st.bar_chart(mix[["Gross profit", "Direct costs"]], stack=True)
    st.dataframe(
        mix.style.format(
            {"Revenue": "${:,.0f}", "Direct costs": "${:,.0f}",
             "Gross profit": "${:,.0f}", "Share of revenue": "{:.0%}"}
        ),
    )

with right:
    st.subheader("Monthly operating costs")
    opex_df = pd.DataFrame({"Cost": opex.values()}, index=opex.keys())
    st.bar_chart(opex_df)
    st.dataframe(opex_df.style.format({"Cost": "${:,.0f}"}))

st.subheader("36-month cash projection")
st.line_chart(proj[["Cumulative cash"]])
with st.expander("See monthly projection table"):
    st.dataframe(proj.style.format("${:,.0f}"))

st.subheader("Monthly P&L at full volume")
pnl = pd.DataFrame(
    {
        "Amount": [total_rev, -total_cogs, gross_profit, -total_opex, net_income],
    },
    index=["Revenue", "Direct costs", "Gross profit", "Operating costs", "Net income"],
)
st.dataframe(pnl.style.format({"Amount": "${:,.0f}"}))

st.caption("Placeholder assumptions for planning only. Not financial advice.")
