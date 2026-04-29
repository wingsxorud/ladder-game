import streamlit as st
from streamlit_echarts import st_echarts
import random
import time

def create_roulette_game():
    st.set_page_config(page_title="운명의 돌림판", layout="centered")
    
    st.title("🎯 운명의 돌림판")
    st.write("행님, 이번엔 돌림판으로 화끈하게 가시죠!")

    # 1. 항목 입력
    items_input = st.text_area("항목들을 쉼표(,)나 엔터로 구분해서 입력하쇼!", 
                               value="커피 쏘기, 밥 쏘기, 꽝, 면제", 
                               help="예: 이름1, 이름2, 이름3")
    
    # 입력값 정리
    items = [item.strip() for item in items_input.replace('\n', ',').split(',') if item.strip()]

    if len(items) < 2:
        st.warning("항목을 최소 2개 이상 입력해야 돌릴 맛이 나죠, 행님!")
        return

    # 2. 돌림판 데이터 구성
    data = [{"value": 1, "name": item} for item in items]
    
    # 돌림판 옵션 설정 (ECharts 활용)
    options = {
        "tooltip": {"trigger": "item"},
        "series": [
            {
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {"borderRadius": 10, "borderColor": "#fff", "borderWidth": 2},
                "label": {"show": True, "position": "inside", "formatter": "{b}"},
                "data": data,
            }
        ],
    }

    # 3. 돌림판 출력
    st_echarts(options=options, height="400px")

    # 4. 실행 버튼
    if st.button("🚀 돌려라 돌려!!"):
        # 긴장감 조성
        with st.empty():
            for _ in range(10):
                temp_choice = random.choice(items)
                st.subheader(f"🎲 돌아가는 중... -> {temp_choice}")
                time.sleep(0.1)
            
            # 최종 결과 선택
            winner = random.choice(items)
            
            # 화려한 결과 발표
            st.divider()
            st.balloons()
            st.snow() # 겨울이면 눈도 내리게 해봤슴다
            st.header(f"🎊 결과: [ {winner} ]")
            st.success(f"행님, 오늘의 운명은 '{winner}'(으)로 결정됐습니다!")

if __name__ == "__main__":
    create_roulette_game()
