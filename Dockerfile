# python3.9のイメージをダウンロード
FROM python:3.9-buster
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY ./requirements.txt ./requirements.txt

# pipを使ってrequirementsをインストール
RUN pip install -r requirements.txt

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]