FROM python:3.11-slim

WORKDIR /aigc

COPY ./ /aigc/

ENV TZ=Asia/Shanghai

RUN apt-get update && \ 
    apt-get install -y musl-dev bash vim && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/* && \
    echo $TZ > /etc/timezone

RUN pip install poetry==1.8.2
    
RUN poetry install --no-root --only main

RUN chmod +x /aigc/entrypoint.sh

EXPOSE 8080

ENTRYPOINT ["/aigc/entrypoint.sh"]