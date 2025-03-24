import streamlit as st 
import polars as pl
import altair as alt

#Data
@st.cache_data
def get_sales():
    lazysales = pl.scan_csv("clean_sales_data.csv", try_parse_dates=True)

    return lazysales
lazysales = get_sales()


st.title("Sales by Location")
st.subheader("Total Sales")
tot1, tot2 = st.columns((1,3))
with tot1:
    salesloc = (lazysales.group_by(pl.col("store_location").alias("Store Location"))
                .agg(pl.col("transaction_value").sum().alias("Total Sales"))
                .sort("Total Sales", descending=True)
                .collect())
    st.dataframe(salesloc,
                column_config={
                    "Total Sales": st.column_config.NumberColumn(
                        format="$ %.2f"
                    )
                },
                hide_index=True, 
                use_container_width=True)
with tot2:
    src = salesloc
    base = alt.Chart(src).encode(
        alt.Theta("Total Sales:Q").stack(True),
        alt.Color("Store Location:N").legend(None)
    )
    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=150, size=20).encode(text="Store Location", color=alt.value("red"))
    chrt = pie + text
    st.altair_chart(chrt, use_container_width=True)

st.write("___")
st.subheader("Sales by Month")
otbreakdown = st.checkbox("Show Breakdown by Store Location", key="otbd", value=True)
tot1, tot2 = st.columns((1,3))
if otbreakdown:
    with tot1:
        salestime = (lazysales.group_by((pl.col("transaction_datetime").dt.to_string("%m") + " - " + pl.col("transaction_datetime").dt.strftime("%B")).alias("Month"), 
                                    pl.col("store_location").alias("Store Location"), 
                                    maintain_order=True)
                .agg(pl.col("transaction_value").sum().cast(pl.Decimal(scale=2)).alias("Total Sales"))
                .collect())
        st.dataframe(salestime,
                column_config={
                    "Total Sales": st.column_config.NumberColumn(
                        format="$ %.2f"
                    )
                }, 
                hide_index=True, 
                use_container_width=True)
    with tot2:
        src = salestime
        chrt2 = alt.Chart(src).mark_bar().encode(
        x="Month",
        y="Total Sales",
        color="Store Location"
        )
        st.altair_chart(chrt2, use_container_width=True)
else:
    with tot1:
        salestime = (lazysales.group_by((pl.col("transaction_datetime").dt.to_string("%m") + " - " + pl.col("transaction_datetime").dt.strftime("%B")).alias("Month"), 
                                    maintain_order=True)
                .agg(pl.col("transaction_value").sum().cast(pl.Decimal(scale=2)).alias("Total Sales"))
                .collect())
        st.dataframe(salestime,
                column_config={
                    "Total Sales": st.column_config.NumberColumn(
                        format="$ %.2f"
                    )
                }, 
                hide_index=True, 
                use_container_width=True)
    with tot2:
        src = salestime
        chrt2 = alt.Chart(src).mark_bar().encode(
        x="Month",
        y="Total Sales",
        )
        st.altair_chart(chrt2, use_container_width=True)

    
st.write("___")
st.subheader("Sales By Day")
breakdown = st.checkbox("Show Breakdown by Store Location", key="bdbd", value=True)
tot1, tot2 = st.columns((1,3))
with tot1:
    if breakdown:
        salestime = (lazysales.group_by((pl.col("transaction_datetime").dt.to_string("%w") + " - " + pl.col("transaction_datetime").dt.strftime("%A")).alias("Day"), 
                                    pl.col("store_location").alias("Store Location"), 
                                    maintain_order=True)
                .agg(pl.col("transaction_value").sum().cast(pl.Decimal(scale=2)).alias("Total Sales"))
                .collect())
        st.dataframe(salestime,
                column_config={
                    "Total Sales": st.column_config.NumberColumn(
                        format="$ %.2f"
                    )
                }, 
                hide_index=True, 
                use_container_width=True)
    else:
        salestime = (lazysales.group_by((pl.col("transaction_datetime").dt.to_string("%w") + " - " + pl.col("transaction_datetime").dt.strftime("%A")).alias("Day"), 
                                    maintain_order=True)
                .agg(pl.col("transaction_value").sum().cast(pl.Decimal(scale=2)).alias("Total Sales"))
                .collect())
        st.dataframe(salestime,
                column_config={
                    "Total Sales": st.column_config.NumberColumn(
                        format="$ %.2f"
                    )
                }, 
                hide_index=True, 
                use_container_width=True)
with tot2:
    src = salestime
    if breakdown:
        chrt3 = alt.Chart(src).mark_bar().encode(
        x="Day",
        y="Total Sales",
        color="Store Location"
        )
    else:
        chrt3 = alt.Chart(src).mark_bar().encode(
        x="Day",
        y="Total Sales",
        )
    st.altair_chart(chrt3, use_container_width=True)

        
st.write("___")
st.subheader("Sales By Hour")
breakdown = st.checkbox("Show Breakdown by Store Location", key="hrbd", value=True)
tot1, tot2 = st.columns((1,3))
with tot1:
    if breakdown:
        salestime = (lazysales.group_by(pl.col("transaction_datetime").dt.to_string("%H").alias("Hour"), 
                                    pl.col("store_location").alias("Store Location"), 
                                    maintain_order=True)
                .agg(pl.col("transaction_value").sum().cast(pl.Decimal(scale=2)).alias("Total Sales"))
                .sort(pl.col("Hour"))
                .collect())
        st.dataframe(salestime,
                column_config={
                    "Total Sales": st.column_config.NumberColumn(
                        format="$ %.2f"
                    )
                }, 
                hide_index=True, 
                use_container_width=True)
    else:
        salestime = (lazysales.group_by(pl.col("transaction_datetime").dt.to_string("%H").alias("Hour"), 
                                    maintain_order=True)
                .agg(pl.col("transaction_value").sum().cast(pl.Decimal(scale=2)).alias("Total Sales"))
                .sort(pl.col("Hour"))
                .collect())
        st.dataframe(salestime,
                column_config={
                    "Total Sales": st.column_config.NumberColumn(
                        format="$ %.2f"
                    )
                }, 
                hide_index=True, 
                use_container_width=True)
with tot2:
    src = salestime
    if breakdown:
        chrt3 = alt.Chart(src).mark_bar().encode(
        x="Hour",
        y="Total Sales",
        color="Store Location"
        )
    else:
        chrt3 = alt.Chart(src).mark_bar().encode(
        x="Hour",
        y="Total Sales",
        )
    st.altair_chart(chrt3, use_container_width=True)