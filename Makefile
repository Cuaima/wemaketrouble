# -----------------------------
# Makefile for Django development
# -----------------------------

# Adjust these variables for your project
APP_NAME = user_profile         # e.g., 'myapp'
DB_NAME = db.sqlite3              # Change if using Postgres/MySQL
CACHE_DIR = __pycache__           # Django/Python cache directory

# Default target
all: reset

# Dump the database (SQLite example)
dump-db:
ifeq ($(DB_NAME),db.sqlite3)
	@echo "Dumping SQLite database to db_backup.sqlite3..."
	cp $(DB_NAME) db_backup.sqlite3
else
	@echo "Please customize database dump command for your DB."
endif

# Remove cache
clean-cache:
	@echo "Removing cache directories..."
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

# Delete migrations
clean-migrations:
	@echo "Deleting existing migrations..."
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete

# Create new migrations
makemigrations:
	@echo "Creating new migrations..."
	python manage.py makemigrations

# Apply migrations
migrate:
	@echo "Applying migrations..."
	python manage.py migrate

# Full reset target
reset: dump-db clean-cache clean-migrations makemigrations migrate
	@echo "Database reset and migrations recreated successfully."

build: 
	@echo "Building the project..."
	poetry install

nuclear: clean-cache clean-migrations makemigrations migrate
	@echo "Nuclear reset complete."

run:
	@echo "Running the development server..."
	python manage.py runserver