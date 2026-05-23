#!/bin/bash
set -e
echo "Rodando migrations..."
python manage.py migrate
echo "Rodando seed..."
python manage.py seed_plans
echo "Pre-deploy concluído."