import streamlit as st 
import polars as pl
import altair as alt

#Data function & filter dictionary
@st.cache_data
def get_sales():
    lazysales = pl.scan_csv("clean_sales_data.csv", try_parse_dates=True)
    locs = lazysales.select("store_location").unique().collect().get_column("store_location").to_list()
    cats = lazysales.select("product_category").unique().collect().get_column("product_category").to_list()
    return lazysales, locs, cats

filterdict = {
    "Month": (pl.col("transaction_datetime").dt.to_string("%m") + " - " + pl.col("transaction_datetime").dt.strftime("%B")).alias("Month"),
    "Day":(pl.col("transaction_datetime").dt.to_string("%w") + " - " + pl.col("transaction_datetime").dt.strftime("%A")).alias("Day"),
    "Hour":(pl.col("transaction_datetime").dt.to_string("%H").alias("Hour")),
}

# Get Data (cached)
lazysales, locs, cats = get_sales()

col1, col2 = st.columns(2)
with col1:
    st.title("Interactive Dashboard")
with col2:
    colors = st.toggle("Display Category Data")
filt1, filt2, filt3 = st.columns((1, 2, 1))
with filt1:
    userlocs = st.multiselect("Filter by Location", options=locs, default=locs)
with filt2:
    usercats = st.multiselect("Filter by Category", options=cats, default=cats)
with filt3:
    userint = st.selectbox("Select Interval", options=["Month","Day","Hour"])
#print(userlocs)

if userlocs is not None and usercats is not None:
    displayframe = (lazysales.filter(pl.col("store_location").is_in(userlocs),
                            pl.col("product_category").is_in(usercats))
                            .select(pl.col("transaction_datetime").alias("Date & Time"),
                                    pl.col("store_location").alias("Store Location"),
                                    pl.col("product_category").alias("Product Category"),
                                    pl.col("product_type").alias("Product Type"),
                                    pl.col("transaction_qty").alias("Quantity"),
                                    pl.col("unit_price").alias("Unit Price"),
                                    pl.col("transaction_value").alias("Total Value"),
                                    )
                            .collect())
    # Charts
    if not colors:
        chartframe = (lazysales.filter(pl.col("store_location").is_in(userlocs),
                            pl.col("product_category").is_in(usercats))
                            .group_by(filterdict[userint],
                                      pl.col("store_location").alias("Store Location"),
                                      maintain_order=True)
                            .agg(pl.col("transaction_value").sum().alias("Total Sales ($)"))
                            .collect())
        src = chartframe
        chrt2 = alt.Chart(src).mark_bar().encode(
            x=userint,
            y="Total Sales ($)",
            color="Store Location"
            )
    else:
        chartframe = (lazysales.filter(pl.col("store_location").is_in(userlocs),
                            pl.col("product_category").is_in(usercats))
                            .group_by(filterdict[userint],
                                      pl.col("product_category").alias("Product Category"),
                                      maintain_order=True)
                            .agg(pl.col("transaction_value").sum().alias("Total Sales ($)"))
                            .collect())
        src = chartframe
        chrt2 = alt.Chart(src).mark_bar().encode(
            x=userint,
            y="Total Sales ($)",
            color="Product Category"
            )
    st.altair_chart(chrt2, use_container_width=True, theme=None)



    # Dataframe
    with st.popover("Filtered Dataframe", use_container_width=True):
        st.dataframe(displayframe,
                column_config={
                    "Unit Price": st.column_config.NumberColumn(
                        format="$ %.2f"
                    ),
                    "Total Value": st.column_config.NumberColumn(
                        format="$ %.2f"
                    ),
                    "Date & Time": st.column_config.DatetimeColumn(
                        format="dddd, MMMM Do YYYY, h:mm a"
                    ),
                },  
                hide_index=True, 
                use_container_width=True)