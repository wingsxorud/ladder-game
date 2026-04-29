import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(page_title="네이버 사다리", layout="centered")
    st.title("🎢 네이버 스타일 사다리 타기")

    # 1. 세션 상태 초기화
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # 2. 입력 섹션 (Form 사용으로 버튼 신뢰도 상승)
    if not st.session_state.game_started:
        st.write("인원과 이름을 입력한 후 생성 버튼을 누르쇼!")
        
        # 폼으로 감싸서 데이터 전송을 확실하게 함
        with st.form("ladder_setup"):
            num_p = st.number_input("참여 인원", min_value=2, max_value=8, value=4)
            
            col1, col2 = st.columns(2)
            input_names = []
            input_items = []
            
            for i in range(int(num_p)):
                name = col1.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"n_{i}")
                item = col2.text_input(f"결과 {i+1}", value=f"결과{i+1}", key=f"i_{i}")
                input_names.append(name)
                input_items.append(item)
            
            submitted = st.form_submit_button("🚀 사다리 생성 및 시작!")
            
            if submitted:
                # 데이터 정제 (문자열로 강제 변환)
                clean_names = [str(n) for n in input_names]
                clean_items = [str(it) for it in input_items]
                
                # 사다리 가로줄 생성
                new_lines = []
                for _ in range(12):
                    row = [0] * (int(num_p) - 1)
                    for j in range(int(num_p) - 1):
                        if random.random() > 0.6 and (j == 0 or row[j-1] == 0):
                            row[j] = 1
                    new_lines.append(row)
                
                # 세션에 값 저장
                st.session_state.ladder_data = new_lines
                st.session_state.names = clean_names
                st.session_state.items = clean_items
                st.session_state.num_people = int(num_p)
                st.session_state.game_started = True
                st.rerun()

    # 3. 게임 실행 섹션 (사다리 표시)
    else:
        # 데이터 로드 및 JSON 직렬화
        l_json = json.dumps(st.session_state.ladder_data)
        n_json = json.dumps(st.session_state.names, ensure_ascii=False)
        i_json = json.dumps(st.session_state.items, ensure_ascii=False)
        p_count = st.session_state.num_people

        html_code = f"""
        <div style="text-align:center;">
            <p style="font-size: 14px; color: #888;">이름을 클릭하면 사다리를 타고 내려갑니다</p>
            <canvas id="ladderCanvas" width="550" height="600" style="cursor:pointer; background:#fff; border:1px solid #eee; border-radius:15px;"></canvas>
        </div>
        <script>
        (function() {{
            const canvas = document.getElementById('ladderCanvas');
            const ctx = canvas.getContext('2d');
            const lines = {l_json};
            const names = {n_json};
            const items = {i_json};
            const numP = {p_count};
            
            const margin = 60;
            const spacing = (canvas.width - margin * 2) / (numP - 1);
            const rowH = (canvas.height - 160) / lines.length;

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.strokeStyle = '#ddd';
                ctx.lineWidth = 3;
                ctx.font = 'bold 15px sans-serif';
                ctx.textAlign = 'center';

                for(let i=0; i<numP; i++) {{
                    let x = margin + i * spacing;
                    ctx.beginPath(); ctx.moveTo(x, 80); ctx.lineTo(x, canvas.height - 80); ctx.stroke();
                    ctx.fillStyle = '#333';
                    ctx.fillText(names[i], x, 60);
                    ctx.fillText(items[i], x, canvas.height - 45);
                }}

                lines.forEach((row, rIdx) => {{
                    row.forEach((has, cIdx) => {{
                        if(has) {{
                            let x = margin + cIdx * spacing;
                            let y = 80 + (rIdx + 0.5) * rowH;
                            ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + spacing, y); ctx.stroke();
                        }}
                    }});
                }});
            }}

            function movePath(pIdx) {{
                let curX = pIdx;
                let step = 0;
                ctx.strokeStyle = '#FF4B4B';
                ctx.lineWidth = 6;
                function stepMove() {{
                    if (step >= lines.length) return;
                    let sX = margin + curX * spacing;
                    let sY = 80 + step * rowH;
                    let mY = sY + rowH / 2;
                    ctx.beginPath(); ctx.moveTo(sX, sY); ctx.lineTo(sX, mY);
                    if(curX > 0 && lines[step][curX-1]) {{
                        curX--; ctx.lineTo(margin + curX * spacing, mY);
                    }} else if(curX < numP - 1 && lines[step][curX]) {{
                        curX++; ctx.lineTo(margin + curX * spacing, mY);
                    }}
                    ctx.lineTo(margin + curX * spacing, sY + rowH); ctx.stroke();
                    step++;
                    setTimeout(stepMove, 70);
                }}
                stepMove();
            }}

            canvas.onclick = (e) => {{
                const r = canvas.getBoundingClientRect();
                const x = e.clientX - r.left;
                for(let i=0; i<numP; i++) {{
                    if(Math.abs(x - (margin + i * spacing)) < 30) {{ movePath(i); break; }}
                }}
            }};
            draw();
        }})();
        </script>
        """
        components.html(html_code, height=660)

        if st.button("🔄 처음부터 다시 설정"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
