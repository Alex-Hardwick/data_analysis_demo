import streamlit as st

pages = {
    "Welcome": [
        st.Page("Home.py", title="Home")
    ],
    "Exploration": [
        st.Page("./pages/explore.py", title="Data Exploration")
    ],
    "Sales Analysis": [
        st.Page("./pages/intro.py", title="Introduction"),
        st.Page("./pages/byloc.py", title="Sales by Location"),
        st.Page("./pages/locdash.py", title="Dashboard"),
    ]
}
pg = st.navigation(pages)
pg.run()