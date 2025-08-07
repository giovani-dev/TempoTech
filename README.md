### Backend Developer (Python/Django)

**Teste 1: API de Clima**
Tempo estimado: 2-3 horas
API: OpenWeatherMap API (https://openweathermap.org/api)

**Requisitos:**
* Endpoint para buscar clima atual de uma cidade
* Cache de 10 minutos
* Histórico das últimas 10 consultas
* Rate limiting básico

**Requisitos Técnicos Mínimos:**
* Django REST Framework
* Redis para cache
* PostgreSQL
* 3 testes (unitário + integração)
* Docker compose

**Diferenciais:**
* Celery para tasks assíncronas
* Logs estruturados
* API documentation (Swagger)

---

**Links de Referência Adicionais:**

* **API de Clima Atual (OpenWeatherMap):** https://openweathermap.org/current
* **API de Geocodificação (OpenWeatherMap):** https://openweathermap.org/api/geocoding-api
* **API de Localidades (IBGE):** https://servicodados.ibge.gov.br/api/docs/localidades#api-_

---

### Critérios de Avaliação Simplificados

**Código e Arquitetura (40%)**
* Organização e clareza
* Boas práticas da linguagem
* Componentização/modularização

**Funcionalidade (30%)**
* Requisitos implementados
* Tratamento de erros
* UX básica

**Testes e Documentação (20%)**
* Testes dos pontos críticos
* README claro
* Comentários onde necessário

**DevOps Básico (10%)**
* Docker configurado
* Variáveis de ambiente
* Deploy funcional

---

### Instruções Simplificadas

**Início:**
* Criar repositório público no Github
* Criar conta nas APIs necessárias (sempre no tier gratuito)

**Entrega:**
* Link do repositório
* Link do deploy do projeto
* README com:
    * Como rodar local
    * Decisões técnicas principais
    * O que faria com mais tempo

**Prazo:** 1 a 2 dias

**Importante:**
* Preferimos código limpo a features extras
* Documente assumções e limitações
* Não precisa ser perfeito - queremos ver seu processo de pensamento

**Mais do que importante**
* Adicionar BackgroundTasks deve ser feito em outro momento devido a falta de tempo
* Explicar o porque nao vou utilizar Celery nesse caso de uso e sim o BackgroundTasks do FastApi
* Outro ponto importante que eu devo expor é o fato de eu usar a arquitetura 'Ports and Adapters'