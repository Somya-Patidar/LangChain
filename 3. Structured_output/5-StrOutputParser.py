
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Here we are sending a query to LLM to generate report then send it back to LLM to get summary
### StrOutputParser

# This is the simplest output parser. it is used to parse the output of the LLM and
# return it as a plain string. It is useful, If we want to create the chains
model = ChatOllama(
    model="qwen2.5:3b",
    base_url="http://127.0.0.1:11434"
)

#1st prompt--> Report
template1=PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=['topic']
)


#2nd prompt--> summary
template2=PromptTemplate(
    template="Write a 5 line summary on the following text lines. \n {text}",
    input_variables=['text']
)

# MANUAL
# prompt1=template1.invoke({"topic","Black hole"})
# result1=model.invoke(prompt1)

# prompt2=template2.invoke({'text':result1.content})
# res=model.invoke(prompt2)
# print("\nSummary:")
# print(res.content)

parser=StrOutputParser()
chain= template1 | model | parser | template2 | model | parser  #last parser gets you just content

result=chain.invoke({'topic':"Black Hole"})
print(result)


