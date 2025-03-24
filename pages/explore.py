import streamlit as st 
import polars as pl

#Data
@st.cache_data
def get_raw_data():
    salesdata = pl.read_excel("Coffee Shop Sales.xlsx", schema_overrides={"transaction_date": pl.String,"transaction_time": pl.String})

    return salesdata

# UI
st.set_page_config(
    page_title="Coffee Shops Sales Demo",
    page_icon=":coffee:",
    layout="wide"
)

displaydata = get_raw_data()

st.title("Data Exploration and Cleaning")

st.write("Before any analysis can begin data should be checked for consistency and completeness. Using the polars library I load the file into memory and call the describe() function")

with st.popover("Click to view", use_container_width=True):
    st.code('''displaydata.describe()''')
    st.write('''We want to focus on the top two rows. These are showing that all columns have the same number of entries and 0 null values likely indicating that the data is complete and no errors were found when parsing.
             We can also see some interesting information about the rest of the data such as the min and max values but we will examine this in more detail when we start our analysis''')
    st.dataframe(displaydata.describe(), hide_index=True, use_container_width=True)

st.write("Next we want to check that the data types have been read correctly. We can do this by inspecting .schema which returns an ordered dictionary of column names and types")

with st.popover("Schema", use_container_width=True):
    st.write("Output of .schema:")
    st.write(displaydata.schema)

st.write("We can see that the transaction_date and transaction_time fields have been read into memory as text strings which could hinder our analysis. I'll convert them to proper datetime objects using the with_columns, to_date and to_time functions")

with st.popover("Date & Time Conversion", use_container_width=True):
    st.write("Code:")
    st.code('''converted_dataframe = raw_dataframe.with_columns(pl.col("transaction_date").str.to_date("%m-%d-%y"), 
                                                pl.col("transaction_time").str.to_time("%H:%M"))''')
    convdata = displaydata.with_columns(pl.col("transaction_date").str.to_date("%m-%d-%y"),
                                    pl.col("transaction_time").str.to_time("%H:%M"))
    st.write("New Frame Head:")
    st.dataframe(convdata.head(), hide_index=True, use_container_width=True)
    st.write("New Schema:")
    st.write(convdata.schema)

    
st.write("We can then combine the two converted columns into one datetime column")
with st.popover("Column Combination", use_container_width=True):
    st.write("Code:")
    st.code('''datetimeframe = converted_data.select(pl.col("transaction_id"), 
                                pl.col("transaction_date").dt.combine(pl.col("transaction_time")).alias("transaction_datetime"),
                                pl.col(["transaction_qty","store_id","store_location","product_id","unit_price","product_category","product_type","product_detail"]))''')
    datetimeframe = convdata.select(pl.col("transaction_id"), 
                                pl.col("transaction_date").dt.combine(pl.col("transaction_time")).alias("transaction_datetime"),
                                pl.col(["transaction_qty","store_id","store_location","product_id","unit_price","product_category","product_type","product_detail"]))
    st.write("Combined Frame Head:")
    st.dataframe(datetimeframe.head(), hide_index=True, use_container_width=True)
    st.write("Combined Schema:")
    st.write(datetimeframe.schema)

st.write("We can also calculate our transaction value.")
with st.popover("Transaction Value", use_container_width=True):
    st.write("Code:")
    st.code('''cleanframe = datetimeframe.with_columns((pl.col("transaction_qty") * pl.col("unit_price")).alias("transaction_value"))''')
    cleanframe = datetimeframe.with_columns((pl.col("transaction_qty") * pl.col("unit_price")).alias("transaction_value"))
    st.write("Clean Frame Head:")
    st.dataframe(cleanframe.head(), hide_index=True, use_container_width=True)

st.write("From here I feel ready to start analysis. To save time I'll save the clean frame in .csv format to make better use of the scan functionality in polars and to ensure an unedited copy of the original data is intact. Please see Sales Analysis - Introduction for more")
with st.popover("Save As...", use_container_width=True):
    st.write("Code:")
    st.code('''cleanframe.write_csv("clean_sales_data.csv")''')
    #cleanframe.write_csv("clean_sales_data.csv")
