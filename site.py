# site.py
import streamlit as st
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from urllib.parse import quote

# 1️⃣ 앱 제목
st.title("한국장애인고용공단 직장 내 인식개선 교육 콘텐츠 현황")

# 2️⃣ API 정보
service_key = "5b4b3917e3b9a6a48763aa2cd0ca266d6ee935d8be01ab9728fb2b77a7f67935"
encoded_key = quote(service_key)  # URL 인코딩
page_no = 1
num_of_rows = 20  # 한 번에 가져올 항목 수
api_url = f"https://apis.data.go.kr/B552583/awarecon?serviceKey={encoded_key}&pageNo={page_no}&numOfRows={num_of_rows}&type=xml"

st.write("API 호출 중...")

# 3️⃣ API 요청
try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()  # 오류 발생 시 예외
except Exception as e:
    st.error(f"⚠️ API 요청 실패: {e}")
    st.stop()

# 4️⃣ XML 파싱
try:
    root = ET.fromstring(response.text)
    items = root.findall(".//item")

    if not items:
        st.warning("⚠️ API에서 데이터가 없습니다.")
        st.stop()

    data = []
    for i in items:
        row = {
            "콘텐츠명": i.findtext("CONT_NM", default=""),
            "교육대상": i.findtext("EDU_TGT", default=""),
            "제공기관": i.findtext("PROV_INSTT_NM", default=""),
            "교육형태": i.findtext("EDU_FORM", default=""),
            "교육시간(분)": i.findtext("EDU_TM", default="")
        }
        data.append(row)

    df = pd.DataFrame(data)

except Exception as e:
    st.error(f"⚠️ 데이터 처리 중 오류 발생: {e}")
    st.stop()

# 5️⃣ 데이터 출력
st.subheader("교육 콘텐츠 현황")
st.dataframe(df)
