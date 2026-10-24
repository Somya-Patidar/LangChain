from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# basically append the history when new session is loaded
template=ChatPromptTemplate([
        ('system',"You are a helpful customer support agent"),
        MessagesPlaceholder(variable_name='chat_history'),   
        ('human','{query}')
])

chat_history=[]
with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())

# print(chat_history)

# final prompt
prompt=template.invoke({'chat_history':chat_history,'query':'Where is my refund'})
print(prompt)