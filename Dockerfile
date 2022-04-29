FROM python:3.9
EXPOSE 80
RUN echo "deb http://deb.debian.org/debian/ unstable main contrib non-free" >> /etc/apt/sources.list.d/debian.list
RUN apt-get update
RUN apt-get install -y --no-install-recommends firefox
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./src /src
WORKDIR "/src"
RUN pip install -r req/requirements.txt
CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port",  "80"]