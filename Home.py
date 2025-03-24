import streamlit as st
import polars as pl

#Data
@st.cache_data
def get_data():
    salesdata = pl.read_excel("Coffee Shop Sales.xlsx")
    return salesdata

# UI
st.set_page_config(
    page_title="Coffee Shops Sales Demo",
    page_icon=":coffee:",
    layout="wide"
)

salesdata = get_data()


st.header("Coffee Shop Sales Analysis")

st.write("Analysis has been performed on the following freely available dataset from Kaggle.com:")
with st.popover("Raw Dataset", use_container_width=True):
    st.dataframe(salesdata, use_container_width=True)

st.subheader("Dataset Description")
st.write("Transaction records for Maven Roasters, a fictitious coffee shop operating out of three NYC locations. Dataset includes the transaction date, timestamp and location, along with product-level details.")
col1, col2 = st.columns(2)
with col1:
    st.write("Total Rows: 149,116")
    st.write("File Format: .xlsx")
with col2:
    st.write("Total Columns: 11")
    st.write("File Size: 8.97 MB")

st.subheader("Tools/Resources Used")
st.write("Dataset - Kaggle.com (https://www.kaggle.com/)")
st.write("Language - Python 3.12")
st.write("UI - Streamlit (https://streamlit.io/)")
st.write("Data Processing - Polars (https://pola.rs/)")
st.write("Data Vizualisation - ")