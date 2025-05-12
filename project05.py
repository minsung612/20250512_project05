import streamlit as st
from datetime import date
import os
from PIL import Image

# 비밀번호 설정
correct_password = "0124"
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

# 로그인 함수
def login():
    name = st.text_input("이름을 입력하세요")
    password = st.text_input("비밀번호를 입력하세요", type="password")
    if st.button("로그인"):
        if password == correct_password and name.strip() != "":
            st.session_state["authenticated"] = True
            st.session_state["username"] = name.strip()
            st.rerun()
        elif name.strip() == "":
            st.error("이름을 입력해주세요.")
        else:
            st.error("비밀번호가 틀렸습니다.")

# 로그인 페이지
if not st.session_state["authenticated"]:
    st.title("🔐 로그인")
    login()

# 로그인 이후 페이지
else:
    # 로그인한 사용자 표시
    st.sidebar.success(f"👤 현재 로그인한 사용자: {st.session_state['username']}")

    # 종목 클래스 정의
    class Nasdaq:
        registry = []

        def __init__(self, name, wantcost, purpose, earnings_date=None):
            self.name = name
            self.wantcost = wantcost
            self.purpose = purpose
            self.earnings_date = earnings_date
            Nasdaq.registry.append(self)

        def display_info(self):
            st.write(f"💰 **{self.name}** 매수 희망가: **{self.wantcost} 달러**")
            st.write(f"📈 목표 매도가: **{self.purpose} 달러**")
            if self.earnings_date:
                days_left = (self.earnings_date - date.today()).days
                status = (
                    f"D-{days_left}" if days_left >= 0 else "실적 발표일이 지났습니다."
                )
                st.write(f"🗓️ 실적 발표일: {self.earnings_date} ({status})")
            else:
                st.write("❌ 실적 발표일 정보 없음")

        def handle_image(self):
            image_filename = f"{self.name}.png"
            if os.path.exists(image_filename):
                st.image(image_filename, width=200)
            else:
                st.write("🖼️ 이미지가 없습니다.")
                uploaded = st.file_uploader(
                    f"{self.name} 이미지 업로드", type=["png", "jpg", "jpeg"], key=self.name
                )
                if uploaded:
                    image = Image.open(uploaded)
                    image.save(image_filename)
                    st.success("이미지 저장 완료! 새로고침 시 표시됩니다.")
                    st.rerun()

        @staticmethod
        def find_by_name(name):
            return next((s for s in Nasdaq.registry if s.name == name), None)

    # 종목 초기화 (한 번만 실행됨)
    if not Nasdaq.registry:
        Nasdaq("테슬라", 280, 300, date(2025, 7, 23))
        Nasdaq("애플", 197, 250, date(2025, 8, 1))
        Nasdaq("엔비디아", 117, 200, date(2025, 5, 29))
        Nasdaq("아이온큐", 31, 45, date(2025, 8, 6))

    # 페이지 선택
    page = st.sidebar.radio("페이지를 선택하세요", ["📘 종목 조회", "📄 보유 종목 리스트"])

    if page == "📘 종목 조회":
        st.title("📊 나스닥 종목 정보 조회")
        stock_name = st.text_input("종목명을 입력하세요 (예: 테슬라, 애플, 엔비디아)")
        if stock_name:
            stock = Nasdaq.find_by_name(stock_name.strip())
            if stock:
                stock.display_info()
            else:
                st.warning("저장된 정보가 없습니다. 정확한 종목명을 입력해주세요.")
    else:
        st.title("📋 보유 중인 종목 리스트")
        for stock in Nasdaq.registry:
            st.subheader(f"📌 {stock.name}")
            stock.handle_image()
            st.markdown("---")
