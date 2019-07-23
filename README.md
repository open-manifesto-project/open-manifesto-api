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


## API Documentation

```
http://localhost:5000/api/docs
```


## Tests

```
docker build -t oma .
docker run -ti --rm -v `pwd`:/app:z oma sh runtests.sh
```
