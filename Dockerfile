FROM python:3.12-slim

ENV UID=1000
ENV GID=1000

RUN groupadd -g $GID hostgroup && \
    useradd -r -u $UID -g hostgroup hostuser

WORKDIR /rpidash

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chown -R hostuser:hostgroup /rpidash

USER hostuser

EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]