import streamlit as st
import os
import json

# --------------------- Config ---------------------
st.set_page_config(page_title="📘 Task Tracker", layout="wide")
st.markdown("<h1 style='text-align:center;'>📘 Interactive Learning Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px; color:gray;'>Track your progress. Save your wins. Reset if needed.</p>", unsafe_allow_html=True)

# --------------------- Tasks ---------------------
tasks = {
    "Pyspark Tutorials": {"units": 15, "duration": 45},
    "Resume": {"units": 6, "duration": 30},
    "SQL with Baraa": {"units": 22, "duration": 30},
}

PROGRESS_FILE = "progress.json"

# --------------------- Functions ---------------------
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress():
    with open(PROGRESS_FILE, "w") as f:
        json.dump({k: v for k, v in st.session_state.items() if isinstance(v, list)}, f)
    st.success("✅ Progress saved!")

def reset_progress():
    for task in tasks:
        st.session_state[task] = [False] * tasks[task]["units"]
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
    st.warning("🔄 Progress reset!")

# --------------------- Load Session State ---------------------
saved_state = load_progress()
for task in tasks:
    if task not in st.session_state:
        st.session_state[task] = saved_state.get(task, [False] * tasks[task]["units"])

# --------------------- Custom CSS ---------------------
st.markdown("""
<style>
    .block-button {
        font-size: 24px;
        border: none;
        background: none;
        cursor: pointer;
    }
    .block-button:hover {
        transform: scale(1.2);
    }
    .card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    .center-text {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --------------------- Task Cards ---------------------
for task_name, info in tasks.items():
    units = info["units"]
    duration = info["duration"]
    total_mins = units * duration

    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"<h3>{task_name}</h3>", unsafe_allow_html=True)
    st.markdown(f"⏱️ {units} × {duration} min = <b>{total_mins // 60}h {total_mins % 60}m</b>", unsafe_allow_html=True)

    cols = st.columns(units)
    for i in range(units):
        with cols[i]:
            label = "🟩" if st.session_state[task_name][i] else "⬜"
            if st.button(label, key=f"{task_name}-{i}"):
                st.session_state[task_name][i] = not st.session_state[task_name][i]

    completed = sum(st.session_state[task_name])
    percent = completed / units
    st.progress(percent, text=f"{completed}/{units} done ({int(percent * 100)}%)")
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------- Control Buttons ---------------------
st.markdown("### ⚙️ Actions")
col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Save Progress"):
        save_progress()

with col2:
    if st.button("🔄 Reset Progress"):
        reset_progress()
