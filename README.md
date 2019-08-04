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

The first time, create database:

```
docker exec -u postgres -ti oma_db psql -c "create user manifesto password 'manifesto'"
docker exec -u postgres -ti oma_db psql -c "create database manifesto owner manifesto"
```



## API Documentation

```
http://localhost:5000/api/docs
```


## Tests

The first time, create test database:
```
docker-compose up -d
docker exec -u postgres -ti oma_db psql -c "create user manifesto password 'manifesto'"
docker exec -u postgres -ti oma_db psql -c "create database manifesto owner manifesto"
```

Run test:

```
docker run -ti --rm -v `pwd`:/app:z oma sh runtests.sh
```
