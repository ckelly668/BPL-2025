import streamlit as st
# from image_loader import render_image
from aesthetic_tables import create_head_to_head_table, create_league_table
from session_module import init_session

# =========== Streamlit Page Configuration ===========
st.set_page_config(page_title="Belfast Padel League", 
                   layout="wide",
                   page_icon = ":trophy:",
                   initial_sidebar_state= "expanded")

st.title("Head to Head Results")

# ============== Initalise Session ====================
init_session()

# ============== Results Tabs ====================
df = st.session_state.League.sets_score_matrix.replace(to_replace=[None], value="-", inplace=False)
# df.index.names = ['Team A ']
df.columns.names = [' ']
# df.style.set_table_styles([dict(selector="th",props=[('max-width', '5px')])])
fig_head_to_head_table = create_head_to_head_table(df)
# st.pyplot(fig_head_to_head_table, width='content')
fig_league_table = create_league_table(st.session_state.League.build_league_table_from_matrix())
st.pyplot(fig_league_table, width='content')

# ================= Add Logo  ==========================
st.sidebar.image('images/padel_logo_2.png', width=300)