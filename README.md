# ASVAB Master Trainer – Practice & Exam Simulator

🎓 Welcome to the **ASVAB Master Trainer**, your interactive study companion for the ASVAB exam!  
This project provides over 1,100 practice questions formatted like a real app, with explanations, timers, and section-specific drills.

---

## 📂 Features

- ✅ 1,100+ Multiple Choice Questions
- ✅ 9 Official ASVAB Sections
- ✅ Realistic Practice Mode
- ✅ Full Exam Simulation (225 questions)
- ✅ Visual Timers & App-like Formatting
- ✅ Explanations and Scoring

---

## 🛠️ How to Use

### 🧠 Option 1: Use with ChatGPT (No Code Needed)

1. Go to [chat.openai.com/gpts](https://chat.openai.com/gpts)
2. Create a custom GPT
3. Upload the `asvab_visual_practice_questions.csv` file as Knowledge
4. Use this prompt for setup:
   ```
   You're ASVAB Master Trainer. Offer practice questions and full exam simulations using the uploaded CSV. After each answer, provide correct response, explanation, and a visual timer.
   ```

---

### 💻 Option 2: Use with Streamlit (Web App)

```bash
pip install streamlit pandas
```

```python
# app.py
import pandas as pd
import streamlit as st

df = pd.read_csv("asvab_visual_practice_questions.csv")

st.title("ASVAB Master Trainer – Practice Questions")

section = st.selectbox("Choose a section", df["Section"].unique())

questions = df[df["Section"] == section].sample(1).iloc[0]
st.markdown(questions["Formatted Question"])
st.markdown(questions["Visual Timer"])

for opt in ["Option A", "Option B", "Option C", "Option D"]:
    st.button(questions[opt])

if "Correct Answer" in questions:
    st.success(f"✅ Correct Answer: {questions['Correct Answer']}")
    st.info(questions["Explanation"])
```

Then run:

```bash
streamlit run app.py
```
