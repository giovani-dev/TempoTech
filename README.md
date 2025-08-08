### Resumo do Projeto

Este projeto é uma API de clima e localização desenvolvida em Python, utilizando o framework FastAPI. A arquitetura segue o padrão "Ports and Adapters" para garantir modularidade e desacoplamento entre as camadas. A API inclui endpoints para buscar informações de clima atual e histórico para cidades, além de endpoints para listar estados e cidades.

### Funcionalidades e Endpoints

A API oferece as seguintes funcionalidades, acessíveis através dos endpoints:

  - `/api/v1/weather/current/{city_name}`: Retorna o clima atual para uma cidade específica. Possui cache de 10 minutos para otimizar o desempenho.
  - `/api/v1/weather/history`: Retorna uma lista paginada das 10 consultas de clima mais recentes. Também possui cache de 10 minutos.
  - `/api/v1/location/state`: Retorna uma lista de todos os estados. O endpoint tem um limitador de taxa de 1 requisição a cada 10 segundos.
  - `/api/v1/location/{state}/cities`: Retorna uma lista paginada de todas as cidades em um estado específico. O endpoint tem um limitador de taxa de 1 requisição a cada 10 segundos.

A API se integra com as seguintes fontes de dados:

  - **IBGE Provider**: Utilizado para buscar listas de estados e cidades brasileiras.
  - **OpenWeatherProvider**: Responsável por obter coordenadas geográficas e dados de clima.

### Pilha de Tecnologias

O projeto é construído com as seguintes tecnologias:

  - **Linguagem**: Python 3.10
  - **Framework**: FastAPI (versão 0.116.1)
  - **Servidor ASGI**: Uvicorn (versão 0.35.0)
  - **Banco de Dados**: PostgreSQL 15
  - **ORM**: SQLModel (versão 0.0.24), com SQLAlchemy 2.0.42 como backend
  - **Cache e Limitação de Taxa**: Redis
  - **Ferramentas de Desenvolvimento**:
      - `isort` (versão 6.0.1) para organização de imports
      - `black` (versão 25.1.0) para formatação de código
      - `pylint` (versão 3.3.7) para análise de código estática
  - **Gerenciamento de Ambiente**: Poetry
  - **Containerização**: Docker e Docker Compose

### Estrutura do Projeto

A estrutura de diretórios é organizada para refletir a arquitetura "Ports and Adapters", separando a lógica de negócios da infraestrutura:

  - **`tempotech/api`**: Contém a configuração principal do FastAPI, a inicialização dos serviços e a definição dos roteadores (endpoints).
  - **`tempotech/core`**: Contém a lógica de negócios e as interfaces para abstrair a camada de infraestrutura.
      - **`interfaces`**: Define contratos para repositórios de banco de dados, provedores de localização e provedores de clima.
      - **`database`**: Contém a implementação dos repositórios para o PostgreSQL e os modelos de dados.
      - **`providers`**: Contém a implementação dos provedores de dados externos, como IBGE e OpenWeatherMap.
      - **`schemas`**: Contém os modelos de dados Pydantic utilizados em toda a aplicação.
      - **`use_case`**: Contém a lógica de negócios encapsulada, como a busca de cidades e estados.
  - **`docker`**: Contém a configuração do Docker Compose para os serviços Redis e PostgreSQL.

### Como Rodar o Projeto Localmente

1.  **Pré-requisitos**:

      - Docker e Docker Compose instalados.
      - Python 3.10 instalado.

2.  **Configuração do Ambiente**:

      - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente, conforme especificado em `tempotech/core/config.py`:
        ```
        REDIS_HOST="redis"
        REDIS_PORT="6379"
        REDIS_USER="developer"
        REDIS_PWD="abc@123"

        OPEN_WEATHER_API_KEY="SUA_CHAVE_API_AQUI" # Obtenha sua chave da API OpenWeatherMap

        DB_ENGINE="POSTGRESQL"
        DB_USER="weather"
        DB_PWD="root@pwd123"
        DB_HOST="db"
        DB_PORT="5432"
        DB_NAME="tempotech-db"
        ```

3.  **Execução com Docker Compose**:

      - Execute o seguinte comando para subir os contêineres do Redis, PostgreSQL e a aplicação:
        ```bash
        docker compose up --build
        ```
      - O banco de dados PostgreSQL será configurado com o usuário `weather` e a senha `root@pwd123`, e o banco de dados `tempotech-db`.
      - O Redis será configurado com o usuário `developer` e a senha `abc@123`.

### Decisões de Design e Arquitetura

  - **Arquitetura "Ports and Adapters"**: A principal motivação para esta arquitetura é separar a lógica de negócios do restante do código, facilitando a manutenção e a substituição de dependências externas.
  - **Background Tasks**: O projeto opta por usar `BackgroundTasks` do FastAPI em vez do Celery para a task de inicialização do banco de dados (`setup_db`). Esta decisão foi tomada para manter a simplicidade do projeto, visto que o Celery seria uma solução excessivamente complexa para o caso de uso atual.

### Licença

O projeto está sob a licença GNU General Public License, Version 3.