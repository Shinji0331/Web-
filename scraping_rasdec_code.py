import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from urllib.parse import urlparse
import sys

# *******************************************************************
# テーブルの情報をCSVへ出力する関数
# ------引数-----------
# １、strUrl  ：対象となるURL
# ２、filePath：出力CSVファイルパス
# --------------------
# *******************************************************************
def outputCsv(strUrl,filePath):

    try:
        # URLの指定
        html = urlopen(strUrl)
        bsObj = BeautifulSoup(html, "html.parser")

        # divを指定
        div = bsObj.findAll("div", {"class":"wb-contents"})[0]
        # テーブルを指定
        table = div.findAll("table", {"class":"tbl"})[0]
        # trを指定
        rows = table.findAll("tr")
        # インデックス初期化
        tmpIndexNo = 0

        # csvファイルを「追記モード」「1レコード間の空白行なしモード」開く
        with open(filePath, "a", newline="",encoding='utf-8') as file:
            writer = csv.writer(file)
            # trの数だけ繰り返す
            for row in rows:
                csvRow = []
                
                # 1行目はスキップ
                if tmpIndexNo == 0:
                    tmpIndexNo += 1
                    continue

                # tdの中のthを繰り返す
                for cell in row.findAll(['td', 'th']):
                    csvRow.append(cell.get_text())
                
                # 1行データを出力
                writer.writerow(csvRow)

                # インデックス更新
                tmpIndexNo += 1

    except Exception as ex:
        print("CSVファイル出力に失敗しました。")
        print(ex)
    

# *******************************************************************
# 北海道から沖縄までの<a>タグリンクを繰り返し、CSV出力関数を呼び出す
# ------引数-----------
# １、jlisCodeUrl  ：地方公共団体情報システム機構のURL
# ２、filePath：出力CSVファイルパス
# --------------------
# *******************************************************************
def selectPrefLink(jlisCodeUrl,filePath):


    try:
        # URLからドメインのみを取得する
        domain_url = '{url.scheme}://{url.netloc}'.format(url=urlparse(jlisCodeUrl))

        # URLの指定
        html = urlopen(jlisCodeUrl)
        bsObj = BeautifulSoup(html, "html.parser")

        # テーブルを指定
        table = bsObj.findAll("table", {"class":"listtbl"})[0]

        # trを指定
        aTags = table.findAll("a")

        # trタグの数だけ繰り返す
        for aTag in aTags:
            
            # 取得したurlとドメインを結合させて引数へ設定する
            outputCsv(domain_url + aTag.get("href"),filePath)

    except Exception as ex:
        print("<a>タグリンク先のURL取得に失敗しました。")
        print(ex)

# *******************************************************************
# メイン処理
# *******************************************************************
if __name__ == '__main__':

    # コマンドラインの引数を配列に格納
    args = sys.argv

    filePath = "rasdec_code.csv"
    strUrl = "https://www.j-lis.go.jp/spd/code-address/jititai-code.html"

    # Webスクレイピング呼び出し
    selectPrefLink(strUrl,filePath)

    print("処理が完了しました。")