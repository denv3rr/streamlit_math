import streamlit as st

st.set_page_config(
    page_title="Interactive Math Tool",
    page_icon="♾️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "An interactive tool for Pre-calculus and Calculus explorations."
    }
)

# Load custom CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass # No custom CSS found

# *** Use the 01_Home.py file as the effective landing page. ***

st.sidebar.success("Select a module above.")

st.sidebar.info(f"Current Time: {st.query_params.get('current_time', 'Not Available')}")
st.sidebar.info(f"Location: {st.query_params.get('location', 'Not Available')}")


# A note about structure for the user:
st.info("Welcome! Please select a learning module from the sidebar on the left.")
st.markdown("This application utilizes files in the `pages/` directory to create the navigation structure.")