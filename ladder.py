import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(page_title="네이버 사다리", layout="centered")
    st.title("🌈 컬러풀 사다리 타기")

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # 1. 입력 섹션
    if not st.session_state.game_started:
        with st.form("ladder_form"):
            num_p = st.number_input("참여 인원", min_value=2, max_value=8, value=4)
            col1, col2 = st.columns(2)
            raw_names, raw_items = [], []
            
            for i in range(int(num_p)):
                raw_names.append(col1.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"n_f_{i}"))
                raw_items.append(col2.text_input(f"결과 {i+1}", value=f"결과{i+1}", key=f"i_f_{i}"))
            
            if st.form_submit_button("🚀 사다리 생성!"):
                st.session_state['names_final'] = [str(x) for x in raw_names]
                st.session_state['items_final'] = [str(x) for x in raw_items]
                
                # 가로줄 생성
                ladder_lines = []
                for _ in range(12):
                    row = [0] * (int(num_p) - 1)
                    for j in range(int(num_p) - 1):
                        if random.random() > 0.6 and (j == 0 or row[j-1] == 0):
                            row[j] = 1
                    ladder_lines.append(row)
                
                st.session_state['ladder_final'] = ladder_lines
                st.session_state['num_p_final'] = int(num_p)
                # 각 참가자별 고유 색상 리스트 (화려한 색상들)
                st.session_state['colors'] = ["#FF4B4B", "#1C83E1", "#00C092", "#FFC61E", "#803DF5", "#FF69B4", "#FFA500", "#45DF31"][:int(num_p)]
                st.session_state.game_started = True
                st.rerun()

    # 2. 게임 실행 섹션
    else:
        l_json = json.dumps(st.session_state['ladder_final'])
        n_json = json.dumps(st.session_state['names_final'], ensure_ascii=False)
        i_json = json.dumps(st.session_state['items_final'], ensure_ascii=False)
        c_json = json.dumps(st.session_state['colors'])
        p_count = st.session_state['num_p_final']

        html_code = f"""
        <div style="text-align:center;">
            <canvas id="ladCanvas" width="550" height="600" style="cursor:pointer; background:#fff; border:1px solid #ddd; border-radius:15px;"></canvas>
        </div>
        <script>
        (function() {{
            const canvas = document.getElementById('ladCanvas');
            const ctx = canvas.getContext('2d');
            const lines = {l_json};
            const names = {n_json};
            const items = {i_json};
            const colors = {c_json};
            const numP = {p_count};
            
            const m = 60;
            const spacing = (canvas.width - m * 2) / (numP - 1);
            const rH = (canvas.height - 160) / lines.length;

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.lineWidth = 3;
                ctx.font = 'bold 15px sans-serif'; ctx.textAlign = 'center';

                for(let i=0; i<numP; i++) {{
                    let x = m + i * spacing;
                    // 기본 세로선도 해당 참가자의 연한 색상으로 표시
                    ctx.strokeStyle = colors[i] + '44'; 
                    ctx.beginPath(); ctx.moveTo(x, 80); ctx.lineTo(x, canvas.height - 80); ctx.stroke();
                    
                    ctx.fillStyle = colors[i];
                    ctx.fillText(names[i], x, 60);
                    ctx.fillStyle = "#333";
                    ctx.fillText(items[i], x, canvas.height - 45);
                }}

                // 가로선
                ctx.strokeStyle = '#ddd';
                lines.forEach((row, rIdx) => {{
                    row.forEach((has, cIdx) => {{
                        if(has) {{
                            let x = m + cIdx * spacing;
                            let y = 80 + (rIdx + 0.5) * rH;
                            ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + spacing, y); ctx.stroke();
                        }}
                    }});
                }});
            }}

            function move(pIdx) {{
                let curX = pIdx;
                let step = 0;
                ctx.strokeStyle = colors[pIdx]; // 해당 참가자의 고유 색상 사용
                ctx.lineWidth = 6;
                ctx.lineCap = 'round';

                function stepMove() {{
                    if (step >= lines.length) return;
                    let sX = m + curX * spacing;
                    let sY = 80 + step * rH;
                    let mY = sY + rH / 2;
                    ctx.beginPath(); ctx.moveTo(sX, sY); ctx.lineTo(sX, mY);
                    if(curX > 0 && lines[step][curX-1]) {{
                        curX--; ctx.lineTo(m + curX * spacing, mY);
                    }} else if(curX < numP - 1 && lines[step][curX]) {{
                        curX++; ctx.lineTo(m + curX * spacing, mY);
                    }}
                    ctx.lineTo(m + curX * spacing, sY + rH); ctx.stroke();
                    step++;
                    setTimeout(stepMove, 70);
                }}
                stepMove();
            }}

            canvas.onclick = (e) => {{
                const r = canvas.getBoundingClientRect();
                const x = e.clientX - r.left;
                for(let i=0; i<numP; i++) {{
                    if(Math.abs(x - (m + i * spacing)) < 30) {{ move(i); break; }}
                }}
            }};
            draw();
        }})();
        </script>
        """
        components.html(html_code, height=660)

        if st.button("🔄 다시 설정"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
