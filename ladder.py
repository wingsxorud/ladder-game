import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(page_title="네이버 사다리", layout="centered")
    st.title("🎢 컬러풀 사다리 (최종 수정판)")

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False
    if 'game_finished' not in st.session_state:
        st.session_state.game_finished = False

    # 1. 입력 섹션
    if not st.session_state.game_started:
        with st.form("ladder_form"):
            num_p = st.number_input("참여 인원", min_value=2, max_value=10, value=5)
            col1, col2 = st.columns(2)
            raw_names, raw_items = [], []
            for i in range(int(num_p)):
                raw_names.append(col1.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"n_f_{i}"))
                raw_items.append(col2.text_input(f"결과 {i+1}", value=f"결과{i+1}", key=f"i_f_{i}"))
            
            if st.form_submit_button("🚀 사다리 생성!"):
                st.session_state['names_final'] = [str(x) for x in raw_names]
                st.session_state['items_final'] = [str(x) for x in raw_items]
                st.session_state['num_p_final'] = int(num_p)
                st.session_state['colors'] = ["#FF4B4B", "#1C83E1", "#00C092", "#FFC61E", "#803DF5", "#FF69B4", "#FFA500", "#45DF31", "#00CCCC", "#9400D3"][:int(num_p)]
                
                ladder_lines = []
                for _ in range(15):
                    row = [0] * (int(num_p) - 1)
                    for j in range(int(num_p) - 1):
                        if random.random() < 0.6 and (j == 0 or row[j-1] == 0):
                            row[j] = 1
                    ladder_lines.append(row)
                st.session_state['ladder_final'] = ladder_lines
                st.session_state.game_started = True
                st.session_state.game_finished = False
                st.rerun()

    # 2. 게임 실행 및 결과 섹션
    else:
        names = st.session_state['names_final']
        items = st.session_state['items_final']
        lines = st.session_state['ladder_final']
        colors = st.session_state['colors']

        if st.session_state.game_finished:
            st.balloons()
            st.success("🎊 모든 결과가 나왔습니다! 🎊")
            
            # [수정포인트] 에러 방지를 위해 HTML 문자열 조립 방식 변경
            cols = st.columns(2)
            for idx, n_val in enumerate(names):
                # 사다리 결과 계산
                curr = idx
                for row in lines:
                    if curr > 0 and row[curr-1]: curr -= 1
                    elif curr < len(names)-1 and row[curr]: curr += 1
                
                res_item = items[curr]
                res_color = colors[idx]
                
                with cols[idx % 2]:
                    # f-string의 중괄호 충돌을 피하기 위해 format() 사용
                    html_card = """
                    <div style="padding:15px; border-radius:10px; border-left: 8px solid {color}; background-color: #f0f2f6; margin-bottom:10px;">
                        <span style="font-weight:bold; font-size:1.1em;">{name}</span> ➡️ 
                        <span style="color:#FF4B4B; font-weight:bold;">{item}</span>
                    </div>
                    """.format(color=res_color, name=n_val, item=res_item)
                    st.markdown(html_card, unsafe_allow_html=True)
            
            if st.button("🔄 처음부터 다시 하기"):
                st.session_state.clear()
                st.rerun()
            st.divider()

        # 3. 사다리 캔버스 영역
        l_js = json.dumps(lines)
        n_js = json.dumps(names, ensure_ascii=False)
        i_js = json.dumps(items, ensure_ascii=False)
        c_js = json.dumps(colors)
        p_cnt = st.session_state['num_p_final']

        # 자바스크립트 중괄호 충돌 방지를 위해 {{ }} 사용
        html_code = f"""
        <div style="text-align:center; width: 100%;">
            <canvas id="ladCanvas" style="cursor:pointer; background:#fff; border:1px solid #ddd; border-radius:15px; width: 100%; max-width: 600px; height: auto; touch-action: none;"></canvas>
            <p id="status_msg" style="margin-top:10px; color:#666; font-weight:bold; font-size:1.2em;">이름을 클릭해 사다리를 타세요!</p>
        </div>
        <script>
        (function() {{
            const canvas = document.getElementById('ladCanvas');
            const ctx = canvas.getContext('2d');
            const dpr = window.devicePixelRatio || 1;
            canvas.width = 600 * dpr; canvas.height = 700 * dpr;
            ctx.scale(dpr, dpr);

            const lines = {l_js};
            const names = {n_js};
            const items = {i_js};
            const colors = {c_js};
            const numP = {p_cnt};
            let clickedCount = 0;
            const clickedSet = new Set();
            
            const m = 40;
            const spacing = (600 - m * 2) / (numP - 1);
            const rH = (700 - 160) / lines.length;

            function draw() {{
                ctx.clearRect(0, 0, 600, 700);
                ctx.lineWidth = 3; ctx.font = 'bold 15px sans-serif'; ctx.textAlign = 'center';
                for(let i=0; i<numP; i++) {{
                    let x = m + i * spacing;
                    ctx.strokeStyle = clickedSet.has(i) ? colors[i] : '#eee';
                    ctx.beginPath(); ctx.moveTo(x, 80); ctx.lineTo(x, 620); ctx.stroke();
                    ctx.fillStyle = colors[i]; ctx.fillText(names[i], x, 60);
                    ctx.fillStyle = "#333"; ctx.fillText(items[i], x, 660);
                }}
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
                if(clickedSet.has(pIdx)) return;
                clickedSet.add(pIdx);
                clickedCount++;
                
                let curX = pIdx;
                let step = 0;
                ctx.strokeStyle = colors[pIdx]; ctx.lineWidth = 6; ctx.lineCap = 'round';

                function stepMove() {{
                    if (step >= lines.length) {{
                        if(clickedCount === numP) {{
                            document.getElementById('status_msg').innerHTML = "🎊 완료! 버튼을 눌러 결과를 확인하세요!";
                        }} else {{
                            document.getElementById('status_msg').innerText = names[pIdx] + "님 도착! 다음 사람?";
                        }}
                        return;
                    }}
                    let sX = m + curX * spacing;
                    let sY = 80 + step * rH;
                    let mY = sY + rH / 2;
                    ctx.beginPath(); ctx.moveTo(sX, sY); ctx.lineTo(sX, mY);
                    if(curX > 0 && lines[step][curX-1]) {{ curX--; ctx.lineTo(m + curX * spacing, mY); }}
                    else if(curX < numP - 1 && lines[step][curX]) {{ curX++; ctx.lineTo(m + curX * spacing, mY); }}
                    ctx.lineTo(m + curX * spacing, sY + rH); ctx.stroke();
                    step++;
                    setTimeout(stepMove, 50);
                }}
                stepMove();
            }}

            canvas.onclick = (e) => {{
                const rect = canvas.getBoundingClientRect();
                const scaleX = 600 / rect.width;
                const x = (e.clientX - rect.left) * scaleX;
                for(let i=0; i<numP; i++) {{
                    if(Math.abs(x - (m + i * spacing)) < 25) {{ move(i); break; }}
                }}
            }};
            draw();
        }})();
        </script>
        """
        components.html(html_code, height=720)

        if not st.session_state.game_finished:
            if st.button("🏁 결과 확인하기"):
                st.session_state.game_finished = True
                st.rerun()

if __name__ == "__main__":
    main()
