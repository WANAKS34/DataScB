import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="Analyze your Data",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Analyze Your Data")
st.write("Upload a **CSV** or **Excel** file to explore your data interactively")

# ------------------ File Upload ------------------
uploaded_file = st.file_uploader(
    "Upload a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    try:
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

    # ------------------ Preview ------------------
    st.subheader("👓 Data Preview")
    st.dataframe(data.head(50), use_container_width=True)

    # ------------------ Data Overview ------------------
    st.subheader("📊 Data Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", data.shape[0])
    c2.metric("Columns", data.shape[1])
    c3.metric("Missing Values", data.isnull().sum().sum())
    c4.metric("Duplicate Rows", data.duplicated().sum())

    # ------------------ Dataset Info ------------------
    st.subheader("🗃️ Dataset Info")
    buffer = io.StringIO()
    data.info(buf=buffer)
    st.text(buffer.getvalue())

    # ------------------ Statistical Summary ------------------
    st.subheader("📈 Statistical Summary (Numerical)")
    numeric_cols = data.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        st.dataframe(data[numeric_cols].describe(), use_container_width=True)
    else:
        st.warning("No numerical columns found.")

    non_numeric_cols = data.select_dtypes(include=["object", "bool"]).columns.tolist()

    if non_numeric_cols:
        st.subheader("📈 Statistical Summary (Non-Numerical)")
        st.dataframe(
            data[non_numeric_cols].describe(),
            use_container_width=True
        )

    # ------------------ Column Selection ------------------
    st.subheader("✂️ Select Columns for Analysis")
    selected_columns = st.multiselect("Choose columns", data.columns)

    if selected_columns:
        st.dataframe(data[selected_columns].head(), use_container_width=True)
    else:
        st.info("No columns selected. Showing full dataset.")
        st.dataframe(data.head(), use_container_width=True)

    # ------------------ Visualizations ------------------
    st.subheader("📊 Data Visualization")

    if numeric_cols:
        left, center, right = st.columns([1, 2, 1])

        with center:
            chart_type = st.radio(
                "Select Chart Type",
                [
                    "Line Chart",
                    "Scatter Chart",
                    "Bar Chart",
                    "Histogram",
                    "Box Plot",
                    "Area Chart",
                    "Violin Plot",
                    "Correlation Heatmap"
                ],
                horizontal=True
            )

        if chart_type != "Correlation Heatmap":
            x_axis = st.selectbox("Select X-Axis", numeric_cols)
            y_axis = st.selectbox(
                "Select Y-Axis",
                numeric_cols,
                index=1 if len(numeric_cols) > 1 else 0
            )

        fig, ax = plt.subplots()

        if chart_type == "Line Chart":
            ax.plot(data[x_axis], data[y_axis])
            ax.set_title(f"Line Chart: {x_axis} vs {y_axis}")

        elif chart_type == "Scatter Chart":
            ax.scatter(data[x_axis], data[y_axis])
            ax.set_title(f"Scatter Chart: {x_axis} vs {y_axis}")

        elif chart_type == "Bar Chart":
            ax.bar(data[x_axis], data[y_axis])
            ax.set_title(f"Bar Chart: {x_axis} vs {y_axis}")

        elif chart_type == "Histogram":
            ax.hist(data[x_axis], bins=30)
            ax.set_title(f"Histogram of {x_axis}")

        elif chart_type == "Box Plot":
            ax.boxplot(data[x_axis])
            ax.set_title(f"Box Plot of {x_axis}")

        elif chart_type == "Area Chart":
            ax.fill_between(data[x_axis], data[y_axis], alpha=0.5)
            ax.set_title(f"Area Chart: {x_axis} vs {y_axis}")

        elif chart_type == "Violin Plot":
            ax.violinplot(data[x_axis], showmeans=True)
            ax.set_title(f"Violin Plot of {x_axis}")

        elif chart_type == "Correlation Heatmap":
            corr = data[numeric_cols].corr()
            im = ax.imshow(corr, cmap="coolwarm")
            ax.set_xticks(range(len(numeric_cols)))
            ax.set_yticks(range(len(numeric_cols)))
            ax.set_xticklabels(numeric_cols, rotation=45, ha="right")
            ax.set_yticklabels(numeric_cols)
            fig.colorbar(im)
            ax.set_title("Correlation Heatmap")

        st.pyplot(fig)

    else:
        st.warning("No numerical columns available for visualization.")

else:
    st.info("👆 Upload a CSV or Excel file to get started")
