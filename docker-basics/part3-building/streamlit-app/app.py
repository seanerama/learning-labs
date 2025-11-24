import streamlit as st
import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Hello Docker!",
    page_icon="🐳",
    layout="wide"
)

# Title
st.title("🐳 Hello from Docker!")
st.markdown("### Your Containerized Streamlit Application")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("This app is running inside a Docker container!")
    st.markdown("---")

    # Add some controls
    st.header("Settings")
    theme_color = st.selectbox("Choose theme", ["Blue", "Green", "Red", "Purple"])
    show_time = st.checkbox("Show current time", value=True)

    st.markdown("---")
    st.markdown("**Tech Stack:**")
    st.markdown("- 🐍 Python 3.11")
    st.markdown("- 🎈 Streamlit " + st.__version__)
    st.markdown("- 🐳 Docker")

# Main content
if show_time:
    st.info(f"⏰ Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Three columns
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Counter")
    if 'counter' not in st.session_state:
        st.session_state.counter = 0

    if st.button("Increment"):
        st.session_state.counter += 1

    st.metric("Count", st.session_state.counter)

with col2:
    st.subheader("🎲 Random Number")
    if st.button("Generate Random"):
        num = random.randint(1, 100)
        st.success(f"Your random number: **{num}**")

with col3:
    st.subheader("✨ Greeting")
    name = st.text_input("Your name:", "Docker User")
    if st.button("Greet Me!"):
        st.success(f"Hello, {name}! 👋")
        st.balloons()

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Charts", "🗂️ Data", "📚 Docs"])

with tab1:
    st.subheader("Sample Chart")
    import numpy as np
    chart_data = np.random.randn(20, 3)
    st.line_chart(chart_data)

with tab2:
    st.subheader("Sample Data")
    import pandas as pd
    df = pd.DataFrame({
        'Column 1': [1, 2, 3, 4],
        'Column 2': [10, 20, 30, 40]
    })
    st.dataframe(df)

with tab3:
    st.markdown("""
    ### 🐳 Docker Commands Used

    Build the image:
    ```bash
    docker build -t streamlit-hello:v1.0 .
    ```

    Run the container:
    ```bash
    docker run -d -p 8501:8501 --name hello-streamlit streamlit-hello:v1.0
    ```

    View logs:
    ```bash
    docker logs -f hello-streamlit
    ```

    Stop and remove:
    ```bash
    docker rm -f hello-streamlit
    ```
    """)

# Progress bar demo
with st.expander("🔄 See a progress bar"):
    import time
    if st.button("Run Progress"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(100):
            progress_bar.progress(i + 1)
            status_text.text(f"Progress: {i + 1}%")
            time.sleep(0.01)

        st.success("Complete!")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using **Streamlit** and **Docker**")
