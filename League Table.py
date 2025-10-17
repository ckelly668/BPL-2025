import streamlit as st
import os
import pickle
from padelLeague import padelLeague
from aesthetic_tables import create_league_table, create_winners_page
from session_module import init_session
# from image_loader import render_image

# =========== Streamlit Page Configuration ===========
st.set_page_config(page_title="Belfast Padel League", 
                   layout="wide",
                   page_icon = ":tennis:",
                   initial_sidebar_state= "expanded")

#  =========== Initalise Session ==============
init_session()

# ============== Generate Winners Page  =================
if st.session_state.weeks_complete == len(st.session_state.schedule):
    fig_winners = create_winners_page(st.session_state.League.build_league_table_from_matrix())
    st.pyplot(fig_winners, width='content')

# ============== Generate League Table  =================
fig_league_table = create_league_table(st.session_state.League.build_league_table_from_matrix())
st.pyplot(fig_league_table, width='content')

# ================= Add Logo  ===========================
st.sidebar.image('images/padel_logo_2.png', width=300)