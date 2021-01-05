# eltrak

### Introduction
**eltrak** intends to become a free to use API to get shipping status for Greek courier services.
<br>Currently, it supports **ACS, Elta, Geniki Taxydromiki and Speedex Courier**. Due to lack of tracking numbers in a variety of states
to test with, some errors are to be expected.
<br>Other Greek courier services will follow, if I can find more tracking codes.

### Usage
Simply, perform a GET request to the following URL:

`http://api.trackingr.eu/v1/track/[COURIER]/[TRACKINGNUMBER]`

or

`https://eltrak.herokuapp.com/v1/track/[COURIER]/[TRACKINGNUMBER]`

For example in Python:
```
import requests
res = requests.get('http://api.trackingr.eu/v1/track/speedex/010011110101')
print(res.json())
```

### Installation

In order to run the server locally (or anywhere else) run the following commands:
1) Clone the repository and change directory:
```
git clone https://github.com/gntouts/eltrak.git
cd eltrak
```

2) Install requirements (it is recommended to use a virtual environment, see [venv](https://docs.python.org/3/library/venv.html) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)):
Because uvloop does not support Windows at the moment, you need to skip installing it if you are using a Windows machine.

For Windows:

```pip install -r windows-requirements.txt```

For Ubuntu and Debian:

```pip install -r requirements.txt```

3) Activate your environment (if you used one) and run the server

```uvicorn main:app --port=8888```

### Contributing
Any help is welcome. Even if you just provide me with test tracking numbers.

