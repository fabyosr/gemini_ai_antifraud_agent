# gemini_ai_antifraud_agent
Projeto contendo a criação de AI Agents utilizando o Gemini.

🛡️ Gemini Fraud Detector Agents
Este projeto utiliza o poder da inteligência artificial generativa Google Gemini para criar um sistema de agentes autônomos focado na identificação de mensagens potencialmente fraudulentas ou golpes. O objetivo principal é analisar uma mensagem de texto recebida e determinar, com alta probabilidade, se ela se trata de uma tentativa de fraude, combinando análise linguística, busca contextual na internet e avaliação de informações encontradas.

🎯 Objetivo do Projeto
O objetivo central deste projeto é fornecer uma ferramenta automatizada para auxiliar na detecção precoce de golpes e fraudes veiculados através de mensagens de texto (SMS, e-mail, mensagens em aplicativos, etc.). Ao empregar múltiplos agentes de IA com tarefas específicas, o sistema busca uma análise mais profunda e contextualizada do que seria possível com métodos tradicionais ou um único modelo de IA.

✨ Arquitetura e Agentes
O sistema é composto por três agentes principais, cada um com uma função distinta e colaborativa:

Agente de Análise Linguística:

Função: Este agente recebe a mensagem original e a analisa focando em padrões linguísticos comumente associados a golpes. Isso inclui:
Uso de linguagem urgente ou coercitiva.
Erros gramaticais ou de ortografia incomuns (comum em golpes internacionais).
Solicitações de informações pessoais ou financeiras sensíveis.
Promessas "boas demais para ser verdade".
Links ou anexos suspeitos.
Tecnologia: Utiliza o Google Gemini para processar a linguagem natural e identificar esses padrões.
Agente Especialista em Busca de Golpes:

Função: Com base em termos-chave extraídos da mensagem pelo Agente de Análise Linguística ou em informações suspeitas identificadas, este agente realiza buscas na internet (utilizando o Google Search) por menções a golpes similares, números de telefone associados a fraudes, reputação de remetentes (se aplicável, como endereços de e-mail), ou qualquer informação que possa corroborar ou refutar a suspeita de fraude.
Tecnologia: Integração com a API do Google Search ou ferramentas de web scraping controladas pelo Google Gemini.
Agente Contextual:

Função: Este agente atua como o "cérebro" final do processo. Ele recebe o relatório de análise linguística do Agente 1 e os resultados das buscas do Agente 2. Sua tarefa é sintetizar todas essas informações, contextualizá-las e gerar uma conclusão sobre a probabilidade da mensagem ser um golpe. Ele avalia a relevância dos resultados da busca em relação ao texto original e fornece uma explicação para sua decisão.
Tecnologia: Utiliza o Google Gemini para raciocínio complexo, síntese de informações e geração da conclusão final.
Fluxo Básico:

Mensagem Original -> Agente de Análise Linguística -> Termos/Padrões Suspeitos -> Agente Especialista em Busca -> Resultados da Busca + Termos/Padrões Suspeitos -> Agente Contextual -> Conclusão: É Golpe? (+ Justificativa)

🚀 Tecnologias Utilizadas
Google Gemini API: O coração dos agentes de IA para análise de texto, busca controlada por IA e contextualização.
Python: Linguagem de programação principal.
