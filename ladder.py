import streamlit as st
import streamlit.components.v1 as components
import json
import random

def main():
    st.set_page_config(page_title="네이버 스타일 사다리", layout="centered")
    st.title("🎢 인터랙티브 사다리 타기")
    st.write("행님, 이름을 클릭하면 선을 타고 내려갑니다!")

    # 1. 입력부
    num_people = st.sidebar.number_input("인원수", min_value=2, max_value=8, value=4)
    
    names = []
    items = []
    col1, col2 = st.sidebar.columns(2)
    for i in range(num_people):
        names.append(col1.text_input(f"이름 {i+1}", value=f"참가자{i+1}", key=f"n_{i}"))
        items.append(col2.text_input(f"결과 {i+1}", value=f"결과{i+1}", key=f"i_{i}"))

    # 사다리 데이터 생성
    if 'ladder_data' not in st.session_state or st.sidebar.button("사다리 재설정"):
        lines = []
        for _ in range(12): # 사다리 층수
            row = [0] * (num_people - 1)
            for j in range(num_people - 1):
                if random.random() > 0.6 and (j == 0 or row[j-1] == 0):
                    row[j] = 1
            lines.append(row)
        st.session_state.ladder_data = lines

    # 2. JavaScript 및 HTML (사다리 시각화 핵심)
    ladder_json = json.dumps(st.session_state.ladder_data)
    names_json = json.dumps(names)
    items_json = json.dumps(items)

    html_code = f"""
    <div id="ladder-container" style="text-align:center;">
        <canvas id="ladderCanvas" width="500" height="600" style="cursor:pointer;"></canvas>
    </div>

    <script>
    const canvas = document.getElementById('ladderCanvas');
    const ctx = canvas.getContext('2d');
    const lines = {ladder_json};
    const names = {names_json};
    const items = {items_json};
    const numPeople = names.length;
    
    const margin = 50;
    const spacing = (canvas.width - margin * 2) / (numPeople - 1);
    const rowHeight = (canvas.height - 150) / lines.length;

    function drawLadder() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#ddd';
        ctx.lineWidth = 4;
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';

        for(let i=0; i<numPeople; i++) {{
            let x = margin + i * spacing;
            // 세로선
            ctx.beginPath();
            ctx.moveTo(x, 70);
            ctx.lineTo(x, canvas.height - 70);
            ctx.stroke();
            // 이름 & 결과
            ctx.fillStyle = '#333';
            ctx.fillText(names[i], x, 50);
            ctx.fillText(items[i], x, canvas.height - 40);
        }}

        // 가로선
        lines.forEach((row, rowIndex) => {{
            row.forEach((hasLine, colIndex) => {{
                if(hasLine) {{
                    let x = margin + colIndex * spacing;
                    let y = 70 + (rowIndex + 0.5) * rowHeight;
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
        let currentY = 70;
        ctx.strokeStyle = '#ff4b4b'; // 당첨선 색깔
        ctx.lineWidth = 6;

        let step = 0;
        function move() {{
            if (step >= lines.length) return;
            
            let startX = margin + currentXIdx * spacing;
            let startY = 70 + step * rowHeight;
            let midY = startY + rowHeight / 2;
            let endY = startY + rowHeight;

            ctx.beginPath();
            ctx.moveTo(startX, startY);
            
            // 아래로 절반
            ctx.lineTo(startX, midY);
            
            // 가로 이동 체크
            if(currentXIdx > 0 && lines[step][currentXIdx-1]) {{
                currentXIdx--;
                ctx.lineTo(margin + currentXIdx * spacing, midY);
            }} else if(currentXIdx < numPeople - 1 && lines[step][currentXIdx]) {{
                currentXIdx++;
                ctx.lineTo(margin + currentXIdx * spacing, midY);
            }}
            
            // 나머지 아래로
            ctx.lineTo(margin + currentXIdx * spacing, endY);
            ctx.stroke();
            
            step++;
            setTimeout(move, 100);
        }}
        move();
    }}

    canvas.addEventListener('click', (e) => {{
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        for(let i=0; i<numPeople; i++) {{
            let columnX = margin + i * spacing;
            if(Math.abs(x - columnX) < 20) {{
                animate(i);
                break;
            }}
        }}
    }});

    drawLadder();
    </script>
    """

    components.html(html_code, height=650)

if __name__ == "__main__":
    main()
