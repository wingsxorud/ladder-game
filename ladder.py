import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(page_title="네이버 스타일 사다리", layout="centered")
    
    st.title("🎢 네이버 스타일 사다리 타기")
    st.write("인원과 이름을 입력한 후, '사다리 생성'을 누르쇼 행님!")

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # 1. 입력 섹션
    if not st.session_state.game_started:
        num_people = st.number_input("참여 인원", min_value=2, max_value=8, value=4)
        
        col1, col2 = st.columns(2)
        
        # 여기서 리스트를 미리 만들어서 값을 저장합니다.
        names_input = []
        items_input = []
        
        for i in range(num_people):
            n = col1.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"name_in_{i}")
            it = col2.text_input(f"결과 {i+1}", value=f"결과{i+1}", key=f"item_in_{i}")
            names_input.append(n)
            items_input.append(it)

        if st.button("🚀 사다리 생성 및 시작!"):
            # 사다리 가로줄 무작위 생성
            lines = []
            for _ in range(12):
                row = [0] * (num_people - 1)
                for j in range(num_people - 1):
                    if random.random() > 0.6 and (j == 0 or row[j-1] == 0):
                        row[j] = 1
                lines.append(row)
            
            # 중요: 객체가 아닌 '값(문자열)'만 저장되도록 확정
            st.session_state.ladder_data = lines
            st.session_state.names = [str(x) for x in names_input]
            st.session_state.items = [str(x) for x in items_input]
            st.session_state.num_people = num_people
            st.session_state.game_started = True
            st.rerun()

    # 2. 게임 실행 섹션
    else:
        # JSON 직렬화 에러 방지를 위해 확실히 문자열로 변환
        ladder_json = json.dumps(st.session_state.ladder_data)
        names_json = json.dumps(st.session_state.names, ensure_ascii=False)
        items_json = json.dumps(st.session_state.items, ensure_ascii=False)
        num_people = st.session_state.num_people

        html_code = f"""
        <div style="text-align:center; font-family: sans-serif;">
            <p style="color: #666;">이름을 클릭하면 사다리를 타고 내려갑니다!</p>
            <canvas id="ladderCanvas" width="550" height="600" style="cursor:pointer; background:#f9f9f9; border-radius:10px;"></canvas>
        </div>

        <script>
        const canvas = document.getElementById('ladderCanvas');
        const ctx = canvas.getContext('2d');
        const lines = {ladder_json};
