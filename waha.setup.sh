docker run --rm -v "$(pwd)":/app/env devlikeapro/waha init-waha /app/env

docker run -d --env-file "$(pwd)/.env" -v "$(pwd)/sessions:/app/.sessions" --rm -p 3000:3000 --name waha devlikeapro/waha

#visit http://localhost:3000/dashboard
#start new session