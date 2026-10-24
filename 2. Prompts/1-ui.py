from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
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

# MAKE IT REUSABLE
# template=PromptTemplate(
#     template="""
#     Please summarize the research paper titled "{paper_input}" with the following specifications

#     Explanation Style: {style_input}
#     Explanation Length: {length_input}

#     1. Mathematical Details:
#     - Include relevant mathematical equations if present in the paper.
#     - Explain the mathematical concepts using simple, intuitive code snippets where applicable.

#     2. Analogies:
#     - Use relatable analogies to simplify complex ideas.

#     If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.

#     Ensure the summary is clear, accurate, and aligned with the provided style and length.
#     """,
#     input_variables=["paper_input","style_input","length_input"]
# )

# ADVANTAGES OF PromptTemplate
# 1. Reusability
# 2. Default validation
# 3. Chain creation
#fill the placeholders

template=load_prompt('template.json')
prompt=template.invoke({
    'paper_input':paper_input,
    'style_input':style_input,
    'length_input':length_input
})


if(st.button("Summarize")):
    st.write(llm.invoke([HumanMessage(content=prompt.to_string())]).content)
