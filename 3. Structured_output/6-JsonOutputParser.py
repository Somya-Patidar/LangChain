
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Problem: We can't enforce the schema

model = ChatOllama(
    model="qwen2.5:3b",
    base_url="http://127.0.0.1:11434"
)

parser=JsonOutputParser()

template = PromptTemplate(
    #format_instruction is not a variable but it just adds the prompt telling the reutrn format with help of parser
    template='Give me the name, age and city of a fictional person \n {format_instruction}',
    input_variables=[],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

#MANUAL see the prompt generated
# prompt = template.format()
# print("Prompt: ",prompt)--> Prompt:  Give me the name, age and city of a fictional person 
#                                       Return a JSON object.

# result=model.invoke(prompt)   #result contect is a dict
# print(type(result.content))
# final_res=parser.parse(result.content)
# print(final_res)

chain= template|model|parser
result=chain.invoke({})  #need to pass dict
print(result)