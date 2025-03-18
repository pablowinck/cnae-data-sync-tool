CNAE Data Synchronization Tool: Gerenciamento Automatizado de Dados da Classificação Nacional de Atividades Econômicas

Este projeto fornece uma solução conteinerizada para buscar e armazenar automaticamente os dados da Classificação Nacional de Atividades Econômicas (CNAE) a partir da API do IBGE (Instituto Brasileiro de Geografia e Estatística). Ele simplifica o processo de manutenção de um banco de dados local atualizado com as classificações do CNAE, essencial para aplicações empresariais brasileiras e conformidade regulatória.

A ferramenta recupera automaticamente os dados completos do CNAE, incluindo divisões e subclasses, e os armazena em um banco de dados MySQL com formatação adequada. Ela possui Docker containerization para facilitar a implantação, sincronização automática de dados e formatação padronizada dos códigos CNAE (formato XXXX-X/XX). O sistema é projetado para lidar com atualizações incrementais, evitando entradas duplicadas e garantindo a consistência dos dados.

⸻

Estrutura do Repositório

.
├── docker-compose.yml # Arquivo de composição do Docker definindo MySQL e serviços da aplicação
├── Dockerfile # Instruções de build do container para a aplicação Python
├── index.py # Script principal da aplicação, responsável por buscar e armazenar os dados do CNAE
└── requirements.txt # Dependências de pacotes Python para a aplicação

⸻

Instruções de Uso

Pré-requisitos
• Docker Engine 19.03.0+
• Docker Compose 1.27.0+
• 1GB de espaço em disco disponível (mínimo)
• Conexão com a Internet para acesso à API do IBGE

Instalação 1. Clone o repositório:

git clone <repository-url>
cd <repository-directory>

    2.	Inicie a aplicação usando Docker Compose:

docker-compose up -d

⸻

Guia Rápido 1. Verifique se os serviços estão rodando:

docker-compose ps

    2.	Verifique os logs da aplicação:

docker-compose logs -f app

    3.	Acesse o banco de dados MySQL:

docker exec -it cnae_mysql mysql -uroot -p1234 cnae_db

⸻

Exemplos Detalhados 1. Consultar os dados armazenados do CNAE:

SELECT codigo, descricao, ramo FROM CNAE LIMIT 5;

    2.	Buscar classificações específicas do CNAE:

SELECT \* FROM CNAE WHERE descricao LIKE '%comercio%';

⸻

Solução de Problemas

Problemas Comuns 1. Falha na Conexão com o Banco de Dados
• Problema: A aplicação não consegue se conectar ao MySQL
• Erro: “Erro ao conectar ao MySQL”
• Solução:

# Verifique se o container do MySQL está rodando

docker-compose ps mysql

# Verifique os logs do MySQL

docker-compose logs mysql

    2.	Problemas na Conexão com a API
    •	Problema: Não é possível buscar os dados do CNAE
    •	Erro: “Erro ao buscar dados da API”
    •	Solução:

# Verifique a conectividade com a API do IBGE

ping servicodados.ibge.gov.br

# Verifique os logs da aplicação

docker-compose logs app

⸻

Otimização de Performance
• Monitore a performance do MySQL:

docker exec cnae_mysql mysqladmin status

    •	O indexing do banco de dados é gerenciado automaticamente na coluna codigo
    •	Tempo médio de carregamento inicial dos dados: 2-5 minutos
    •	Tamanho esperado do banco de dados: ~50MB

⸻

Fluxo de Dados

A aplicação busca os dados do CNAE na API do IBGE, processa-os por meio de uma camada de validação e os armazena em um banco de dados MySQL. O processo inclui formatação automática dos códigos do CNAE e eliminação de entradas duplicadas.

[IBGE API] -> [Python App] -> [MySQL Database]
| | |
+-- JSON +-- Validation +-- Formatted
Data & Formatting Storage

Interações Principais dos Componentes: 1. A aplicação estabelece conexão com o MySQL utilizando environment variables 2. A API do IBGE é consultada para buscar divisões e subclasses 3. Cada entrada do CNAE é validada para verificar se já existe no banco 4. Novas entradas são inseridas com códigos formatados 5. Os dados são armazenados no MySQL com indexação apropriada 6. Health checks garantem a disponibilidade do banco de dados 7. O volume mounting assegura a persistência dos dados

⸻

Infraestrutura

Recursos do Banco de Dados
• MySQL 8.0 container
• Porta: 3306
• Database: cnae_db
• Volume: mysql_data
• Healthcheck: intervalo de 10s

Recursos da Aplicação
• Python 3.9 container
• Dependências: requests, mysql-connector-python
• Variáveis de ambiente para configuração do banco de dados
• Volume mounted para permitir atualizações no código

⸻

Deployment

Pré-requisitos:
• Docker e Docker Compose instalados
• Acesso à rede para a API do IBGE (servicodados.ibge.gov.br)

Configuração do Ambiente:
• Credenciais padrão do banco de dados estão definidas no docker-compose.yml
• Podem ser personalizadas através de environment variables:
• DB_HOST
• DB_USER
• DB_PASSWORD
• DB_NAME

Passos para Deploy:

# Build e inicialização dos serviços

docker-compose up --build -d

# Verificar se o deploy foi bem-sucedido

docker-compose ps

# Monitorar logs

docker-compose logs -f
