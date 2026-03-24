# Mandato Aberto API

Bem-vindo(a) ao Mandato Aberto API! Este é um sistema back-end construído em Python moderno focado em transparência pública. Ele fornece dados abertos estruturados sobre deputados federais brasileiros, seus mandatos, atuações em órgãos (como comissões) e histórico de votações.

O projeto coleta, trata e expõe dados através de endpoints de alta performance, prontos para serem consumidos por aplicações front-end, painéis de análise ou aplicativos mobile.

## Tecnologias e Conceitos Aplicados

Este projeto se baseia em uma Arquitetura em Camadas (Routers, Services, Models e Schemas), garantindo Separação de Responsabilidades (Separation of Concerns) e fácil manutenção.

Principais tecnologias empregadas:
- [FastAPI](https://fastapi.tiangolo.com/): Framework web de altíssima performance para construção e roteamento da API.
- [SQLAlchemy](https://www.sqlalchemy.org/): ORM (Object-Relational Mapping) utilizado para modelagem e abstração do banco de dados relacional.
- [SQLite](https://www.sqlite.org/): Banco de dados leve e portátil, utilizado para armazenamento.
- [Alembic / Pydantic](https://docs.pydantic.dev/): Serialização, validação estrita de dados baseada em tipagem do Python e estrutura de respostas JSON.
- [Pandas](https://pandas.pydata.org/): Utilizado no processo de ETL (Extração, Transformação e Carga) para limpeza de grandes lotes de dados.
- [Acesso à Nuvem (Base dos Dados / Google BigQuery)](https://basedosdados.org/): Consumo direto de dados governamentais armazenados na nuvem através de queries em SQL otimizadas pelo supercomputador do BigQuery, trazendo dados em massa para o banco de dados local.

---

## Estrutura de Diretórios

```text
mandato-aberto/
|
|-- app/
|   |-- api/          # Definição e roteamento dos endpoints (Controllers)
|   |-- core/         # Configurações essenciais e gerência do banco de dados
|   |-- models/       # Modelos SQLAlchemy refletindo as tabelas reais do banco
|   |-- schemas/      # Modelos Pydantic (Validação das entradas e saídas da API)
|   |-- services/     # Lógica de negócio, filtros cruzados e processamento
|   |-- db_loader.py  # Script de carga de dados locais via arquivo CSV
|
|-- scripts/
|   |-- ingestor_votacoes.py # Rotina de Cloud: Busca dados direto do BigQuery para o SQLite
|
|-- data/             # Arquivos-fonte locais do governo (.csv) auxiliares
|-- main.py           # Ponto de entrada (Entrypoint) do aplicativo Web/Uvicorn
|-- requirements.txt  # Dependências do projeto
|-- mandato_aberto.db # Banco SQLite (gerado pelo banco local / ignorado em produção)
```

---

## Como rodar o projeto localmente

Siga o passo a passo abaixo para rodar a aplicação:

### 1. Clonar o repositório
```bash
git clone https://github.com/SEU-USUARIO/mandato-aberto.git
cd mandato-aberto
```

### 2. Criar e ativar o ambiente virtual (Recomendado)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Alimentar o Banco de Dados (ETL)

Você tem duas formas de trazer os dados governamentais para dentro do seu .db local:

#### Opção A: Carga de CSV Local
Se você baixou as planilhas da câmara salva em sua pasta /data:
```bash
python -m app.db_loader
```
Isto vai ler e formatar os dados localmente usando Pandas.

#### Opção B: Carga via Nuvem (Google Cloud BigQuery)
Se você quer preencher os registros gigantes de Votações baixando a forma mais atualizada direto da nuvem (projeto Base dos Dados):
```bash
python scripts/ingestor_votacoes.py
```
(Ele solicitará confirmação antes de rodar para manter o controle do seu Billing Google Cloud).

### 5. Iniciar a API
Com o banco populado por um dos métodos acima, inicie o servidor da API:
```bash
uvicorn main:app --reload
```
A API estará rodando no endereço: http://127.0.0.1:8000

---

## Documentação e Swagger UI

A API conta com documentação interativa automática (Doc Swagger / OpenAPI). Com o servidor rodando, acesse a URL abaixo em seu navegador para testar botões, enviar valores e ler detalhes sobre os JSONs de retorno:

http://127.0.0.1:8000/docs

---

## Endpoints Principais (Funcionalidades)

- GET /deputados/advanced_search
  Pesquisa multiparâmetro (Nome, UF do estado, Sigla do partido) e filtros de corte temporal sobrepostos.

- GET /deputados/analise_votos
  Buscador quantitativo do histórico do mandato. Computa dezenas de sessões num ano específico e consolida o comportamento do parlamentar (Soma total de votos "Sim", "Não", "Abstenção", etc).

---
Este projeto foi desenvolvido com foco em Ciência de Dados, Integração com Nuvem, Engenharia Back-end e Transparência Pública.
