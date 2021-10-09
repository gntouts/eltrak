FROM python:3.9
EXPOSE 80
RUN /usr/local/bin/python -m pip install --upgrade pip
COPY ./ /src
WORKDIR "/src"
RUN pip install -r requirements.txt
ENTRYPOINT [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]