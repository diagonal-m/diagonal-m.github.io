# 【Ruby】ダッグタイピング

`ruby` 

ダッグタイピングについて



## ダッグタイピングとは

　動的型付け言語では実行前にそのメソッドが確実に呼び出されることを保証しようとする。そのため、コンパイル時にオブジェクトのデータ型をチェックし、特定のクラスを継承していたり、特定のインターフェースを実装していたりすればメソッドの呼び出しは可能、そうでなければNGとなる。

　一方、動的型付け言語では実行時にそのメソッドが呼び出せるかどうかを判断し、呼び出せないときにエラーが起きる。Rubyが気にするのは「コードを実行するその瞬間に、そのメソッドが呼び出せるか否か」であって、「そのオブジェクトのクラス(データ型)が何か」ではない。

例えば、次のようなメソッドがあったとする。

```ruby
def call_name(object)
  puts "Hello #{object.name}!"
end
```

　`call_name`メソッドは引数で渡されたオブジェクトが`name`メソッドを持っていること(object.nameが呼び出せること)を想定しており、それ以外のことは何も気にすることはない。そのため、以下のようにまったく別々のオブジェクトを渡すことができる。

```ruby
class User
  def name
    'Alice'
  end
end

class Product
  def name
    'a great movie'
  end
end
```

```ruby
# UserクラスとProductクラスはお互いに無関係なクラスだが、call_nameメソッドは何も気にしない。
user = User.new
call_name(user)
#=> Hello Alice!

product = Product.new
call_name(product)
#=> Hello a great movie!
```

　このように、オブジェクトのクラスがなんであろうとそのメソッドが呼び出だすことができればよしとするプログラミングスタイルのことを「ダックタイピング」と呼ぶ。これは「もしそれがアヒルのように歩き、アヒルのように鳴くのなら、それはアヒルである」という言葉に由来するプログラミング言語である。

　この考え方に基づくと、静的型付け言語でよく見かける具象クラスと抽象クラスのような区別もなくなる。

```ruby
class Product
  def initialize(name, price)
    @name = name
    @price = price
  end
  
  def call_text
    # stock?メソッドはサブクラスで必ず実装する想定
    stock = stock? ? 'あり' : 'なし'
    "商品名: #{@name} 価格: #{@price}円 在庫: #{stock}"
  end
end
```

　`call_text`メソッドに注目する。このメソッドでは在庫(stock)のあり/なしを表示させるメソッドである。ただし、在庫の確認は商品の種類によって確認方法が異なるため、サブクラスで必ず`stock?`メソッドを実装してもらうようにする。スーパークラスの`Product`クラスでは`stock?`メソッドを実装しない。以下は`Product`クラスを継承したCDクラスを定義するコードである。

```ruby
class CD < Product
  # 在庫があればtrueを返す
  def stock?
    true
  end
end
```

　ProductクラスとDVDクラスのそれぞれについて、実際にcall_textメソッドを呼び出してみる。

```ruby
product = Product.new('A great film', 1000)
# スーパークラスはstock?メソッドを持たないのでエラーが起きる
product.display_text
#=> NoMethodError: undefined method `stock?
cd = CD.new('A great music', 3000)
cd.call_text
#=> "商品名: A great music 価格: 3000円 在庫: あり"
```

　上記のコードのように、Productクラスではdisplay_textの呼び出しに失敗し、DVDクラスでは成功した。とはいえ、表面上はどちらも普通のクラス定義になっている。Productクラスが抽象クラスで、CDクラスが具象クラスだと見分ける構文はなく、Productクラスのインスタンス化も普通に行うことができる。

　Rubyが気にするのはあくまで`Stock?`メソッドが呼び出せるかどうかである。よって、`stock?`メソッドが呼び出せないProductクラスではエラーが発生し、呼び出せるCDクラスでは正常にメソッドが実行できた。

　このままだと、何も知らない人がProductクラスを使ったり、継承したりしたときに突然エラーが出現して驚いてしまうかもしれない。なので、Productクラス内でもstock?メソッドを定義し、わかりやすいエラーメッセージとともにエラーがを発生させる、といった手法をとることがあります。

```ruby
class Product
  def initialize(name, price)
    @name = name
    @price = price
  end
  
  def call_text
    # stock?メソッドはサブクラスで必ず実装する想定
    stock = stock? ? 'あり' : 'なし'
    "商品名: #{@name} 価格: #{@price}円 在庫: #{stock}"
  end
  
  def stock?
    # 「サブクラスでstock?メソッドを実装すること」というメッセージとともにエラーを発生させる
    raise 'Must implement stock? in subclass.'
  end
end
```

エラーは発生するが、エラーが起きた理由がより具体的に表示されるのでデバックはしやすくなる。

