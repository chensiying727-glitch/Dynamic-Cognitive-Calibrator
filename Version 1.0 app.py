import streamlit as st
import random
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# [全局配置层] 网页基础设置与记忆初始化
# ==========================================
# Streamlit 规定：set_page_config 必须是全篇第一个调用的 UI 命令
st.set_page_config(page_title="Dynamic Perceptual Calibrator", layout="centered", page_icon="✨")

# --- 提取题库池 (避免先有鸡还是先有蛋的冲突) ---
Q6_POOL = [
    "In the past week, I have taken time to feed stray animals or engage in pure relaxation unrelated to academics.",
    "I can quietly enjoy a meal without listening to any podcast or music.",
    "Today, I spent at least five minutes observing the sky outside or feeling the breeze, rather than staring at a screen."
]

# --- 初始化会话记忆 (确保 Q6 锁定) ---
if 'fixed_q6' not in st.session_state:
    st.session_state.fixed_q6 = random.choice(Q6_POOL)

# ==========================================
# [后端逻辑层] 核心引擎定义
# ==========================================
class DynamicPerceptualCalibrator:
    def __init__(self):
        self.threshold = 1.5
        self.questions = {
            "Q1": "Facing EngSci's high admission bar, I feel very calm and not anxious.",
            "Q2": "I believe that with reasonable planning, I can fully control my application progress and learning pace.",
            "Q3": "The stories of people holding multiple top offers on social media do not affect my objective judgment of my own abilities.",
            "Q4": "In the past week, I have often had trouble falling asleep, muscle tension, or unexplained stomach pain.",
            "Q5": "When facing a challenge like the last problem of the Euclid contest, my first reaction is 'break it down', not self-doubt.",
            "Q6": st.session_state.fixed_q6, # 这里完美调用记忆库
            "Q7": "I feel the competitive atmosphere around me pressing down like a wall, making it hard to breathe.",
            "Q8": "If I only complete 50% of today's plan, I can rest without guilt and won't punish myself by staying up late.",
            "Q9": "I uncontrollably refresh university application forums or admission score predictions multiple times a day."
        }

# ==========================================
# [前端 UI 层] Streamlit 网页渲染
# ==========================================
st.title("Dynamic Perceptual Calibrator ✨")
st.info(">>> [System Status] Re-anchoring your true self-coordinates.")
st.markdown("---")

# 实例化校准仪
calibrator = DynamicPerceptualCalibrator()

# --- 第一部分：认知维度采集 (滑动条) ---
st.subheader("Phase 1: Cognitive Dimension Assessment")
st.write("Please rate each statement from 1 to 5 (1 = strongly disagree, 5 = strongly agree)")

answers = {}
for q_id, q_text in calibrator.questions.items():
    answers[q_id] = st.slider(f"{q_id}: {q_text}", 1, 5, 3)

st.markdown("---")

# --- 第二部分：客观成长速率采集 (数字输入框) ---
st.subheader("Phase 2: Objective Growth Rate (dy/dt)")
st.write("Enter the three most recent percentage scores (0-100) for your most challenging core course (e.g., Calculus):")

col1, col2, col3 = st.columns(3)
with col1:
    t1 = st.number_input("Score 1 (T1)", min_value=0.0, max_value=100.0, value=80.0)
with col2:
    t2 = st.number_input("Score 2 (T2)", min_value=0.0, max_value=100.0, value=85.0)
with col3:
    t3 = st.number_input("Score 3 (T3)", min_value=0.0, max_value=100.0, value=90.0)

st.markdown("---")

# --- 第三部分：计算与生成报告 (一键触发) ---
if st.button("Generate Calibration Report", type="primary"):
    with st.spinner("Analyzing meta-cognitive signals..."):
        
        # 1. 逻辑冲突校验
        flags = []
        inconsistency_score = 0
        if answers["Q1"] >= 4 and answers["Q4"] >= 4:
            flags.append("Somatic_Disconnect")
            inconsistency_score += 2.0
        if answers["Q2"] >= 4 and answers["Q7"] >= 4:
            flags.append("Projection_Trap")
            inconsistency_score += 2.0
        if answers["Q3"] >= 4 and answers["Q9"] >= 4:
            flags.append("Action_Belief_Conflict")
            inconsistency_score += 2.0

        # 2. 计算基准变量
        objective_growth = t3 - t1 
        raw_stress = (answers["Q4"] + answers["Q7"] + answers["Q9"]) / 3
        subjective_growth = answers["Q5"]
        tolerance = answers["Q8"]

        # 3. 动态权重分配 & 核心公式计算
        if inconsistency_score >= calibrator.threshold:
            st.warning(f"**[!] Warning: Significant internal logic deviation detected (Deviation value: {inconsistency_score:.1f}/6.0).**\n\n>>> System detects 'defensive interference'. Initiating dynamic weight restructuring....")
            w_cog, w_physio = 0.2, 0.8
        else:
            w_cog, w_physio = 0.5, 0.5
            
        final_stress = (w_cog * (15 - answers["Q1"] - answers["Q2"] - answers["Q3"])/3) + (w_physio * raw_stress)
        resilience_index = (subjective_growth + tolerance + answers["Q6"]) / 3
        snr = resilience_index / (final_stress + 0.1)
        
        # 4. 渲染核心数据面板 (Metrics)
        st.subheader("【Dynamic Perceptual Calibration Report】")
        m1, m2, m3 = st.columns(3)
        m1.metric("Stress Coefficient (σ)", f"{final_stress:.2f}/5.00")
        m2.metric("Growth Rate (dy/dt)", f"{objective_growth:+.1f}")
        m3.metric("Signal-to-Noise Ratio (SNR)", f"{snr:.2f}")

        # ==========================================
        # [Plotly 视觉层] 绘制带颜色的四象限相空间
        # ==========================================
        st.markdown("### Personal Resilience Phase Space")
        fig = px.scatter(x=[final_stress], y=[objective_growth], labels={'x': 'Stress Coefficient (σ)', 'y': 'Objective Growth Rate (dy/dt)'})
        
        # 设置红色的星星作为坐标点
        fig.update_traces(marker=dict(size=20, color='red', symbol='star'))
        
        # 绘制背景颜色象限 (修复了不对称的问题，现在中心点完美在 3.0)
        fig.update_layout(
            xaxis=dict(range=[1, 5]),
            yaxis=dict(range=[-20, 20]), 
            shapes=[
                dict(type="rect", x0=3, x1=5, y0=0, y1=20, fillcolor="orange", opacity=0.2, line_width=0), # Q1 超频
                dict(type="rect", x0=3, x1=5, y0=-20, y1=0, fillcolor="red", opacity=0.1, line_width=0),    # Q2 失速
                dict(type="rect", x0=1, x1=3, y0=0, y1=20, fillcolor="skyblue", opacity=0.2, line_width=0), # Q3 心流
                dict(type="rect", x0=1, x1=3, y0=-20, y1=0, fillcolor="gray", opacity=0.1, line_width=0)    # Q4 怠速
            ]
        )
        st.plotly_chart(fig, use_container_width=True)

        # 5. 组装终态反馈 (Agency Recovery)
        is_high_stress = final_stress > 3.0
        is_high_growth = objective_growth > 0
        
        if is_high_stress and is_high_growth:
            st.info("**【Quadrant 1: Overclocking】**\nYour grades are steadily improving, yet the high stress level suggests your system is running on a deficit. Keep using your effective methods, but be sure to schedule intentional physical cooldown time. Reconnect with your original purpose — you are not a machine. No need to change direction; just ease off the accelerator.")
        elif is_high_stress and not is_high_growth:
            st.error("**【Quadrant 2: Stall】**\nAlert: Massive internal friction is not translating into productive output; your system is in a high-energy stall. Stop overloading immediately! Cease the endless, blind problem-solving and seek an external perspective to reassess. More pressure will no longer fuel your motivation. What you need is a walk in a snow-covered park to breathe fresh air, or warm, steaming comfort food under soft lighting. Your coordinate system needs recalibration.")
        elif not is_high_stress and is_high_growth:
            st.success("**【Quadrant 3: Flow】**\nPerfect state. Your SNR is exceptionally high; your cognitive assessment aligns seamlessly with reality. No need to compare — continue moving forward steadily at your own pace, and the world will open up to you.")
        else:
            st.warning("**【Quadrant 4: Idle】**\nStress is low, but the growth engine hasn't ignited. However, by actively seeking this calibration tool, you've already taken the first step toward growth. What you need now is not to force anxiety, but to find the spark — to reignite your inner drive toward your goals. Try envisioning the future you dream of.")

        # 6. 点破盲区
        if flags or tolerance <= 2:
            st.markdown("### [System Insight - Blind Spot Breakdown]")
            if "Somatic_Disconnect" in flags:
                st.markdown("- **Cognitive-Physiological Disconnect:** Your brain is using 'I'm fine' to override your body's fatigue. Allowing yourself to feel anxious is the first step in unloading cognitive burden.")
            if "Projection_Trap" in flags:
                st.markdown("- **Environmental Projection Trap:** Your sense of control is a defensive mechanism held together by force. Accept the unpredictability of plans; true mastery includes embracing the possibility of losing control.")
            if "Action_Belief_Conflict" in flags:
                st.markdown("- **Reverse Survivorship Bias:** Frequently checking admission data reveals 'information compulsion'. Suggestion: Immediately enforce a 48-hour digital detox from forums.")
            if tolerance <= 2:
                st.markdown("- **Self-Exploitation Warning:** Your efficiency is built on harsh self-pressure. Allow your system to enter low-power mode when necessary.")

        st.markdown("---")
        st.markdown(">>> [System Status] Baseline established. You have re-anchored your true self.")
        st.success("### ✨ Embrace your life freely.")
