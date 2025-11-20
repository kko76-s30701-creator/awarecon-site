# site.py
import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from urllib.parse import quote

st.set_page_config(page_title="직장 내 인식개선 교육 콘텐츠 현황", layout="wide")

st.title("🏢 직장 내 인식개선 교육 콘텐츠 현황")

# 1️⃣ 사용자 설정
service_key = "5b4b3917e3b9a6a48763aa2cd0ca266d6ee935d8be01ab9728fb2b77a7f67935"
service_key_encoded = quote(service_key)  # 인증키 URL 인코딩

page_no = 1
num_of_rows = 100
response_type = "xml"

# 2️⃣ API 요청 URL
url = f"https://apis.data.go.kr/B552583/awarecon?serviceKey={service_key_encoded}&pageNo={page_no}&numOfRows={num_of_rows}&type={response_type}"

# 3️⃣ API 요청
try:
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"⚠️ API 요청 실패: HTTP {response.status_code}")
        st.stop()
except Exception as e:
    st.error(f"⚠️ API 요청 중 오류 발생: {e}")
    st.stop()

# 4️⃣ XML 파싱
try:
    root = ET.fromstring(response.content)
    items = root.findall(".//item")
    data = []
    for r in items:
        row_dict = {
            "교육기관명": r.findtext("INSTT_NM", default=""),
            "교육명": r.findtext("EDU_NM", default=""),
            "교육내용": r.findtext("EDU_CN", default=""),
            "주소": r.findtext("EDU_ADDR", default=""),
            "담당자": r.findtext("EDU_RPRSNTV_NM", default=""),
            "연락처": r.findtext("EDU_TELNO", default=""),
        }
        data.append(row_dict)
except Exception as e:
    st.error(f"⚠️ 데이터 처리 중 오류 발생: {e}")
    st.stop()

df = pd.DataFrame(data)

if df.empty:
    st.warning("⚠️ API에서 데이터가 없습니다.")
    st.stop()

# 5️⃣ 전체 데이터 표시
st.dataframe(df, use_container_width=True)
