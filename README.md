# Mandato Aberto API

Bem-vindo(a) ao Mandato Aberto API! Este é um sistema back-end construído em Python moderno focado em transparência pública. Ele fornece dados abertos estruturados sobre deputados federais brasileiros, incluindo mandatos, atuações em órgãos (como comissões) e histórico de votações.

O objetivo é facilitar o acesso da população brasileira a informações sobre atuação parlamentar, contribuindo para a educação política e o exercício da cidadania.

O projeto coleta, trata e expõe dados através de endpoints de alta performance, prontos para serem consumidos por aplicações front-end (com potencial de evolução para um portal completo), painéis de análise ou aplicativos mobile.

---

## Resumo

API backend desenvolvida com FastAPI para coleta, processamento e disponibilização de dados públicos de deputados federais brasileiros.

Foco em:
* Integração com dados governamentais
* Processamento em larga escala (ETL)
* Arquitetura escalável e organizada

---

## Tecnologias e Conceitos Aplicados

Este projeto se baseia em uma Arquitetura em Camadas (Routers, Services, Models e Schemas), garantindo Separação de Responsabilidades (Separation of Concerns) e fácil manutenção.

Principais tecnologias empregadas:
- [FastAPI](https://fastapi.tiangolo.com/): Framework web de altíssima performance para construção e roteamento da API.
- [SQLAlchemy](https://www.sqlalchemy.org/): ORM (Object-Relational Mapping) utilizado para modelagem e abstração do banco de dados relacional.
- [SQLite](https://www.sqlite.org/): Banco de dados leve e portátil, utilizado para armazenamento.
- [Alembic / Pydantic](https://docs.pydantic.dev/): Serialização, validação estrita de dados baseada em tipagem do Python e estrutura de respostas JSON.
- [Pandas](https://pandas.pydata.org/): Utilizado no processo de ETL (Extração, Transformação e Carga) para limpeza de grandes lotes de dados.
- [Acesso à Nuvem (Base dos Dados / Google BigQuery)](https://basedosdados.org/): Consumo direto de dados governamentais na nuvem através de queries SQL otimizadas pelo BigQuery.
- [Pytest](https://docs.pytest.org/): Framework de testes automatizados utilizado para garantir a estabilidade das regras de negócio através de testes unitários isolados com banco em memória.

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
|-- tests/            # Pasta de testes automatizados unitários
|   |-- conftest.py   # Configurações globais e fixtures do pytest (banco em memória)
|   |-- test_deputado_service.py # Casos de teste unitário do serviço de deputados
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
git clone https://github.com/DaniellySobral/mandato-aberto.git
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

⚠️ Observação: Requer configuração prévia de credenciais do Google Cloud.

Se você quer preencher os registros gigantes de Votações baixando a forma mais atualizada direto da nuvem:
```bash
python -m scripts.ingestor_votacoes
```
(Ele solicitará confirmação antes de rodar para manter o controle do seu Billing Google Cloud).

### 5. Iniciar a API
Com o banco populado por um dos métodos acima, inicie o servidor da API:
```bash
uvicorn main:app --reload
```
A API estará rodando no endereço: http://127.0.0.1:8000

### 6. Como rodar os testes automatizados
Para rodar a suíte de testes unitários isolados com banco de dados SQLite em memória através do pytest:
```bash
PYTHONPATH=. ./venv/bin/pytest tests/
```

---

## Documentação e Swagger UI

A API conta com documentação interativa automática (Doc Swagger / OpenAPI). Com o servidor rodando, acesse a URL abaixo em seu navegador para testar botões, enviar valores e ler detalhes sobre os JSONs de retorno:

http://127.0.0.1:8000/docs

---

## Endpoints Principais (Funcionalidades)

- GET /deputados/advanced_search
  Pesquisa multiparâmetro (Nome, UF do estado, Sigla do partido) e filtros de corte temporal sobrepostos.

- GET /deputados/analise_votos
  Buscador detalhado do comportamento de votação do parlamentar e histórico de partidos. 
  Retorna o partido atual, total de mudanças partidárias (`total_mudancas_partido`), partidos passados (`partidos_anteriores`), resumo quantitativo de votos em determinado ano e a listagem de proposições votadas como "Sim" ou "Não" com status de aprovação na Câmara (`aprovada_na_camara`).

### Exemplo de Consulta (Terminal)

```bash
curl -s -X GET "http://127.0.0.1:8000/deputados/analise_votos?nome=Salles&ano=2023" | python -m json.tool
```

```json
[
  {
    "id_deputado": "220633",
    "nome": "Ricardo Salles",
    "partido_atual": "PL",
    "total_mudancas_partido": 1,
    "partidos_anteriores": [
      "NOVO"
    ],
    "uf": "SP",
    "resumo": {
      "sim": 12,
      "nao": 8,
      "abstencao": 0,
      "obstrucao": 0,
      "total": 20
    },
    "proposicoes_votadas_sim": [
      {
        "id_proposicao": "2349493",
        "descricao": "Aprovado o Requerimento de Urgência...",
        "aprovada_na_camara": true,
        "data": "2023-05-21T00:00:00"
      }
    ],
    "proposicoes_votadas_nao": [
      {
        "id_proposicao": "2200561",
        "descricao": "Mantido o texto...",
        "aprovada_na_camara": null,
        "data": "2023-12-15T00:00:00"
      }
    ]
  }
]
```

---

## Possíveis melhorias futuras

* Implementação de autenticação e segurança das rotas
* Deploy em ambiente cloud (AWS, GCP ou Azure)
* Criação de interface frontend para visualização em painéis interativos

---

## Sobre o desenvolvimento

Este projeto foi desenvolvido individualmente com foco em:
* Engenharia de software back-end moderna
* Integração com APIs e dados em nuvem (BigQuery)
* Arquitetura em camadas e organização refinada de código

Representa a aplicação prática de conceitos modernos de desenvolvimento, manipulação de banco de dados e transparência pública.
