import streamlit as st
# from image_loader import render_image
from aesthetic_tables import  create_weekly_schedule_table
from session_module import init_session

# =========== Streamlit Page Configuration ===========
st.set_page_config(page_title="Belfast Padel League", 
                   layout="wide",
                   page_icon = ":calendar:", 
                   initial_sidebar_state= "expanded")

st.title("Remaining Weeks Schedule")

# ============== Initalise Session ====================
init_session()

# ============== Schedule Tabs ====================
# Create tabs dynamically based on weeks completed
tab_contents = []
for week in range(st.session_state.weeks_complete+1, len(st.session_state.League.teams) + 1):
    tab_contents.append({
        'title': f'Week {week}',#{" \N{check mark}" if week < st.session_state.weeks_complete +1 else ""}',

        'content': create_weekly_schedule_table(st.session_state.League, week=week)
    })

# Create tabs
tab_names = [content['title'] for content in tab_contents]
tabs = st.tabs(tab_names)
 
# Iterate through each tab and build content
for tab, tab_content in zip(tabs, tab_contents):
    with tab:
        # st.header(tab_content['title'])
        st.write(tab_content['content'])

# ================= Add Logo  ===========================
st.sidebar.image('images/padel_logo_2.png', width=300)