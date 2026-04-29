import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(page_title="네이버 스타일 사다리", layout="centered")
    
    st.title("🎢 네이버 스타일 사다리 타기")

    # 세션 상태 초기화
    if 'game_started' not in st.session_state:
        st.session_state.game_started = False

    # 1. 입력 섹션
    if not st.session_state.game_started:
        st.write("인원과 이름을 입력한 후, '사다리 생성'을 누르쇼 행님!")
        num_p = st.number_input("참여 인원", min_value=2, max_value=8, value=4, key="main_num_p")
        
        col1, col2 = st.columns(2)
        
        # 임시 리스트에 '값'만 담기 위해 확실히 처리
        input_names = []
        input_items = []
        
        for i in range(int(num_p)):
            # 변수에 담을 때 즉시 값을 확정 지음
            name_val = col1.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"n_idx_{i}")
            item_val = col2.text_input(f"결과 {i+1}", value=f"결과{i+1}", key=f"i_idx_{i}")
            input_names.append(str(name_val))
            input_items.append(str(item_val))

        if st.button("🚀 사다리 생성 및 시작!"):
            # 가로줄 생성 로직
            new_lines = []
            for _ in range(12):
                row = [0] * (int(num_p) - 1)
                for j in range(int(num_p) - 1):
                    if random.random() > 0.6 and (j == 0 or row[j-1] == 0):
                        row[j] = 1
                new_lines.append(row)
            
            # 세션 스테이트에 순수 데이터(문자열, 숫자, 리스트)만 저장
            st.session_state.ladder_data = new_lines
            st.session_state.names = input_names
            st.session_state.items = input_items
            st.session_state.num_people = int(num_p)
            st.session_state.game_started = True
            st.rerun()

    # 2. 게임 실행 섹션
    else:
        # 세션에서 꺼내올 때 다시 한번 데이터 타입 체크
        try:
            # 순수 리스트와 문자열인지 확인 후 JSON 변환
            l_data = list(st.session_state.ladder_data)
            n_data = [str(x) for x in st.session_state.names]
            i_data = [str(x) for x in st.session_state.items]
            p_count = int(st.session_state.num_people)

            ladder_json = json.dumps(l_data)
            names_json = json.dumps(n_data, ensure_ascii=False)
            items_json = json.dumps(i_data, ensure_ascii=False)
        except Exception as e:
            st.error(f"데이터 정제 중 오류: {e}")
            st.session_state.game_started = False
            st.rerun()
            return

        html_code = f"""
        <div style="text-align:center;">
            <canvas id="ldCanvas" width="550" height="600" style="cursor:pointer; background:#fff; border-radius:10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);"></canvas>
        </div>
        <script>
        (function() {{
            const cvs = document.getElementById('ldCanvas');
            const ctx = cvs.getContext('2d');
            const lines = {ladder_json};
            const names = {names_json};
            const items = {items_json};
            const numP = {p_count};
            
            const m = 60;
            const spc = (cvs.width - m * 2) / (numP - 1);
            const rH = (cvs.height - 160) / lines.length;

            function draw() {{
                ctx.clearRect(0, 0, cvs.width, cvs.height);
                ctx.strokeStyle = '#ddd';
                ctx.lineWidth = 3;
                ctx.font = 'bold 15px sans-serif';
                ctx.textAlign = 'center';

                for(let i=0; i<numP; i++) {{
                    let x = m + i * spc;
                    ctx.beginPath();
                    ctx.moveTo(x, 80); ctx.lineTo(x, cvs.height - 80);
                    ctx.stroke();
                    ctx.fillStyle = '#333';
                    ctx.fillText(names[i], x, 60);
                    ctx.fillText(items[i], x, cvs.height - 45);
                }}

                lines.forEach((row, rIdx) => {{
                    row.forEach((has, cIdx) => {{
                        if(has) {{
                            let x = m + cIdx * spc;
                            let y = 80 + (rIdx + 0.5) * rH;
                            ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + spc, y); ctx.stroke();
                        }}
                    }});
                }});
            }}

            function movePath(pIdx) {{
                let curX = pIdx;
                let step = 0;
                ctx.strokeStyle = '#FF4B4B';
                ctx.lineWidth = 5;
                function stepMove() {{
                    if (step >= lines.length) return;
                    let sX = m + curX * spc;
                    let sY = 80 + step * rH;
                    let mY = sY + rH / 2;
                    ctx.beginPath(); ctx.moveTo(sX, sY); ctx.lineTo(sX, mY);
                    if(curX > 0 && lines[step][curX-1]) {{
                        curX--; ctx.lineTo(m + curX * spc, mY);
                    }} else if(curX < numP - 1 && lines[step][curX]) {{
                        curX++; ctx.lineTo(m + curX * spc, mY);
                    }}
                    ctx.lineTo(m + curX * spc, sY + rH); ctx.stroke();
                    step++;
                    setTimeout(stepMove, 70);
                }}
                stepMove();
            }}

            cvs.onclick = (e) => {{
                const r = cvs.getBoundingClientRect();
                const x = e.clientX - r.left;
                for(let i=0; i<numP; i++) {{
                    if(Math.abs(x - (m + i * spc)) < 30) {{ movePath(i); break; }}
                }}
            }};
            draw();
        }})();
        </script>
        """
        components.html(html_code, height=650)

        if st.button("🔄 다시 설정하기"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
