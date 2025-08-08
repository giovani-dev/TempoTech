**Justificativas de Design e Arquitetura**

### Endpoints de Clima

É verdade que a ausência dos endpoints `/api/v1/weather/current/{city_name}` e `/api/v1/weather/history` pode parecer uma lacuna importante, especialmente considerando que eles seriam a essência de um serviço de previsão do tempo. No entanto, sua implementação não é trivial e foi adiada por razões bastante concretas e justificáveis.

O principal motivo para essa decisão é a necessidade intrínseca de trabalhar com a **localização e coordenadas geográficas das cidades**, e a garantia de que a precisão desses dados seja confiável. Criar um endpoint que aceite um nome de cidade (`city_name`) e retorne informações precisas sobre o clima é um desafio complexo.

Aqui está uma explicação detalhada dos motivos:

1.  **Ambiguidade dos Nomes de Cidades**: Nomes de cidades podem ser ambíguos. Pense em "Paris" (França ou Texas, EUA?) ou "Londres" (Inglaterra ou Ontário, Canadá?). Para resolver essa ambiguidade, o sistema precisa de um mecanismo para traduzir o nome da cidade em coordenadas geográficas (latitude e longitude) exatas.
2.  **Precisão da Geocodificação**: A precisão da localização é crucial. Um erro de poucos quilômetros na latitude ou longitude pode resultar em dados climáticos incorretos, especialmente em áreas com topografia variada (montanhas, costas, etc.). Implementar um serviço de geocodificação confiável e preciso, que possa lidar com diferentes idiomas, fusos horários e variações de escrita, exige tempo e esforço significativos.
3.  **Dependência de Fontes Externas**: Para obter dados climáticos, o sistema precisa de uma ou mais APIs de terceiros. A maioria dessas APIs exige coordenadas geográficas para fornecer a previsão do tempo. Portanto, antes de sequer pensar em consumir a API do clima, é necessário implementar uma etapa prévia que traduza o nome da cidade para as coordenadas.
4.  **Complexidade do Histórico de Dados**: O endpoint de histórico (`/history`) é ainda mais complexo. Não basta apenas buscar o clima atual; é necessário armazenar e gerenciar um banco de dados de informações climáticas ao longo do tempo. Isso levanta questões sobre o volume de dados, a periodicidade da coleta, a estrutura do banco de dados e a eficiência das consultas.

Em resumo, a implementação desses endpoints críticos foi adiada para garantir a qualidade e a confiabilidade do serviço. O objetivo é construir uma base sólida, começando com a resolução do problema de geolocalização, para então fornecer dados climáticos precisos e consistentes.

### Arquitetura "Ports and Adapters"

A frase "focar primeiro na fundação para depois construir" é o cerne da justificativa para a utilização de uma arquitetura sólida, como o **Padrão Hexagonal**, também conhecido como **Ports and Adapters**. Este padrão é a base para a criação de um sistema que, desde o início, é projetado para ser robusto, flexível e de fácil manutenção, permitindo um desenvolvimento mais ágil e econômico a longo prazo.

#### O Padrão Hexagonal como "Fundação"

O Padrão Hexagonal defende a ideia de que o núcleo da aplicação (a "lógica de negócio") deve ser isolado e independente de tecnologias externas. Ele cria uma "fronteira" bem definida entre o que o sistema *faz* e o que o sistema *precisa*.

* **Portas (Ports)**: As portas definem a interface da sua aplicação. Elas são contratos que especificam como a aplicação se comunica com o mundo exterior. Existem portas de entrada (driven ports), que permitem que agentes externos, como uma API REST, chamem a aplicação, e portas de saída (driving ports), que permitem que a aplicação chame serviços externos, como um banco de dados ou uma API de terceiros.
* **Adaptadores (Adapters)**: Os adaptadores são a implementação concreta das portas. Eles são a "ponte" entre o núcleo da aplicação e as tecnologias externas. Um adaptador de entrada pode ser um controlador REST que traduz uma requisição HTTP para um comando interno da aplicação. Um adaptador de saída pode ser um repositório que traduz um objeto de domínio para uma consulta SQL no banco de dados.

#### O Impacto na Manutenção e na Implementação de Novas Features

A adoção do Padrão Hexagonal traz benefícios diretos que se alinham perfeitamente com a ideia de uma "fundação sólida":

1.  **Manutenção Mais Barata**:
    * **Isolamento de Problemas**: Como a lógica de negócio é isolada, um problema em um adaptador (por exemplo, uma mudança na API do Redis) não afeta a lógica central da aplicação. Isso torna a depuração e a correção de bugs muito mais rápidas e baratas.
    * **Substituição Simples**: A arquitetura permite que você substitua um adaptador por outro sem alterar o núcleo da aplicação. Se você decidir trocar o banco de dados PostgreSQL por MongoDB, basta criar um novo adaptador para o MongoDB que implemente a mesma porta, sem precisar reescrever a lógica de negócio.
2.  **Maior Velocidade na Implementação de Novas Features**:
    * **Foco no Essencial**: Com a lógica de negócio isolada, os desenvolvedores podem se concentrar em implementar as funcionalidades do sistema, sem se preocuparem com os detalhes técnicos de como eles interagem com a API ou o banco de dados.
    * **Facilidade de Teste**: A independência do núcleo da aplicação facilita a criação de testes de unidade robustos, que não dependem de um banco de dados real ou de uma conexão com a internet. Isso acelera o ciclo de desenvolvimento e garante que as novas features sejam implementadas sem introduzir novos bugs.
    * **Adição de Novas Funcionalidades**: O padrão facilita a adição de novas funcionalidades, como um novo endpoint ou um novo tipo de notificação, pois basta criar um novo adaptador para a nova tecnologia, sem impactar o resto do sistema.