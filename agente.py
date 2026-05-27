# agente.py
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

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

historial = [SystemMessage(content="Eres un asistente experto en mantenimiento náutico. Responde en español.")]

def chat(mensaje: str):
    historial.append(HumanMessage(content=mensaje))
    respuesta = llm_con_tool.invoke(historial)

    if respuesta.tool_calls:
        historial.append(respuesta)
        for call in respuesta.tool_calls:
            resultado = consultar_mantenimiento.invoke(call["args"])
            historial.append(ToolMessage(content=resultado, tool_call_id=call["id"]))
            print(f"[Tool] {call['name']}({call['args']}) → {resultado}")
        respuesta = llm_con_tool.invoke(historial)

    historial.append(respuesta)
    return respuesta.content

print(chat("¿Cada cuánto hay que revisar el motor?"))
print(chat("¿Y el casco?"))
print(chat("¿Cuál de los dos requiere revisiones más frecuentes?"))