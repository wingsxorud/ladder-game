import streamlit as st
import random
import time

def create_ladder_logic(num_people):
    # 사다리 가로줄 생성 (랜덤)
    ladder_steps = []
    for _ in range(10):  # 사다리 높이 10층
        row = [False] * (num_people - 1)
        for j in range(num_people - 1):
            if random.random() > 0.6: # 40% 확률로 가로줄 생성
                row[j] = True
        ladder_steps.append(row)
    return ladder_steps

def get_path(start_pos, ladder_steps):
    # 특정 위치에서 시작했을 때의 경로 추적
    current_pos = start_pos
    path = [current_pos]
    for row in ladder_steps:
        if current_pos > 0 and row[current_pos - 1]: # 왼쪽으로 가는 줄이 있다면
            current_pos -= 1
        elif current_pos < len(row) and row[current_pos]: # 오른쪽으로 가는 줄이 있다면
            current_pos += 1
        path.append(current_pos)
    return path

def main():
    st.set_page_config(page_title="클릭! 진짜 사다리 타기", layout="centered")
    st.title("🎢 진짜 선 타고 내려가는 사다리")

    if 'game_ready' not in st.session_state:
        st.session_state.game_ready = False

    # 1. 설정 단계
    if not st.session_state.game_ready:
        num_people = st.number_input("인원수", min_value=2, max_value=8, value=4)
        
        col1, col2 = st.columns(2)
        with col1:
            names = [st.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"n_{i}") for i in range(num_people)]
        with col2:
            items = [st.text_input(f"결과 {i+1}", value=f"결과{i+1}", key=f"i_{i}") for i in range(num_people)]

        if st.button("사다리판 생성하기"):
            st.session_state.num_people = num_people
            st.session_state.names = names
            st.session_state.items = items
            st.session_state.ladder_steps = create_ladder_logic(num_people)
            st.session_state.revealed = {i: False for i in range(num_people)}
            st.session_state.game_ready = True
            st.rerun()

    # 2. 게임 실행 단계
    else:
        # 사다리 모양 시각화 (간이 버전)
        st.subheader("🪜 사다리 맵")
        ladder_visual = ""
        for row in st.session_state.ladder_steps:
            line = "  |  "
            for step in row:
                line += "──" if step else "  "
                line += "  |  "
            ladder_visual += line + "\n"
        st.code(ladder_visual, language="text") # 사다리 모양 출력

        st.write("👇 이름을 클릭하면 사다리를 타고 내려갑니다!")
        
        cols = st.columns(st.session_state.num_people)
        for i in range(st.session_state.num_people):
            with cols[i]:
                if st.button(f"{st.session_state.names[i]}", key=f"btn_{i}"):
                    # 경로 계산 및 연출
                    path = get_path(i, st.session_state.ladder_steps)
                    final_idx = path[-1]
                    
                    with st.status(f"{st.session_state.names[i]}님 내려가는 중...", expanded=True) as status:
                        for step_idx, pos in enumerate(path):
                            time.sleep(0.2)
                            st.write(f"{step_idx}층 통과: {'  ' * pos}🏃")
                        status.update(label="도착 완료!", state="complete")
                    
                    st.session_state.revealed[i] = st.session_state.items[final_idx]

        # 결과 표시 영역
        st.divider()
        res_cols = st.columns(st.session_state.num_people)
        for i in range(st.session_state.num_people):
            with res_cols[i]:
                if st.session_state.revealed[i]:
                    st.success(f"**{st.session_state.revealed[i]}**")
                else:
                    st.info("?")

        if st.button("판 새로 짜기"):
            st.session_state.game_ready = False
            st.rerun()

if __name__ == "__main__":
    main()
