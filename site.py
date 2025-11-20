import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET

# ==========================
# 0️⃣ Streamlit 페이지 설정
# ==========================
st.set_page_config(page_title="경기도 장애인 복지관 프로그램", layout="wide")
st.title("가톨릭대 주변 장애인 복지관 운영 프로그램 🌟")
st.markdown("장애인 복지관 프로그램 정보를 확인하고, 성인용 프로그램과 학교에서 활용 가능한 프로그램을 추천합니다. 데이터는 자동 업데이트 됩니다.")

# ==========================
# 1️⃣ API 호출
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
URL = f"https://openapi.gg.go.kr/DspsnCmwelfctOpertProg?KEY={API_KEY}&Type=xml&pIndex=1&pSize=1000"

try:
    response = requests.get(URL)
    response.raise_for_status()
except Exception as e:
    st.error(f"⚠️ API 요청 실패: {e}")
    st.stop()

# ==========================
# 2️⃣ XML 파싱
# ==========================
try:
    root = ET.fromstring(response.content)
    rows = root.findall(".//row")
except Exception as e:
    st.error(f"⚠️ XML 파싱 오류: {e}")
    st.stop()

# ==========================
# 3️⃣ 데이터프레임 생성
# ==========================
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

# ==========================
# 4️⃣ 사이드바 필터
# ==========================
st.sidebar.header("필터 설정")
age_filter = st.sidebar.checkbox("성인용 프로그램만 보기", value=True)
if age_filter:
    df = df[df["이용대상상세조건(연령제한)"].str.contains("성인", na=False)]

category_filter = st.sidebar.multiselect(
    "구분 선택",
    options=df["구분"].unique(),
    default=df["구분"].unique()
)
df = df[df["구분"].isin(category_filter)]

# ==========================
# 5️⃣ 추천 프로그램 (학교 활용용)
# ==========================
st.header("📌 교직원/학생 참고용 추천 프로그램")
school_df = df[
    (df["구분"].str.contains("교육|체험|워크숍", na=False))
]

if not school_df.empty:
    st.dataframe(school_df.reset_index(drop=True))
else:
    st.info("추천할 프로그램이 없습니다.")

# ==========================
# 6️⃣ 전체 데이터 테이블
# ==========================
st.header("📋 전체 프로그램 목록")
st.dataframe(df.reset_index(drop=True))
