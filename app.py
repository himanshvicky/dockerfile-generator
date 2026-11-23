import streamlit as st
import requests

st.set_page_config(
    page_title="AI Dockerfile Generator",
    page_icon="🐳"
)

st.title("🐳 AI Dockerfile Generator")

st.write(
    "Generate optimized Dockerfiles using "
    "Python, Ollama and Llama 3.2."
)

language = st.selectbox(
    "Select Programming Language",
    ["Python", "Node.js", "Java", "Go", "PHP"]
)

framework = st.text_input(
    "Framework",
    placeholder="Example: Flask, Django, React"
)

port = st.number_input(
    "Application Port",
    min_value=1,
    max_value=65535,
    value=8000
)

if st.button("Generate Dockerfile"):

    prompt = f"""
    Generate a production-ready Dockerfile.

    Language: {language}
    Framework: {framework}
    Application Port: {port}

    Follow Docker best practices:
    1. Use an appropriate base image.
    2. Optimize image size.
    3. Use multi-stage builds where appropriate.
    4. Avoid running as root.
    5. Expose the application port.

    Return only the Dockerfile.
    """

    try:
        with st.spinner("AI is generating Dockerfile..."):

            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3.2:1b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=180
            )

            response.raise_for_status()

            dockerfile = response.json()["response"]

        st.success("Dockerfile generated successfully!")

        st.code(dockerfile, language="dockerfile")

        st.download_button(
            label="Download Dockerfile",
            data=dockerfile,
            file_name="Dockerfile"
        )

    except requests.RequestException as error:
        st.error(f"Error connecting to Ollama: {error}")