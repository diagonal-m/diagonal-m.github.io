"""
writingディレクトリにある.md(マークダウンファイル)をhtmlに変換し、カテゴリーディレクトリに配置する
"""
import markdown
import glob
from os import path

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

    def _get_title(self) -> None:
        """
        記事タイトルを取得する(マークダウンファイルの１行目)
        """
        self.article_title = self.md_content.split('\n')[0].lstrip('# ')

    def _get_category(self) -> None:
        """
        記事カテゴリーを取得する(マークダウンファイルの2行目の１つ目)
        """
        tags = self.md_content.split('\n')[1].split(' ')
        self.article_category = tags[0].strip('`')

    def _convert_md_to_html(self):
        """
        md文字列をhtml文字列に変換する
        """
        self.html_content = markdown.markdown(self.md_content)

    def _create_html_file(self):
        """
        カテゴリーディレクトリにhtmlを作成する
        """
        file_name = path.splitext(path.basename(self.md_file_path))[0]
        with open(path.join(self.article_category, f"{file_name}.html"), 'w') as f:
            f.write(self.html_content)

    def execute(self):
        """
        ConvertMarkDownToHTMLのメイン関数
        """
        self._read_article()
        self._get_title()
        self._get_category()
        self._convert_md_to_html()
        self._create_html_file()


def main():
    """
    メイン関数
    """
    convert_md_html = ConvertMarkDownToHTML()
    convert_md_html.execute()
    print(glob.glob('test/*'))


if __name__ == '__main__':
    main()
