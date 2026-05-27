# tool.py
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

@tool
def consultar_mantenimiento(sistema: str) -> str:
    """Devuelve el intervalo de mantenimiento de un sistema de la embarcación."""
    intervalos = {
        "motor": "Revisión cada 100 horas o anualmente",
        "casco": "Inspección visual cada 6 meses, limpieza anual",
        "velas": "Revisión antes de cada temporada",
        "electricidad": "Revisión anual de conexiones y batería",
        "seguridad": "Verificar equipos de seguridad cada 12 meses",
    }
    return intervalos.get(sistema.lower(), f"No tengo datos de mantenimiento para: {sistema}")

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
llm_con_tool = llm.bind_tools([consultar_mantenimiento])

respuesta = llm_con_tool.invoke([HumanMessage(content="¿Cada cuánto hay que revisar el casco?")])
print(respuesta.tool_calls)