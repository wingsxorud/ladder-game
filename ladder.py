import streamlit as st
import random

def create_ladder_game():
    st.set_page_config(page_title="인생은 복불복! 사다리 타기", layout="centered")
    
    st.title("RollerCoaster 🎢 사다리 타기")
    st.write("행님, 인원수 정하고 이름이랑 항목만 넣으쇼!")

    # 1. 인원 설정
    num_people = st.number_input("참여 인원 (2~10명)", min_value=2, max_value=10, value=3)

    # 2. 이름 및 항목 입력 레이아웃
    col1, col2 = st.columns(2)
    names = []
    items = []

    with col1:
        st.subheader("👤 이름")
        for i in range(num_people):
            names.append(st.text_input(f"사람 {i+1}", value=f"참가자{i+1}", key=f"name_{i}"))

    with col2:
        st.subheader("🎁 항목")
        for i in range(num_people):
            items.append(st.text_input(f"항목 {i+1}", value=f"결과{i+1}", key=f"item_{i}"))

    # 3. 사다리 타기 실행 버튼
    if st.button("운명의 사다리 타기 시작!"):
        if len(set(names)) != len(names):
            st.error("이름이 중복되면 헷갈려요, 행님!")
            return

        # 랜덤 매칭 로직
        shuffled_items = items.copy()
        random.shuffle(shuffled_items)
        results = dict(zip(names, shuffled_items))

        with st.spinner('운명을 결정하는 중...'):
            import time
            time.sleep(1.2) # 약간의 긴장감을 위한 대기 시간

        st.success("🎉 결과가 나왔습니다!")
        
        res_col1, res_col2 = st.columns(2)
        for name, result in results.items():
            with res_col1:
                st.info(f"**{name}**")
            with res_col2:
                st.warning(f"👉 {result}")

        st.balloons()

if __name__ == "__main__":
    create_ladder_game()