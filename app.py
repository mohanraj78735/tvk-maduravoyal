import streamlit as st
from PIL import Image

st.set_page_config(page_title="TVK Maduravoyal")

# Load Images
flag = Image.open("tvk_flag.png")
vijay = Image.open("vijay.jpg")

# Show Banner
st.image(flag, use_container_width=True)

# Vijay Image
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image(vijay, width=300)

# Title
st.title("தமிழக வெற்றி கழகம்")
st.subheader("மதுரவாயல் மக்கள் குறைதீர் மையம்")

# Complaint Form
name = st.text_input("பெயர்")
area = st.text_input("பகுதி")
problem = st.text_area("உங்கள் பிரச்சனை")

# Women Complaint
women = st.text_area("பெண்கள் பாதுகாப்பு புகார்")

# Submit Button
if st.button("Submit Complaint"):
    st.success("உங்கள் புகார் பதிவு செய்யப்பட்டது")
