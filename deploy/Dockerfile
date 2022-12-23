FROM python:3.10

RUN pip3 install poetry --no-cache-dir

RUN mkdir /app
WORKDIR /app
ADD gif_api gif_api
ADD pyproject.toml pyproject.toml

RUN poetry install --no-root --without dev

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

ADD deploy/start.sh start.sh
RUN chmod +x start.sh

EXPOSE 8000

CMD /wait && ./start.sh
