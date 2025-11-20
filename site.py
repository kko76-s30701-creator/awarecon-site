import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET

# -----------------------------
# 1️⃣ API 정보
# -----------------------------
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
URL = f"https://openapi.gg.go.kr/DisablePersonProg?KEY={API_KEY}&Type=xml&pIndex=1&pSize=1000"

st.set_page_config(page_title="경기도 장애인복지관 운영 프로그램 현황", layout="wide")
st.title("경기도 장애인복지관 운영 프로그램 현황")

# -----------------------------
# 2️⃣ API 요청
# -----------------------------
try:
    response = requests.get(URL)
    response.raise_for_status()  # HTTP 오류가 발생하면 예외 발생
except requests.exceptions.RequestException as e:
    st.error(f"⚠️ API 요청 실패: {e}")
    st.stop()

# -----------------------------
# 3️⃣ XML 파싱
# -----------------------------
try:
    root = ET.fromstring(response.content)
    rows = root.findall(".//row")
except ET.ParseError:
    st.error("⚠️ XML 데이터 파싱 실패")
    st.stop()

# -----------------------------
# 4️⃣ 데이터프레임 생성
# -----------------------------
data = []
for r in rows:
    row_dict = {
        "이용대상상세조건(장애유형)": r.findtext("USE_TARGET_OBSTCL_TYPE_COND", default=""),
        "이용대상상세조건(연령제한)": r.findtext("USE_TARGET_AGE_LIMITN_COND", default=""),
        "이용대상상세조건(기타조건)": r.findtext("USE_TARGET_ETC_COND", default=""),
        "구분": r.findtext("PROG_DIV_NM", default=""),
        "상세구분": r.findtext("DETAIL_DIV_NM", default=""),
        "프로그램명": r.findtext("PROG_TITLE", default=""),
        "프로그램내용": r.findtext("PROG_CONT", default=""),
        "이용시간": r.findtext("USE_TM_INFO", default="")
    }
    data.append(row_dict)

df = pd.DataFrame(data)

if df.empty:
    st.warning("⚠️ API에서 데이터가 없습니다.")
    st.stop()

# -----------------------------
# 5️⃣ 데이터 표시
# -----------------------------
st.dataframe(df)
