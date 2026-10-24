
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

#PydanticOutputParser: StructuredOutputParser that uses Pydantic models to enforce schema validation 
# when processing LLM responses.

# *Why Use this?*

# - Strict schema enforcement
# - Type safety
# - Easy validation
# - Seamless integration

model = ChatOllama(
    model="qwen2.5:3b",
    base_url="http://127.0.0.1:11434"
)

class Person(BaseModel):
    name: str = Field(description='Name of the person')
    age: int = Field(gt=18, description='Age of the person')
    city: str = Field(description='Name of the city the person belongs to')

parser=PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template='Generate the name, age and city of a fictional {place} person \n {format_instructions}',
    input_variables=['place'],
    partial_variables={'format_instructions':parser.get_format_instructions()}
)

#MANUAL
# prompt=template.invoke({'place':'India'})
# print("Prompt: ",prompt)
# result=model.invoke(prompt)
# final_res=parser.parse(result.content)
# print(type(result.content))
# print(type(final_res))
# print(final_res)

chain=template|model|parser
result=chain.invoke({'place':"Korea"})
print(type(result))  #result is not dict/jon but a Pydantic onject
#You can convert it by: result.model_dump_json()
print(result)