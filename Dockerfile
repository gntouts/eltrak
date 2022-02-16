FROM python:3.9
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./src /src
WORKDIR "/src"
RUN pip install -r req/requirements.txt
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port",  "80"]