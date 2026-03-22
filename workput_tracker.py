import streamlit as st
import pandas as pd
from datetime import datetime
import os
import random

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Workout Tracker Pro", layout="wide")

# -------------------------------
# LOGIN SYSTEM
# -------------------------------
PASSWORD = "ilovemybubu"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔐 Login Required")

    pwd = st.text_input("Enter Password", type="password")

    if st.button("Login"):
        if pwd == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Wrong password ❌")

    st.stop()

# -------------------------------
# CUSTOM CSS (QUOTE BIGGER)
# -------------------------------
st.markdown("""
<style>
.quote {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    color: #2e7dff;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# MOTIVATIONAL QUOTES
# -------------------------------
quotes = [
    "Push yourself because no one else will 💪",
    "Consistency beats motivation 🔥",
    "Small progress is still progress 👊",
    "Discipline creates results 🚀",
    "No pain, no gain 🏋️"
]
quote = random.choice(quotes)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("<h1 style='text-align:center;'>💪 Workout Tracker Pro</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='quote'>{quote}</div>", unsafe_allow_html=True)

# -------------------------------
# FILE SETUP
# -------------------------------
FILE = "workout_history.xlsx"

if not os.path.exists(FILE):
    df_init = pd.DataFrame(columns=[
        "Date", "Workout", "Set", "Weight", "Reps", "Volume"
    ])
    df_init.to_excel(FILE, index=False)

# -------------------------------
# MAIN LAYOUT
# -------------------------------
col1, col2 = st.columns([2, 2])

# ===============================
# 🏋️ LEFT → INPUT
# ===============================
with col1:
    st.subheader("🏋️ Workout Tracker")

    workout = st.text_input("Workout Name")
    date = st.date_input("Date")

    sets = st.number_input("Sets", min_value=1, max_value=6, value=3)

    set_data = []
    for i in range(sets):
        c1, c2 = st.columns(2)
        with c1:
            w = st.number_input(f"Weight {i+1}", value=20, key=f"w{i}")
        with c2:
            r = st.number_input(f"Reps {i+1}", value=10, key=f"r{i}")
        set_data.append((w, r))

    save = st.button("💾 Save Workout")

# ===============================
# 📅 RIGHT → HISTORY + DOWNLOAD
# ===============================
with col2:
    st.subheader("📅 Workout History")

    selected_date = st.date_input("Select Date")

    df_all = pd.read_excel(FILE)

    filtered = df_all[df_all["Date"] == selected_date.strftime("%Y-%m-%d")]

    if not filtered.empty:
        st.dataframe(filtered, use_container_width=True)

        total = filtered["Volume"].sum()
        st.success(f"Total Volume: {total} kg")
    else:
        st.info("No workout found")

    # -------------------------------
    # DOWNLOAD BELOW HISTORY
    # -------------------------------
    st.markdown("---")
    st.subheader("📥 Download")

    with open(FILE, "rb") as f:
        st.download_button(
            "⬇️ Download Excel",
            f,
            file_name="workout_history.xlsx"
        )

# -------------------------------
# SAVE LOGIC
# -------------------------------
if save:
    df_existing = pd.read_excel(FILE)

    new_rows = []
    for i, (w, r) in enumerate(set_data):
        new_rows.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Workout": workout,
            "Set": i+1,
            "Weight": w,
            "Reps": r,
            "Volume": w * r
        })

    df_new = pd.DataFrame(new_rows)

    df_final = pd.concat([df_existing, df_new], ignore_index=True)
    df_final.to_excel(FILE, index=False)

    st.success("Workout saved successfully ✅")
    st.rerun()
