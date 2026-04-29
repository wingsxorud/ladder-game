import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(page_title="네이버 사다리", layout="centered")
    st.title("🎢 네이버 스타일 사다리 타기")

    # 1. 상태 초기화
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # 2. 입력 섹션
    if not st.session_state.game_started:
        st.write("인원과 이름을 입력하고 아래 버튼을 누르쇼!")
        
        # 폼 내부에서 데이터를 먼저 수집
        with st.form("ladder_form"):
            num_p = st.number_input("참여 인원", min_value=2, max_value=8, value=4)
            
            col1, col2 = st.columns(2)
            raw_names = []
            raw_items = []
            
            for i in range(int(num_p)):
                n_val = col1.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"n_field_{i}")
                i_val = col2.text_input(f"결과 {i+1}", value=f"결과{i+1}", key=f"i_field_{i}")
                raw_names.append(n_val)
                raw_items.append(i_val)
            
            submit = st.form_submit_button("🚀 사다리 생성!")
            
            if submit:
                # [핵심] JSON 에러의 원인인 객체를 제거하고 순수 문자열만 추출
                # 이 단계에서 리스트를 새로 생성하여 세션에 저장
                st.session_state['names_final'] = [str(x) for x in raw_names]
                st.session_state['items_final'] = [str(x) for x in raw_items]
                
                # 사다리 발판 생성
                ladder_lines = []
                for _ in range(12):
                    row = [0] * (int(num_p) - 1)
                    for j in range(int(num_p) - 1):
                        if random.random() > 0.6 and (j == 0 or row[j-1] == 0):
                            row[j] = 1
                    ladder_lines.append(row)
                
                st.session_state['ladder_final'] = ladder_lines
                st.session_state['num_p_final'] = int(num_p)
                st.session_state.game_started = True
                st.rerun()

    # 3. 게임 실행 섹션
    else:
        # 세션에 저장된 '순수 데이터'만 꺼내서 JSON으로 변환
        try:
            final_lines = st.session_state['ladder_final']
            final_names = st.session_state['names_final']
            final_items = st.session_state['items_final']
            final_count = st.session_state['num_p_final']

            l_json = json.dumps(final_lines)
            n_json = json.dumps(final_names, ensure_ascii=False)
            i_json = json.dumps(final_items, ensure_ascii=False)
        except Exception as e:
            st.error("데이터 변환 오류가 발생했습니다. 다시 시도해주세요.")
            if st.button("초기화"):
                st.session_state.clear()
                st.rerun()
            return

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
            const numP = {final_count};
            
            const m = 60;
            const spacing = (canvas.width - m * 2) / (numP - 1);
            const rH = (canvas.height - 160) / lines.length;

            function draw() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                ctx.strokeStyle = '#ccc'; ctx.lineWidth = 3;
                ctx.font = 'bold 15px sans-serif'; ctx.textAlign = 'center';

                for(let i=0; i<numP; i++) {{
                    let x = m + i * spacing;
                    ctx.beginPath(); ctx.moveTo(x, 80); ctx.lineTo(x, canvas.height - 80); ctx.stroke();
                    ctx.fillStyle = '#333';
                    ctx.fillText(names[i], x, 60);
                    ctx.fillText(items[i], x, canvas.height - 45);
                }}

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
                ctx.strokeStyle = '#FF4B4B'; ctx.lineWidth = 6;
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
