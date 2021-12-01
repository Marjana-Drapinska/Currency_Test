FROM python:3.7 AS build
WORKDIR /Currency_Test

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENTRYPOINT ["pytest", "--log-cli-level=INFO", "./Tests/"]
