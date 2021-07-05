"""
writingディレクトリにある.md(マークダウンファイル)をhtmlに変換し、カテゴリーディレクトリに配置する
"""
import json
from datetime import datetime
import glob
import shutil
import subprocess
from os import path, mkdir, makedirs

WRITING_PATH = 'writing'


def get_article_md_file() -> str:
    """
    writing/ディレクトリ直下のマークダウンのファイル名を取得する
    @return: ファイル名文字列
    """
    all_path = glob.glob(path.join(WRITING_PATH, '*'))
    if len(all_path) != 1:
        raise RuntimeError

    return all_path[0]


class ConvertMarkDownToHTML:
    """
    マークダウンファイルをHTMLに変換し、カテゴリーディレクトリに配置する
    """
    def __init__(self):
        """
        初期化関数
        """
        self.md_file_path = get_article_md_file()
        self.file_name = None  # 拡張子を含まないファイル名
        self.md_content = None  # マークダウン形式記事文字列
        self.article_title = None  # 記事タイトル
        self.article_category = None  # 記事カテゴリー

        self.html_content = None  # HTML形式記事文字列

    def _read_article(self) -> None:
        """
        writing/xx.mdを読み込み文字列を返す
        """
        with open(self.md_file_path, 'r') as f:
            self.md_content = f.read()

    def _get_filename(self) -> None:
        """
        拡張子を含まないファイル名を取得する
        """
        self.file_name = path.splitext(path.basename(self.md_file_path))[0]

    def _get_title(self) -> None:
        """
        記事タイトルを取得する(マークダウンファイルの１行目)
        """
        self.article_title = self.md_content.split('\n')[0].lstrip('# ')

    def _get_category(self) -> None:
        """
        記事カテゴリーを取得する(マークダウンファイルの3行目の１つ目)
        """
        tags = self.md_content.split('\n')[2].split(' ')
        self.article_category = tags[0].strip('`')

    def _convert_md_to_html(self) -> None:
        """
        pandocコマンドを使ってmdファイルをhtmlファイルに変換する
        参考: https://dev.classmethod.jp/articles/pandoc-markdown2html/
        """
        # カテゴリーディレクトリが存在しない場合は作成する
        if not path.exists(self.article_category):
            mkdir(self.article_category)

        subprocess.run([
            "pandoc", "-s", "--toc", "--template=template/template.html",
            f"{self.md_file_path}", "-o", f"{self.article_category}/{self.file_name}.html"
        ])

    def _backup_md_file(self):
        """
        writingのmdファイルをバックアップする
        backup/category/xx.md
        """
        # カテゴリーディレクトリが存在しない場合は作成する
        backup_path = path.join('backup', self.article_category)
        if not path.exists(backup_path):
            makedirs(backup_path)
        # バックアップ
        shutil.move(self.md_file_path, backup_path)

    def execute(self):
        """
        ConvertMarkDownToHTMLのメイン関数
        """
        self._read_article()
        self._get_filename()
        self._get_title()
        self._get_category()
        self._convert_md_to_html()
        self._backup_md_file()
        url = f"https://diagonal-m.github.io/{self.article_category}/{self.file_name}.html"

        return self.article_title, url


class CreateIndex:
    """
    indexページを作成するためのクラス
    """
    def __init__(self, title, url, category, description):
        """
        初期化関数
        """
        self.title = title
        self.url = url
        self.category = category
        self.description = description
        self.parts_json = self._load_json()
        self.html_parts = """
        <div class="card">
            <div class="card-body" onclick="location = '{url}';">
                <h6 class="card-subtitle mb-2 text-muted">{date}/{category}</h6>
                <h5 class="card-title">{title}</h5>
                <p class="card-text">{description}</p>
            </div>
        </div>
        """
        self.html = None

    @staticmethod
    def _load_json() -> dict:
        """
        categories/category.jsonを辞書型として読み込む
        """
        with open("app/categories/category.json", "r") as f:
            parts_json = json.load(f)
        return parts_json

    def _update_json(self) -> None:
        """
        新しく追加された記事の情報をcategory.jsonに書き込む
        """
        self.parts_json[self.category][self.title] = {
            "date": datetime.today().strftime("%Y年%m月%d日"),
            "category": self.category,
            "description": self.description,
            "url": self.url
        }
        with open('app/categories/category.json', mode='w', encoding='utf-8') as f:
            json.dump(self.parts_json, f, indent=2)

    def create_html_str(self) -> None:
        """
        self.parts_jsonを元にhtml文字列を作成する
        """
        with open("app/base.html", 'r') as f:
            base_html = f.read()
        h2_base = ' <h2 id="{category}">{category}</h2>\n'
        parts = ""
        for category, articles in self.parts_json.items():
            html_parts = h2_base.format(category=category)
            for title, article_info in articles.items():
                html_parts += self.html_parts.format(
                    url=article_info["url"],
                    date=article_info["date"],
                    category=article_info["category"],
                    title=title,
                    description=article_info["description"]
                )
            parts += html_parts

        self.html = base_html.format(articles=parts)

    def _update_index_html(self):
        """
        index.htmlをアップデートする
        """
        with open("index.html", "w") as f:
            f.write(self.html)

    def execute(self):
        """
        メイン処理
        """
        self._update_json()
        self.create_html_str()
        self._update_index_html()


def main():
    """
    メイン関数
    """
    # 記事が存在しないときは処理を終える
    if len(glob.glob(path.join(WRITING_PATH, '*'))) == 0:
        return

    convert_md_html = ConvertMarkDownToHTML()
    title, url = convert_md_html.execute()
    print(title, url)


if __name__ == '__main__':
    main()
