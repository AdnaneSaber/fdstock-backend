import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Task Data Collection
task_data = [
    {'task_name': 'Task 1', 'start_date': '2023-06-01', 'end_date': '2023-06-05', 'duration': 4, 'status': 'completed'},
    {'task_name': 'Task 2', 'start_date': '2023-06-03', 'end_date': '2023-06-07', 'duration': 4, 'status': 'uncompleted'},
    {'task_name': 'Task 3', 'start_date': '2023-06-06', 'end_date': '2023-06-10', 'duration': 4, 'status': 'canceled'},
    {'task_name': 'Task 4', 'start_date': '2023-07-01', 'end_date': '2023-07-05', 'duration': 4, 'status': 'completed'},
    {'task_name': 'Task 5', 'start_date': '2023-07-02', 'end_date': '2023-07-06', 'duration': 4, 'status': 'uncompleted'},
    {'task_name': 'Task 6', 'start_date': '2023-07-06', 'end_date': '2023-07-10', 'duration': 4, 'status': 'completed'},
    # Add more tasks...
]

# Step 2: Data Analysis
df = pd.DataFrame(task_data)
df['start_date'] = pd.to_datetime(df['start_date'])
df['end_date'] = pd.to_datetime(df['end_date'])

# Last month statistics
last_month = df[(df['start_date'].dt.month == pd.Timestamp.now().month - 1)]
last_month_stats = last_month['status'].value_counts()

# Last 7 days statistics
last_7_days = df[(df['start_date'] >= pd.Timestamp.now() - pd.DateOffset(days=7))]
last_7_days_stats = last_7_days['status'].value_counts()

# Step 3: Visualization
fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# Last month chart
axs[0].pie(last_month_stats, labels=last_month_stats.index, autopct='%1.1f%%', startangle=90)
axs[0].set_title('Task Status (Last Month)')

# Last 7 days chart
axs[1].pie(last_7_days_stats, labels=last_7_days_stats.index, autopct='%1.1f%%', startangle=90)
axs[1].set_title('Task Status (Last 7 Days)')

plt.tight_layout()
plt.show()
