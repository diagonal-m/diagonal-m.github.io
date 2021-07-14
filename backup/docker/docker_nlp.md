# 【Docker】Pythonの自然言語処理開発環境構築

`docker` `python` `自然言語処理`

dockerで日本語の自然言語処理環境を構築する。



## 使用できるようになるライブラリ

- **mecab-python3**
- **cabocha-python**
- **gensim**
- **spacy**
- **ginza**

 

## 1. Dockerfile・requirements.txtの記述

`Dockerfile`

```dockerfile
FROM ubuntu:18.04

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo
ENV PYTHONIOENCODING "utf-8"
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y && \
    apt-get upgrade -y

RUN apt-get install -y python3 python3-pip make curl git libffi-dev cron vim wget tree language-pack-ja


# MeCab
WORKDIR /opt
RUN git clone https://github.com/taku910/mecab.git
WORKDIR /opt/mecab/mecab
RUN ./configure  --enable-utf8-only \
  && make \
  && make check \
  && make install \
  && ldconfig
WORKDIR /opt/mecab/mecab-ipadic
RUN ./configure --with-charset=utf8 \
 && make \
 && make install

# neolog-ipadic
WORKDIR /opt
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
WORKDIR /opt/mecab-ipadic-neologd
RUN ./bin/install-mecab-ipadic-neologd -n -y

# CRF++
RUN wget -O /tmp/CRF++-0.58.tar.gz 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ' \
    && cd /tmp/ \
    && tar zxf CRF++-0.58.tar.gz \
    && cd CRF++-0.58 \
    && ./configure \
    && make \
    && make install

# CaboCha
RUN cd /tmp \
  && curl -c cabocha-0.69.tar.bz2 -s -L "https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU" \
    | grep confirm | sed -e "s/^.*confirm=\(.*\)&amp;id=.*$/\1/" \
    | xargs -I{} curl -b  cabocha-0.69.tar.bz2 -L -o cabocha-0.69.tar.bz2 \
      "https://drive.google.com/uc?confirm={}&export=download&id=0B4y35FiV1wh7SDd1Q1dUQkZQaUU" \
  && tar jxf cabocha-0.69.tar.bz2 \
  && cd cabocha-0.69 \
  && export CPPFLAGS=-I/usr/local/include \
  && ./configure --with-mecab-config=`which mecab-config` --with-charset=utf8 \
  && make \
  && make install \
  && cd python \
  && python3 setup.py build \
  && python3 setup.py install \
  && cd / \
  && rm /tmp/cabocha-0.69.tar.bz2 \
  && rm -rf /tmp/cabocha-0.69 \
  && ldconfig

# pip
COPY requirements.txt /home
WORKDIR /home
RUN python3 -m pip install pip --upgrade \
    && python3 -m pip install -r requirements.txt
```

`requirements.txt`

```
mecab-python3==0.996.3
cabocha-python
gensim==3.8.1
spacy==2.2.4
ginza==3.1.2
scikit-learn==0.22.2
scipy==1.4.1
ipython
```



## 2. buildしてdockerイメージを作成する

イメージ名`nlp`としてdockerイメージを作成する。

```bash
$ ls
Dockerfile  requirements.txt
$ docker build -f Dockerfile -t hoge --no-cache .
```

`docker images`でDockerイメージ一覧を表示してイメージができていることを確認

```bash
$ docker images
REPOSITORY      TAG            IMAGE ID           CREATED                SIZE
nlp             latest         34fe1550f1cc       About a minute ago     5.35GB
```

 

## 3. コンテナを起動してコンテナに入る

```bash
$ docker run -it --name nlp --rm -v $(pwd):/home nlp:latest /bin/bash
root@4b45770ea0e2:/tmp$ pwd
/tmp
root@4b45770ea0e2:/tmp$ ls
Dockerfile  requirements.txt
```



## 4. Python・自然言語処理ライブラリが使用できることを確認

```bash
root@4b45770ea0e2:/tmp$ python -V
Python 3.8.2
root@4b45770ea0e2:/tmp$ ipython
```

**Mecab**

```python
In [1]: import MeCab

In [2]: m = MeCab.Tagger ("-Ochasen")

In [3]: print(m.parse ("すもももももももものうち"))
すもも スモモ すもも 名詞-一般   
も モ も 助詞-係助詞    
もも  モモ  もも  名詞-一般   
も モ も 助詞-係助詞    
もも  モモ  もも  名詞-一般   
の ノ の 助詞-連体化    
うち  ウチ  うち  名詞-非自立-副詞可能   
EOS
```

**Cabocha**

```python
In [1]: import CaboCha

In [2]: c = CaboCha.Parser()

In [3]: print(c.parseToString("太郎はこの本を二郎を見た女性に渡した。"))
  太郎は-----------D
      この-D       |
        本を---D   |
        二郎を-D   |
            見た-D |
            女性に-D
            渡した。
EOS
```

**gensim**

```python
In [1]: import gensim
In [2]: gensim.__version__
Out[2]: '3.8.1'
```

**spaCy**

```python
In [1]: import spacy

In [2]: nlp = spacy.load('ja_ginza')

In [3]: doc = nlp('spaCy はオープンソースの自然言語処理ライブラリです。学習済みの統計モデルと単語ベクトルが付属しています。')

In [4]: list(doc.sents)
Out[4]: [spaCy はオープンソースの自然言語処理ライブラリです。, 学習済みの統計モデルと単語ベクトルが付属しています。]

In [5]: list(doc.noun_chunks)
Out[5]: [spaCy, オープンソース, 自然言語処理ライブラリ, 学習済み, 統計モデル, 単語ベクトル]

In [6]: list(doc)
Out[6]: 
[spaCy,
 は,
 オープンソース,
 の,
 自然,
 言語,
 処理,
 ライブラリ,
 です,
 。,
 学習,
 済み,
 の,
 統計,
 モデル,
 と,
 単語,
 ベクトル,
 が,
 付属,
 し,
 て,
 い,
 ます,
 。]
```

 

