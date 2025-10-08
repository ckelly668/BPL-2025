
import streamlit as st
# from image_loader import render_image
from aesthetic_tables import create_weekly_results_table

# =========== Streamlit Page Configuration ===========
st.set_page_config(page_title="Belfast Padel League", 
                   layout="wide",
                   page_icon = ":trophy:",
                   initial_sidebar_state= "expanded")

st.title("Results")

# ============== Results Tabs ====================
# Create tabs dynamically based on weeks completed
tab_contents = []
for week in range(1, st.session_state['weeks_complete'] + 1):
    tab_contents.append({
        'title': f'Week {week}',
        'content': create_weekly_results_table(st.session_state.League, week=week)
    })
 
# Create tabs
tab_names = [content['title'] for content in tab_contents]
tabs = st.tabs(tab_names)
 
# Iterate through each tab and build content
for tab, tab_content in zip(tabs, tab_contents):
    with tab:
        # st.header(tab_content['title'])
        st.write(tab_content['content'])

# ================= Add Logo  ==========================
st.sidebar.image('images/padel_logo_2.png', width=300)