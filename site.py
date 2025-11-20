# site.py
import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET

# -----------------------------
# 1️⃣ 페이지 설정
# -----------------------------
st.set_page_config(page_title="경기도 장애인복지관 운영 프로그램", layout="wide")
st.title("가톨릭대 학생용 장애인복지관 프로그램 🌟")
st.markdown("""
경기도 내 장애인복지관에서 운영하는 다양한 프로그램 정보를 실시간으로 제공합니다.
학생들은 본 정보를 참고해 참여 가능 프로그램을 확인할 수 있습니다.
""")

# -----------------------------
# 2️⃣ API 호출
# -----------------------------
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
URL = f"https://openapi.gg.go.kr/DspsnCmwelfctOpertProg?KEY={API_KEY}&Type=xml&pIndex=1&pSize=1000"

try:
    response = requests.get(URL)
    response.raise_for_status()
except Exception as e:
    st.error(f"⚠️ API 요청 실패: {e}")
    st.stop()

# -----------------------------
# 3️⃣ XML 파싱
# -----------------------------
try:
    root = ET.fromstring(response.content)
    rows = root.findall(".//row")
except Exception as e:
    st.error(f"⚠️ XML 파싱 오류: {e}")
    st.stop()

# -----------------------------
# 4️⃣ 데이터프레임 생성
# -----------------------------
data = []
for r in rows:
    row_dict = {
        "장애유형": r.findtext("USE_TARGET_OBSTCL_TYPE_COND", ""),
        "연령제한": r.findtext("USE_TARGET_AGE_LIMITN_COND", ""),
        "기타조건": r.findtext("USE_TARGET_ETC_COND", ""),
        "구분": r.findtext("PROG_DIV_NM", ""),
        "상세구분": r.findtext("DETAIL_DIV_NM", ""),
        "프로그램명": r.findtext("PROG_TITLE", ""),
        "프로그램내용": r.findtext("PROG_CONT", ""),
        "이용시간": r.findtext("USE_TM_INFO", "")
    }
    data.append(row_dict)

df = pd.DataFrame(data)

if df.empty:
    st.warning("⚠️ API에서 데이터가 없습니다.")
    st.stop()

# -----------------------------
# 5️⃣ 필터링 옵션
# -----------------------------
st.sidebar.header("필터 선택")
filter_obstcl = st.sidebar.multiselect("장애유형", options=df["장애유형"].unique())
filter_age = st.sidebar.multiselect("연령제한", options=df["연령제한"].unique())
filter_div = st.sidebar.multiselect("구분", options=df["구분"].unique())

filtered_df = df.copy()
if filter_obstcl:
    filtered_df = filtered_df[filtered_df["장애유형"].isin(filter_obstcl)]
if filter_age:
    filtered_df = filtered_df[filtered_df["연령제한"].isin(filter_age)]
if filter_div:
    filtered_df = filtered_df[filtered_df["구분"].isin(filter_div)]

# -----------------------------
# 6️⃣ 최신 프로그램 하이라이트
# -----------------------------
st.subheader("✨ 최신 등록 프로그램 5개")
st.dataframe(filtered_df.head(5).reset_index(drop=True))

-------------------------------
# 성인용만 필터링
adult_df = filtered_df[filtered_df["연령제한"].str.contains("성인", na=False)]
school_df = adult_df[
    (adult_df["구분"].str.contains("교육|체험|워크숍", na=False)) &
    (adult_df["이용시간"].str.contains("월|화|수|목|금", na=False))
]


# -----------------------------
# 7️⃣ 전체 데이터 테이블
# -----------------------------
st.subheader("전체 프로그램 목록")
st.dataframe(filtered_df.reset_index(drop=True))
