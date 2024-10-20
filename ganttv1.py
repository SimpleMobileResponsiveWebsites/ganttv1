import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the application
st.title('Basic Gantt Chart Application')

# Input data for the Gantt chart
st.subheader("Enter Gantt Chart Data")

# Sample data for the Gantt chart
sample_data = {
    'Task': ['Task 1', 'Task 2', 'Task 3', 'Task 4'],
    'Start': ['2024-10-01', '2024-10-05', '2024-10-10', '2024-10-15'],
    'End': ['2024-10-05', '2024-10-10', '2024-10-15', '2024-10-20'],
    'Completion (%)': [100, 50, 20, 0]
}

# Load data into a DataFrame
task_data = pd.DataFrame(sample_data)

# Allow user to upload their own CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # If the user uploads a CSV, read the file into a DataFrame
    task_data = pd.read_csv(uploaded_file)

# Display an editable table for users to modify the data
st.write("Modify the task data below if necessary:")
task_data = st.data_editor(task_data)

# Ensure the Start and End columns are in datetime format, handling errors gracefully
task_data['Start'] = pd.to_datetime(task_data['Start'], errors='coerce')
task_data['End'] = pd.to_datetime(task_data['End'], errors='coerce')

# Remove rows with invalid dates (NaT)
task_data.dropna(subset=['Start', 'End'], inplace=True)

# Check if there are still valid rows to plot
if not task_data.empty:
    # Convert timedelta to a readable format (avoid timedelta in Plotly serialization)
    task_data['Start'] = task_data['Start'].dt.strftime('%Y-%m-%d')
    task_data['End'] = task_data['End'].dt.strftime('%Y-%m-%d')

    # Generate the Gantt Chart using Plotly
    fig = px.timeline(
        task_data,
        x_start="Start",
        x_end="End",
        y="Task",
        color="Task",
        hover_name="Task",
        title="Gantt Chart",
        labels={"Task": "Task Name"}
    )

    # Sort tasks by start date
    fig.update_yaxes(categoryorder="total ascending")

    # Customize layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Tasks",
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    # Display the Gantt chart
    st.plotly_chart(fig)
else:
    st.warning("No valid data to display in the Gantt chart. Please check the input dates.")

# Option for users to download the modified task data as a CSV
st.write("Download the current task data as a CSV:")
csv = task_data.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='gantt_tasks.csv',
    mime='text/csv'
)
