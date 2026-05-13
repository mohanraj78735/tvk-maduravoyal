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

conn = sqlite3.connect("complaints.db", check_same_thread=False)
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

    col1, col2, col3 = st.columns([1,2,1])

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

st.metric("📢 Total Complaints", count_df["total"][0])

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

    if "water" in text or "தண்ணீர்" in text:
        category = "Water Issue"
        priority = "High"

    elif "road" in text or "சாலை" in text:
        category = "Road Problem"
        priority = "Medium"

    elif "eb" in text or "current" in text:
        category = "EB Issue"
        priority = "High"

    elif "garbage" in text or "waste" in text:
        category = "Garbage"
        priority = "Medium"

    elif "women" in text or "harassment" in text:
        category = "Women Safety"
        priority = "High"

    return category, priority

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
        type=["png", "jpg", "jpeg"]
    )

    camera_photo = st.camera_input("Take Live Photo")

    category, ai_priority = ai_analyzer(problem)

    st.info(f"AI Detected Category: {category}")
    st.info(f"AI Priority: {ai_priority}")

    priority = st.selectbox(
        "Priority",
        ["High", "Medium", "Low"],
        index=["High", "Medium", "Low"].index(ai_priority)
    )

    if st.button("Submit Complaint"):

        tracking_id = "TVK" + str(random.randint(10000,99999))

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        if uploaded_file is not None:

            save_path = os.path.join("uploads", uploaded_file.name)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

        if camera_photo is not None:

            camera_path = os.path.join(
                "uploads",
                camera_photo.name
            )

            with open(camera_path, "wb") as f:
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
            f"✅ Complaint Submitted Successfully\nTracking ID: {tracking_id}"
        )

# ---------------- WOMEN SAFETY ----------------

if page == "Women Safety":

    st.header("👩 பெண்கள் பாதுகாப்பு")

    woman_name = st.text_input("பெயர் அல்லது Anonymous")

    woman_phone = st.text_input("Phone Number")

    woman_problem = st.text_area("பாதுகாப்பு புகார்")

    emergency = st.checkbox("Emergency")

    if st.button("Submit Women Complaint"):

        tracking_id = "TVK" + str(random.randint(10000,99999))

        current_time = datetime.now().strftime("%d-%m-%Y %H:%M")

        priority = "High" if emergency else "Medium"

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
                woman_phone,
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
            f"✅ Women Complaint Submitted\nTracking ID: {tracking_id}"
        )

        if emergency:
            st.error("🚨 EMERGENCY ALERT SENT")

# ---------------- TRACKING ----------------

if page == "Tracking":

    st.header("🔎 Complaint Tracking")

    search_id = st.text_input("Enter Tracking ID")

    if st.button("Track Complaint"):

        result = pd.read_sql(
            f"SELECT * FROM complaints WHERE tracking_id='{search_id}'",
            conn
        )

        if not result.empty:

            st.success("Complaint Found")

            st.dataframe(result)

        else:
            st.error("Invalid Tracking ID")

# ---------------- AREA CHARTS ----------------

if page == "Area Charts":

    st.header("📊 Area Wise Complaints")

    df = pd.read_sql("SELECT * FROM complaints", conn)

    if not df.empty:

        chart = df.groupby("area").size().reset_index(name="Complaints")

        st.bar_chart(chart.set_index("area"))

        category_chart = df.groupby("category").size()

        st.subheader("Category Wise Complaints")

        st.pyplot(category_chart.plot.pie(autopct='%1.1f%%').figure)

        st.dataframe(df)

    else:
        st.info("No complaints available")

# ---------------- HEAT MAP ----------------

if page == "Heat Map":

    st.header("🔥 Red Zone Complaint Heat Map")

    m = folium.Map(
        location=[13.0732, 80.2016],
        zoom_start=12
    )

    heat_data = [
        [13.0732,80.2016],
        [13.0827,80.1672],
        [13.0715,80.1547],
        [13.0732,80.2016],
        [13.0732,80.2016]
    ]

    HeatMap(heat_data).add_to(m)

    folium.Marker(
        [13.0732,80.2016],
        popup="Maduravoyal"
    ).add_to(m)

    st_folium(m, width=1000)

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

        df = pd.read_sql("SELECT * FROM complaints", conn)

        st.subheader("📋 All Complaints")

        search = st.text_input("Search Complaint")

        if search:
            filtered = df[
                df["name"].str.contains(search, case=False)
            ]
            st.dataframe(filtered)

        else:
            st.dataframe(df)

        total = len(df)

        st.metric("Total Complaints", total)

        st.subheader("Update Complaint Status")

        update_id = st.text_input("Tracking ID")

        new_status = st.selectbox(
            "Status",
            ["Pending", "In Progress", "Completed"]
        )

        if st.button("Update Status"):

            c.execute(
                "UPDATE complaints SET status=? WHERE tracking_id=?",
                (new_status, update_id)
            )

            conn.commit()

            st.success("Status Updated")

        st.subheader("Delete Complaint")

        delete_id = st.number_input(
            "Delete Complaint ID",
             step=1
)
            
