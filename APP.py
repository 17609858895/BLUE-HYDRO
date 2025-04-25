import streamlit as st
import numpy as np
import pandas as pd
import joblib
from io import BytesIO

# 页面配置：居中显示、模拟A4横向布局
st.set_page_config(
    page_title="Methylene Blue Adsorption Predictor",
    layout="centered"
)

# 🌿 自定义样式优化
st.markdown("""
    <style>
    .stApp {
        max-width: 1100px;
        margin: auto;
        background-color: #f6fbf9;
        padding: 2rem 3rem 3rem 3rem;
        border-radius: 16px;
        box-shadow: 0px 0px 10px rgba(0, 100, 80, 0.05);
    }
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
    }
    .custom-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1b4332;
        margin-bottom: 0.3rem;
        text-align: center;
    }
    .custom-sub {
        font-size: 1.1rem;
        color: #4b4b4b;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        color: #2d6a4f;
    }
    .stButton>button {
        background-color: #52b788;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 8px;
        padding: 0.5rem 1.1rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #40916c;
    }
    .stDownloadButton>button {
        background-color: white;
        color: #333;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 0.45rem 1rem;
        margin-top: 0.8rem;
    }
    .stDownloadButton>button:hover {
        background-color: #f0fdf4;
        border-color: #a3d9c8;
    }
    .stSuccess {
        background-color: #d8f3dc;
        color: #1b4332;
        padding: 0.9rem;
        border-radius: 8px;
        font-weight: 500;
        font-size: 1.1rem;
        margin-top: 1.2rem;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 加载模型
@st.cache_resource
def load_model():
    return joblib.load("HGB.pkl")

model = load_model()

# 🎯 页面标题
st.markdown('<div class="custom-header">🌿 Methylene Blue Adsorption Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-sub">Estimate the adsorption capacity (Q, mmol/g) of hydrothermal carbon based on synthesis, material properties, and adsorption environment.</div>', unsafe_allow_html=True)

# 🎛 三列输入（A4横向布局）
col1, col2, col3 = st.columns([1.05, 1.05, 1.05], gap="large")

with col1:
    st.markdown('<div class="section-title">🧪 Synthesis Conditions</div>', unsafe_allow_html=True)
    T_H = st.number_input("Hydrothermal Temperature (°C)", min_value=80.0, max_value=300.0, value=180.0, step=1.0)
    time = st.number_input("Reaction Time (h)", min_value=0.5, max_value=48.0, value=6.0, step=0.5)
    ratio = st.number_input("Solid-to-liquid Ratio (g/mL)", min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    modified = st.selectbox("Surface Modification?", ["No", "Yes"])
    modified_val = 1 if modified == "Yes" else 0

with col2:
    st.markdown('<div class="section-title">🧬 Material Properties</div>', unsafe_allow_html=True)
    C = st.number_input("Carbon Content (wt%)", min_value=10.0, max_value=90.0, value=60.0, step=0.5)
    ONC = st.number_input("Molar Ratio (O+N)/C", min_value=0.01, max_value=2.0, value=0.5, step=0.01)
    HC = st.number_input("Molar Ratio H/C", min_value=0.01, max_value=2.0, value=0.3, step=0.01)
    OC = st.number_input("Molar Ratio O/C", min_value=0.01, max_value=2.0, value=0.2, step=0.01)
    BET = st.number_input("BET Surface Area (m²/g)", min_value=5.0, max_value=2000.0, value=400.0, step=10.0)

with col3:
    st.markdown('<div class="section-title">⚗️ Adsorption Environment</div>', unsafe_allow_html=True)
    pH = st.number_input("Solution pH", min_value=1.0, max_value=14.0, value=7.0, step=0.1)
    T = st.number_input("Adsorption Temperature (°C)", min_value=10.0, max_value=60.0, value=25.0, step=1.0)
    C0 = st.number_input("Initial Dye/Adsorbent Ratio (mg/g)", min_value=0.1, max_value=500.0, value=100.0, step=1.0)

# ⏱ 预测与结果展示
prediction = None
df_result = None

col_btn, col_download = st.columns([1.5, 1])

with col_btn:
    if st.button("🔍 Predict Adsorption Capacity"):
        input_array = np.array([[T_H, time, ratio, modified_val, C, ONC, HC, OC, BET, pH, T, C0]])
        prediction = model.predict(input_array)[0]
        st.success(f"✅ Predicted Adsorption Capacity: **{prediction:.3f} mmol/g**")

        df_result = pd.DataFrame([{
            "T_H (°C)": T_H, "Time (h)": time, "S/L Ratio": ratio, "Modified": modified,
            "C (wt%)": C, "(O+N)/C": ONC, "H/C": HC, "O/C": OC, "BET (m²/g)": BET,
            "pH": pH, "T (°C)": T, "C₀ (mg/g)": C0, "Predicted Q (mmol/g)": round(prediction, 3)
        }])

with col_download:
    if prediction is not None and df_result is not None:
        towrite = BytesIO()
        df_result.to_csv(towrite, index=False)
        st.download_button(
            label="📁 Export Result as CSV",
            data=towrite.getvalue(),
            file_name="MB_Adsorption_Prediction.csv",
            mime="text/csv"
        )

