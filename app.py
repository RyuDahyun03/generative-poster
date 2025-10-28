import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Generative Abstract Poster",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 1. Generative Functions ---

def random_palette(k=5):
    """
    K개의 무작위 따뜻한 색상 팔레트를 반환합니다.
    """
    warm_colors = [
        (0.8, 0.2, 0.2),  # Reddish
        (0.9, 0.5, 0.1),  # Orangeish
        (0.9, 0.7, 0.2),  # Yellowish
        (0.7, 0.3, 0.1),  # Darker Orange
        (0.6, 0.1, 0.1)   # Darker Red
    ]
    # 팔레트의 개수가 5개 이하인 경우에만 random.sample을 사용합니다.
    k = min(k, len(warm_colors))
    return random.sample(warm_colors, k)

def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    """
    중앙, 반경, 흔들림 정도를 기반으로 불규칙한 형태의 닫힌 도형(blob)을 생성합니다.
    """
    angles = np.linspace(0, 2*math.pi, points)
    # 무작위 노이즈를 추가하여 모양을 흔들리게 만듭니다.
    radii = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# --- 2. Streamlit UI and Plotting Logic ---

def generate_and_display_poster(seed_value):
    """
    특정 시드 값을 사용하여 포스터를 생성하고 Streamlit에 표시합니다.
    """
    # 매 실행 시 동일한 포스터가 나오도록 시드를 고정
    random.seed(seed_value)
    np.random.seed(int(seed_value * 1000000))

    # Matplotlib Figure 생성
    fig, ax = plt.subplots(figsize=(7, 10))
    ax.axis('off')

    # 배경색 설정
    ax.set_facecolor((0.98, 0.98, 0.97))

    palette = random_palette(5)
    n_layers = 8
    
    # 8개의 무작위 블롭 레이어 생성
    for i in range(n_layers):
        # 무작위 위치, 크기, 흔들림 정도 설정
        cx, cy = random.random(), random.random()
        rr = random.uniform(0.15, 0.45)
        
        x, y = blob(center=(cx, cy), r=rr, wobble=random.uniform(0.1, 0.35))
        color = random.choice(palette)
        alpha = random.uniform(0.25, 0.6)
        
        # 블롭을 채우기 (테두리 없음)
        ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0, 0, 0, 0))

    # 간단한 텍스트 라벨 추가
    ax.text(0.05, 0.95, "Generative Poster", fontsize=18, weight='bold', transform=ax.transAxes)
    ax.text(0.05, 0.91, "Week 2 • Arts & Advanced Big Data", fontsize=11, transform=ax.transAxes)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    # Matplotlib Figure를 Streamlit에 표시
    st.pyplot(fig)
    plt.close(fig) # 메모리 절약을 위해 그림 닫기

# --- 3. Main Streamlit App Execution ---

st.title("🎨 Generative Abstract Art")
st.markdown("## Streamlit + Matplotlib을 활용한 추상 포스터 생성기")

# 세션 상태를 사용하여 시드(seed) 값을 저장
if 'seed' not in st.session_state:
    st.session_state.seed = random.random()

# 새 포스터 생성 버튼
if st.button('🖼️ 새 포스터 생성', type="primary"):
    # 버튼을 누르면 새로운 무작위 시드 값으로 업데이트
    st.session_state.seed = random.random()
    # Streamlit은 시드 변경 후 자동으로 앱을 다시 실행합니다.

# 현재 시드 값으로 포스터 생성 및 표시
generate_and_display_poster(st.session_state.seed)

st.caption(f"현재 생성 시드: {st.session_state.seed:.6f}")
