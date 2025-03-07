import streamlit as st
import pandas as pd
import os
from io import BytesIO
import plotly.express as px

st.set_page_config(page_title="🚀 Data Sweeper", layout='wide')

st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 42px;
            font-weight: bold;
            color: #ff9800;
        }
        .sub-title {
            text-align: center;
            font-size: 20px;
            color: #6c757d;
        }
        .file-info {
            font-size: 18px;
            font-weight: bold;
            color: #17a589;
        }
        .stButton>button {
            background-color: #ff6f61;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
        }
        .stButton>button:hover {
            background-color: #e64a45;
        }
        .stDownloadButton>button {
            background-color: #28a745;
            color: white;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
        }
        .stDownloadButton>button:hover {
            background-color: #1e7e34;
        }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown("<p class='title'>🚀 Data Sweeper</p>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>🔄 Transform CSV & Excel files with built-in data cleaning, visualization, and smart conversions!</p>", unsafe_allow_html=True)
st.divider()

st.subheader("📂 Upload your Files")
uploaded_files = st.file_uploader(
    "🗂 Drag & drop or browse your files (CSV/XLSX)", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Invalid file format: {file_extension}. Please upload a CSV or Excel file.")
            continue
        
        st.divider()
        st.markdown(f"<p class='file-info'>📄 **File Name:** {file.name} | 📏 **Size:** {file.size / 1024:.2f} KB</p>", unsafe_allow_html=True)
        st.dataframe(df.head())

        with st.expander("🧹 Data Cleaning Options", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"🗑 Remove Duplicates - {file.name}"):
                    original_count = len(df)
                    df.drop_duplicates(inplace=True)
                    st.success(f"✅ **{original_count - len(df)} duplicates removed!** 🎉")
                    
            with col2:
                if st.button(f"🛠 Fill Missing Values - {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ **Missing values filled with column mean!** 📊")

        with st.expander("🔍 Select Columns to Convert", expanded=False):
            columns = st.multiselect(f"📌 Choose Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        with st.expander("📊 Data Visualization", expanded=False):
            if st.checkbox(f"📉 Show Charts for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) >= 2:
                    col_x = st.selectbox("📌 Select X-Axis:", numeric_cols, key=f"x_{file.name}")
                    col_y = st.selectbox("📌 Select Y-Axis:", numeric_cols, key=f"y_{file.name}")
                    
                    fig = px.bar(df, x=col_x, y=col_y, color=col_y, 
                                 title=f"📊 {col_x} vs {col_y}",
                                 labels={col_x: col_x, col_y: col_y},
                                 template="plotly_dark")
                    fig.update_layout(
                        xaxis_title=col_x,
                        yaxis_title=col_y,
                        plot_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=40, r=40, t=40, b=40)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("⚠️ Not enough numeric columns for visualization. Add more numeric data!")

        # File Conversion
        with st.expander("🔄 Convert File", expanded=False):
            conversion_type = st.radio(f"📥 Convert {file.name} to:", ("CSV", "Excel"), key=file.name)
            if st.button(f"🔽 Convert & Download - {file.name}"):
                buffer = BytesIO()
                file_name = file.name.replace(file_extension, f".{conversion_type.lower()}")
                mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                else:
                    df.to_excel(buffer, index=False)

                buffer.seek(0)
                st.download_button(
                    label=f"⬇️ Download {file_name}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                    key=f"download_{file.name}",
                )

st.success("🎉 All files processed successfully! 🚀")
