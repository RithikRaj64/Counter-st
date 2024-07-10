import streamlit as st
import json
import os


# Helper functions to read from and write to a JSON file
def load_scores():
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as file:
            return json.load(file)
    else:
        return {participant: 0 for participant in participants}


def save_scores(scores):
    with open("scores.json", "w") as file:
        json.dump(scores, file)


# List of participants
participants = ["Rajpal", "Prasanna", "Magesh", "Jeeva", "Rithik", "Deeksha"]

# Load scores from the JSON file
if "scores" not in st.session_state:
    st.session_state.scores = load_scores()

# Title of the application
st.header("Zone Out ScoreBoard")

st.markdown("----")

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
            save_scores(st.session_state.scores)  # Save scores to the JSON file
            st.experimental_rerun()
        col3.text(st.session_state.scores[participant])
        if col4.button("Increase", key=f"{participant}_increase"):
            st.session_state.scores[participant] += 1
            save_scores(st.session_state.scores)  # Save scores to the JSON file
            st.experimental_rerun()

# Reset scores button
if st.button("Reset Scores"):
    for participant in participants:
        st.session_state.scores[participant] = 0
    save_scores(st.session_state.scores)  # Save scores to the JSON file
    st.experimental_rerun()
