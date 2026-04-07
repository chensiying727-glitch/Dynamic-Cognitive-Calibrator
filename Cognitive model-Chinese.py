import random

class DynamicPerceptualCalibrator:
    def __init__(self):
        self.threshold = 1.5  # 矛盾阈值
        
        # Q6 随机缓冲池 (Noise Injector)
        self.q6_pool = [
            "我最近一周有抽出时间去喂流浪小动物，或者进行与学业完全无关的纯粹放松。",
            "我能在不听任何播客或音乐的情况下，安静地品尝完一顿饭。",
            "我今天有花哪怕五分钟的时间，去观察窗外的天空或感受一阵风，而不是只盯着屏幕。" # 新增的第三题
        ]
        
        # 9节点黄金矩阵题库
        self.questions = {
            "Q1": " 面对 EngSci 的高录取门槛，我目前的心态非常平稳，不觉得焦虑。",
            "Q2": " 我相信通过合理的规划，我能够完全掌控自己的申请进度和学习节奏。",
            "Q3": " 社交媒体上那些手握多个顶级 Offer 的经历，不会影响我对自身实力的客观判断。",
            "Q4": " 最近一周，我经常出现难以入睡、肌肉紧绷或无端胃痛的情况。",
            "Q5": " 遇到 Euclid 压轴题级别的挑战时，我的第一反应是‘拆解它’，而不是自我否定。",
            "Q6": f" {random.choice(self.q6_pool)}",
            "Q7": " 我觉得周围的竞争氛围像一堵墙一样压着我，让我喘不过气。",
            "Q8": " 如果今天计划只完成50%（如身体不适），我能坦然休息，不会熬夜惩罚自己。",
            "Q9": " 我每天会不受控制地多次刷新大学申请论坛或录取分数线预测。"
        }
        self.answers = {}

    def run_assessment(self):
        print(">>> [System] 动态感知校准仪 (Dynamic Perceptual Calibrator) 已启动。")
        print(">>> 请使用 1-5 分进行评价 (1=完全不符合, 5=完全符合)\n" + "-"*50)
        
        for q_id, q_text in self.questions.items():
            while True:
                try:
                    ans = int(input(f"{q_id}: {q_text}\n您的打分 (1-5): "))
                    if 1 <= ans <= 5:
                        self.answers[q_id] = ans
                        break
                    else:
                        print(" [!] 错误：请输入 1 到 5 之间的整数。")
                except ValueError:
                    print(" [!] 错误：检测到无效输入，请输入数字。")
                    
        # --- [新增代码块 1: 获取客观成绩 dy/dt] ---
        print("\n>>> [System] 认知维度采集完毕。现在需要获取您的客观成长速率 (dy/dt)。")
        print(">>> 请输入您最具挑战性的一门核心课（如 Calculus）最近的三次百分制成绩（0-100）：")
        self.scores = []
        for i in range(1, 4):
            while True:
                try:
                    s = float(input(f"  第 {i} 次成绩 (T{i}): "))
                    if 0 <= s <= 100:
                        self.scores.append(s)
                        break
                    else:
                        print("  [!] 请输入 0-100 之间的有效成绩。")
                except ValueError:
                    print("  [!] 错误：请输入数字。")
        # ----------------------------------------
        
        self._analyze_and_report() # 原本就在这里的调用

    def _analyze_and_report(self):
        print("\n" + "="*50 + "\n>>> [System] 数据采集成完毕，正在执行交叉校验...\n")
        
        flags = []
        inconsistency_score = 0
        
        # 地雷 1：认知 vs 生理 (Q1 高分且 Q4 高分表示严重冲突)
        if self.answers["Q1"] >= 4 and self.answers["Q4"] >= 4:
            flags.append("Somatic_Disconnect")
            inconsistency_score += 2.0
            
        # 地雷 2：控制感 vs 环境投影
        if self.answers["Q2"] >= 4 and self.answers["Q7"] >= 4:
            flags.append("Projection_Trap")
            inconsistency_score += 2.0
            
        # 地雷 3：反向幸存者偏差
        if self.answers["Q3"] >= 4 and self.answers["Q9"] >= 4:
            flags.append("Action_Belief_Conflict")
            inconsistency_score += 2.0
        # --- [新增代码块 2: 四象限计算与动态结论组装] ---
        
        # 1. 计算客观成长速率 (利用 T3 - T1 简单求导)
        t1, t2, t3 = self.scores
        objective_growth = t3 - t1 
        
        # 2. 计算基础变量
        raw_stress = (self.answers["Q4"] + self.answers["Q7"] + self.answers["Q9"]) / 3
        subjective_growth = self.answers["Q5"]
        tolerance = self.answers["Q8"]
        
        # 3. 动态加权逻辑 (Dynamic Weighting)
        # --- 修改后的权重重置显示 ---
        if inconsistency_score >= self.threshold:
            # 这里的 6.0 是三组地雷 (2.0 * 3) 的总和
            print(f"\n[!] 警告：检测到显著的内部逻辑偏移 (偏差值: {inconsistency_score:.1f}/6.0)。")
            print(">>> 系统判定当前认知层存在‘防御性干扰’，正在执行动态权重重构...")
            w_cog, w_physio = 0.2, 0.8
        else:
            w_cog, w_physio = 0.5, 0.5
            
        final_stress = (w_cog * (15 - self.answers["Q1"] - self.answers["Q2"] - self.answers["Q3"])/3) + (w_physio * raw_stress)
        resilience_index = (subjective_growth + tolerance + self.answers["Q6"]) / 3
        snr = resilience_index / (final_stress + 0.1) # 避免除以0
        
        print("-" * 50)
        print(f"【动态感知校准报告】")
        print(f" ▶ 压力系数 (Stress, σ): {final_stress:.2f}/5.00")
        print(f" ▶ 客观成长速率 (dy/dt): {objective_growth:+.1f}")
        print(f" ▶ 信噪比 (SNR): {snr:.2f}")
        print("-" * 50)
        
        # 4. 动态组装最终结论 (Dynamic String Assembly)
        final_report = "\n>>> [System Conclusion & Agency Recovery]\n"
        
        # 象限判断 (设定压力>3.0为高压，dy/dt>0为高成长)
        is_high_stress = final_stress > 3.0
        is_high_growth = objective_growth > 0
        
        if is_high_stress and is_high_growth:
            final_report += "【Quadrant 1: 超频状态 (Overclocking)】\n您的成绩在稳步上升，但高昂的压力系数说明系统正在透支。请保持当前有效的方法，但必须强制引入物理冷却时间，尝试回忆您的初心，人类并不是机器。您不需要改变方向，只需降低转速。\n"
        elif is_high_stress and not is_high_growth:
            final_report += "【Quadrant 2: 失速状态 (Stall)】\n警报：巨大的内耗没有转化为有效输出，系统处于高耗能失速中。立刻停止当前的超载！停止盲目且无止境地写题，去寻求外部视角进行复盘，更多的压力无法再转化您的动力了，您需要的是雪后公园中呼吸新鲜空气的漫步，或者暖黄灯光下热气腾腾的美食。您的坐标系需要重新校准。\n"
        elif not is_high_stress and is_high_growth:
            final_report += "【Quadrant 3: 心流状态 (Flow)】\n完美状态。您的 SNR 极高，认知评估与现实反馈严丝合缝。不需要去比较，继续按照您的节奏稳定推进，世界会向您敞开。\n"
        else:
            final_report += "【Quadrant 4: 怠速状态 (Idle)】\n压力虽低，但成长引擎并未点火。但您主动寻求定位工具，就是已经在成长的起步点了。您现在需要的不是逼自己焦虑，而是去寻找启动电流，重拾对目标的内驱力。试着规划一下，你梦想中的未来吧。\n"
            
        # 5. 动态叠加“盲区点破” (Appending Implicit Flags)
        if flags or tolerance <= 2:
            final_report += "\n[系统附加洞察 - 盲区破解]\n"
            
        if "Somatic_Disconnect" in flags:
            final_report += "- 认知与生理脱节：您的大脑正用‘我没事’强压身体的疲惫。允许自己感到焦虑，是卸下认知负荷的第一步。\n"
        if "Projection_Trap" in flags:
            final_report += "- 环境投影陷阱：您的控制感是强撑的防御机制。请接受计划的不可控性，真正的掌控感包含对失控的接纳。\n"
        if "Action_Belief_Conflict" in flags:
            final_report += "- 反向幸存者偏差：高频搜集录取数据的行为暴露出‘信息强迫症’。建议：立即对外部论坛执行 48 小时物理断网。\n"
        if tolerance <= 2:
            final_report += "- 自我剥削警告：您的高效建立在严苛的自我压榨上。允许系统在必要时进入低功耗模式。\n"
            
        final_report += "\n>>> [System Status] Baseline established. 您已重新锚定真实的自我坐标。"
               
        # ---人文关怀
        final_report += "\n\n✨ 尽情享受您自由的生命吧。" 
        # ------------------------
        
        print(final_report)
        # ----------------------------------------
# --- 确保这两行在文件的最底部，且左边没有空格 ---
if __name__ == "__main__":
    calibrator = DynamicPerceptualCalibrator()
    calibrator.run_assessment()
