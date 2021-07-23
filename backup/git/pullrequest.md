# プルリクエストの手順

`git` `Github` `プルリクエスト`

プルリクエストの手順



## 1. [開発者]リポジトリを自分のリポジトリにfork

Githubにあるリポジトリを自分のリポジトリにforkする。リポジトリにアクセスして、右上の「Fork」ボタンを押下。

<a href="https://gyazo.com/a0eafc970dbc7ee420a31bbd2881de3f"><img src="https://i.gyazo.com/a0eafc970dbc7ee420a31bbd2881de3f.png" alt="Image from Gyazo" style="zoom:50%;" /></a>

自分のリポジトリにフォーク(コピー)される。



## 2. [開発者]作業用のソースをcloneまたはpullする

```bash
$ git clone https://github.com/xxxx/yyyyy.git
$ cd repository_dict
(main)$ 
```



## 3. [開発者]作業用のブランチを作成する

```bash
(main)$ git checkout -b development
Switched to a new branch 'development'
(development)$ 
```



## 4. [開発者]機能追加、改修等作業



## 5. [開発者]作業が完了したらpushする

```bash
(development)$ git add .
(development)$ git commit -m 'commitmessage'
(development)$ git push
```



## 6. [開発者]プルリクエストを作成する

フォーク元のリポジトリを見ると、Compare & pull request」ボタンが現れているので押下

[![Image from Gyazo](https://i.gyazo.com/9a6bde29d153a29fca6e5e9900974aae.png)](https://gyazo.com/9a6bde29d153a29fca6e5e9900974aae)

　タイトルとコメントを記載して、`Create pull request`を押下

[![Image from Gyazo](https://i.gyazo.com/bcbfaa79180b376d10a368ed3e97738f.png)](https://gyazo.com/bcbfaa79180b376d10a368ed3e97738f)

