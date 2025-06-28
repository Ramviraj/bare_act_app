import streamlit as st
import openai
import pdfplumber
import graphviz

# Set the OpenAI API key securely from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI setup
st.set_page_config(page_title="Bare Act Analyzer", layout="wide")
st.title("📘 Bare Act Summarizer & Visualizer")

# Sidebar options
st.sidebar.header("Input Options")
input_mode = st.sidebar.radio("Choose input type:", ["Act Name & Section", "Upload PDF"])

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
    return text

# Function to get summary using OpenAI GPT
def query_openai(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a legal expert that explains Indian laws with clear summaries and visual formats."},
                {"role": "user", "content": f"Summarize the following legal text into a structured format like a flowchart or table:\n\n{text}"}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error from OpenAI: {e}")
        return ""

# Input text variable
text_data = ""

# Input handling
if input_mode == "Act Name & Section":
    act_name = st.text_input("Enter the name of the Bare Act")
    section_name = st.text_input("Enter the Section number/name")

    if st.button("Fetch & Summarize"):
        if not act_name or not section_name:
            st.warning("Please enter both Act name and Section name.")
        else:
            # In production, you can replace this with actual scraping
            simulated_text = f"Simulated text from {act_name}, section {section_name}. Replace with real fetch logic."
            text_data = simulated_text

elif input_mode == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF of the Bare Act", type=["pdf"])
    if uploaded_file is not None:
        text_data = extract_text_from_pdf(uploaded_file)

# Summary and output
if text_data:
    with st.spinner("Generating summary using OpenAI..."):
        summary = query_openai(text_data)

    if summary:
        st.subheader("📄 Summary")
        st.write(summary)

        st.subheader("📊 Visual Flowchart (Basic)")
        graph = graphviz.Digraph()
        graph.node("Start", "Start")
        graph.node("Summary", summary[:100] + "...")
        graph.edge("Start", "Summary")
        st.graphviz_chart(graph)
