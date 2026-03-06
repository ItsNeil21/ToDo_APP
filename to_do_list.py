import pandas as pd
import streamlit as st
from datetime import datetime
import os

# Force Streamlit to start with an empty dataframe
if os.path.exists("To_Do.csv"):
    os.remove("To_Do.csv")
st.session_state.clear()
# File path for CSV
filepath = "To_Do.csv"

# Initialize session state
if 'tasks_df' not in st.session_state:
    try:
        st.session_state.tasks_df = pd.read_csv(filepath)
    except FileNotFoundError:
        st.session_state.tasks_df = pd.DataFrame(columns=["Task", "Days_Due_In"])

df = st.session_state.tasks_df  # use session state everywhere

# Streamlit App
st.title("To-Do List")

# Show current tasks
st.subheader("Current Tasks")
st.dataframe(df)

# Section to add a new task
st.subheader("Add A Task")
task = st.text_input("Task Name")
due = st.text_input("Days Due In")

if st.button("Add Task"):
    if task and due.isdigit():
        new_row = pd.DataFrame({"Task": [task], "Days_Due_In": [int(due)]})
        df = pd.concat([df, new_row], ignore_index=True)
        st.session_state.tasks_df = df  # update session state
        df.to_csv(filepath, index=False)
        st.success("Task added!")
    else:
        st.error("Enter a task name and a number for Days Due In.")
today = datetime.today()

df["Days_Left"] = df["Days_Due_In"]

df["Status"] = df["Days_Left"].apply(
    lambda x: "Overdue" if x < 0 else "Due Date Soon"
)
if df["Days_Left"].min() < 0:
    st.warning("You have overdue tasks!")
# Section to delete a task
st.subheader("Delete A Task")
if not df.empty:
    task_to_delete = st.selectbox(
        "Choose a task to delete",
        df.index,
        format_func=lambda x: f"{df.at[x,'Task']} (Due {df.at[x,'Days_Due_In']} days)"
    )

    if st.button("Delete Task"):
        df = df.drop(task_to_delete).reset_index(drop=True)
        st.session_state.tasks_df = df
        df.to_csv(filepath, index=False)
        st.success("Task deleted!")
else:
    st.info("No tasks to delete.")