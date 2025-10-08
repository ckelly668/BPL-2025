import streamlit as st
# from image_loader import render_image
from aesthetic_tables import create_league_table, create_weekly_schedule_table, create_weekly_results_table, create_winners_page




st.set_page_config(page_title="Belfast Padel League", 
                   layout="wide",
                   page_icon = ":calendar:")


st.title("Schedule")


# week1, week2, week3, week4, week5, week6, week7, week8, week9 = st.tabs(["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8", "Week 9"])

# with week1:
#     # st.header("A cat")
#     # st.image("https://static.streamlit.io/examples/cat.jpg", width=200)
#     # render_image("league_2025-10-12_init_2025-10-07/Report Images/Padel Week 1.jpg")
#     # fig_schedule = create_weekly_schedule_table(st.session_state.League, week = st.session_state.weeks_complete+1)
#     fig_results = create_weekly_results_table(st.session_state.League, week = st.session_state.weeks_complete)
#     st.pyplot(fig_results)
# with week2:
#     st.header("A dog")
#     st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
# with week3:
#     st.header("An owl")
#     st.image("https://static.streamlit.io/examples/owl.jpg", width=200)


    # Function to get tab content from server
# def get_tab_content():
#     return [
#         {'title': 'Topic A', 'content': 'Topic A content'},
#         {'title': 'Topic B', 'content': 'Topic B content'},
#         {'title': 'Topic C', 'content': 'Topic C content'},
#     ]

# Create tabs dynamically based on weeks completed
# [ 'Week'+s for s in range(1,9)]
tab_contents = []
for week in range(1, 9 + 1):
    tab_contents.append({
        'title': f'Week {week}',
        'content': create_weekly_schedule_table(st.session_state.League, week=week)
    })

 
# Pull tab content from server
# tab_contents = get_tab_content()
 
# Create tabs
tab_names = [content['title'] for content in tab_contents]
tabs = st.tabs(tab_names)
 
# Iterate through each tab and build content
for tab, tab_content in zip(tabs, tab_contents):
    with tab:
        # st.header(tab_content['title'])
        st.write(tab_content['content'])

st.sidebar.image('images/padel_logo_2.png', width=300)