
# In the D: drive we have done the basic by creating api/payload on own 
# here langchain handles the http communication and constructs payload
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

#ChatPromptTemplate is used for sending the dynamic prompt in list of messages
#PromptTemplate was used for single msgs

# template=ChatPromptTemplate([
#     ('system',"You are a helpful {domian} expert ")
#     ('human',"Explain in simple terms, what is {topic}")
# ])

# MESSAGE PLACEHOLDER: generally use to maintain history : read about it

model=ChatOllama(
    model="qwen2.5:3b",
    base_url="http://127.0.0.1:11434"
)

# Dynamic system message template
template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful {domain} expert. "
              "Give short, direct answers in plain text.")
])

domain = input("Enter domain: ")

# Invoke only once because the domain stays fixed
system_prompt = template.invoke({"domain": domain})

# Maintain history manually
messages = list(system_prompt.to_messages())

while True:
    user_input=input("You: ")
    if user_input.lower()=="exit":
        break
    messages.append(HumanMessage(content=user_input))
    prompt = template.invoke({
        "domain": domain,
        "history": messages,
        "user_input": user_input
    })
    response=model.invoke(messages)
    print("AI: ", response.content)
    messages.append(AIMessage(content=response.content))
    messages.append(response.content)

print(messages)
