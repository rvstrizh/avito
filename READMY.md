# Avito

## Run database (docker)

docker run -d \
	--name hunting_db \
	-e POSTGRES_PASSWORD=123456 \
	-e POSTGRES_USER=user \
    -e POSTGRES_DB=hunting_new \
    -p 5432:5432 \
    -d \
	postgres:14.0-alpine