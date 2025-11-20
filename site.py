import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd

st.set_page_config(page_title="직장 내 인식개선 교육 콘텐츠 현황", layout="wide")
st.title("📚 한국장애인고용공단 직장 내 인식개선 교육 콘텐츠 현황")

# ==========================
# 1️⃣ API 요청 설정
# ==========================
API_KEY = "5b4b3917e3b9a6a48763aa2cd0ca266d6ee935d8be01ab9728fb2b77a7f67935"
URL = f"https://apis.data.go.kr/B552583/awarecon?serviceKey={API_KEY}&pageNo=1&numOfRows=10&type=xml"

# ==========================
# 2️⃣ API 호출
# ==========================
try:
    response = requests.get(URL)
    response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
except requests.exceptions.RequestException as e:
    st.error(f"⚠️ API 요청 실패: {e}")
    st.stop()

# ==========================
# 3️⃣ XML 파싱
# ==========================
try:
    root = ET.fromstring(response.content)
    rows = root.findall(".//row")
except ET.ParseError:
    st.error("⚠️ XML 파싱 중 오류 발생")
    st.stop()

# ==========================
# 4️⃣ 데이터 정리
# ==========================
data = []
for r in rows:
    row_dict = {
        "교육 콘텐츠 제목": r.findtext("CONTENT_TITLE", default=""),
        "콘텐츠 유형": r.findtext("CONTENT_TYPE", default=""),
        "대상": r.findtext("TARGET_AUDIENCE", default=""),
        "제공기관": r.findtext("CONTENT_PROVIDER", default=""),
        "콘텐츠 링크": r.findtext("CONTENT_URL", default=""),
        "내용 설명": r.findtext("CONTENT_DESC", default=""),
        "등록일": r.findtext("CREATE_DATE", default="")
    }
    data.append(row_dict)

df = pd.DataFrame(data)

# ==========================
# 5️⃣ 데이터 출력
# ==========================
if df.empty:
    st.warning("⚠️ API에서 데이터가 없습니다.")
else:
    st.dataframe(df)
