import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET

st.set_page_config(page_title="직장 내 인식개선 교육 콘텐츠 현황", layout="wide")
st.title("한국장애인고용공단 - 직장 내 인식개선 교육 콘텐츠 현황")

# 🔹 XML 샘플 파일 경로
XML_FILE = "data/awarecon_sample.xml"

# 🔹 XML 읽기
try:
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
except Exception as e:
    st.error(f"⚠️ XML 파일 읽기 실패: {e}")
    st.stop()

# 🔹 데이터 파싱
data = []
rows = root.findall(".//row")  # XML 구조에 따라 row 경로 수정 가능
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

if df.empty:
    st.warning("⚠️ XML 데이터가 없습니다.")
    st.stop()

# 🔹 테이블 출력
st.dataframe(df, use_container_width=True)
