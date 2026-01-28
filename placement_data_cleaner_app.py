import streamlit as st
import pandas as pd
import numpy as np
import re
from io import BytesIO

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Placement Data Cleaning System",
    page_icon="🧹",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS FOR UI
# --------------------------------
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    color: #2E86C1;
}
.sub-title {
    text-align: center;
    color: #555;
}
.section {
    background-color: #F8F9F9;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# HEADER
# --------------------------------
st.markdown("<div class='main-title'>🧹 Placement Data Cleaning System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Mini Project | Data Preprocessing & Cleaning Tool</div>", unsafe_allow_html=True)
st.markdown("---")

# --------------------------------
# SIDEBAR
# --------------------------------
st.sidebar.header("⚙️ Controls")
show_sample = st.sidebar.checkbox("Show Sample Dataset", True)
show_summary = st.sidebar.checkbox("Show Summary Report", True)

# --------------------------------
# SAMPLE DATA
# --------------------------------
def generate_sample_dataset():
    data = {
        "Name": ["ajit", "RIYA ", "sneha", "Ajit", "Mohit "],
        "Email": ["ajit@GMAIL.COM", "riya.gmail.com", " sneha@mail.com", "AJIT@GMAIL.COM", "mohit@mail"],
        "Phone": ["+91 98765-43210", "99887766", " 1234567890 ", "9876543210", "not phone"],
        "Dept": ["CSE", "IT", None, "CSE", "ECE"],
        "CGPA": ["8.5", "nine", "7.2", None, "9.1"],
        "Placed": ["Yes", None, "No", "Yes", "No"]
    }
    return pd.DataFrame(data)

# --------------------------------
# DATA CLEANING FUNCTION
# --------------------------------
def clean_data(df):
    df.columns = [c.strip() for c in df.columns]

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()

    if 'Name' in df.columns:
        df['Name'] = df['Name'].str.title()

    if 'Email' in df.columns:
        df['Email'] = df['Email'].str.lower()
        df['Email'] = df['Email'].apply(
            lambda x: x if re.match(r"[^@]+@[^@]+\.[^@]+", x) else np.nan
        )

    if 'Phone' in df.columns:
        df['Phone'] = df['Phone'].astype(str).str.replace(r'\D', '', regex=True)
        df['Phone'] = df['Phone'].apply(lambda x: x if len(x) >= 10 else np.nan)

    if 'CGPA' in df.columns:
        df['CGPA'] = pd.to_numeric(df['CGPA'], errors='coerce')
        df['CGPA'] = df['CGPA'].fillna(df['CGPA'].mean())

    if 'Dept' in df.columns:
        df['Dept'] = df['Dept'].fillna('Unknown')

    df = df.drop_duplicates()
    return df

# --------------------------------
# DOWNLOAD FUNCTION
# --------------------------------
def download_df(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()

# --------------------------------
# SAMPLE DATA DISPLAY
# --------------------------------
if show_sample:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("📄 Sample Placement Dataset")
    sample = generate_sample_dataset()
    st.dataframe(sample, use_container_width=True)

    st.download_button(
        "⬇️ Download Sample CSV",
        data=download_df(sample),
        file_name="sample_placement_data.csv",
        mime="text/csv"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------
# FILE UPLOAD
# --------------------------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📤 Upload Raw Placement Data")
file = st.file_uploader("Upload CSV File", type=["csv"])
st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------
# PROCESSING
# --------------------------------
if file:
    raw_df = pd.read_csv(file)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("🔍 Raw Uploaded Data")
    st.dataframe(raw_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    cleaned_df = clean_data(raw_df)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("✅ Cleaned Data Output")
    st.dataframe(cleaned_df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if show_summary:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.subheader("📊 Summary Report")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Records", len(cleaned_df))
        col2.metric("Departments", cleaned_df['Dept'].nunique() if 'Dept' in cleaned_df.columns else "NA")
        col3.metric("Average CGPA", round(cleaned_df['CGPA'].mean(), 2) if 'CGPA' in cleaned_df.columns else "NA")

        if "Placed" in cleaned_df.columns:
            st.write("**Placement Status Distribution:**")
            st.bar_chart(cleaned_df['Placed'].value_counts())

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.subheader("⬇️ Download Cleaned Dataset")
    st.download_button(
        "Download Cleaned CSV",
        data=download_df(cleaned_df),
        file_name="cleaned_placement_data.csv",
        mime="text/csv"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------
# FOOTER
# --------------------------------
st.markdown("---")
st.markdown(
    "<center>💡 Developed as a Mini Project | Data Cleaning using Python & Streamlit</center>",
    unsafe_allow_html=True
)
