# chain.py
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente experto en mantenimiento náutico. Responde en español de forma concisa."),
    ("human", "{pregunta}")
])

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

chain = prompt | llm

respuesta = chain.invoke({"pregunta": "¿Cada cuánto hay que revisar el motor de una embarcación?"})
print(respuesta.content)