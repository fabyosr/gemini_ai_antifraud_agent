import os
import streamlit as st

from google import genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
from datetime import date
import textwrap # Para formatar melhor a saída de texto
import requests # Para fazer requisições HTTP

GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"] 

# Configura o cliente da SDK do Gemini
client = genai.Client()
MODEL_ID = "gemini-2.0-flash"
# Cria um serviço de sessão em memória
session_service = InMemorySessionService()

# Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
async def call_agent(agent: Agent, message_text: str) -> str:
   
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = await session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run_async(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response

# Função auxiliar para exibir texto formatado em Markdown no Colab
def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

##########################################
# --- Agente 1: Agente Principal: Classificador de fraudes (CORE-ANTIFRAUD) --- #
##########################################

async def agente_core_antifraud(topico):

    core_antifraud = Agent(
        name="agente_core_antifraude",
        model="gemini-2.0-flash",
        instruction="""
        Você é um assistente especialista em anti fraudes. A sua tarefa é avaliar o tópico e determimnar se há indícios de padrões de golpes e engenharia social sendo aplicada no tópico.
        Após essa análise, gere um relatório sobre o counteúdo e sua conclusão, como golpe provável, suspeito, seguro ou indeterminado.
        Detecte padrões linguísticos típicos de engenharia social (urgência, medo, recompensa fácil, prazo final, você ganhou). Avalie o tom emocional/manipulativo.
        Junto do seu relatório final deve constar um prompt que será enviado para um agente de inteligência artificial que fará buscas sobre golpes similares na internet,
        este prompt final deve ser trabalhdo para que a busca na internet retorne resultados relevantes e com casos similares de golpes,
        anexe ao prompt a mensagem principal da fraude, com textos mais suspeitos, url, links, e-mails, números de telefones, cpf, cnpj, domínios, redes sociais caso sejam informados.
        """,
        description="Agente CORE-ANTIFRAUD, que avalia o texto em busca de padrôes de fraude e engenharia social",
        tools=[google_search]
    )

    entrada_do_agente_core_antifraud = f"Tópico: {topico}"

    lancamentos = await call_agent(core_antifraud, entrada_do_agente_core_antifraud)
    return lancamentos

################################################
# --- Agente 2: Especialista em buscas na internet --- #
################################################

async def agente_buscador(topico, lancamentos_buscados):
    buscador = Agent(
        name="agente_buscador",
        model="gemini-2.0-flash",
        # Inserir as instruções do Agente Planejador #################################################
        instruction="""
        Você é um especialista em investigação com forte expertise em consultas de golpes e fraudes em geral, você deve:
        usar a ferramenta de busca do Google (google_search) para identificar golpes similares ao proposto no tópico,
        Você também pode usar o (google_search) para encontrar mais informações sobre os temas e aprofundar.

        consultandos sites sobre fraudes, golpes, banco de dados de phishing, malwares, serviços como virustotal, google safe browsing,
        abuseipdb e serviços similares. verifique se as url, links, e-mails, números de telefones, cpf, cnpj, domínios, redes sociais, caso sejam informados no tópico, são suspeitos ou maliciosos.
        Aponte falsificações, domínios parecidos, e-mails spoofados. analise fóruns, sites de reclamções, redes sociais.

        Ao final, você irá escolher os temas mais relevante e similares ao tópico com base nas suas pesquisas
        e retornar esses temas, seus pontos mais relevantes, e um plano com os assuntos
        a serem abordados no post que será escrito posteriormente. Faça um resumo do tópico com sua análise.
        Este texto final deve conter um prompt que será enviado para um agente de inteligência artificial que fará fará uma análise contextual do seu texto final.
        """,
        description="Agente especialista em busca de internet",
        tools=[google_search]
    )

    entrada_do_agente_buscador = f"Tópico:{topico}\nLançamentos buscados: {lancamentos_buscados}"
    # Executa o agente
    busca_result = await call_agent(buscador, entrada_do_agente_buscador)
    return busca_result

################################################
# --- Agente 2: Contextual --- #
################################################

async def agente_contextual(topico, busca_result):
    contextual = Agent(
        name="agente_buscador",
        model="gemini-2.0-flash",
        # Inserir as instruções do Agente Planejador #################################################
        instruction="""
        Você é um especialista em investigação com forte expertise em consultas de golpes e fraudes em geral,
        o tópico em questão é resultado de um trabalho de investigação de um agente de inteligência artificial especialista em investigação de golpes e fraudes,
        você deve:
        analisar o tópico em busca de padrões de fraudes e golpes, comparando o conteúdo com padrões legais ou práticas legítimas:

        ####

        exemplos:
        Ofertas de trabalhos não solicitadas com salários irreais.
        Pedidos de pagamentos antecipados por "taxasa administrativas".
        Empréstimos que exigem depósito prévio.

        Analise o tópico e verifique se o mesmo se encaixa em uma tentativa de golpe e faça uma conclusão se o mesmo é um golpe provável, suspeito, seguro ou indeterminado.
        """,
        description="Agente especialista em busca de internet",
        tools=[google_search]
    )

    entrada_do_agente_contextual = f"Tópico:{topico}\nResultados buscados: {busca_result}"
    # Executa o agente
    final_result = await call_agent(contextual, entrada_do_agente_contextual)
    return final_result

st.title("🤖 Gemini Fraud Detector Chatbot")
st.subheader("Cole ou digite a mensagem que você deseja verificar:")

# Área para o usuário inserir a mensagem
user_message = st.text_area("Mensagem:", height=200)

if st.button("Analisar Mensagem"):
    if user_message:
        st.markdown("---")
        st.subheader("Análise da Mensagem:")

        # --- Agente de Análise Linguística ---
        with st.spinner("Analisando padrões linguísticos..."):
            result_agent_core_antifraud = agente_core_antifraud(user_message)
            print(result_agent_core_antifraud)
            st.markdown("#### Agente de Análise Linguística:")
            st.markdown(result_agent_core_antifraud)
            st.info(result_agent_core_antifraud)
            st.markdown("---")

        # --- Agente Especialista em Busca de Golpes ---
        with st.spinner("Buscando informações relevantes..."):
            result_agent_buscador = agente_buscador(user_message, result_agent_core_antifraud)
            st.markdown("#### Agente Especialista em Busca de Golpes:")
            if result_agent_buscador:
                for i, result in enumerate(result_agent_buscador):
                    st.markdown(f"**Resultado {i+1}:**")
                    st.write(result) # Ajuste como você exibe os resultados da busca
            else:
                st.warning("Nenhum resultado de busca relevante encontrado.")
            st.markdown("---")
            
        # --- Agente Contextual ---
        with st.spinner("Contextualizando as informações..."):
            result_agent_contextual = agente_contextual(user_message, result_agent_buscador)

            st.markdown("#### Agente Contextual:")
            if "probabilidade" in result_agent_contextual.lower(): # Exemplo de como destacar a conclusão
                if "alta" in result_agent_contextual.lower():
                    st.error(result_agent_contextual)
                elif "baixa" in result_agent_contextual.lower():
                    st.success(result_agent_contextual)
                else:
                    st.warning(result_agent_contextual)
            else:
                st.info(result_agent_contextual)
            st.markdown("---")
    else:
        st.warning("Por favor, digite ou cole uma mensagem para análise.")
