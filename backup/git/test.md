# Github Actionsでdocker run

`git` `Github Actions` `docker` `python`

Github Actionsでpushをトリガーにdocker runでpythonスクリプトを実行し、Githubで設定した環境変数を出力する。



## Github Actionsとは

Githubから提供されているワークフローを自動化するためのツールであり、リポジトリの`.github/workflows`下にYAML形式のファイルを配置することで利用することができる。Linuxで利用されるcronによる定期実行やリポジトリへのpushをトリガーに、ワークフローを実行することができる。



## Githubの環境変数の設定

`リポジトリページ` → `Settings` → `Options/SecretsNew` → `New repository secret`で設定することができる。

[![Image from Gyazo](https://i.gyazo.com/c75d9b866eab1421fc04d8371fc59afb.png)](https://gyazo.com/c75d9b866eab1421fc04d8371fc59afb)

[![Image from Gyazo](https://i.gyazo.com/2ffb13fd0a099bd83309e6426ae8e774.png)](https://gyazo.com/2ffb13fd0a099bd83309e6426ae8e774)

[![Image from Gyazo](https://i.gyazo.com/2a18e14b26bc30b1eb3a344e0e3d500e.png)](https://gyazo.com/2a18e14b26bc30b1eb3a344e0e3d500e)



## ディレクトリ構成

```
actions_test
├── README.md
├── .github
│   └── workflows
│       └── docker-app.yml
├── app
│   └── app.py
└── Dockerfile
```





## `app/app.py`

```python
import os

# Github Actionsのコンソールで環境変数が出力されないため以下の形式でテスト
print("test_value" == os.environ.get('TEST'))
print("test" == os.environ.get('TEST'))
print("test_value_2" == os.environ.get('TEST2'))
```





## `docker/Dockerfile`

`Dockerfile`

```dockerfile
FROM python:3.8.2

# デフォルトの locale `C` を `C.UTF-8` に変更する
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# タイムゾーンを日本時間に変更
ENV TZ Asia/Tokyo

# 環境変数の設定
ARG test
ENV TEST=$test

# /tmpにappとdockerをコピー
COPY ../backup/git /tmp

# 相対パスの基準ディレクトリ
WORKDIR /tmp

CMD ["python3", "app/app.py"]
```





## `.github/workflows/docker-app.yml`

```yaml
name: DockerActions

on:
  push:
    branches: [ main ]

jobs:

  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Build the Docker image
      run: |
        docker build --build-arg test=${{ secrets.TEST }} -t actions --no-cache .
        

    - name: Run the Docker image
      run: |
        docker run -i -e "TEST2=${{ secrets.TEST2 }}" actions:latest
```





## git push

```bash
$ ls
Dockerfile  README.md   app/
$ git add .
$ git commit -m 'test'
$ git push
```





## 実行結果の確認

Github Actionsのコンソールで実行確認。出力結果が以下のようになっていれば成功。

```
True
False
True
```



[![Image from Gyazo](https://i.gyazo.com/8208d7dd906856c48adacf0fb29aeb43.png)](https://gyazo.com/8208d7dd906856c48adacf0fb29aeb43)

2通りの方法で環境変数が無事読み込めていることが確認できた



## ローカル実行時

```bash
$ docker build --build-arg test='test_value' -t actions --no-cache .
$ docker images
REPOSITORY           TAG       IMAGE ID       CREATED          SIZE
actions              latest    b2fd27cfdf6a   13 seconds ago   934MB
$ docker run -it --rm -e "TEST2=test_value_2" actions:latest                                
True
False
True
```

