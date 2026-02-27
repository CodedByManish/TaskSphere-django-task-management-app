#!/bin/bash

echo "🐳 TaskSphere - Docker Setup"
echo "======================================"

# Check Docker installation
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed!"
    exit 1
fi

echo "✓ Docker found: $(docker --version)"

# Create .env file if doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
fi

# Build and start containers
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting containers..."
docker-compose up -d

echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🗄️  Running migrations..."
docker-compose exec -T web python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
docker-compose exec web python manage.py createsuperuser

# Collect static files
echo "📁 Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo ""
echo "✅ Docker setup complete!"
echo "🌐 Visit http://localhost:8000"
echo ""
echo "Useful commands:"
echo "  docker-compose logs -f web      # View logs"
echo "  docker-compose down             # Stop containers"
echo "  docker-compose ps               # List containers"