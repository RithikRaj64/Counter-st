import streamlit as st
import json
import os

st.title("Zone Out ScoreBoard")


# Helper functions to read from and write to JSON files
def load_scores():
    if os.path.exists("scores.json"):
        with open("scores.json", "r") as file:
            return json.load(file)
    else:
        return {participant: 0 for participant in participants}


def save_scores(scores):
    with open("scores.json", "w") as file:
        json.dump(scores, file)


def load_credentials():
    if os.path.exists("credentials.json"):
        with open("credentials.json", "r") as file:
            return json.load(file)
    else:
        return {participant: "123" for participant in participants}


def save_credentials(credentials):
    with open("credentials.json", "w") as file:
        json.dump(credentials, file)


def load_logs():
    if os.path.exists("logs.txt"):
        with open("logs.txt", "r") as file:
            return file.readlines()
    else:
        return []


def save_log(log_entry):
    with open("logs.txt", "a") as file:
        file.write(log_entry + "\n")


# List of participants
participants = ["Rajpal", "Prasanna", "Magesh", "Jeeva", "Rithik", "Deeksha"]

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Load credentials from JSON file
credentials = load_credentials()


def login(username, password):
    if username in credentials and credentials[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.page = "scoreboard"  # Set the page to scoreboard after login
        st.success("Logged in successfully!")
        st.experimental_rerun()  # Ensure page reruns to reflect changes
    else:
        st.error("Invalid username or password")


def change_password(username, old_password, new_password):
    if username in credentials and credentials[username] == old_password:
        credentials[username] = new_password
        save_credentials(credentials)
        st.success("Password changed successfully!")
    else:
        st.error("Invalid username or old password")


def log_score_change(participant, change_type):
    score = st.session_state.scores[participant]
    log_entry = f"{st.session_state.username} {change_type} {participant}'s score: Current score of {participant} = {score}"
    save_log(log_entry)


def log_scores_reset():
    log_entry = f"{st.session_state.username} reset all scores"
    save_log(log_entry)


# Display login/change password form if not logged in
if not st.session_state.logged_in:
    # Login/Change Password selection
    auth_choice = st.radio("Select an option", ["Login", "Change Password"])

    if auth_choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(username, password)
    elif auth_choice == "Change Password":
        username = st.text_input("Username")
        old_password = st.text_input("Old Password", type="password")
        new_password = st.text_input("New Password", type="password")
        if st.button("Change Password"):
            change_password(username, old_password, new_password)

else:
    # Load scores from the JSON file
    if "scores" not in st.session_state:
        st.session_state.scores = load_scores()

    # Create tabs
    tabs = st.tabs(["Scoreboard", "Logs"])

    # Scoreboard Tab
    with tabs[0]:
        st.header(f"Welcome, {st.session_state.username}!")
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
                    log_score_change(participant, "decreased")
                    st.experimental_rerun()
                col3.text(st.session_state.scores[participant])
                if col4.button("Increase", key=f"{participant}_increase"):
                    st.session_state.scores[participant] += 1
                    save_scores(st.session_state.scores)  # Save scores to the JSON file
                    log_score_change(participant, "increased")
                    st.experimental_rerun()

        # Reset scores button
        if st.button("Reset Scores"):
            for participant in participants:
                st.session_state.scores[participant] = 0
            save_scores(st.session_state.scores)  # Save scores to the JSON file
            log_scores_reset()  # Log the scores reset
            st.experimental_rerun()

        # Logout button
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.page = "login"  # Redirect to login page
            st.experimental_rerun()

    # Logs Tab
    with tabs[1]:
        st.header("Activity Log")
        logs = load_logs()
        if logs:
            for log in logs:
                st.text(log)

    # Update tab selection state
    # Handle tab changes
    st.session_state.selected_tab = tabs[0].selected_index
