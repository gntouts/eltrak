# eltrak

### Introduction

**eltrak** intends to become a free to use API to get shipping status for Greek courier services.
<br>Currently, it supports **ACS, Elta, Geniki Taxydromiki, Speedex Courier and Skroutz Last Mile**. Due to lack of tracking numbers in a variety of states
to test with, some errors are to be expected.<br>**Geniki Taxidromiki is causing Internal Server Errors due to Amazon Cloudfront blocking access from Heroku dynos. Trying to find a proxy solution.**
<br>Other Greek courier services will follow, if I can find more tracking codes.

### Usage

Simply, perform a GET request to the following URL:

`https://eltrak.herokuapp.com/v2/track/[COURIER]/[TRACKINGNUMBER]`

For example in Python:

```
import requests
res = requests.get('https://eltrak.herokuapp.com/v1/track/speedex/010011110101')
print(res.json())
```

Or if you don't know which courier has issued the tracking number you can use the following URL:

`https://eltrak.herokuapp.com/v2/track-all/[TRACKINGNUMBER]`


### Installation

#### Deploy locally

In order to run the server locally (or anywhere else) run the following commands:

1. Clone the repository and change directory:

```
git clone https://github.com/gntouts/eltrak.git
cd eltrak
```

2. Install requirements (it is recommended to use a virtual environment, see [venv](https://docs.python.org/3/library/venv.html) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)):
   Because uvloop does not support Windows at the moment, you need to skip installing it if you are using a Windows machine.

For Windows:

`pip install -r windows-requirements.txt`

For Ubuntu and Debian:

`pip install -r requirements.txt`

3. Activate your environment (if you used one) and run the server

`uvicorn main:app --port=8888`

#### Deploy to Docker

1. Clone the repository and change directory:
```
git clone https://github.com/gntouts/eltrak.git
cd eltrak
```

2. Build the Docker image from the Dockerfile

`docker build -t eltrak .`

3. Start the container

`docker run -dp 8888:80 eltrak`

#### Other methods

You can deploy to Heroku using the Procfile and runtime.txt. It is also possible to deploy to Caprover using the captain-definition and the dockerfile.

### Contributing

Any help is welcome. Even if you just provide me with test tracking numbers.
