import random

class DynamicPerceptualCalibrator:
    def __init__(self):
        self.threshold = 1.5  # conflict threshold
        
        # Q6 random buffer pool (Noise Injector)
        self.q6_pool = [
            "In the past week, I have taken time to feed stray animals or engage in pure relaxation unrelated to academics.",
            "I can quietly enjoy a meal without listening to any podcast or music.",
            "Today, I spent at least five minutes observing the sky outside or feeling the breeze, rather than staring at a screen."  # third added question
        ]
        
        # 9-node golden matrix question set
        self.questions = {
            "Q1": " Facing EngSci's high admission bar, I feel very calm and not anxious.",
            "Q2": " I believe that with reasonable planning, I can fully control my application progress and learning pace.",
            "Q3": " The stories of people holding multiple top offers on social media do not affect my objective judgment of my own abilities.",
            "Q4": " In the past week, I have often had trouble falling asleep, muscle tension, or unexplained stomach pain.",
            "Q5": " When facing a challenge like the last problem of the Euclid contest, my first reaction is 'break it down', not self-doubt.",
            "Q6": f" {random.choice(self.q6_pool)}",
            "Q7": " I feel the competitive atmosphere around me pressing down like a wall, making it hard to breathe.",
            "Q8": " If I only complete 50% of today's plan (e.g., due to physical discomfort), I can rest without guilt and won't punish myself by staying up late.",
            "Q9": " I uncontrollably refresh university application forums or admission score predictions multiple times a day."
        }
        self.answers = {}

    def run_assessment(self):
        print(">>> [System] Dynamic Perceptual Calibrator initiated.")
        print(">>> Please rate each statement from 1 to 5 (1 = strongly disagree, 5 = strongly agree)\n" + "-"*50)
        
        for q_id, q_text in self.questions.items():
            while True:
                try:
                    ans = int(input(f"{q_id}: {q_text}\nYour rating (1-5): "))
                    if 1 <= ans <= 5:
                        self.answers[q_id] = ans
                        break
                    else:
                        print(" [!] Error: Please enter an integer between 1 and 5.")
                except ValueError:
                    print(" [!] Error: Invalid input detected. Please enter a number.")
                    
        # --- [New Code Block 1: Obtain objective growth rate dy/dt] ---
        print("\n>>> [System] Cognitive dimensions collected. Now please provide your objective growth rate (dy/dt).")
        print(">>> Enter the three most recent percentage scores (0-100) for your most challenging core course (e.g., Calculus):")
        self.scores = []
        for i in range(1, 4):
            while True:
                try:
                    s = float(input(f"  Score {i} (T{i}): "))
                    if 0 <= s <= 100:
                        self.scores.append(s)
                        break
                    else:
                        print("  [!] Please enter a valid score between 0 and 100.")
                except ValueError:
                    print("  [!] Error: Please enter a number.")
        # ----------------------------------------
        
        self._analyze_and_report() 

    def _analyze_and_report(self):
        print("\n" + "="*50 + "\n>>> [System] Data collection complete. Performing cross-validation....\n")
        
        flags = []
        inconsistency_score = 0
        
        # Conflict 1: Cognition vs. Physiology (High scores in both Q1 and Q4 indicate a severe conflict)
        if self.answers["Q1"] >= 4 and self.answers["Q4"] >= 4:
            flags.append("Somatic_Disconnect")
            inconsistency_score += 2.0
            
        # Conflict 2: Sense of Control vs. Perceived Environmental Pressure (High scores in both Q2 and Q7 indicate a conflict)
        if self.answers["Q2"] >= 4 and self.answers["Q7"] >= 4:
            flags.append("Projection_Trap")
            inconsistency_score += 2.0
            
        # Conflict 3:Reverse Survivorship Bias（Focus on Other's Failures
        if self.answers["Q3"] >= 4 and self.answers["Q9"] >= 4:
            flags.append("Action_Belief_Conflict")
            inconsistency_score += 2.0
        # --- [New Code Block 2: Four-Quadrant Calculation and Dynamic Conclusion Assembly] ---
        
        # 1.Calculate objective growth rate (using T3 - T1 as a simple derivative) 
        t1, t2, t3 = self.scores
        objective_growth = t3 - t1 
        
        # 2.Calculate baseline variables 
        raw_stress = (self.answers["Q4"] + self.answers["Q7"] + self.answers["Q9"]) / 3
        subjective_growth = self.answers["Q5"]
        tolerance = self.answers["Q8"]
        
        # 3. Dynamic Weighting
        # --- Display of recalculated weights ---
        if inconsistency_score >= self.threshold:
            print(f"\n[!] Warning: Significant internal logic deviation detected (Deviation value: {inconsistency_score:.1f}/6.0)。")
            print(">>> System detects 'defensive interference' in current cognitive layer. Initiating dynamic weight restructuring....")
            w_cog, w_physio = 0.2, 0.8
        else:
            w_cog, w_physio = 0.5, 0.5
            
        final_stress = (w_cog * (15 - self.answers["Q1"] - self.answers["Q2"] - self.answers["Q3"])/3) + (w_physio * raw_stress)
        resilience_index = (subjective_growth + tolerance + self.answers["Q6"]) / 3
        snr = resilience_index / (final_stress + 0.1) # Avoid dividing by 0
        
        print("-" * 50)
        print(f"【Dynamic Perceptual Calibration Report】")
        print(f" ▶ Stress Coefficient (Stress, σ): {final_stress:.2f}/5.00")
        print(f" ▶ Objective Growth Rate (dy/dt): {objective_growth:+.1f}")
        print(f" ▶ Signal-to-Noise Ratio (SNR): {snr:.2f}")
        print("-" * 50)

        
        # 4. Dynamic String Assembly
        final_report = "\n>>> [System Conclusion & Agency Recovery]\n"
        
                #  (let press >3.0 is high press，dy/dt>0 is high grow gate)The operationalized model for these four states is implemented as follows:
        is_high_stress = final_stress > 3.0
        is_high_growth = objective_growth > 0
        
        if is_high_stress and is_high_growth:
            final_report += "【Quadrant 1: Overclocking】\nYour grades are steadily improving, yet the high stress level suggests your system is running on a deficit. Keep using your effective methods, but be sure to schedule intentional physical cooldown time. Reconnect with your original purpose — you are not a machine. No need to change direction; just ease off the accelerator.\n"
        elif is_high_stress and not is_high_growth:
            final_report += "【Quadrant 2: Stall】\nAlert: Massive internal friction is not translating into productive output; your system is in a high-energy stall. Stop overloading immediately! Cease the endless, blind problem-solving and seek an external perspective to reassess. More pressure will no longer fuel your motivation. What you need is a walk in a snow-covered park to breathe fresh air, or warm, steaming comfort food under soft lighting. Your coordinate system needs recalibration.\n"
        elif not is_high_stress and is_high_growth:
            final_report += "【Quadrant 3: Flow】\nPerfect state. Your SNR is exceptionally high; your cognitive assessment aligns seamlessly with reality. No need to compare — continue moving forward steadily at your own pace, and the world will open up to you.\n"
        else:
            final_report += "【Quadrant 4: Idle】\nStress is low, but the growth engine hasn't ignited. However, by actively seeking this calibration tool, you've already taken the first step toward growth. What you need now is not to force anxiety, but to find the spark — to reignite your inner drive toward your goals. Try envisioning the future you dream of.\n"

        # 5. Dynamic overlay - Blind Spot Revelation  (Appending Implicit Flags)
        if flags or tolerance <= 2:
            final_report += "\n[System Insight - Blind Spot Breakdown]\n"
            
        if "Somatic_Disconnect" in flags:
            final_report += "- Cognitive-Physiological Disconnect: Your brain is using 'I'm fine' to override your body's fatigue. Allowing yourself to feel anxious is the first step in unloading cognitive burden.\n"
        if "Projection_Trap" in flags:
            final_report += "- Environmental Projection Trap: Your sense of control is a defensive mechanism held together by force. Accept the unpredictability of plans; true mastery includes embracing the possibility of losing control.\n"
        if "Action_Belief_Conflict" in flags:
            final_report += "- Reverse Survivorship Bias: Frequently checking admission data reveals 'information compulsion'. Suggestion: Immediately enforce a 48-hour digital detox from forums.\n"
        if tolerance <= 2:
            final_report += "- Self-Exploitation Warning: Your efficiency is built on harsh self-pressure. Allow your system to enter low-power mode when necessary.\n"
            
        final_report += "\n>>> [System Status] Baseline established. You have re-anchored your true self."
               
        # ---Humanistic touch
        final_report += "\n\n✨ Embrace your life freely." 
        # ------------------------
        
        print(final_report)
        # ----------------------------------------
if __name__ == "__main__":
    calibrator = DynamicPerceptualCalibrator()
    calibrator.run_assessment()
