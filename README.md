### Resumo do Projeto

Este projeto é uma API de clima e localização desenvolvida em Python, utilizando o framework FastAPI. A arquitetura segue o padrão "Ports and Adapters" para garantir modularidade e desacoplamento entre as camadas.

### Funcionalidades e Endpoints

A API oferece as seguintes funcionalidades, acessíveis através dos endpoints:

  - **`/api/v1/weather/current/{city_name}`**: Retorna o clima atual para uma cidade específica. Possui cache de 10 minutos para otimizar o desempenho. As consultas também são armazenadas para fornecer um histórico de buscas.
  - **`/api/v1/weather/history`**: Retorna uma lista paginada das 10 consultas de clima mais recentes. Este endpoint também possui cache de 10 minutos.
  - **`/api/v1/location/state`**: Retorna uma lista de todos os estados. O endpoint tem um limitador de taxa de 1 requisição a cada 10 segundos.
  - **`/api/v1/location/{state}/cities`**: Retorna uma lista paginada de todas as cidades em um estado específico. O endpoint tem um limitador de taxa de 1 requisição a cada 10 segundos.

A API se integra com as seguintes fontes de dados:

  - **IBGE Provider**: Utilizado para buscar listas de estados e cidades brasileiras.
  - **OpenWeatherProvider**: Responsável por obter coordenadas geográficas e dados de clima.

### Pilha de Tecnologias

O projeto é construído com as seguintes tecnologias:

  - **Linguagem**: Python 3.10.
  - **Framework**: FastAPI (versão 0.116.1).
  - **Servidor ASGI**: Uvicorn (versão 0.35.0).
  - **Banco de Dados**: PostgreSQL 15.
  - **ORM**: SQLModel (versão 0.0.24), com SQLAlchemy 2.0.42 como backend. O driver assíncrono para PostgreSQL é o `asyncpg` (versão 0.30.0) e a biblioteca de banco de dados para Python é `psycopg2` (versão 2.9.10).
  - **Cache e Limitação de Taxa**: Redis.
  - **Ferramentas de Desenvolvimento**:
      - `isort` (versão 6.0.1) para organização de imports.
      - `black` (versão 25.1.0) para formatação de código.
      - `pylint` (versão 3.3.7) para análise de código estática.
  - **Gerenciamento de Ambiente**: Poetry.
  - **Containerização**: Docker e Docker Compose.

### Estrutura do Projeto

A estrutura de diretórios é organizada para refletir a arquitetura "Ports and Adapters", separando a lógica de negócios da infraestrutura:

  - **`tempotech/api`**: Este diretório é o ponto de entrada da API. Ele contém toda a lógica de inicialização, configuração e roteamento dos endpoints.
      - `main.py`: É o arquivo principal que inicializa a aplicação FastAPI. Ele configura o `lifespan` para a inicialização do banco de dados, o Redis para cache e limitação de taxa, e inclui os roteadores de `weather` e `location`.
      - `deps/`: Contém os arquivos de injeção de dependência.
          - `database.py`: Gerencia a injeção de dependência para o repositório de localização do banco de dados (`LocationDbRepository`).
          - `provider.py`: Gerencia a injeção de dependência para o provedor de localização do país (`CountryProvider`).
          - `use_case.py`: Define as dependências para os casos de uso `SearchStateUseCase` e `SearchCityUseCase`.
      - `router/`: Contém os arquivos que definem os endpoints da API.
          - `location_router.py`: Define os endpoints para listar estados e cidades.
          - `weather_router.py`: Define os endpoints para obter o clima atual e o histórico de clima.
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
      - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:
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
      - Para subir os contêineres do Redis e PostgreSQL, execute o seguinte comando:
        ```bash
        docker compose -f docker/docker-compose.yml up db redis -d
        ```
          - O banco de dados PostgreSQL será configurado com o usuário `weather` e a senha `root@pwd123`, e o banco de dados `tempotech-db`.
          - O Redis será configurado com o usuário `developer` e a senha `abc@123`.
4.  **Aplicação (Docker build e Docker run)**:
      - Construa a imagem da aplicação a partir do diretório raiz do projeto:
        ```sh
        docker build -t tempo-tech-app -f docker/Dockerfile .
        ```
      - Execute o contêiner da aplicação, substituindo `"SUA_CHAVE_API_AQUI"` pela sua chave real da API OpenWeatherMap.
        ```sh
        docker run --name tempo-tech-app-container \
          -p 8080:8080 \
          --network tempo-tech-network \
          -e REDIS_HOST="redis-server" \
          -e REDIS_PORT="6379" \
          -e REDIS_USER="developer" \
          -e REDIS_PWD="abc@123" \
          -e OPEN_WEATHER_API_KEY="SUA_CHAVE_API_AQUI" \
          -e DB_ENGINE="POSTGRESQL" \
          -e DB_USER="weather" \
          -e DB_PWD="root@pwd123" \
          -e DB_HOST="postgres-server" \
          -e DB_PORT="5432" \
          -e DB_NAME="tempotech-db" \
          tempo-tech-app
        ```
    > **Observação**: Para a execução completa e simplificada, o método `docker compose up --build` é o recomendado, pois ele gerencia todos os serviços de uma só vez.

### Decisões de Design e Arquitetura

O projeto adota a arquitetura "Ports and Adapters" como base para a sua construção, focando em uma fundação sólida antes de implementar todas as funcionalidades. Para uma explicação detalhada das justificativas por trás desta e de outras decisões de design, consulte o arquivo **`JUSTIFICATIVAS.md`**.

  - **Arquitetura "Ports and Adapters"**: A principal motivação é separar a lógica de negócios do restante do código, facilitando a manutenção e a substituição de dependências externas.
  - **Endpoints de Clima Desabilitados**: A implementação foi adiada devido à complexidade em lidar com a ambiguidade de nomes de cidades e a dependência de serviços externos de geocodificação.
  - **Background Tasks**: O projeto opta por usar `BackgroundTasks` do FastAPI em vez do Celery para a task de inicialização do banco de dados, mantendo a simplicidade.
  - **Configuração do Pylint**: O Pylint foi configurado para desabilitar mensagens específicas (`unnecessary-pass`, `too-few-public-methods`, `missing-class-docstring`) e para seguir a formatação do Black.

### Licença

O projeto está sob a licença GNU General Public License, Versão 3.
