import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET

st.set_page_config(page_title="경기도 장애인복지관 운영 프로그램", layout="wide")
st.title("가톨릭대학 주변 장애인복지관 프로그램 🌟")
st.markdown("장애인복지관에서 운영하는 프로그램 정보를 확인할 수 있습니다. 프로그램들 중 가톨릭대학교에서 진행할 수 있을만한 프로그램을 추천해드립니다. 📌아래 내용은 자동 업데이트 됩니다.")

# ==========================
# 📌 복지관 홈페이지 매핑
# ==========================
homepages = {
    "양주시장애인종합복지관": "http://www.yjwel.or.kr/",
    "용인시처인장애인종합복지관": "https://www.heart4u.or.kr/",
    "호매실장애인종합복지관": "https://hmsrehab.or.kr/",
    "수원시장애인종합복지관": "https://www.suwonrehab.or.kr/",
    "군포시장애인종합복지관": "https://gunporehab.or.kr/",
    "시흥시장애인종합복지관": "https://shwcd.org/",
    "용인시수지장애인복지관": "http://www.sujiable.or.kr/",
    "김포시장애인복지관": "https://www.gimpowel.or.kr/",
    "남양주시장애인복지관": "https://nyjwel.or.kr/",
    "성남시장애인종합복지관": "https://www.rehab21.or.kr/",
    "과천시장애인복지관": "https://www.happyseed.or.kr/",
    "오산시하나울복지센터": "https://hanaul.or.kr/",
    "오산장애인종합복지관": "https://osrc.or.kr/index.php",
    "희망나래장애인복지관": "https://uwnare.or.kr/main/main.php",
    "부천시장애인종합복지관": "https://www.pchand.or.kr/",
    "파주시장애인종합복지관": "http://www.pajurehab.or.kr/",
    "하남시장애인복지관": "http://www.hanamrehab.or.kr/",
    "가평군장애인복지관": "http://www.gapyeongjb.or.kr/gboard/html/index.html",
    "양평군장애인복지관": "https://www.yprehab.or.kr/",
    "광명장애인종합복지관": "https://withlight.or.kr/"
}

# ==========================
# 1️⃣ API 호출
# ==========================
API_KEY = "c9955392cc82450eb32d33c996ad1a9a"
URL = f"https://openapi.gg.go.kr/DspsnCmwelfctOpertProg?KEY={API_KEY}&Type=xml&pIndex=1&pSize=1000"

with st.spinner("📡 장애인복지관 프로그램 데이터를 불러오는 중입니다..."):
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
    name = r.findtext("CMWELFCT_NM_INFO", default="")  # 복지관명

    homepage = homepages.get(name, "")  # 매핑된 홈페이지 주소 불러오기

    row_dict = {
        "이용대상상세조건(장애유형)": r.findtext("USE_TARGET_OBSTCL_TYPE_COND", default=""),
        "구분": r.findtext("PROG_DIV_NM", default=""),
        "상세구분": r.findtext("DETAIL_DIV_NM", default=""),
        "프로그램명": r.findtext("PROG_TITLE", default=""),
        "프로그램내용": r.findtext("PROG_CONT", default=""),
        "복지관명": name,
        "소재지도로명주소": r.findtext("REFINE_ROADNM_ADDR", default=""),
        "데이터기준일자": r.findtext("DATA_STD_DE", default=""),
        "홈페이지": homepage
    }

    data.append(row_dict)

df = pd.DataFrame(data)

if df.empty:
    st.warning("⚠️ API에서 데이터가 없습니다.")
    st.stop()

# 홈페이지 컬럼을 클릭 가능한 Markdown 링크로 변환
df["홈페이지"] = df["홈페이지"].apply(
    lambda x: f"[🌐 바로가기]({x})" if x else ""
)

# ==========================
# 4️⃣ 전체 프로그램 표시
# ==========================
st.subheader("장애인복지관 프로그램 현황(학생 참고용)")
st.markdown("학교 주변 장애인 복지관에서 진행하는 프로그램 현황을 알려드립니다.")
st.dataframe(df.reset_index(drop=True))

# ==========================
# 5️⃣ 추천 프로그램
# ==========================
recommended_df = df[df["구분"] == "교육"]
st.subheader("가톨릭대 프로그램 제안 (교직원 참고용)")
st.markdown("학교 주변 장애인 복지관에서 진행하는 프로그램들 중 가톨릭대에서 진행할 수 있는 프로그램을 추천드립니다.")
st.dataframe(recommended_df.reset_index(drop=True))
