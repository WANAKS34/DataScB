import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(
    page_title="Analyze your Data",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Analyze Your Data")
st.write("Upload a **CSV** or **Excel** file to explore your data interactively")

# File uploader (TASK 1)
uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
        # Detect file type
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        # Convert boolean columns to string
        bool_cols = data.select_dtypes(include=["bool"]).columns
        data[bool_cols] = data[bool_cols].astype(str)

    except Exception as e:
        st.error("❌ Could not read the uploaded file")
        st.exception(e)
        st.stop()

    st.success("✅ File uploaded successfully")

    # Preview
    st.subheader("👓 Data Preview")
    st.dataframe(data.head(50), use_container_width=True)

    # Data overview
    st.subheader("📊 Data Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", data.shape[0])
    col2.metric("Columns", data.shape[1])
    col3.metric("Missing Values", data.isnull().sum().sum())
    col4.metric("Duplicate Rows", data.duplicated().sum())

    # Dataset info
    st.subheader("🗃️ Dataset Info")
    buffer = io.StringIO()
    data.info(buf=buffer)
    st.text(buffer.getvalue())

    # Statistical summary (numeric)
    st.subheader("📈 Statistical Summary (Numerical)")
    numeric_cols = data.select_dtypes(include=np.number).columns

    if len(numeric_cols) > 0:
        st.dataframe(data[numeric_cols].describe(), use_container_width=True)
    else:
        st.warning("No numerical columns found.")

    # TASK 2: Conditional non-numeric summary
    non_numeric_cols = data.select_dtypes(include=["object", "bool"]).columns

    if len(non_numeric_cols) > 0:
        st.subheader("📈 Statistical Summary (Non-Numerical)")
        st.dataframe(
            data[non_numeric_cols].describe(),
            use_container_width=True
        )

    # Column selection
    st.subheader("✂️ Select Columns for Analysis")
    selected_columns = st.multiselect("Choose columns", data.columns)

    if selected_columns:
        st.dataframe(data[selected_columns].head(), use_container_width=True)
    else:
        st.info("No columns selected. Showing full dataset.")
        st.dataframe(data.head(), use_container_width=True)

    # ------------------ TASK 3: Visualizations ------------------
    st.subheader("📊 Data Visualization")

    if len(numeric_cols) >= 1:
        x_axis = st.selectbox("Select X-Axis", numeric_cols)
        y_axis = st.selectbox("Select Y-Axis", numeric_cols)

        col1, col2, col3 = st.columns(3)

        with col1:
            line_btn = st.button("📈 Line Chart")
        with col2:
            scatter_btn = st.button("🔵 Scatter Chart")
        with col3:
            bar_btn = st.button("📊 Bar Chart")

        col4, col5 = st.columns(2)
        with col4:
            hist_btn = st.button("📉 Histogram")
        with col5:
            box_btn = st.button("📦 Box Plot")

        if line_btn:
            fig, ax = plt.subplots()
            ax.plot(data[x_axis], data[y_axis])
            ax.set_title(f"Line Chart: {x_axis} vs {y_axis}")
            st.pyplot(fig)

        if scatter_btn:
            fig, ax = plt.subplots()
            ax.scatter(data[x_axis], data[y_axis])
            ax.set_title(f"Scatter Chart: {x_axis} vs {y_axis}")
            st.pyplot(fig)

        if bar_btn:
            fig, ax = plt.subplots()
            ax.bar(data[x_axis], data[y_axis])
            ax.set_title(f"Bar Chart: {x_axis} vs {y_axis}")
            st.pyplot(fig)

        if hist_btn:
            fig, ax = plt.subplots()
            ax.hist(data[x_axis], bins=30)
            ax.set_title(f"Histogram of {x_axis}")
            st.pyplot(fig)

        if box_btn:
            fig, ax = plt.subplots()
            ax.boxplot(data[x_axis])
            ax.set_title(f"Box Plot of {x_axis}")
            st.pyplot(fig)

    else:
        st.warning("No numerical columns available for visualization.")

else:
    st.info("👆 Upload a CSV or Excel file to get started")