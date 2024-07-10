import streamlit as st

# Title of the application
st.header("Zone Out ScoreBoard")

st.markdown("----")

# List of participants
participants = ["Rajpal", "Prasanna", "Magesh", "Jeeva", "Rithik", "Deeksha"]

# Initialize session state for each participant
if "scores" not in st.session_state:
    st.session_state.scores = {participant: 0 for participant in participants}

# Sort participants by their scores in descending order
sorted_participants = sorted(
    participants, key=lambda x: st.session_state.scores[x], reverse=True
)

# Create a container for the scoreboard
container = st.container()

# Display each participant's score and buttons in a row
for participant in sorted_participants:
    with container:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        col1.text(participant)
        if col2.button("Decrease", key=f"{participant}_decrease"):
            st.session_state.scores[participant] -= 1
            st.experimental_rerun()
        col3.text(st.session_state.scores[participant])
        if col4.button("Increase", key=f"{participant}_increase"):
            st.session_state.scores[participant] += 1
            st.experimental_rerun()

# Reset scores button
if st.button("Reset Scores"):
    for participant in participants:
        st.session_state.scores[participant] = 0
    st.experimental_rerun()
