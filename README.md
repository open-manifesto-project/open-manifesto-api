# open-manifesto-api

Open Manifesto API


## Requirements

* docker
* docker-compose


## Setup

```
git clone git@github.com:open-manifesto-project/open-manifesto-api.git
cd open-manifesto-api
docker-compose up -d
```

For expose api in other PORT, for example 5001:

```
PORT=5001 docker-compose up -d
```

## Load initial data

With docker-compose running you can exec the next command for load initial data:

```
docker exec -ti oma_web flask database initial FOLDER
```

FOLDER is a folder with .json files


## API Documentation

```
http://localhost:5000
```


## Tests

Run test:

```
docker-compose -f docker-compose-test.yml run test
```
