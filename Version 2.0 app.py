import streamlit as st
import json
import requests
import plotly.express as px

# ==========================================
# [全局配置层]
# ==========================================
st.set_page_config(page_title="Dynamic Perceptual Calibrator", layout="centered", page_icon="✨")

# ==========================================
# [安全密钥读取] 从 Streamlit Secrets 获取
# ==========================================
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    API_KEY = ""

# ==========================================
# [i18n] 多语言字典映射 (EN, ZH, FR)
# ==========================================
LANG_DICT = {
  "EN": {
    "title": "Dynamic Perceptual Calibrator",
    "subtitle": "EngSci Praxis AI-Core",
    "tipDesc": "This module utilizes Gemini AI to analyze subconscious stress responses. ⚠️ Note: Switching languages will refresh the dynamic scenario. Please avoid clicking multiple times in a short period.",
    "phase1Title": "Phase 1: Baseline Assessment",
    "phase1Desc": "Please rate your cognitive state and input your recent academic progress.",
    "phase2Title": "Phase 2: AI Dynamic Simulation",
    "btnSubmitP1": "Generate Calibration Report",
    "btnInitializeP2": "Initialize AI Deep Calibration",
    "btnDecrypt": "Execute AI Insight Decryption",
    "btnRestart": "Begin Next Simulation",
    "q1": "Q1: Facing EngSci's high admission bar, I feel very calm and not anxious.",
    "q2": "Q2: I believe that with reasonable planning, I can fully control my application progress.",
    "q3": "Q3: The stories of people holding multiple top offers on social media do not affect my objective judgment.",
    "q4": "Q4: In the past week, I have often had trouble falling asleep or unexplained tension.",
    "q5": "Q5: When facing a challenge, my first reaction is 'break it down', not self-doubt.",
    "q6": "Q6: In the past week, I have engaged in pure relaxation unrelated to academics.",
    "q7": "Q7: I feel the competitive atmosphere around me pressing down like a wall.",
    "q8": "Q8: If I only complete 50% of today's plan, I can rest without guilt.",
    "q9": "Q9: I uncontrollably refresh admission score predictions multiple times a day.",
    "score1": "Score 1 (T1)", "score2": "Score 2 (T2)", "score3": "Score 3 (T3)",
    "aiInsightTitle": "AI Consultant Deep Insight",
    "p1ReportTitle": "Baseline Phase Space",
    "stressLabel": "Stress (σ)", "snrLabel": "SNR", "growthLabel": "Growth (dy/dt)",
    "loadingAI": "AI is constructing the dynamic stress field...",
    "analyzingAI": "AI is decrypting your meta-cognition...",
    "availableActions": "Available Actions (Click to Select)",
    "yourSequence": "Your Sequential Response (Max 5, Click X to remove)",
    "langName": "English",
    "apiKeyPrompt": "System Config Error: Missing API Key in Streamlit Secrets.",
    "apiError": "Connection Timeout or AI Format Error. Please refresh and try again."
  },
  "ZH": {
    "title": "动态感知校准仪",
    "subtitle": "EngSci 核心算法驱动",
    "tipDesc": "本模块已接入 Gemini AI 用以分析潜意识应激反应。⚠️ 提示：切换语言会刷新动态场景。请避免短时间内多次点击。",
    "phase1Title": "第一阶段：认知基准评估",
    "phase1Desc": "请对您的认知状态进行评分，并输入您最近的学术成绩。",
    "phase2Title": "第二阶段：AI 动态应激博弈",
    "btnSubmitP1": "生成基准校准报告",
    "btnInitializeP2": "启动 AI 深度校准引擎",
    "btnDecrypt": "执行 AI 心理学解密",
    "btnRestart": "开启下一轮动态博弈",
    "q1": "Q1: 面对 EngSci 的高录取线，我感到非常平静，并不焦虑。",
    "q2": "Q2: 我相信通过合理的规划，我能完全掌控我的申请进度。",
    "q3": "Q3: 社交媒体上那些手握多个顶尖 Offer 的故事不会影响我对自身能力的客观判断。",
    "q4": "Q4: 过去一周，我经常难以入睡、肌肉紧张或有不明原因的胃痛。",
    "q5": "Q5: 面对类似 Euclid 竞赛最后一题的挑战，我的第一反应是\"拆解它\"，而不是自我怀疑。",
    "q6": "Q6: 过去一周，我有花时间去进行纯粹的放松，与学业毫无关系。",
    "q7": "Q7: 我感觉周围的竞争氛围像墙一样压过来，让人难以呼吸。",
    "q8": "Q8: 即使今天只完成了 50% 的计划，我也能毫无负罪感地休息。",
    "q9": "Q9: 我每天会不受控制地多次刷新大学申请论坛或录取分数预测。",
    "score1": "成绩 1 (T1)", "score2": "成绩 2 (T2)", "score3": "成绩 3 (T3)",
    "aiInsightTitle": "AI 心理顾问深度分析",
    "p1ReportTitle": "基准相空间坐标",
    "stressLabel": "应激系数 (σ)", "snrLabel": "信噪比 (SNR)", "growthLabel": "客观成长率 (dy/dt)",
    "loadingAI": "AI 正在构建专属动态场景...",
    "analyzingAI": "AI 正在破译元认知底层逻辑...",
    "availableActions": "行为组件库 (点击添加)",
    "yourSequence": "应激反应序列 (最多5项，点击 × 移除)",
    "langName": "Simplified Chinese",
    "apiKeyPrompt": "系统配置错误：未在 Streamlit Secrets 中读取到密钥。",
    "apiError": "网络连接超时或 AI 解析错误，请刷新重试。"
  },
  "FR": {
    "title": "Calibrateur Perceptif Dynamique",
    "subtitle": "Moteur IA EngSci Praxis",
    "tipDesc": "Ce module utilise l'IA Gemini pour analyser les réactions de stress. ⚠️ Remarque: Changer de langue actualisera le scénario. Veuillez éviter de cliquer plusieurs fois en peu de temps.",
    "phase1Title": "Phase 1 : Évaluation de base",
    "phase1Desc": "Veuillez évaluer votre état cognitif et saisir vos résultats académiques.",
    "phase2Title": "Phase 2 : Simulation Dynamique IA",
    "btnSubmitP1": "Générer le rapport de calibration",
    "btnInitializeP2": "Initialiser la calibration profonde IA",
    "btnDecrypt": "Exécuter le décryptage IA",
    "btnRestart": "Commencer la prochaine simulation",
    "q1": "Q1: Face à la barre d'admission élevée d'EngSci, je me sens très calme.",
    "q2": "Q2: Je crois qu'avec une planification, je peux contrôler l'avancement de ma candidature.",
    "q3": "Q3: Les multiples offres sur les réseaux sociaux n'affectent pas mon jugement objectif.",
    "q4": "Q4: La semaine dernière, j'ai souvent eu du mal à m'endormir ou des tensions inexpliquées.",
    "q5": "Q5: Face à un défi, ma première réaction est de 'le décomposer', pas de douter de moi.",
    "q6": "Q6: La semaine dernière, j'ai pris le temps de me détendre purement, sans lien avec les études.",
    "q7": "Q7: Je sens l'atmosphère compétitive autour de moi m'écraser comme un mur.",
    "q8": "Q8: Si je ne termine que 50% de mon plan, je peux me reposer sans culpabilité.",
    "q9": "Q9: Je rafraîchis de manière incontrôlable les forums de candidature plusieurs fois par jour.",
    "score1": "Note 1 (T1)", "score2": "Note 2 (T2)", "score3": "Note 3 (T3)",
    "aiInsightTitle": "Aperçu Profond du Consultant IA",
    "p1ReportTitle": "Espace de Phase de Base",
    "stressLabel": "Stress (σ)", "snrLabel": "SNR", "growthLabel": "Croissance (dy/dt)",
    "loadingAI": "L'IA construit le champ de stress dynamique...",
    "analyzingAI": "L'IA décrypte votre métacognition...",
    "availableActions": "Actions Disponibles (Cliquez)",
    "yourSequence": "Votre Réponse Séquentielle (Max 5)",
    "langName": "French",
    "apiKeyPrompt": "Erreur système : Clé API manquante dans les Secrets.",
    "apiError": "Erreur de connexion. Veuillez réessayer."
  }
}

DYNAMIC_WEIGHTS_MATRIX = {
  1: [1.0], 2: [0.6, 0.4], 3: [0.5, 0.3, 0.2], 4: [0.4, 0.3, 0.15, 0.15], 5: [0.35, 0.25, 0.15, 0.15, 0.1]
}

# ==========================================
# [Session State Initialization]
# ==========================================
for key in ['lang', 'current_phase', 'p1_result', 'p2_scenario', 'selected_sequence', 'p2_calibrated', 'final_report']:
    if key not in st.session_state:
        if key == 'lang': st.session_state[key] = 'EN'
        elif key == 'current_phase': st.session_state[key] = 1
        elif key == 'selected_sequence': st.session_state[key] = []
        else: st.session_state[key] = None

# ==========================================
# [Backend API Logic]
# ==========================================
def clean_json_response(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def call_gemini_api(prompt, model_name, expect_json=False):
    if not API_KEY: return None, "Missing API Key"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY.strip()}"
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    if expect_json:
        payload["generationConfig"] = {"responseMimeType": "application/json"}
        
    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, timeout=45)
            if response.status_code != 200:
                return None, f"Error {response.status_code}: {response.text}"
            return response.json(), None
        except Exception as e:
            if attempt == 2:
                return None, str(e)

def change_language():
    if st.session_state.current_phase == 2 and not st.session_state.p2_calibrated:
        st.session_state.p2_scenario = None
        st.session_state.selected_sequence = []

# ==========================================
# [Frontend UI]
# ==========================================
with st.sidebar:
    st.markdown("### ⚙️ System Config")
    model_choice = st.selectbox("Engine Core", [
        "gemini-flash-latest",
        "gemini-pro-latest"
    ], index=0)
    st.markdown("---")
    if API_KEY:
        st.success("✅ Secure Connection Established")
    else:
        st.error("❌ Warning: Secrets Configuration Missing")
    st.markdown("*Underground Engine v3.7 (Fusion)*")

col_title, col_lang = st.columns([3, 1])
with col_title:
    st.title(f"✨ {LANG_DICT[st.session_state.lang]['title']}")
with col_lang:
    selected_lang = st.selectbox("🌐 Language", ["EN", "ZH", "FR"], index=["EN", "ZH", "FR"].index(st.session_state.lang), key="lang_selector", on_change=change_language)
    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

t = LANG_DICT[st.session_state.lang]
st.info(f"💡 Tip: {t['tipDesc']}")

# Phase 1
if st.session_state.current_phase == 1:
    st.subheader(f"📊 {t['phase1Title']}")
    with st.form("phase1_form"):
        ans = {}
        for i in range(1, 10): ans[f"q{i}"] = st.slider(t[f"q{i}"], 1, 5, 3)
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        with c1: t1 = st.number_input(t["score1"], value=80.0)
        with c2: t2 = st.number_input(t["score2"], value=85.0)
        with c3: t3 = st.number_input(t["score3"], value=90.0)
        if st.form_submit_button(t["btnSubmitP1"], type="primary"):
            obj_growth = t3 - t1
            raw_stress = (ans["q4"] + ans["q7"] + ans["q9"]) / 3
            final_stress = (0.5 * (15 - ans["q1"] - ans["q2"] - ans["q3"])/3) + (0.5 * raw_stress)
            res_index = (ans["q5"] + ans["q8"] + ans["q6"]) / 3
            snr = res_index / (final_stress + 0.1)
            st.session_state.p1_result = {"final_stress": final_stress, "objective_growth": obj_growth, "snr": snr}
            st.rerun()

    if st.session_state.p1_result:
        res = st.session_state.p1_result
        st.success(f"### 🎯 {t['p1ReportTitle']}")
        m1, m2, m3 = st.columns(3)
        m1.metric(t["stressLabel"], f"{res['final_stress']:.2f}")
        m2.metric(t["growthLabel"], f"{res['objective_growth']:+.1f}")
        m3.metric(t["snrLabel"], f"{res['snr']:.2f}")
        
        # ========== 修复：图表和按钮用独立 container 隔开 ==========
        with st.container():
            fig = px.scatter(x=[res['final_stress']], y=[res['objective_growth']], labels={'x': 'Stress (σ)', 'y': 'Growth (dy/dt)'})
            fig.update_traces(marker=dict(size=20, color='red', symbol='star'))
            fig.update_layout(xaxis=dict(range=[1, 5]), yaxis=dict(range=[-20, 20]),
                              shapes=[
                                  dict(type="rect", x0=3, x1=5, y0=0, y1=20, fillcolor="orange", opacity=0.2, line_width=0),
                                  dict(type="rect", x0=3, x1=5, y0=-20, y1=0, fillcolor="red", opacity=0.1, line_width=0),
                                  dict(type="rect", x0=1, x1=3, y0=0, y1=20, fillcolor="skyblue", opacity=0.2, line_width=0),
                                  dict(type="rect", x0=1, x1=3, y0=-20, y1=0, fillcolor="gray", opacity=0.1, line_width=0)
                              ])
            st.plotly_chart(fig, use_container_width=True)

        with st.container():
            if st.button(t["btnInitializeP2"], type="primary"):
                if not API_KEY: 
                    st.error(t["apiKeyPrompt"])
                else:
                    st.session_state.current_phase = 2
                    st.session_state.p2_scenario = None
                    st.rerun()
        # ========== 修复结束 ==========

# Phase 2
if st.session_state.current_phase == 2:
    st.subheader(f"🧠 {t['phase2Title']}")
    if st.session_state.p2_scenario is None and not st.session_state.p2_calibrated:
        with st.spinner(t['loadingAI']):
            p1 = st.session_state.p1_result
            target_lang = t['langName']
            
            unified_prompt = f"""
            You are a Psychological Engineering AI Consultant. Your user is an Engineering Science student facing high academic pressure.
            Based on Phase 1 baseline: Stress Level={p1['final_stress']:.2f}, Growth={p1['objective_growth']}.
            Generate a customized, high-stress academic scenario (approx 50 words) and 8 behavioral options for them to sort.
            
            CRITICAL INSTRUCTIONS:
            1. You MUST generate the "context" and all option "text" values entirely in {target_lang}.
            2. Return ONLY a raw JSON object. Do NOT wrap it in Markdown formatting.
            3. The JSON must exactly match this structure:
            {{
              "context": "scenario text here",
              "options": [
                {{"id": "opt_1", "text": "action description", "tag": "Panic", "type": "Red", "score": 30}}
              ]
            }}
            4. The "type" MUST BE EXACTLY "Red", "Green", or "Gray".
            """
            
            res_json, err = call_gemini_api(unified_prompt, model_choice, expect_json=True)
            if res_json:
                try:
                    raw_text = res_json['candidates'][0]['content']['parts'][0]['text']
                    clean_text = clean_json_response(raw_text)
                    data = json.loads(clean_text)
                    
                    for i, opt in enumerate(data.get('options', [])):
                        opt['id'] = opt.get('id', f'opt_{i}')
                        opt['score'] = float(opt.get('score', 0))
                        opt['type'] = opt.get('type', 'Gray')
                    
                    st.session_state.p2_scenario = data
                    st.rerun()
                except Exception as e: 
                    st.error(f"{t['apiError']}")
                    if st.button("Go Back"):
                        st.session_state.current_phase = 1
                        st.rerun()
            else:
                st.error(f"{t['apiError']}")
                if st.button("Go Back"):
                    st.session_state.current_phase = 1
                    st.rerun()

    elif st.session_state.p2_scenario and not st.session_state.p2_calibrated:
        st.info(st.session_state.p2_scenario.get('context', 'No context generated.'))
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{t['availableActions']}**")
            for opt in st.session_state.p2_scenario.get('options', []):
                if not any(o['id'] == opt.get('id') for o in st.session_state.selected_sequence):
                    if st.button(opt.get('text', 'Action'), key=f"add_{opt.get('id')}", use_container_width=True):
                        st.session_state.selected_sequence.append(opt)
                        st.rerun()
        with col2:
            st.markdown(f"**{t['yourSequence']}**")
            for idx, s_opt in enumerate(st.session_state.selected_sequence):
                c_text, c_btn = st.columns([8, 2])
                c_text.write(f"#{idx+1} {s_opt.get('text', 'Action')}")
                if c_btn.button("❌", key=f"rm_{s_opt.get('id')}"):
                    st.session_state.selected_sequence.remove(s_opt)
                    st.rerun()
            if len(st.session_state.selected_sequence) > 0:
                if st.button(t['btnDecrypt'], type="primary"):
                    with st.spinner(t['analyzingAI']):
                        anx_score = sum(o.get('score', 0) * DYNAMIC_WEIGHTS_MATRIX[len(st.session_state.selected_sequence)][i] for i, o in enumerate(st.session_state.selected_sequence))
                        
                        analysis_prompt = f"""
                        Analyze this stress response sequence: {json.dumps(st.session_state.selected_sequence)}.
                        Stress Score: {anx_score:.1f}.
                        Write a warm 100-word analysis in {t['langName']}. 
                        End strictly with '✨ Embrace your life freely.'
                        """
                        res, err = call_gemini_api(analysis_prompt, model_choice, expect_json=False)
                        if res:
                            insight = res['candidates'][0]['content']['parts'][0]['text']
                            st.session_state.final_report = {"anxietyScore": f"{anx_score:.1f}", "aiInsight": insight}
                            st.session_state.p2_calibrated = True
                            st.rerun()
                        else: 
                            st.error(t["apiError"])
                            if st.button("Go Back"):
                                st.session_state.current_phase = 1
                                st.rerun()

    elif st.session_state.p2_calibrated:
        st.success("### Calibration Complete")
        r1, r2 = st.columns(2)
        r1.metric("Dynamic Stress Level", st.session_state.final_report['anxietyScore'])
        st.markdown(f"**{t['aiInsightTitle']}**")
        st.info(st.session_state.final_report['aiInsight'])
        if st.button(t['btnRestart']):
            st.session_state.selected_sequence = []; st.session_state.p2_calibrated = False; st.session_state.p2_scenario = None; st.session_state.current_phase = 1; st.rerun()

st.markdown("---")
st.caption("SYSTEM ENGAGED | Final Fusion v3.7")
