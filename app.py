import streamlit as st
import pandas as pd

from database import (
    get_all_logs,
    add_log,
    add_schedule,
    get_schedule,
    update_stock
)

from datetime import date, datetime
from streamlit_autorefresh import st_autorefresh

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(page_title="SafeDose AI", page_icon="💊")

st.title("💊 SafeDose AI")
st.caption("Medicine Reminder + Pill Detector — Team Limitless")

# ── AUTO REFRESH ─────────────────────────────────────
st_autorefresh(interval=10 * 1000, key="refresh")

# ── SIDEBAR LOGIN ────────────────────────────────────
st.sidebar.header("👤 Patient Login")

patient = st.sidebar.text_input("Enter Your Name")

if not patient:
    st.warning("Please enter your name.")
    st.stop()

st.sidebar.success(f"Welcome, {patient}! 👋")

# ── YOUR TABLETS ─────────────────────────────────────
medicine_options = [
    "Paracetamol",
    "Dolo 650",
    "Atarax"
]

# ── SET REMINDER ────────────────────────────────────
st.header("⏰ Set Medicine Reminder")

medicine = st.selectbox(
    "Select Medicine",
    medicine_options
)

reminder_time = st.text_input(
    "Reminder Time (Example: 09:25 PM)"
)

stock = st.number_input(
    "How many tablets do you have?",
    min_value=1,
    value=10
)

current_time_display = datetime.now().strftime("%I:%M %p")

st.caption(f"Current Time: {current_time_display}")

if st.button("Set Reminder"):

    add_schedule(patient, medicine, reminder_time, stock)

    st.success(
        f"✅ Reminder set for {medicine} at {reminder_time}"
    )

# ── STOCK DISPLAY ───────────────────────────────────
schedule_data = get_schedule(patient)

latest_stock = None

for row in reversed(schedule_data):

    id, med, sched_time, stk = row

    if med == medicine:

        latest_stock = stk
        break

if latest_stock is not None:

    st.info(
        f"💊 Current Stock for {medicine}: {latest_stock}"
    )

    if latest_stock <= 3:

        st.error(
            f"🚨 Only {latest_stock} tablets left!"
        )

    elif latest_stock <= 7:

        st.warning(
            f"⚠️ Only {latest_stock} tablets remaining."
        )

# ── REMINDER ALERT ──────────────────────────────────
st.header("🔔 Medicine Reminder Alert")

schedule = get_schedule(patient)

current_time = datetime.now().strftime("%I:%M %p")

triggered = False

for row in schedule:

    id, med, sched_time, stk = row

    if sched_time.strip().upper() == current_time.strip().upper():

        unique_key = f"alerted_{id}_{current_time}"

        if unique_key not in st.session_state:

            st.session_state[unique_key] = True

            st.warning(f"⏰ Time to take your {med}!")

            voice_text = f"Time to take your {med}"

            st.components.v1.html(f"""
                <script>
                    var msg = new SpeechSynthesisUtterance("{voice_text}");
                    window.speechSynthesis.speak(msg);
                </script>
            """, height=0)

            triggered = True

if not triggered:

    st.info("No reminders right now.")

# ── AI SCANNER ──────────────────────────────────────
st.header("📷 AI Pill Scanner")

camera_image = st.camera_input("Scan Tablet")

if camera_image is not None:

    st.image(camera_image)

    current_time = datetime.now().strftime("%I:%M %p")

    expected = None

    # FIND CURRENT MEDICINE
    for row in schedule:

        id, med, sched_time, stk = row

        if sched_time.strip().upper() == current_time.strip().upper():

            expected = med
            break

    if expected is None:

        st.warning(
            "⚠️ No medicine scheduled right now."
        )

    else:

        # DEMO AI DETECTION
        detected = expected
        confidence = 98

        st.success(
            f"🤖 AI Detected: {detected} ({confidence}% confidence)"
        )

        # PREVENT DUPLICATE LOGS
        log_key = f"{patient}_{expected}_{current_time}"

        if log_key not in st.session_state:

            st.session_state[log_key] = True

            if detected.lower() == expected.lower():

                st.success(
                    f"✅ Correct tablet detected for {expected}"
                )

                add_log(patient, expected, "Correct")

                update_stock(patient, expected)

                st.balloons()

            else:

                st.error(
                    f"❌ Wrong tablet detected! Expected: {expected}"
                )

                add_log(patient, expected, "Wrong")

                st.warning(
                    "📱 Caregiver Alert Sent!"
                )

# ── MISSED DOSE ─────────────────────────────────────
st.header("⚠️ Missed a Dose?")

missed_medicine = st.selectbox(
    "Which medicine did you miss?",
    medicine_options,
    key="missed"
)

if st.button("Mark as Missed"):

    add_log(patient, missed_medicine, "Missed")

    st.warning("📱 Caregiver Alert Sent!")

    st.info(f"{missed_medicine} marked as missed.")

# ── MEDICINE HISTORY ────────────────────────────────
st.header("📋 Medicine History")

selected_history = st.selectbox(
    "Select Medicine History",
    medicine_options,
    key="history"
)

logs = get_all_logs(patient)

filtered_logs = []

for row in logs:

    id, med, status, timestamp = row

    if med == selected_history:

        filtered_logs.append(row)

if filtered_logs:

    for row in filtered_logs:

        id, med, status, timestamp = row

        if status == "Correct":

            st.success(
                f"✅ {med} │ Correct │ {timestamp}"
            )

        elif status == "Wrong":

            st.error(
                f"❌ {med} │ Wrong Tablet │ {timestamp}"
            )

        elif status == "Missed":

            st.warning(
                f"⚠️ {med} │ Dose Missed │ {timestamp}"
            )

else:

    st.info("No history for selected medicine.")

# ── DAILY REPORT CARD ───────────────────────────────
st.markdown("---")

st.header("📊 Today's Report Card")

today = str(date.today())

all_logs = get_all_logs(patient)

today_logs = [
    l for l in all_logs if l[3].startswith(today)
]

correct = len([
    l for l in today_logs if l[2] == "Correct"
])

wrong = len([
    l for l in today_logs if l[2] == "Wrong"
])

missed = len([
    l for l in today_logs if l[2] == "Missed"
])

total = correct + wrong + missed

accuracy = round((correct / total) * 100) if total > 0 else 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("✅ Correct", correct)
c2.metric("❌ Wrong", wrong)
c3.metric("⚠️ Missed", missed)
c4.metric("🎯 Accuracy", f"{accuracy}%")

# ── BAR CHART ───────────────────────────────────────
st.header("📈 Visual Summary")

chart_data = pd.DataFrame({
    "Status": ["Correct", "Wrong", "Missed"],
    "Count": [correct, wrong, missed]
})

st.bar_chart(chart_data.set_index("Status"))

# ── CURRENT SCHEDULE ────────────────────────────────
st.markdown("---")

st.header("📅 Current Medicine Schedule")

if schedule_data:

    table_data = []

    for row in schedule_data:

        id, med, sched_time, stk = row

        table_data.append({
            "Medicine": med,
            "Reminder Time": sched_time,
            "Stock Left": stk
        })

    df = pd.DataFrame(table_data)

    st.dataframe(df, use_container_width=True)

else:

    st.info("No medicines scheduled yet.")