import streamlit as st
from PIL import Image
import pandas as pd
import sqlite3
import folium
from streamlit_folium import st_folium

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="TVK Maduravoyal",
    layout="wide"
)

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

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- DATABASE ----------------

conn = sqlite3.connect("complaints.db")
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS complaints(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    area TEXT,
    category TEXT,
    problem TEXT
)
''')

conn.commit()

# ---------------- LOAD IMAGES ----------------

vijay = Image.open("vijay.jpg")
flag = Image.open("tvk_flag.png")

# ---------------- HEADER ----------------

st.image(flag, use_container_width=True)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(vijay, width=350)

st.markdown(
    '<div class="main-title">தமிழக வெற்றி கழகம்</div>',
    unsafe_allow_html=True
)

st.subheader("மதுரவாயல் மக்கள் குறைதீர் மையம்")

# ---------------- SIDEBAR ----------------

st.sidebar.title("MENU")

page = st.sidebar.radio(
    "Select Page",
    [
        "Complaint Form",
        "Women Safety",
        "Area Charts",
        "Google Maps",
        "Admin Dashboard"
    ]
)

# ---------------- COMPLAINT FORM ----------------

if page == "Complaint Form":

    st.header("📢 மக்கள் புகார் பதிவு")

    name = st.text_input("பெயர்")

    area = st.selectbox(
        "பகுதி",
        [
            "Maduravoyal",
            "Nolambur",
            "Vanagaram",
            "Alapakkam",
            "Mugappair"
        ]
    )

    category = st.selectbox(
        "பிரச்சனை வகை",
        [
            "Road Problem",
            "Water Issue",
            "EB Issue",
            "Garbage",
            "Women Safety",
            "Medical Help"
        ]
    )

    problem = st.text_area("உங்கள் பிரச்சனை")

    uploaded_file = st.file_uploader(
        "Photo Upload",
        type=["png", "jpg", "jpeg"]
    )

    if st.button("Submit Complaint"):

        c.execute(
            "INSERT INTO complaints(name,area,category,problem) VALUES(?,?,?,?)",
            (name, area, category, problem)
        )

        conn.commit()

        st.success("✅ உங்கள் புகார் பதிவு செய்யப்பட்டது")

# ---------------- WOMEN SAFETY ----------------

if page == "Women Safety":

    st.header("👩 பெண்கள் பாதுகாப்பு")

    woman_name = st.text_input("பெயர் அல்லது Anonymous")

    woman_problem = st.text_area("பாதுகாப்பு புகார்")

    emergency = st.checkbox("Emergency")

    if st.button("Submit Women Complaint"):

        c.execute(
            "INSERT INTO complaints(name,area,category,problem) VALUES(?,?,?,?)",
            (
                woman_name,
                "Women Section",
                "Women Safety",
                woman_problem
            )
        )

        conn.commit()

        st.success("✅ Women Complaint Submitted")

        if emergency:
            st.warning("🚨 Emergency Alert Sent")

# ---------------- AREA CHARTS ----------------

if page == "Area Charts":

    st.header("📊 பகுதி வாரியான புகார்கள்")

    df = pd.read_sql("SELECT * FROM complaints", conn)

    if not df.empty:

        chart = df.groupby("area").size().reset_index(name="Complaints")

        st.bar_chart(chart.set_index("area"))

        st.dataframe(df)

    else:
        st.info("No complaints available")

# ---------------- GOOGLE MAPS ----------------

if page == "Google Maps":

    st.header("🗺 Maduravoyal Complaint Map")

    m = folium.Map(
        location=[13.0732, 80.2016],
        zoom_start=12
    )

    folium.Marker(
        [13.0732, 80.2016],
        popup="Maduravoyal"
    ).add_to(m)

    st_folium(m, width=1000)

# ---------------- ADMIN LOGIN ----------------

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

        st.dataframe(df)

        total = len(df)

        st.metric("Total Complaints", total)

    elif username != "" and password != "":

        st.error("Invalid Login")
