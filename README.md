# eltrak

## Introduction

**eltrak** intends to become a free to use API to get shipping status for Greek courier services.

Currently, it supports **ACS, Elta, Geniki Taxydromiki, Speedex Courier, Skroutz Last Mile and EasyMail Courier**. Due to lack of tracking numbers in a variety of states to test with, some errors are to be expected.

**Geniki Taxidromiki is causing Internal Server Errors due to Amazon Cloudfront blocking access from Heroku dynos. Trying to find a proxy solution.**

Other Greek courier services will follow, if I can find more tracking codes.

### Usage

Simply, perform a GET request to the following URL:

`https://eltrak.herokuapp.com/v2/track/[COURIER]/[TRACKINGNUMBER]`

For example in Python:

```python
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

   ```bash
   git clone https://github.com/gntouts/eltrak.git
   cd eltrak
   ```

2. Install requirements (it is recommended to use a virtual environment, see [venv](https://docs.python.org/3/library/venv.html) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)):
   Because uvloop does not support Windows at the moment, you need to skip installing it if you are using a Windows machine.

   For Windows:

   `pip install -r src/req/windows-requirements.txt`

   For Ubuntu and Debian:

   `pip install -r src/req/requirements.txt`

3. Activate your environment (if you used one) and run the server

   ```bash
   cd src
   uvicorn app:app --port=8888
   ```

#### Deploy to Docker

1. Clone the repository and change directory:

   ```bash
   git clone https://github.com/gntouts/eltrak.git
   cd eltrak
   ```

2. Build the Docker image from the Dockerfile

   `docker build -t eltrak .`

3. Start the container

   `docker run -dp 8888:80 eltrak`

#### Deploy to Heroku

1. Clone the repository and change directory:

   ```bash
   git clone https://github.com/gntouts/eltrak.git
   cd eltrak

2. Create a new app:

   ```bash
   heroku login
   heroku apps:create --region eu eltrak
   ```
3. Set your deployment method:
 
   ```bash
   heroku container:login
   heroku stack:set container -a eltrak
   heroku git:remote -a eltrak
   ```
5. Build and push your app to Heroku

   ```bash
   git push heroku main
   ```

#### Other methods

It is also possible to deploy to Caprover using the captain-definition and the dockerfile.

### Contributing

Any help is welcome. Even if you just provide me with test tracking numbers.
