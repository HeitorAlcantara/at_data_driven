# Football Analysis App ⚽ ★彡

## Visão Geral
Este é um aplicativo de análise de futebol que permite aos usuários explorar dados detalhados sobre partidas, jogadores e estatísticas utilizando a biblioteca `statsbombpy`. A aplicação foi desenvolvida com Streamlit para proporcionar uma interface interativa, permitindo que os usuários selecionem campeonatos, temporadas e partidas específicas para análise. Além de uma API no backend possibilitando algumas funcionalidades.

O aplicativo possui duas funcionalidades principais:
1. **Match Events**: Apresenta uma visão detalhada dos eventos de uma partida, incluindo estatísticas dos jogadores e informações gerais dos times.
2. **Narrative**: Oferece uma experiência interativa com um chatbot que utiliza inteligência artificial para responder perguntas sobre a partida, fornecendo insights detalhados e contextualizados.

## Features
- **Frameworks**: Streamlit, FastAPI, LangChain.
- **Custom Tools**: 
  - Ferramentas específicas para análise de futebol, como `search_team_information`, `get_match_details`, e `get_specialist_comments`.
- **Language Model**: Gemini 1-5 Flash, utilizado no chatbot da funcionalidade Narrative.

## Tools
O programa utiliza as seguintes ferramentas:

**Ferramentas específicas:**
   - `search_team_information`: Busca informações detalhadas sobre um time.
   - `get_match_details`: Retorna dados específicos de uma partida.
   - `get_specialist_comments`: Gera comentários especializados sobre a partida.
   - `self-ask-agent`: Permite ao chatbot interagir com perguntas mais complexas.
   - `wikipedia`: Utiliza informações da Wikipédia para contextualizar respostas.

## Como Funciona
Os usuários interagem com o aplicativo através de uma interface intuitiva. As funcionalidades são divididas em duas telas principais:

1. **Match Events**:
   - Exibe detalhes de eventos da partida, como gols, cartões, substituições e mais.
   - Mostra as estatísticas individuais dos jogadores, incluindo passes, chutes e posse de bola.

2. **Narrative**:
   - Permite aos usuários conversar com um chatbot treinado para responder perguntas sobre a partida, como desempenho de jogadores, decisões estratégicas e informações adicionais sobre os times.
   - O chatbot utiliza o modelo Gemini 1-5 Flash e integra ferramentas como Wikipedia para oferecer respostas precisas e enriquecidas.

Além disso, a aplicação possui endpoints desenvolvidos com FastAPI:

- **GET** `/match_summary/{competition_id}/{season_id}`
  - Retorna uma sumarização detalhada da partida.

- **POST** `/player_profile`
  - Cria um perfil de jogador, retornando nome, match_id e stats do jogador.

## Exemplo de execução
**Input:**
```
Selecione o campeonato: Premier League
Selecione a temporada: 2023/2024
Selecione a partida: Liverpool vs Manchester City
```

**Output:**
```
Match Events:
- Gol marcado por Mohamed Salah aos 23 minutos.
- Cartão amarelo para Kevin De Bruyne aos 45 minutos.

Narrative:
Pergunta: Qual foi o destaque do Liverpool na partida?
Resposta: Mohamed Salah se destacou com 1 gol e 2 assistências, contribuindo significativamente para a vitória do time.
```

## How to Run

1. **Instale as dependências:**
```python
pip install -r requirements.txt
```

2. **Crie um arquivo `.env` e configure as chaves de API necessárias (Gemini e outras ferramentas):**
```python
GOOGLE_API_KEY =
SERPER_API_KEY =
```

3. **Rode o programa:**
```python
cd src
streamlit run app.py 
```

> [!NOTE]
> Espere que a aplicação carregue completamente antes de fazer alguma mudança como escolher campeonato, season ou jogos.

> [!IMPORTANT]
> O chatbot na tela 'Narrative' dá erro ao tentar utilizar a tool `get_specialist_comments`. Alguma implementação no stats de cada jogador no arquivo `tools/football.py`.

## Conclusão
O Football Analysis App oferece uma solução poderosa para análise de futebol, combinando dados ricos da `statsbombpy` com interatividade e inteligência artificial. Ideal para entusiastas de futebol, analistas e profissionais, o aplicativo proporciona uma experiência única para explorar jogos e obter insights detalhados sobre o desempenho dos jogadores e equipes.
