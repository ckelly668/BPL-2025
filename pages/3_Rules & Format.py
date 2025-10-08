import streamlit as st

def main():
    st.set_page_config(page_title="Belfast Padel League", 
                   layout="wide",
                   page_icon = ":clipboard:", 
                   initial_sidebar_state= "collapsed")
    st.title("Padel League Rules")

    st.header("League Rules & Format")
    st.markdown("""
    - Each match is the **best of 3 sets**.
    - **All 3 sets must be played** even if you win the first 2 sets.
    - Send your scores into the grou p chat after your match.
    - The **home** team serves first in the first set, **away** team serves
                 first in the second set and the **home** serves first again in the third set.
    """)

    st.header("Set Scoring")
    st.markdown("""
    - A set is won by the **first team to win 4 games**, **unless** the score reaches 3-3, a tie-breaker.
    - If there is a tie-breaker (**3-3**), the **first team to reach 5 games wins the set**.
    """)

    st.header("Substitutions")
    st.markdown("""
    - Each team is allowed to **substitute a player a maximum of 2 times** throughout the league.
    """)

    st.header("Court Booking")
    st.markdown("""
    - It is the responsibility of **both teams to organise and book their own courts** for their scheduled matches.
    - Use the **Playtomic app** or **Let's Go Padel** to book courts and split the payments.
    """)
    st.sidebar.image('images/padel_logo_2.png', width=300)

if __name__ == "__main__":
    main()
