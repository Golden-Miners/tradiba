#!/bin/bash
echo "Welcome to Tradiba v4.0 Installation Wizard"
echo "==========================================="
echo "Generating default configuration..."

cat <<EOF > .env
DATABASE_URL=postgresql://tradiba:tradiba@db:5432/tradiba
REDIS_URL=redis://redis:6379/0
ENVIRONMENT=production
ADMIN_EMAIL=admin@tradiba.local
ADMIN_PASSWORD=admin
EOF

echo ".env file generated successfully."
echo "You can now run 'docker compose up -d' to start the platform."
