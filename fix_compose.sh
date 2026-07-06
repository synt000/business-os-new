# Check if docker compose works
if ! command -v docker-compose &> /dev/null; then
    alias docker-compose='docker compose'
fi
