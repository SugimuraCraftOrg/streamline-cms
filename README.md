# streamline-cms
The simple and intuitive headless CMS.

# For Execute on Local

## Sytem Requirements

* Docker
* Port 18000 on local. (see docker-compose.yml and configure if you needed.)

## Local Setup

Create .env file like .env.template.

```bash
cp .env.template .env
```

And run docker containers.

```bash
docker compose up -d
```

## Show API Specifications.

* see: http://localhost:18000/docs/

# For Development

## Run tests

```bash
pytest -v
```
