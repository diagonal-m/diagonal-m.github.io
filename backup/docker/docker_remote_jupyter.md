# 【Docker】リモートサーバでjupyter notebook

`docker` `python` `jupyter notebook` `リモート`

リモートサーバーで起動したjupyter notebookをローカルのブラウザで開けるようにする

## 1. Dockerfile・requirements.txtの記述

`Dockerfile`

```dockerfile
FROM python:3.8.2

# デフォルトの locale `C` を `C.UTF-8` に変更する
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# タイムゾーンを日本時間に変更
ENV TZ Asia/Tokyo

COPY . /tmp
WORKDIR /tmp

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
```

`requirements.txt`

```txt
jupyter
```



## 2. buildしてdockerイメージを作成する

イメージ名`hoge`としてdockerイメージを作成する.

```bash
$ ls
Dockerfile  requirements.txt
$ docker build -f Dockerfile -t hoge --no-cache .
```

`docker images`でDockerイメージ一覧を表示してイメージができていることを確認.

```bash
$ docker images
REPOSITORY      TAG            IMAGE ID           CREATED                SIZE
hoge            latest         768307cdb962       About a minute ago     886MB
```



## 3. ポート番号を指定してバックグラウンドでコンテナを作成

```bash
$ docker run --name hoge -it -d -v $(pwd):/tmp -p 8887:8887 hoge:latest /bin/bash
```

`docker ps`でコンテナが起動していることを確認

```bash
$ docker ps
CONTAINER ID   IMAGE      COMMAND      CREATED       STATUS        PORTS      
eacb5690788a   hk:latest "/bin/bash"  3 seconds ago  Up 2 seconds  0.0.0.0:8887->8887/tcp
```



## 4. コンテナに入る

`CONTAINER ID`を指定してコンテナに入る

```bash
$ docker exec -it eacb5690788a bash
root@eacb5690788a:/tmp$
```



## 5. ipythonを起動して、パスワードを作成する

```bash
root@eacb5690788a:/tmp$ ipython
In [1]: from notebook.auth import passwd
In [2]: passwd() # password生成  
Enter password: 
Verify password: 
Out[2]: 'sha1:e9e300ed2f8e:5ae7dacdabb25fb60436f4aa687910dc1e4c1010'
# jupterに入るときに入力するhash値
In [3]: quit()  # ipython終了
```



## 6. jupyter notebookのconfigファイル設定

```bash
tmp$ jupyter notebook --generate-config # jupyter notebook コンフィグファイルの生成
Writing default config to: /root/.jupyter/jupyter_notebook_config.py

tmp$ echo “c.NotebookApp.ip = ‘0.0.0.0’” >> $HOME/.jupyter/jupyter_notebook_config.py

tmp$ echo “c.NotebookApp.open_browser = False” >> $HOME/.jupyter/jupyter_notebook_config.py

tmp$ echo “c.NotebookApp.port = 8887” >> $HOME/.jupyter/jupyter_notebook_config.py

tmp$ echo “c.NotebookApp.password = u’sha1:e9e300ed2f8e:5ae7dacdabb25fb60436f4aa687910dc1e4c1010’” >> $HOME/.jupyter/jupyter_notebook_config.py
```



## 7. jupyter notebook起動

コンテナ起動時に指定したポート番号を指定する

```bash
tmp$ nohup jupyter notebook --port 8887 --ip=0.0.0.0 --allow-root &
```





## 8. ローカルホストとリモートサーバーを繋ぐ

以下ローカル実行

```bash
$ ssh -L [ローカルのポート番号(任意)]:localhost:8887 ユーザー名@サーバー名
```

e.g.) 

```bash
$ ssh -L 8889:localhost:8887 satoichi@111.22.33.44
```





## 9. ブラウザで開く

好きなブラウザで以下を入力

```
http://localhost:8889/
```





## 10. トークンを入力

リモートサーバー上の`nohup.out`というファイルから`token`を確認

```bash
tmp$  grep -i "token" nohup.out | tail -n 1
or http://127.0.0.1:8887/?token=35709607237510c97d1e42e90abb1fa39d769112478d13c3
```



jupyter notebookからtokenの入力を求められるため入力