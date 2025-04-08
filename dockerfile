FROM python:3.12-slim

WORKDIR /app

ENV PATH=/app:$PATH
ENV TZ="Asia/Shanghai"

COPY . .

RUN pip install -r requirements.txt

VOLUME ["/src", "/dest"]

ENTRYPOINT ["python", "main.py"]