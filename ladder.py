import streamlit as st
import random
import time

def create_ladder_game():
    st.set_page_config(page_title="인생은 복불복!", layout="centered")
    
    st.title("🎢 쪼는 맛이 있는 사다리 타기")
    st.write("행님, 과연 결과는 어디로 갈까요?")

    num_people = st.number_input("참여 인원 (2~10명)", min_value=2, max_value=10, value=3)

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

    if st.button("운명의 사다리 내려가기! 👇"):
        if len(set(names)) != len(names):
            st.error("이름이 중복되면 안 됩니다, 행님!")
            return

        # 1. 랜덤 매칭 생성
        shuffled_items = items.copy()
        random.shuffle(shuffled_items)
        results = dict(zip(names, shuffled_items))

        # 2. 긴장감 연출 (Progress Bar)
        st.divider()
        st.subheader("🧗 사다리 타는 중...")
        
        # 이름별로 하나씩 결과를 공개하는 연출
        for i, name in enumerate(names):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 사다리 타고 내려가는 로딩 연출
            for percent_complete in range(0, 101, 20):
                time.sleep(0.2) # 속도 조절 (더 느리게 하면 더 쫄림)
                progress_bar.progress(percent_complete)
                status_text.text(f"{name}님이 사다리를 내려가는 중... {percent_complete}%")
            
            # 해당 사람의 결과 공개
            st.write(f"✅ **{name}** 님은? 👉 **{results[name]}**")
            status_text.empty() # 상태 메시지 삭제
            time.sleep(0.5) # 다음 사람으로 넘어가기 전 휴식

        # 3. 최종 결과 총정리
        st.divider()
        st.success("🎉 모든 결과가 확정되었습니다!")
        st.balloons()
        
        with st.expander("한눈에 보기"):
            for n, r in results.items():
                st.write(f"**{n}** : {r}")

if __name__ == "__main__":
    create_ladder_game()
