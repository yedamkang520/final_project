import streamlit as st
import google.auth
from datetime import date
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class Minwon:
    def __init__(self, author, content, lat, lon, created_at):
        self.author = author
        self.content = content
        self.lat = lat
        self.lon = lon
        self.created_at = created_at

    def __str__(self):
        return f"작성자: {self.author}\n내용: {self.content}\n좌표: ({self.lat}, {self.lon})\n날짜: {self.created_at}"


# 신촌캠퍼스 중심 좌표
CENTER_LAT = 37.565784
CENTER_LON = 126.938572

st.title("연세대학교 신촌캠퍼스 민원 지도")


def append_minwon_to_sheet(spreadsheet_id, minwon):
    creds, _ = google.auth.default()
    try:
        service = build("sheets", "v4", credentials=creds)
        values = [[minwon.author, minwon.content, minwon.lat, minwon.lon, str(minwon.created_at)]]
        body = {"values": values}
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range="A1",
            valueInputOption="USER_ENTERED",
            body=body,
        ).execute()
        st.success("민원이 구글 시트에 저장되었습니다!")
    except HttpError as error:
        st.error(f"에러 발생: {error}")

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    #Google API를 통해 어떤 권한을 요청할지 지정합니다. 이건 스프레드시트에 접근하고 수정할 권한이에요.

    # 무조건 새 로그인
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret_1037659309261-v5u1aa0up3rgjq67mi3jd509fkdgm15p.apps.googleusercontent.com.json',
        SCOPES
    )
    creds = flow.run_local_server(port=0)

    service = build('sheets', 'v4', credentials=creds)

SPREADSHEET_ID = "1ziXdUljIrIJQ8XsZKwkePN_ciMK2IUfS5OsfVUptp6w"

with st.form("minwon_form"):
    st.subheader("민원 등록")
    lat = st.number_input("위도", value=CENTER_LAT, format="%.6f")
    lon = st.number_input("경도", value=CENTER_LON, format="%.6f")
    author = st.text_input("작성자")
    content = st.text_area("민원 내용")
    created_at = st.date_input("작성 날짜", value=date.today())
    submitted = st.form_submit_button("민원 등록")

    if submitted:
        minwon = Minwon(author, content, lat, lon, created_at)
        append_minwon_to_sheet(SPREADSHEET_ID, minwon)