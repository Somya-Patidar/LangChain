
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from typing import Literal
from pydantic import BaseModel,Field

load_dotenv()

#Giving the response based on Users feedback
# IT could have been better if we make agent which so some task based on sentiment of feedback instead of just replying back

model = ChatOpenAI()
parser = StrOutputParser()

class Feedback:
    sentiment: Literal["negative","positive"]=Field(description="Give the sentiment of the feedback")


parser2=PydanticOutputParser(pydantic_object=Feedback)

prompt1 = PromptTemplate(
    template='Classify the sentiment of the following feedback text into positive or negative \n {feedback} \n {format_instr}' ,
    input_variables=['feedback'],
    partial_variables={'format_instr':parser2.get_format_instructions()}
)

classifier_chain = prompt1 | model | parser2

prompt2 = PromptTemplate(
    template='Generate an appropriate response to this positive feedback \n {feedback}',
    input_variables=['feedback']
)

prompt3 = PromptTemplate(
    template='Write an appropriate response to this positive feedback \n {feedback}',
    input_variables=['feedback']
)

# branch_chain = RunnableBranch(
#     (condition1, chain1),
#     (condition2, chain2),
#     default_chain
# )

branch_chain=RunnableBranch(
    #x is a pydantic object from classifier_chain
    (lambda x:x.sentiment=="positive", prompt2|model|parser),
    (lambda x:x.sentiment=="negative", prompt3|model|parser),
    RunnableLambda(lambda x: "Could Not find the the sentiment")  #runnablelmabda converts lambda into runnable
)

chain=classifier_chain | branch_chain
res= chain.invoke({'feedback':"nice phone"})