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

### Como Rodar o Projeto com Docker

Esta seção descreve como inicializar a aplicação e seus serviços dependentes usando Docker.

#### Usando Docker Compose (Método Recomendado)

O `docker-compose.yml` está configurado para orquestrar todos os serviços necessários (a aplicação, o banco de dados PostgreSQL e o Redis) com um único comando. O arquivo `docker-compose.yml` e o `Dockerfile` devem estar na pasta `docker`, enquanto os arquivos de configuração do projeto estão na raiz.

1.  **A partir do diretório raiz do projeto**, execute o seguinte comando para construir e iniciar os containers:
    ```sh
    docker compose -f docker/docker-compose.yml up --build
    ```
      - O comando `up` cria e inicia todos os serviços definidos no arquivo.
      - A flag `-f docker/docker-compose.yml` especifica o caminho para o arquivo de configuração.
      - A flag `--build` garante que a imagem da sua aplicação seja construída a partir do `Dockerfile` antes de iniciar o container.

#### Usando Comandos Docker Nativos

Se preferir gerenciar os containers manualmente, você pode construir e executar a imagem da sua aplicação separadamente. Note que você precisará garantir que o banco de dados e o Redis estejam em execução e acessíveis.

1.  **Construa a imagem da aplicação:**
    Execute o comando abaixo a partir do diretório raiz do projeto. Isso usará o `Dockerfile` na pasta `docker` para criar uma imagem chamada `tempo-tech-app`.
    ```sh
    docker build -t tempo-tech-app -f docker/Dockerfile .
    ```
2.  **Inicie os serviços de dependência (PostgreSQL e Redis):**
    A forma mais simples é usar o Docker Compose para iniciar apenas os serviços `db` e `redis`.
    ```sh
    docker compose -f docker/docker-compose.yml up db redis -d
    ```
3.  **Execute o container da aplicação:**
    Execute o comando a seguir, substituindo `"SUA_CHAVE_API_AQUI"` com sua chave real da API OpenWeatherMap. As variáveis de ambiente devem ser passadas manualmente.
    ```sh
    docker run --name tempo-tech-app-container \
      -p 8080:8080 \
      --network tempotech_tempo-tech-network \
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

### Licença

O projeto está sob a licença GNU General Public License, Version 3.