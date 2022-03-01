FROM python:3.9.10-alpine as base

RUN mkdir /svc
WORKDIR /svc

COPY src/req/requirements.txt .

RUN rm -rf /var/cache/apk/* && \
    rm -rf /tmp/*

RUN apk update

RUN apk add --update \
    python3 \ 
    pkgconfig \ 
    python3-dev \
    openssl-dev \ 
    libffi-dev \ 
    musl-dev \
    make \ 
    gcc \
    && rm -rf /var/cache/apk/* \
    && pip wheel -r requirements.txt --wheel-dir=/svc/wheels


FROM python:3.9.10-alpine

COPY --from=base /svc /svc
WORKDIR /svc

RUN pip install --no-index --find-links=/svc/wheels -r requirements.txt

EXPOSE 80

COPY ./src .

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port",  "80"]