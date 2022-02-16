FROM python:3.9
# Set port in env, so that Heroku can override if necessary
# ENV PORT=80
# EXPOSE $PORT
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./src /src
WORKDIR "/src"
RUN pip install -r req/requirements.txt
ENTRYPOINT [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port",  "80"]