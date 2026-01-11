#!/bin/bash
# Run script for LeetCode Tutor application

echo "🎯 LeetCode Репетитор - Установка и запуск"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Install dependencies
echo "📚 Установка зависимостей..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден. Создайте его из .env.example"
    echo "   cp .env.example .env"
    echo "   Затем отредактируйте .env и добавьте свой OPENAI_API_KEY"
    exit 1
fi

# Initialize database
echo "🗄️  Инициализация базы данных..."
python -c "from models import init_db; init_db()"

echo ""
echo "✅ Установка завершена!"
echo ""
echo "Доступные команды:"
echo "  1. Парсинг задач:      python leetcode_parser.py"
echo "  2. Генерация решений:  python solution_generator.py"
echo "  3. Запуск веб-сервера: python app.py"
echo ""
echo "Для быстрого старта:"
echo "  1. Запустите парсер для загрузки задач"
echo "  2. Запустите генератор для создания решений"
echo "  3. Запустите веб-сервер и откройте http://localhost:5000"
