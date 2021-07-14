# 【Rails】rails consoleでSQL確認

 `rails` `Ruby on Rails` `sql`

rails consoleでSQLを実行する方法とメソッドのsql文字列を得る方法



## rails consoleでSQLを実行する

rails consoleでsqlを実行して、hash形式で実行結果を受け取る

```ruby
sql = "SELECT * FROM users"
hash = ActiveRecord::Base.connection.select_all(sql).to_hash
```



```bash
$ bin/rails c
```

```ruby
[1] pry(main)> sql = "SELECT * FROM users"
=> "SELECT * FROM users"
[2] pry(main)> hash = ActiveRecord::Base.connection.select_all(sql).to_hash
[{"id"=>1,
  "email"=>"satoichi@example.com",
  "crypted_password"=>"$2a$10$s4SH0ymEuVd02..B34pVh.Z5aGkHn5vGVfH.zRWojpoiVh/U8aFyq",
  "salt"=>"3py6sY7ahKW_JKxGchV4",
  "username"=>"satoichi",
  "created_at"=>2021-07-07 17:48:58 +0900,
  "updated_at"=>2021-07-07 17:48:58 +0900},
 {"id"=>2,
  "email"=>"elana@renner-bednar.co",
  "crypted_password"=>"$2a$10$hnYkbRruvyc8tEbzpxmXmeRgS2G9gCcM0TwPfB19iExawZvyKte4a",
  "salt"=>"nyqcLntLFjfhRWKm-F8t",
  "username"=>"oliva",
  "created_at"=>2021-07-09 10:00:32 +0900,
  "updated_at"=>2021-07-09 10:00:32 +0900},
 {"id"=>3,
  "email"=>"estefana@hessel.name",
  "crypted_password"=>"$2a$10$J70KhBMqwzMGpENHiKitveDbGTfb.0frZsxzbefZ29YTr4qiSNIRS",
  "salt"=>"y__g8L1-3SxicteQ6dsm",
  "username"=>"sandy_zemlak",
  "created_at"=>2021-07-09 10:00:32 +0900,
  "updated_at"=>2021-07-09 10:00:32 +0900},]
```



## メソッドのSQLの挙動を確認する

`to_sql`メソッドを使う

```bash
$ bin/rails c
```

```ruby
[1] pry(main)> user = User.first
[2] pry(main)> user.like_posts.to_sql
=> "SELECT `posts`.* FROM `posts` INNER JOIN `likes` ON `posts`.`id` = `likes`.`post_id` WHERE `likes`.`user_id` = 1"
```

整理すると

```sql
SELECT
  *
FROM
  posts
INNER JOIN
  likes
ON
  post.id = likes.post_id
WHERE
  likes.user_id = 1
;
```

というSQLが発行されていることがわかる。

