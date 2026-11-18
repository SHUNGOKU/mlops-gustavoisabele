# Classificador de Spam — MLOps e Deploy

Projeto desenvolvido em dupla para a disciplina **MLOps e Deploy**, do curso técnico em Inteligência Artificial.

O objetivo é disponibilizar um modelo de Machine Learning que classifica mensagens em português como **spam** ou **não spam**, por meio de uma API e de uma interface web. A atividade enfatiza a disponibilização e a operação do modelo, e não a melhoria de sua acurácia.

## Funcionalidades e andamento

| Funcionalidade | Situação |
| --- | --- |
| Modelo de classificação treinado e armazenado em `model/modelo.joblib` | Disponível |
| API FastAPI com `GET /health` | Implementada e testada localmente |
| API FastAPI com `POST /predict` | Implementada; testes completos pendentes |
| Validação de entrada e autenticação opcional por chave | Implementadas no código |
| Página HTML servida pelo FastAPI | Acessível localmente |
| Integração dos controles da página com a API | Verificação pendente |
| Testes automatizados | Pendentes |
| Publicação na internet | Pendente |
| Monitoramento, Docker e CI/CD | Previstos para próximas etapas |

> **Situação do projeto:** versão inicial em desenvolvimento. Os itens marcados como pendentes não devem ser considerados entregues.

## Tecnologias utilizadas

| Tecnologia | Utilização e justificativa |
| --- | --- |
| Python | Linguagem utilizada para carregar o modelo e implementar a API. |
| FastAPI | Criação dos endpoints HTTP, validação das requisições e documentação interativa. |
| scikit-learn | Pipeline de Machine Learning com TF-IDF e Regressão Logística. |
| joblib | Carregamento do modelo previamente treinado. |
| HTML | Interface para utilização do classificador no navegador. |
| Uvicorn | Servidor de desenvolvimento para executar a aplicação FastAPI. |

O projeto usa a API e a interface no **mesmo servidor**, simplificando a comunicação local entre a página e os endpoints.

## Estrutura do projeto

```text
mlops-gustavoisabele/
├── app/
│   ├── __init__.py
│   └── main.py              # API, validações e entrega da página web
├── front/
│   └── index.html           # Página inicial (e seus arquivos auxiliares, se houver)
├── data/
│   └── mensagens.csv        # Base de treinamento
├── docs/
│   └── modelo_de_pagina.md  # Requisitos da interface
├── model/
│   ├── modelo.joblib        # Modelo fornecido para a atividade
│   ├── train.py             # Script de treinamento
│   └── exemplo_uso.py       # Exemplo de inferência em Python
├── .env.example             # Exemplo de configurações
├── .gitignore
├── requirements.txt
├── requirements-treino.txt
└── README.md
```

## Como executar localmente

### 1. Pré-requisitos

- Python instalado (recomendamos a versão **3.12**).
- Git, para clonar o repositório.
- Terminal, PowerShell ou terminal integrado do VS Code.

O arquivo do modelo foi preparado para **scikit-learn 1.8.0**, versão fixada em `requirements.txt`. Utilize as dependências do repositório para evitar incompatibilidades.

### 2. Obter o código

```bash
git clone https://github.com/SHUNGOKU/mlops-gustavoisabele.git
cd mlops-gustavoisabele
```

### 3. Criar o ambiente virtual

No **Windows (PowerShell)**:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

No **Linux/macOS**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 5. Iniciar a aplicação

Na pasta raiz, execute:

```bash
python -m uvicorn app.main:app --reload
```

Depois, acesse:

| Endereço local | Finalidade |
| --- | --- |
| <http://127.0.0.1:8000/> | Interface HTML |
| <http://127.0.0.1:8000/health> | Verificação de funcionamento |
| <http://127.0.0.1:8000/docs> | Documentação interativa e testes da API |

O endpoint `/predict` deve ser chamado pelo método **POST**, e não por acesso direto à barra de endereços.

## Configurações e chave de API

O código recebe configurações por variáveis de ambiente:

| Variável | Finalidade | Comportamento padrão |
| --- | --- | --- |
| `APP_ENV` | Identifica o ambiente (`dev`, `test` etc.). | `dev` |
| `MODEL_VERSION` | Versão apresentada nas respostas. | `v1` |
| `API_KEY` | Chave exigida no cabeçalho `X-API-Key` de `POST /predict`. | Se ausente, não exige chave. |
| `MODEL_PATH` | Caminho alternativo para o arquivo do modelo. | `model/modelo.joblib` |

O arquivo `.env.example` mostra o formato esperado. **Não publique o arquivo `.env` nem chaves reais no GitHub.**

**Atenção:** a função `os.getenv()` não lê um arquivo `.env` automaticamente. Na configuração atual, é possível definir as variáveis diretamente no terminal **antes** de iniciar o Uvicorn.

Exemplo no **Windows (PowerShell)**:

```powershell
$env:APP_ENV="dev"
$env:MODEL_VERSION="v1"
$env:API_KEY="chave-ficticia-para-teste"
python -m uvicorn app.main:app --reload
```

Exemplo no **Linux/macOS**:

```bash
export APP_ENV=dev
export MODEL_VERSION=v1
export API_KEY=chave-ficticia-para-teste
python -m uvicorn app.main:app --reload
```

Essas chaves são apenas exemplos de desenvolvimento. Em uma publicação online, as configurações deverão ser cadastradas como variáveis de ambiente no serviço de hospedagem.

## Contrato da API

### `GET /health`

Consulta o estado básico da aplicação. Não exige chave de API.

Resposta esperada (HTTP 200):

```json
{
  "status": "ok",
  "versao": "v1",
  "ambiente": "dev"
}
```

### `POST /predict`

Recebe um texto e devolve a classe prevista e a probabilidade estimada da classe escolhida.

Corpo da requisição:

```json
{
  "texto": "Parabéns! Você ganhou um prêmio, clique para resgatar"
}
```

Estrutura da resposta (valores ilustrativos):

```json
{
  "rotulo": "spam",
  "probabilidade": 0.67,
  "versao": "v1"
}
```

Validações e respostas previstas:

- **200:** classificação realizada.
- **401:** chave de API incorreta ou ausente, caso `API_KEY` esteja configurada.
- **422:** corpo inválido, texto vazio ou texto com somente espaços.

Quando houver autenticação, enviar o cabeçalho `X-API-Key` com a chave configurada. A chave **não** deve ficar escrita no código JavaScript da página; o usuário pode informá-la em um campo da interface.

## Como testar

Com a aplicação iniciada, acesse <http://127.0.0.1:8000/docs>:

1. Execute `GET /health` e confira se o resultado é HTTP 200.
2. Execute `POST /predict` com uma mensagem de propaganda ou golpe.
3. Repita `POST /predict` com uma mensagem cotidiana.
4. Envie `{"texto": "   "}` para conferir a rejeição da entrada inválida.
5. Com `API_KEY` configurada, repita o teste sem o cabeçalho `X-API-Key` (esperado: HTTP 401).
6. Acesse `/` para verificar se a página HTML é carregada.

Os resultados e evidências desses testes devem ser registrados conforme a implementação evoluir.

## Modelo e limitações

O classificador utiliza um pipeline **TF-IDF + Regressão Logística**. A base fornecida para a atividade contém **66 mensagens em português**, rotuladas como `spam` e `nao_spam`.

Como o conjunto de treinamento é pequeno, o modelo pode produzir classificações incorretas e probabilidades pouco confiáveis. Este projeto tem finalidade **educacional**, com foco em disponibilização, testes, configuração e operação do modelo.

Para treinar novamente (atividade opcional):

```bash
python -m pip install -r requirements-treino.txt
python model/train.py
```

O treinamento substitui o arquivo de saída do modelo; faça isso apenas quando a atividade exigir ou quando houver uma cópia de segurança.

## Próximas etapas

- [ ] Confirmar a integração de todos os botões da interface com a API.
- [ ] Executar testes de comportamento e registrar evidências.
- [ ] Documentar os testes e adicionar testes automatizados.
- [ ] Publicar API e interface em uma plataforma de hospedagem.
- [ ] Configurar variáveis de ambiente na hospedagem e testar a URL pública.
- [ ] Preparar a tag `v1` para a entrega da etapa.
- [ ] Desenvolver as próximas etapas de Docker, CI/CD e monitoramento, conforme orientação da disciplina.

**URL pública:** ainda não disponível.

## Equipe e divisão de tarefas

> Preencher estas informações antes da entrega final, sem atribuir atividades que não foram realizadas.

| Integrante | Responsabilidades e contribuições |
| --- | --- |
| [Nome do integrante 1] | [Descrever atividades realizadas] |
| [Nome do integrante 2] | [Descrever atividades realizadas] |

O histórico do Git deverá registrar contribuições dos dois integrantes. O professor deverá ser adicionado como colaborador do repositório, conforme as instruções da atividade.

## Licença

Projeto acadêmico. Nenhuma licença de reutilização foi definida até o momento.
