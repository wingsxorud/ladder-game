import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(page_title="네이버 사다리", layout="centered")
    st.title("🌈 컬러풀 사다리 (전체 결과 공개)")

    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

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
                
                # 사다리 발판 생성
                ladder_lines = []
                for _ in range(15):
                    row = [0] * (int(num_p) - 1)
                    for j in range(int(num_p) - 1):
                        if random.random() < 0.6 and (j == 0 or row[j-1] == 0):
                            row[j] = 1
                    ladder_lines.append(row)
                st.session_state['ladder_final'] = ladder_lines
                
                # 진행 상태 관리용
                st.session_state['clicked_count'] = 0
                st.session_state['results_map'] = {} # {이름: 결과}
                st.session_state.game_started = True
                st.rerun()

    # 2. 게임 실행 섹션
    else:
        # 데이터 준비
        l_js = json.dumps(st.session_state['ladder_final'])
        n_js = json.dumps(st.session_state['names_final'], ensure_ascii=False)
        i_js = json.dumps(st.session_state['items_final'], ensure_ascii=False)
        c_js = json.dumps(st.session_state['colors'])
        p_cnt = st.session_state['num_p_final']

        # 자바스크립트에서 클릭 완료 신호를 보낼 때 사용할 함수 (Streamlit query params 이용)
        st.write(f"현재 완료 인원: {st.session_state['clicked_count']} / {p_cnt}")

        html_code = f"""
        <div style="text-align:center; width: 100%;">
            <canvas id="ladCanvas" style="cursor:pointer; background:#fff; border:1px solid #ddd; border-radius:15px; width: 100%; max-width: 600px; height: auto; touch-action: none;"></canvas>
            <p id="status_msg" style="margin-top:10px; color:#666; font-weight:bold;">이름을 클릭해 사다리를 타세요!</p>
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
            const clicked = new Set();
            
            const m = 40;
            const spacing = (600 - m * 2) / (numP - 1);
            const rH = (700 - 160) / lines.length;

            function draw() {{
                ctx.clearRect(0, 0, 600, 700);
                ctx.lineWidth = 3; ctx.font = 'bold 14px sans-serif'; ctx.textAlign = 'center';
                for(let i=0; i<numP; i++) {{
                    let x = m + i * spacing;
                    ctx.strokeStyle = clicked.has(i) ? colors[i] : '#eee';
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
                if(clicked.has(pIdx)) return;
                clicked.add(pIdx);
                
                let curX = pIdx;
                let step = 0;
                ctx.strokeStyle = colors[pIdx]; ctx.lineWidth = 6; ctx.lineCap = 'round';

                function stepMove() {{
                    if (step >= lines.length) {{
                        // 종료 시 부모(Streamlit)에게 알림을 보내는 대신 메시지만 변경
                        document.getElementById('status_msg').innerText = names[pIdx] + "님 도착! 다음 사람 클릭!";
                        if(clicked.size === numP) {{
                             document.getElementById('status_msg').innerText = "모든 인원 완료! 아래 버튼을 눌러 결과를 확인하세요!";
                             // 클릭 완료 이벤트를 커스텀하게 발생시키거나 버튼 노출 유도
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
                    setTimeout(stepMove, 60);
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
        components.html(html_code, height=730)

        # 3. 결과 공개 섹션
        # 실시간으로 JS와 소통하는 대신, 수동으로 결과를 확인할 수 있는 버튼을 배치
        st.divider()
        if st.button("🏁 전체 결과 최종 확인"):
            # 사다리 로직을 파이썬에서 한 번 더 계산해서 결과 리스트 생성
            st.write("### 🎊 최종 결과 발표 🎊")
            final_lines = st.session_state['ladder_final']
            names = st.session_state['names_final']
            items = st.session_state['items_final']
            
            summary = []
            for i in range(len(names)):
                curr = i
                for row in final_lines:
                    if curr > 0 and row[curr-1]: curr -= 1
                    elif curr < len(names)-1 and row[curr]: curr += 1
                summary.append(f"**{names[i]}** ➡️ {items[curr]}")
            
            st.info("\n\n".join(summary))

        if st.button("🔄 게임 초기화"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
