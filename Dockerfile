FROM python:3.12-slim

WORKDIR /rpidash

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["./docker-entrypoint.sh"]