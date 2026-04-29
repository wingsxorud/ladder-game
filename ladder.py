import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(page_title="네이버 스타일 사다리", layout="centered")
    
    st.title("🎢 네이버 스타일 사다리 타기")

    # 1. 세션 상태 초기화 (에러 방지를 위해 미리 선언)
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'names' not in st.session_state:
        st.session_state.names = []
    if 'items' not in st.session_state:
        st.session_state.items = []

    # 2. 입력 섹션
    if not st.session_state.game_started:
        st.write("인원과 이름을 입력한 후, '사다리 생성'을 누르쇼 행님!")
        num_people = st.number_input("참여 인원", min_value=2, max_value=8, value=4)
        
        col1, col2 = st.columns(2)
        
        tmp_names = []
        tmp_items = []
        
        for i in range(num_people):
            n = col1.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"n_in_{i}")
            it = col2.text_input(f"결과 {i+1}", value=f"결과{i+1}", key=f"i_in_{i}")
            tmp_names.append(n)
            tmp_items.append(it)

        if st.button("🚀 사다리 생성 및 시작!"):
            # 사다리 가로줄 무작위 생성
            lines = []
            for _ in range(12):
                row = [0] * (num_people - 1)
                for j in range(num_people - 1):
                    if random.random() > 0.6 and (j == 0 or row[j-1] == 0):
                        row[j] = 1
                lines.append(row)
            
            # 여기서 데이터를 '값'으로만 강제 추출해서 저장 (JSON 에러 원천 봉쇄)
            st.session_state.ladder_data = lines
            st.session_state.names = [str(x) for x in tmp_names]
            st.session_state.items = [str(x) for x in tmp_items]
            st.session_state.num_people = int(num_people)
            st.session_state.game_started = True
            st.rerun()

    # 3. 게임 실행 섹션
    else:
        # 이미 값으로 변환된 세션 데이터를 사용
        try:
            ladder_json = json.dumps(st.session_state.ladder_data)
            names_json = json.dumps(st.session_state.names, ensure_ascii=False)
            items_json = json.dumps(st.session_state.items, ensure_ascii=False)
            num_people = st.session_state.num_people
        except Exception as e:
            st.error(f"데이터 변환 중 에러 발생: {e}")
            if st.button("초기화 후 다시 시도"):
                st.session_state.game_started = False
                st.rerun()
            return

        html_code = f"""
        <div style="text-align:center; font-family: sans-serif;">
            <p style="color: #666;">이름을 클릭하면 사다리를 타고 내려갑니다!</p>
            <canvas id="ladderCanvas" width="550" height="600" style="cursor:pointer; background:#f9f9f9; border-radius:10px;"></canvas>
        </div>

        <script>
        (function() {{
            const canvas = document.getElementById('ladderCanvas');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            const lines = {ladder_json};
            const names = {names_json};
            const items = {items_json};
            const numPeople = {num_people};
            
            const margin = 60;
            const spacing = (canvas.width - margin * 2) / (numPeople - 1);
            const rowHeight = (canvas.height - 160) / lines.length;

            function drawLadder() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.strokeStyle = '#ccc';
                ctx.lineWidth = 3;
                ctx.font = 'bold 16px Arial';
                ctx.textAlign = 'center';

                for(let i=0; i<numPeople; i++) {{
                    let x = margin + i * spacing;
                    ctx.beginPath();
                    ctx.moveTo(x, 80);
                    ctx.lineTo(x, canvas.height - 80);
                    ctx.stroke();
                    
                    ctx.fillStyle = '#333';
                    ctx.fillText(names[i], x, 60);
                    ctx.fillText(items[i], x, canvas.height - 50);
                }}

                lines.forEach((row, rowIndex) => {{
                    row.forEach((hasLine, colIndex) => {{
                        if(hasLine) {{
                            let x = margin + colIndex * spacing;
                            let y = 80 + (rowIndex + 0.5) * rowHeight;
                            ctx.beginPath();
                            ctx.moveTo(x, y);
                            ctx.lineTo(x + spacing, y);
                            ctx.stroke();
                        }}
                    }});
                }});
            }}

            function animate(playerIdx) {{
                let currentXIdx = playerIdx;
                let step = 0;
                ctx.strokeStyle = '#FF4B4B';
                ctx.lineWidth = 6;
                ctx.lineCap = 'round';

                function move() {{
                    if (step >= lines.length) return;
                    
                    let startX = margin + currentXIdx * spacing;
                    let startY = 80 + step * rowHeight;
                    let midY = startY + rowHeight / 2;
                    let endY = startY + rowHeight;

                    ctx.beginPath();
                    ctx.moveTo(startX, startY);
                    ctx.lineTo(startX, midY);
                    
                    if(currentXIdx > 0 && lines[step][currentXIdx-1]) {{
                        currentXIdx--;
                        ctx.lineTo(margin + currentXIdx * spacing, midY);
                    }} else if(currentXIdx < numPeople - 1 && lines[step][currentXIdx]) {{
                        currentXIdx++;
                        ctx.lineTo(margin + currentXIdx * spacing, midY);
                    }}
                    
                    ctx.lineTo(margin + currentXIdx * spacing, endY);
                    ctx.stroke();
                    
                    step++;
                    setTimeout(move, 80);
                }}
                move();
            }}

            canvas.onclick = (e) => {{
                const rect = canvas.getBoundingClientRect();
                const x = e.clientX - rect.left;
                for(let i=0; i<numPeople; i++) {{
                    let colX = margin + i * spacing;
                    if(Math.abs(x - colX) < 30) {{
                        animate(i);
                        break;
                    }}
                }}
            }};

            drawLadder();
        }})();
        </script>
        """

        components.html(html_code, height=650)

        if st.button("🔄 다시 설정하기"):
            st.session_state.game_started = False
            st.rerun()

if __name__ == "__main__":
    main()
