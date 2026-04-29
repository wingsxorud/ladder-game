import streamlit as st
import random
import time

def create_interactive_ladder():
    st.set_page_config(page_title="클릭! 사다리 타기", layout="centered")
    
    st.title("🎢 클릭 사다리 타기")
    st.write("행님, 이름을 클릭해서 운명을 하나씩 확인하쇼!")

    # 1. 입력 섹션
    if 'game_ready' not in st.session_state:
        st.session_state.game_ready = False

    if not st.session_state.game_ready:
        num_people = st.number_input("참여 인원", min_value=2, max_value=10, value=3)
        
        col1, col2 = st.columns(2)
        with col1:
            names = [st.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"input_n_{i}") for i in range(num_people)]
        with col2:
            items = [st.text_input(f"항목 {i+1}", value=f"결과{i+1}", key=f"input_i_{i}") for i in range(num_people)]
            
        if st.button("사다리 생성하기"):
            # 데이터 섞기 및 초기화
            shuffled_items = items.copy()
            random.shuffle(shuffled_items)
            
            st.session_state.results = dict(zip(names, shuffled_items))
            st.session_state.revealed = {name: False for name in names}
            st.session_state.game_ready = True
            st.rerun()

    # 2. 게임 실행 섹션
    else:
        st.subheader("📍 누구의 결과를 확인해볼까요?")
        
        # 이름별로 버튼 생성
        cols = st.columns(len(st.session_state.results))
        
        for i, (name, result) in enumerate(st.session_state.results.items()):
            with cols[i]:
                # 이미 클릭한 경우 결과 표시, 아니면 버튼 표시
                if st.session_state.revealed[name]:
                    st.success(f"**{name}**")
                    st.write(f"👇")
                    st.warning(f"**{result}**")
                else:
                    if st.button(f"👤 {name}", key=f"btn_{name}"):
                        with st.spinner("내려가는 중..."):
                            time.sleep(1) # 사다리 타는 시간
                        st.session_state.revealed[name] = True
                        st.rerun()

        st.divider()
        if st.button("다시 시작하기"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

        # 전부 다 확인했으면 축하!
        if all(st.session_state.revealed.values()):
            st.balloons()
            st.write("🎉 모든 운명이 결정됐습니다, 행님!")

if __name__ == "__main__":
    create_interactive_ladder()
