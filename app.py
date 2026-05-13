import streamlit as st
from PIL import Image
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium
from folium.plugins import HeatMap
from datetime import datetime
from fpdf import FPDF
import random
import os

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="TVK Maduravoyal",
    layout="wide"
)

# ---------------- FOLDER ----------------

if not os.path.exists("uploads"):
    os.makedirs("uploads")

# ---------------- DARK THEME ----------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0E1117;
        color: white;
    }

    h1,h2,h3,h4,h5,h6,p,label {
        color: white !important;
    }

    .main-title {
        text-align:center;
        font-size:50px;
        font-weight:bold;
        color:#FFD700;
        animation: glow 2s infinite;
    }

    @keyframes glow {
        0% {opacity:0.5;}
        50% {opacity:1;}
        100% {opacity:0.5;}
    }

    .stButton>button {
        background: linear-gradient(45deg,#FFD700,#FFB300);
        color:black;
        border-radius:10px;
        font-weight:bold;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- DATABASE ----------------

conn = sqlite3.connect(
    "complaints.db",
    check_same_thread=False
)

c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS complaints(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_id TEXT,
    name TEXT,
    phone TEXT,
    area TEXT,
    category TEXT,
    priority TEXT,
    problem TEXT,
    status TEXT,
    date TEXT
)
''')

conn.commit()

# ---------------- LOAD IMAGES ----------------

try:

    vijay = Image.open("vijay.jpg")
    flag = Image.open("tvk_flag.png")

    st.image(flag, use_container_width=True)

    col1,col2,col3 = st.columns([1,2,1])

    with col2:
        st.image(vijay, width=350)

except:
    st.warning("Upload vijay.jpg and tvk_flag.png")

# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">தமிழக வெற்றி கழகம்</div>',
    unsafe_allow_html=True
)

st.subheader("மதுரவாயல் மக்கள் குறைதீர் மையம்")

# ---------------- LIVE COUNT ----------------

count_df = pd.read_sql(
    "SELECT COUNT(*) as total FROM complaints",
    conn
)

st.metric(
    "📢 Total Complaints",
    count_df["total"][0]
)

# ---------------- SIDEBAR ----------------

st.sidebar.title("MENU")

page = st.sidebar.radio(
    "Select Page",
    [
        "Complaint Form",
        "Women Safety",
        "Tracking",
        "Area Charts",
        "Heat Map",
        "Admin Dashboard",
        "MLA Dashboard"
    ]
)

# ---------------- ANNOUNCEMENT ----------------

st.sidebar.subheader("📢 Public Announcement")

announcement = st.sidebar.text_area(
    "Announcement"
)

if announcement:
    st.sidebar.success(announcement)

# ---------------- LIVE CLOCK ----------------

st.sidebar.subheader("⏰ Current Time")

st.sidebar.write(
    datetime.now().strftime("%d-%m-%Y %H:%M:%S")
)

# ---------------- OFFICER LOGIN ----------------

st.sidebar.subheader("👮 Officer Login")

officer_name = st.sidebar.text_input(
    "Officer Name"
)

# ---------------- STREET LIST ----------------

street_list = [
    "Maduravoyal Main Road",
    "Alapakkam",
    "Vanagaram Main Road",
    "Nerkundram",
    "Porur Garden",
    "Kamarajar Salai",
    "Mettukuppam",
    "Mugalivakkam",
    "Karambakkam",
    "Velappanchavadi",
    "Ayyappanthangal",
    "Nolambur Phase 1",
    "Nolambur Phase 2",
    "Mugappair West",
    "MMDA Colony",
    "Ganapathy Nagar",
    "Sri Devi Nagar",
    "Kandasamy Nagar",
    "Perumal Koil Street",
    "Anna Street",
    "Ambedkar Street",
    "VOC Street",
    "Pillaiyar Koil Street",
    "Teachers Colony",
    "Thiruvalluvar Nagar",
    "Rajiv Gandhi Nagar",
    "Indira Nagar",
    "Sakthi Nagar",
    "Church Street",
    "Lake View Road"
]

# ---------------- AI ANALYZER ----------------

def ai_analyzer(problem_text):

    text = problem_text.lower()

    category = "General"
    priority = "Low"

    if "water" in text:
        category = "Water Issue"
        priority = "High"

    elif "road" in text:
        category = "Road Problem"
        priority = "Medium"

    elif "eb" in text:
        category = "EB Issue"
        priority = "High"

    elif "garbage" in text:
        category = "Garbage"
        priority = "Medium"

    elif "women" in text:
        category = "Women Safety"
        priority = "High"

    return category, priority

# ---------------- FAKE DETECTOR ----------------

def fake_detector(problem_text):

    if len(problem_text) < 5:
        return True

    return False

# ---------------- COMPLAINT FORM ----------------

if page == "Complaint Form":

    st.header("📢 மக்கள் புகார் பதிவு")

    name = st.text_input("பெயர்")

    phone = st.text_input("Phone Number")

    area = st.selectbox(
        "பகுதி / தெரு",
        street_list
    )

    problem = st.text_area("உங்கள் பிரச்சனை")

    uploaded_file = st.file_uploader(
        "Photo Upload",
        type=["png","jpg","jpeg"]
    )

    camera_photo = st.camera_input(
        "Take Live Photo"
    )

    st.subheader("🎤 Voice Complaint")

    audio_file = st.file_uploader(
        "Upload Voice Complaint",
        type=["mp3","wav"]
    )

    if audio_file:
        st.audio(audio_file)

    category, ai_priority = ai_analyzer(problem)

    st.info(f"AI Category: {category}")
    st.info(f"AI Priority: {ai_priority}")

    priority = st.selectbox(
        "Priority",
        ["High","Medium","Low"]
    )

    if fake_detector(problem):
        st.warning("⚠ Possible Fake Complaint")

    if st.button("Submit Complaint"):

        tracking_id = "TVK" + str(
            random.randint(10000,99999)
        )

        current_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        if uploaded_file is not None:

            save_path = os.path.join(
                "uploads",
                uploaded_file.name
            )

            with open(save_path,"wb") as f:
                f.write(uploaded_file.getbuffer())

        if camera_photo is not None:

            camera_path = os.path.join(
                "uploads",
                camera_photo.name
            )

            with open(camera_path,"wb") as f:
                f.write(camera_photo.getbuffer())

        c.execute(
            """
            INSERT INTO complaints
            (
                tracking_id,
                name,
                phone,
                area,
                category,
                priority,
                problem,
                status,
                date
            )
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                tracking_id,
                name,
                phone,
                area,
                category,
                priority,
                problem,
                "Pending",
                current_time
            )
        )

        conn.commit()

        st.success(
            f"Complaint Submitted ✅\nTracking ID: {tracking_id}"
        )

# ---------------- WOMEN SAFETY ----------------

if page == "Women Safety":

    st.header("👩 பெண்கள் பாதுகாப்பு")

    woman_name = st.text_input(
        "பெயர் அல்லது Anonymous"
    )

    woman_problem = st.text_area(
        "பாதுகாப்பு புகார்"
    )

    emergency = st.checkbox("Emergency")

    if st.button("Submit Women Complaint"):

        tracking_id = "TVK" + str(
            random.randint(10000,99999)
        )

        current_time = datetime.now().strftime(
            "%d-%m-%Y %H:%M"
        )

        priority = "High"

        c.execute(
            """
            INSERT INTO complaints
            (
                tracking_id,
                name,
                phone,
                area,
                category,
                priority,
                problem,
                status,
                date
            )
            VALUES(?,?,?,?,?,?,?,?,?)
            """,
            (
                tracking_id,
                woman_name,
                "",
                "Women Section",
                "Women Safety",
                priority,
                woman_problem,
                "Pending",
                current_time
            )
        )

        conn.commit()

        st.success(
            f"Women Complaint Submitted ✅\nTracking ID: {tracking_id}"
        )

        if emergency:
            st.error("🚨 SOS ALERT SENT")

# ---------------- TRACKING ----------------

if page == "Tracking":

    st.header("🔎 Complaint Tracking")

    search_id = st.text_input(
        "Enter Tracking ID"
    )

    if st.button("Track Complaint"):

        result = pd.read_sql(
            f"SELECT * FROM complaints WHERE tracking_id='{search_id}'",
            conn
        )

        if not result.empty:

            st.success("Complaint Found")

            st.dataframe(result)

            st.subheader("⭐ Rate Resolution")

            rating = st.slider(
                "Rate Service",
                1,
                5
            )

            if st.button("Submit Rating"):
                st.success(
                    f"Thanks For Rating {rating} ⭐"
                )

        else:
            st.error("Invalid Tracking ID")

# ---------------- AREA CHARTS ----------------

if page == "Area Charts":

    st.header("📊 Area Wise Complaints")

    df = pd.read_sql(
        "SELECT * FROM complaints",
        conn
    )

    if not df.empty:

        chart = df.groupby(
            "area"
        ).size().reset_index(
            name="Complaints"
        )

        st.bar_chart(
            chart.set_index("area")
        )

        st.dataframe(df)

    else:
        st.info("No complaints available")

# ---------------- HEAT MAP ----------------

if page == "Heat Map":

    st.header("🔥 Red Zone Heat Map")

    m = folium.Map(
        location=[13.0732,80.2016],
        zoom_start=12
    )

    heat_data = [
        [13.0732,80.2016],
        [13.0827,80.1672],
        [13.0715,80.1547],
        [13.0732,80.2016]
    ]

    HeatMap(heat_data).add_to(m)

    folium.Marker(
        [13.0732,80.2016],
        popup="Maduravoyal"
    ).add_to(m)

    st_folium(m,width=1000)

# ---------------- ADMIN DASHBOARD ----------------

if page == "Admin Dashboard":

    st.header("🔐 Admin Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if username == "admin" and password == "tvk123":

        st.success("Login Successful")

        df = pd.read_sql(
            "SELECT * FROM complaints",
            conn
        )

        st.subheader("📋 All Complaints")

        st.dataframe(df)

        total = len(df)

        st.metric(
            "Total Complaints",
            total
        )

        st.subheader("Update Status")

        update_id = st.text_input(
            "Tracking ID"
        )

        new_status = st.selectbox(
            "Status",
            [
                "Pending",
                "In Progress",
                "Completed"
            ]
        )

        if st.button("Update Status"):

            c.execute(
                "UPDATE complaints SET status=? WHERE tracking_id=?",
                (
                    new_status,
                    update_id
                )
            )

            conn.commit()

            st.success("Status Updated")

        st.subheader("Delete Complaint")

        delete_id = st.number_input(
            "Delete Complaint ID",
            step=1
        )

        if st.button("Delete Complaint"):

            c.execute(
                "DELETE FROM complaints WHERE id=?",
                (delete_id,)
            )

            conn.commit()

            st.success("Complaint Deleted")

        st.subheader("🛠 Before / After Work")

        before = st.file_uploader(
            "Before Image",
            type=["png","jpg"]
        )

        after = st.file_uploader(
            "After Image",
            type=["png","jpg"]
        )

        if before:
            st.image(before)

        if after:
            st.image(after)

    elif username != "" and password != "":
        st.error("Invalid Login")

# ---------------- MLA DASHBOARD ----------------

if page == "MLA Dashboard":

    st.header("🏛 MLA Smart Dashboard")

    df = pd.read_sql(
        "SELECT * FROM complaints",
        conn
    )

    if not df.empty:

        total = len(df)

        pending = len(
            df[df["status"] == "Pending"]
        )

        completed = len(
            df[df["status"] == "Completed"]
        )

        high_priority = len(
            df[df["priority"] == "High"]
        )

        col1,col2,col3,col4 = st.columns(4)

        col1.metric("Total", total)
        col2.metric("Pending", pending)
        col3.metric("Completed", completed)
        col4.metric("High Priority", high_priority)

        st.subheader("Area Analytics")

        area_chart = df.groupby("area").size()

        st.bar_chart(area_chart)

        st.subheader("Priority Analytics")

        priority_chart = df.groupby(
            "priority"
        ).size()

        st.bar_chart(priority_chart)

        st.subheader("🔔 Live Notifications")

        st.info(
            "5 High Priority Complaints Pending"
        )

        st.subheader("Recent Complaints")

        st.dataframe(df.tail(10))

    else:
        st.info("No complaints available")
