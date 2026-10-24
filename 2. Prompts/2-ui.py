from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate, load_prompt
import streamlit as st

llm=ChatOllama(
    model="qwen2.5:3b",
    base_url="http://127.0.0.1:11434",
    temperature=0.7
)

st.header("Research Tool")
# Statice Prompt
# user_input=st.text_input("Enter the Prompt")

# Dynamic Prompt
paper_input=st.selectbox("Select the Research paper",[
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis"
    ])

style_input = st.selectbox(
    "Select Explanation Style",
    ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"]
)

length_input = st.selectbox(
    "Select Explanation Length",
    ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"]
)


#fill the placeholders
template=load_prompt('template.json')

# Instead of calling invoke two times create chain
if(st.button("Summarize")):
    chain=template | llm
    result=chain.invoke({
        'paper_input':paper_input,
        'style_input':style_input,
        'length_input':length_input
    })
    st.write(result.content)
