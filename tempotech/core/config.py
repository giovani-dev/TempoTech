"""
Módulo de configuração da aplicação.

Este módulo carrega as variádveis de ambiente a partir do arquivo `.env`,
centralizando todas as configurações essenciais para a aplicação.
Isso inclui credenciais de banco de dados, chaves de API e configurações
de serviços externos como Redis.
"""
import os

from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
"""
Host do servidor Redis, utilizado para cache e limitação de taxa.
"""
REDIS_PORT = os.getenv("REDIS_PORT")
"""
Porta do servidor Redis.
"""
REDIS_USER = os.getenv("REDIS_USER")
"""
Nome de usuário para autenticação no Redis.
"""
REDIS_PWD = os.getenv("REDIS_PWD")
"""
Senha para autenticação no Redis.
"""

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
"""
Chave da API do OpenWeatherMap, necessária para buscar dados de clima e coordenadas.
"""

DB_ENGINE = os.getenv("DB_ENGINE")
"""
Motor do banco de dados a ser utilizado (ex: 'POSTGRESQL').
"""

DB_USER = os.getenv("DB_USER")
"""
Nome de usuário para o banco de dados.
"""
DB_PWD = os.getenv("DB_PWD")
"""
Senha para o banco de dados.
"""
DB_HOST = os.getenv("DB_HOST")
"""
Host do servidor do banco de dados.
"""
DB_PORT = os.getenv("DB_PORT")
"""
Porta do servidor do banco de dados.
"""
DB_NAME = os.getenv("DB_NAME")
"""
Nome do banco de dados.
"""

COUNTRY = "BR"
"""
Código do país para o qual a aplicação está configurada, como 'BR' para Brasil.
"""