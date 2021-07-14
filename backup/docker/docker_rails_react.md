# 【Docker】rails6×react×MySQL環境構築

`docker` `ruby on rails` `react`

DockerでRails6×React×MySQLの開発環境を構築する。



## 1. 各種ファイルの準備

```bash
rails_react
├── api/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── Gemfile
│   └── Gemfile.lock
├── front/
│   └── Dockerfile
└── docker-compose.yml
```



#### docker-compose.yml

```yaml
version: '3'

services:
  db:
    image: mysql:5.7
    environment:
      - MYSQL_ALLOW_EMPTY_PASSWORD=yes
  phpmyadmin:
    image: phpmyadmin
    ports:
      - '1080:80'
    environment:
      - PMA_ARBITRARY=1
      - PMA_HOST=db
      - PMA_USER=root
  api:
    build: 
      context: ./api/
      dockerfile: Dockerfile
    command: /bin/sh -c "rm -f /myapp/tmp/pids/server.pid && bundle exec rails s -p 3000 -b '0.0.0.0'"
    image: rails:dev
    volumes:
      - ./api:/myapp
      - ./api/vendor/bundle:/myapp/vendor/bundle
    environment:
      TZ: Asia/Tokyo
      RAILS_ENV: development
    ports:
      - 3000:3000
    depends_on:
      - db
  front:
    build: 
      context: ./front/
      dockerfile: Dockerfile
    volumes:
      - ./front:/usr/src/app
    command: sh -c "cd react-app && yarn start"
    ports:
      - "8000:3000"
```



#### api/Dockerfile

```Dockerfile
FROM ruby:2.7
RUN apt-get update -qq && apt-get install -y nodejs mariadb-client shared-mime-info
RUN mkdir /myapp
WORKDIR /myapp
COPY Gemfile /myapp/Gemfile
COPY Gemfile.lock /myapp/Gemfile.lock
RUN bundle install
COPY . /myapp

# Add a script to be executed every time the container starts.
COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
EXPOSE 3000

# Start the main process.
CMD ["rails", "server", "-b", "0.0.0.0"]
```



#### Gemfile

```ruby
source 'https://rubygems.org'
gem 'rails', '~> 6.0.3', '>= 6.0.3.6'
```



#### entrypoint.sh

```sh
#!/bin/bash
set -e

# Remove a potentially pre-existing server.pid for Rails.
rm -f /myapp/tmp/pids/server.pid

# Then exec the container's main process (what's set as CMD in the Dockerfile).
exec "$@"
```



#### front/Dockerfile

```dockerfile
FROM node:12.18.2-alpine  
WORKDIR /usr/src/app
```



## 2. コマンド実行

```bash
$ docker-compose run api rails new . --force --no-deps --database=mysql --api
$ docker-compose build
$ docker-compose run --rm front sh -c "npm install -g create-react-app && create-react-app react-app"
```



#### api/config/database.ymlの書き換え

```yml
default: &default
  adapter: mysql2
  encoding: utf8mb4
  pool: <%= ENV.fetch("RAILS_MAX_THREADS") { 5 } %>
  username: root
  password:
  host: db

development:
  <<: *default
  database: myapp_development

# Warning: The database defined as "test" will be erased and
# re-generated from your development database when you run "rake".
# Do not set this db to the same as development or production.
test:
  <<: *default
  database: myapp_test
```



```bash
$ docker-compose up -d
$ docker-compose run api rake db:create
```

以上で環境構築完了。



### Rails: localhost:3000

[![Image from Gyazo](https://i.gyazo.com/49003fdf99343259057f9d583996e982.png)](https://gyazo.com/49003fdf99343259057f9d583996e982)



### React: localhost8000

[![Image from Gyazo](https://i.gyazo.com/52e852f81e69d12b454289eb391e3869.png)](https://gyazo.com/52e852f81e69d12b454289eb391e3869)



### phpMyAdmin: localhost:1080

[![Image from Gyazo](https://i.gyazo.com/4975dbc2a5d1213ebbc722660e1afbeb.png)](https://gyazo.com/4975dbc2a5d1213ebbc722660e1afbeb)

