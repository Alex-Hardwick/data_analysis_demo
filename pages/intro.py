import streamlit as st 
import polars as pl

#Data
@st.cache_data
def get_sales():
    lazysales = pl.scan_csv("clean_sales_data.csv", try_parse_dates=True)

    return lazysales

# UI
st.set_page_config(
    page_title="Coffee Shops Sales Demo",
    page_icon=":coffee:",
    layout="wide"
)

lazydisplaydata = get_sales()

st.title("Sales Analysis (Intro)")

st.subheader("Lazy vs. Eager Data Processing")
st.write('''When I saved the data from the cleaning process I changed the format from .xlsx to .csv. While in many ways this is a more primitive file type it opens up the ability to only read the data we care about using the lazyframe functionality of polars.
         When we reload the file into memory to begin our analysis instead of pulling in the entire dataset we can instead scan the file to understand it's contents and then apply filters to only extract the data we need.
         In practice this means complex analysis and filtering can be applied to the same underlying set of data with little loss in performance. In addition to this as I am using the streamlit 
         library for my UI I will load the frame into the browser cache using the @st.cache_data decorator meaning this process will complete only once on initial page load and retain it's data throughout the session.
         A byproduct of using this technique is the collect() method that you may see scattered throughout the data processing code. This is the command to execute the current query and retrieve the data for display''')
with st.popover("Code Snippet", use_container_width=True):
    st.code('''
@st.cache_data
def get_sales():
    lazysales = pl.scan_csv("clean_sales_data.csv", try_parse_dates=True)
    return lazysales

lazydisplaydata = get_sales()
            
displayframe = lazydisplaydata.filter(pl.col("store_location").is_in(userlocs)).collect()    
''')
st.markdown("This concept is best explained by the polars team themselves. More information can be found here: https://docs.pola.rs/user-guide/concepts/lazy-api/")

st.subheader("Goals of Analysis")

st.write('''Now we have our data we should decide what insights we are trying to extract. As we are simulating an independant 
         business owner we should calculate the following:''')
st.write("* Which location brings in the most revenue?")
st.write("* What is the bestselling product?")
st.write("* When are the stores busiest?")

st.subheader("Analysis")
st.write('''I have broken the analysis down into two major components: Locations and Product categories. For each I have generated a series of charts showing the breakdown of sales from various angles.
        I have also created a combined interactive dashboard for stakeholders to explore the data for themselves. Finally I have created a short write up with some of my insights into the dataset as a whole after analysis ''')