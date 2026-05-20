# Makefile para o Projeto BackendTemplate
# -----------------------------------------
# Este Makefile simplifica a interação com o ambiente Docker e Django.
#
# Uso:
#   make <comando>
#
# Exemplo:
#   make up       # Inicia os contêineres Docker em segundo plano.
#   make migrate  # Executa as migrações do Django dentro do contêiner.
#   make test     # Roda os testes com pytest.
#

# --- Configurações ---
# Define o nome do serviço 'web' no docker-compose.yml para ser usado nos comandos.
SERVICE_NAME = web
# Define o comando base para executar comandos Python dentro do contêiner.
# Usamos 'poetry run' para garantir que o ambiente virtual correto seja usado.
PYTHON_EXEC = docker-compose exec $(SERVICE_NAME) python

.PHONY: help
help: ## ✨ Mostra esta ajuda.
	@awk 'BEGIN {FS = ":.*##"; printf "\n\033[1mComandos Disponíveis:\033[0m\n\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

##
## 🐳 Comandos do Docker
##--------------------------------------------------
.PHONY: up
up: ## 🚀 Inicia os contêineres Docker em segundo plano.
	@echo "🚀 Subindo os contêineres Docker..."
	docker-compose up -d --build

.PHONY: down
down: ## 🛑 Para e remove os contêineres Docker.
	@echo "🛑 Parando os contêineres Docker..."
	docker-compose down

.PHONY: logs
logs: ## 📜 Mostra os logs dos contêineres em tempo real.
	@echo "📜 Exibindo logs..."
	docker-compose logs -f

.PHONY: shell
shell: ## 💻 Acessa o terminal (shell) do contêiner da aplicação web.
@@ -55,48 +55,48 @@ reset: ## 💥 NUCLEAR: Para tudo, apaga volumes, imagens e cache. Use com cuida
## 📦 Comandos do Django
##--------------------------------------------------
.PHONY: migrate
migrate: ## 🏃 Executa as migrações do banco de dados (makemigrations e migrate).
	@echo "🔍 Gerando arquivos de migração..."
	docker-compose exec $(SERVICE_NAME) python manage.py makemigrations
	@echo "🏃 Aplicando migrações ao banco de dados..."
	docker-compose exec $(SERVICE_NAME) python manage.py migrate

.PHONY: superuser
superuser: ## 👤 Cria um novo superusuário.
	@echo "👤 Criando um novo superusuário..."
	docker-compose exec $(SERVICE_NAME) python manage.py createsuperuser

.PHONY: collectstatic
collectstatic: ## 🎨 Coleta os arquivos estáticos para produção.
	@echo "🎨 Coletando arquivos estáticos..."
	docker-compose exec $(SERVICE_NAME) python manage.py collectstatic --noinput

##
## ✅ Qualidade de Código e Testes
##--------------------------------------------------
.PHONY: test
test: ## 🧪 Roda todos os testes com pytest.
	@echo "🧪 Rodando testes com pytest..."
	docker-compose exec $(SERVICE_NAME) python -m pytest

.PHONY: coverage
coverage: ## 📊 Roda os testes e gera um relatório de cobertura de código.
	@echo "📊 Gerando relatório de cobertura de testes..."
	docker-compose exec $(SERVICE_NAME) python -m pytest --cov=. --cov-report=html

.PHONY: lint
lint: format check ## 💅 Roda todas as verificações de formatação e qualidade.

.PHONY: format
format: ## 🎨 Formata o código automaticamente com black e isort (DENTRO do contêiner).
	@echo "🎨 Formatando o código com black e isort..."
	docker-compose exec $(SERVICE_NAME) python -m black .
	docker-compose exec $(SERVICE_NAME) python -m isort .

.PHONY: check
check: ## 🧐 Verifica a formatação e a qualidade do código (DENTRO do contêiner).
	@echo "🧐 Verificando a qualidade do código..."
	docker-compose exec $(SERVICE_NAME) python -m flake8 .
	docker-compose exec $(SERVICE_NAME) python -m black --check .
	docker-compose exec $(SERVICE_NAME) python -m isort --check .

##
## 🌱 Dados Iniciais
##--------------------------------------------------
.PHONY: seed
seed: ## 🌱 Popula o banco com os planos de assinatura.
	@echo "🌱 Rodando seed de planos..."
	docker-compose exec $(SERVICE_NAME) python manage.py seed_plans


.PHONY: setup
setup: migrate seed ## ⚙️ Configura o ambiente: migra o banco e popula os dados iniciais.