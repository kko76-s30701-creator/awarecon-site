import streamlit as st
import requests
import xml.etree.ElementTree as ET
import pandas as pd

# 1️⃣ API 요청 정보
api_url = "https://apis.data.go.kr/B552583/awarecon"
service_key = "5b4b3917e3b9a6a48763aa2cd0ca266d6ee935d8be01ab9728fb2b77a7f67935"

params = {
    "ServiceKey": service_key,
    "pageNo": "1",
    "numOfRows": "100"
}

# 2️⃣ API 호출
response = requests.get(api_url, params=params)
if response.status_code != 200:
    st.error("API 요청 실패")
    st.stop()

# 3️⃣ XML 파싱
root = ET.fromstring(response.text)
rows = root.findall(".//row")

# 4️⃣ 데이터프레임 생성
data = []
for r in rows:
    row_dict = {
        "제목": r.findtext("CONTENT_TITLE", ""),
        "유형": r.findtext("CONTENT_TYPE", ""),
        "대상": r.findtext("TARGET_AUDIENCE", ""),
        "제공기관": r.findtext("CONTENT_PROVIDER", ""),
        "링크": r.findtext("CONTENT_URL", ""),
        "설명": r.findtext("CONTENT_DESC", ""),
        "등록일": r.findtext("CREATE_DATE", "")
    }
    data.append(row_dict)

df = pd.DataFrame(data)

# 5️⃣ 데이터 없으면 경고
if df.empty:
    st.warning("⚠️ API에서 데이터가 없습니다.")
    st.stop()

# 6️⃣ 검색 및 표시
search_term = st.text_input("제목/대상 검색")
if search_term:
    df = df[df["제목"].str.contains(search_term) | df["대상"].str.contains(search_term)]

st.dataframe(df)
