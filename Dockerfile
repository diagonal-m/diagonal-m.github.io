FROM python:3.8.2

# デフォルトの locale `C` を `C.UTF-8` に変更する
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# タイムゾーンを日本時間に変更
ENV TZ Asia/Tokyo

COPY . /tmp
WORKDIR /tmp

RUN pip3 install --upgrade pip && pip3 install markdown
