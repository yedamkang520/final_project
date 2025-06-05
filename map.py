import streamlit as st
import pandas as pd

# 신촌캠퍼스 중심 좌표
center_lat = 37.5649231574
center_lon = 126.9383080636

st.title("연세대학교 신촌캠퍼스 지도")

# 중심 좌표로 마커 하나만 표시
df = pd.DataFrame({
    'lat': [center_lat],
    'lon': [center_lon]
})

# 지도 표시
st.map(df, latitude="lat", longitude="lon",zoom=10)