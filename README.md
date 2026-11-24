# Classificador de Spam — MLOps e Deploy

Projeto desenvolvido em dupla para a disciplina **MLOps e Deploy**, do curso técnico em Inteligência Artificial.

O objetivo é disponibilizar um modelo de Machine Learning que classifica mensagens em português como **spam** ou **não spam**, por meio de uma API e de uma interface web.

A atividade enfatiza a disponibilização, implantação e operação do modelo, e não apenas a melhoria de sua acurácia.

## Aplicação publicada

O projeto está disponível na internet por meio da plataforma Render.

**Link da aplicação:**

https://mlops-gustavoisabele-ix4w.onrender.com/

**Tecnologia de hospedagem:** Render  
**Versão:** v1  
**Ambiente:** produção (prod)

## Funcionalidades e andamento

| Funcionalidade | Situação |
|---|---|
| Modelo de classificação treinado | Concluído |
| API FastAPI com GET /health | Implementada e testada |
| API FastAPI com POST /predict | Implementada e testada |
| Validação de entrada | Implementada |
| Autenticação opcional por chave | Implementada |
| Página HTML integrada à API | Testada |
| Testes locais de classificação | Concluídos |
| Publicação na internet | Concluída |
| Teste da API em produção | Aprovado |
| Teste de classificação online | Aprovado |
| Documentação | Em atualização |
| Tag de versão v1 no Git | Pendente |
| Docker, CI/CD e monitoramento | Próximas etapas |

## Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem de programação |
| FastAPI | Desenvolvimento da API |
| scikit-learn | Pipeline de Machine Learning |
| joblib | Carregamento do modelo treinado |
| HTML, CSS e JavaScript | Interface web |
| Uvicorn | Servidor da aplicação |
| Render | Hospedagem e implantação |
| python-dotenv | Carregamento das variáveis do arquivo .env |

O modelo utiliza TF-IDF e Regressão Logística para classificar as mensagens.

## Estrutura do projeto

```text
mlops-gustavoisabele/
├── app/
│   ├── __init__.py
│   └── main.py
├── front/
│   └── index.html
├── data/
│   └── mensagens.csv
├── docs/
│   └── modelo_de_pagina.md
├── model/
│   ├── modelo.joblib
│   ├── train.py
│   └── exemplo_uso.py
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-treino.txt
└── README.md
```

## Como executar localmente

### 1. Pré-requisitos

- Python instalado.
- Git.
- VS Code ou outro editor de código.

### 2. Clonar o repositório

```bash
git clone https://github.com/SHUNGOKU/mlops-gustavoisabele.git
cd mlops-gustavoisabele
```

### 3. Criar o ambiente virtual

No Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 4. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Configurar as variáveis de ambiente

Crie um arquivo `.env` na pasta principal, utilizando o `.env.example` como referência.

Exemplo:

```env
APP_ENV=dev
MODEL_VERSION=v1
API_KEY=sua-chave-de-teste
```

O arquivo `.env` não deve ser enviado ao GitHub. Utilize apenas chaves fictícias nos exemplos da documentação.

A aplicação utiliza `load_dotenv()` para carregar as configurações locais.

### 6. Iniciar a aplicação

Na pasta principal do projeto, execute:

```bash
python -m uvicorn app.main:app --reload
```

Acesse os seguintes endereços:

| Endereço | Finalidade |
|---|---|
| http://127.0.0.1:8000/ | Interface web |
| http://127.0.0.1:8000/health | Verificação da API |
| http://127.0.0.1:8000/docs | Documentação interativa |

## Configurações e variáveis de ambiente

| Variável | Finalidade |
|---|---|
| APP_ENV | Identifica o ambiente de execução |
| MODEL_VERSION | Identifica a versão do modelo |
| API_KEY | Define a chave de autenticação |
| MODEL_PATH | Define o caminho do arquivo do modelo |

Quando a variável `API_KEY` está configurada, o endpoint `/predict` exige a chave no cabeçalho `X-API-Key`.

Na hospedagem, as variáveis são configuradas diretamente no painel do Render.

**Importante:** não publique chaves reais ou o arquivo `.env` no GitHub.

## Contrato da API

### GET /health

Verifica se a aplicação está funcionando.

Resposta em produção:

```json
{
  "status": "ok",
  "versao": "v1",
  "ambiente": "prod"
}
```

### POST /predict

Recebe uma mensagem e retorna a classificação realizada pelo modelo.

Exemplo de requisição:

```json
{
  "texto": "Parabéns! Você ganhou um prêmio. Clique para receber!"
}
```

Exemplo de resposta:

```json
{
  "rotulo": "spam",
  "probabilidade": 0.68,
  "versao": "v1"
}
```

A resposta pode apresentar:

- HTTP 200: classificação realizada.
- HTTP 401: chave de API inválida ou ausente.
- HTTP 422: dados inválidos ou texto vazio.

## Implantação no Render

A aplicação foi publicada utilizando a plataforma Render, conectada ao repositório do GitHub.

Configurações utilizadas:

| Campo | Configuração |
|---|---|
| Serviço | Web Service |
| Linguagem | Python 3 |
| Branch | main |
| Build Command | pip install -r requirements.txt |
| Start Command | uvicorn app.main:app --host 0.0.0.0 --port $PORT |
| Plano | Free |

As variáveis de ambiente foram configuradas no painel do Render.

**Endereço público:**

https://mlops-gustavoisabele-ix4w.onrender.com/

## Testes realizados

Foram realizados testes locais e online para verificar o funcionamento do classificador.

### Testes locais

**Teste 1 — Mensagem de spam**

Mensagem: "PARABÉNS! Você ganhou um prêmio. Clique agora para receber!"

Resultado: spam.

Probabilidade: 0,68 (68%).

Tempo de resposta: 64 ms.

**Teste 2 — Mensagem comum**

Mensagem: "Olá, tudo bem? Gostaria de confirmar nossa reunião de amanhã."

Resultado: não spam.

Probabilidade: 0,58 (58%).

Tempo de resposta: 17 ms.

### Testes em produção

**Verificação da API**

O endereço `/health` foi acessado e retornou:

```json
{
  "status": "ok",
  "versao": "v1",
  "ambiente": "prod"
}
```

Resultado: aprovado.

**Teste de classificação online**

A mesma mensagem utilizada no primeiro teste local foi enviada pela interface publicada.

Resultado: spam.

Probabilidade: 0,68 (68%).

Tempo de resposta: 292 ms.

Os resultados demonstraram que o modelo conseguiu realizar a classificação tanto no ambiente local quanto no ambiente de produção.

O tempo de resposta online foi maior devido à execução da aplicação em um servidor remoto.

## Modelo e limitações

O classificador utiliza um pipeline composto por TF-IDF e Regressão Logística.

A base de treinamento disponibilizada para a atividade contém 66 mensagens em português, classificadas entre `spam` e `nao_spam`.

Como o conjunto de dados é pequeno, o modelo pode apresentar classificações incorretas e probabilidades pouco confiáveis.

O projeto possui finalidade educacional e demonstra as etapas de disponibilização, implantação e operação de um modelo de Machine Learning.

## Próximas etapas

- [x] Desenvolver a API.
- [x] Integrar o modelo de Machine Learning.
- [x] Criar a interface web.
- [x] Realizar testes locais.
- [x] Empacotar as dependências.
- [x] Publicar a aplicação no Render.
- [x] Testar a API em produção.
- [x] Testar a classificação online.
- [ ] Finalizar a documentação.
- [ ] Criar e registrar a tag v1 no Git.
- [ ] Desenvolver as próximas etapas de Docker, CI/CD e monitoramento, conforme orientação da disciplina.

## Considerações finais

O projeto permitiu colocar em prática conhecimentos de Machine Learning e MLOps, desde a integração do modelo com uma API até sua publicação em um ambiente de produção.

A implantação no Render possibilitou disponibilizar o classificador pela internet e verificar seu funcionamento fora do ambiente local, concluindo a etapa de empacotamento e implantação da aplicação.