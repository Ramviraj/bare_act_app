import streamlit as st
import openai
import pdfplumber
import graphviz
import os
from dotenv import load_dotenv

# Load the API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Bare Act Analyzer", layout="wide")
st.title("📘 Bare Act Summarizer & Visualizer")

# Step 1: Input options
st.sidebar.header("Input Options")
input_mode = st.sidebar.radio("Choose input type:", ["Act Name & Section", "Upload PDF"])

# Step 2: Text or PDF Input
def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

def query_openai(text):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a legal analyst AI that summarizes Indian Bare Acts into flowcharts or structured summaries."},
            {"role": "user", "content": f"Summarize the following legal content into a flowchart/table format:\n\n{text}"}
        ],
        temperature=0.5,
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

# Step 3: Input handling
text_data = ""

if input_mode == "Act Name & Section":
    act_name = st.text_input("Enter the name of the Bare Act")
    section_name = st.text_input("Enter the Section number/name")

    if st.button("Fetch & Summarize"):
        # For now, simulate fetch
        simulated_text = f"This is placeholder legal text from the {act_name}, section {section_name}. You can integrate scraping here."
        text_data = simulated_text

elif input_mode == "Upload PDF":
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded_file:
        text_data = extract_text_from_pdf(uploaded_file)

# Step 4: Summarize and Display
if text_data:
    with st.spinner("Generating summary using OpenAI..."):
        summary = query_openai(text_data)

    st.subheader("📄 Summary")
    st.write(summary)

    st.subheader("📊 Flowchart (Simplified)")
    graph = graphviz.Digraph()
    graph.node("Start", "Start")
    graph.node("Summary", summary[:100] + "...")
    graph.edge("Start", "Summary")
    st.graphviz_chart(graph)

