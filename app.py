import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. SETUP DATABASE
def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            status TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    return conn

conn = init_db()

# 2. UI LAYOUT
st.title("Midnight Attendance 🌙")
st.write("Offline Logger v1.0")

# 3. INPUT FORM
with st.form("attendance_form"):
    # Dropdown for team members
    name = st.selectbox("Select Student:", ["Nasir", "Abdulazeez", "Breeze"])
    
    # Radio button for status
    status = st.radio("Status:", ["Present ✅", "Absent ❌", "Late ⏰"])
    
    # Submit button
    submitted = st.form_submit_button("Mark Attendance")

    if submitted:
        c = conn.cursor()
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO logs (name, status, timestamp) VALUES (?, ?, ?)", 
                  (name, status, time_now))
        conn.commit()
        st.success(f"Recorded: {name} is {status}")

# 4. VIEW DATA (The "Admin" View)
st.divider()
st.subheader("Today's Logs")

# Load data into a pretty table
df = pd.read_sql_query("SELECT * FROM logs ORDER BY id DESC", conn)
st.dataframe(df, use_container_width=True)

# 5. DOWNLOAD BUTTON (For manual export if sync fails)
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    "Download CSV",
    csv,
    "attendance_logs.csv",
    "text/csv",
    key='download-csv'
)