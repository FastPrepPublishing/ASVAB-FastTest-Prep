# app_debug.py – Debug del caricamento CSV
import streamlit as st
import pandas as pd

st.set_page_config(page_title="ASVAB Debug Mode", layout="wide")
st.title("🔍 ASVAB Exam CSV Debug Mode")

try:
    df = pd.read_csv("asvab_exam_simulation.csv")
    st.success("✅ CSV loaded successfully!")
    st.markdown("### 📊 Preview of First 10 Rows:")
    st.dataframe(df.head(10))
except Exception as e:
    st.error("❌ Error loading 'asvab_exam_simulation.csv'")
    st.exception(e)
