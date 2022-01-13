from bs4 import BeautifulSoup

import csv

import score
import data
import features


if __name__ == "__main__":
    score_path = ["score_nameS.txt", "score_nameU.txt", "score_nameN.txt"] # xmlファイル名がまとめられたテキストファイルのファイル名
    data_path = ["featuresS.csv", "featuresU.csv", "featuresN.csv"] # 特徴量をまとめるcsvファイルのファイル名
    xml_dir = ["xml/S/", "xml/U/", "xml/N/"] # xmlファイルが存在するディレクトリ名

    for i in range(len(score_path)):
        # 使用するデータのxmlファイル名を変数score_liに格納する
        with open("config/" + score_path[i]) as f: # xmlファイル名がまとめられたテキストファイルを読み込む
            scores_name = f.read()

        score_name = scores_name.splitlines() # 読み込んだファイルの1行分を取り出す
        score_li = []

        for j in range(len(score_name)): # 楽曲を「,」で区切っているため、楽曲ごとにscore_liに格納する
            s = score_name[j].split(",")
            for k in range(len(s)):
                score_li.append(s[k])
        
        # 特徴量をまとめるcsvファイルを作成する
        with open("data/" + data_path[i], "w", encoding="utf_8_sig") as f:
            writer = csv.writer(f)
            writer.writerow(["曲目", "作曲者", "音域_r", "音符数_r", "和音_r", "黒鍵_r", "臨時記号_r", "奏法記号_r", "音程_r", "移動_r",\
            "音の類似度_r", "音価の類似度_r", "音域_l", "音符数_l", "和音_l", "黒鍵_l", "臨時記号_l", "奏法記号_l", "音程_l", "移動_l",\
            "音の類似度_l", "音価の類似度_l", "難易度"])
        
        # Scoreクラスのインスタンスを格納するためのリストを用意
        obj_li = [] 

        # 1曲ずつ特徴量を作成し、csvファイルに書き込む
        for m in range(len(score_li)):
            # xmlファイルを読み込む
            xml_path = xml_dir[i] + score_li[m] + ".xml"
            soup = BeautifulSoup(open(xml_path,'r').read(), "lxml")

            # Scoreクラスのインスタンスを作成し、リストobj_liに格納する
            obj_li.append(score.Score())

            # データを取得する（取得したデータはインスタンス変数にセットされる）
            data.get_data(obj_li[m], soup, score_li[m])

            # 特徴量をまとめるcsvファイルに作成した特徴量を書き込む
            with open("data/" + data_path[i], "a", encoding="utf_8_sig") as f:
                writer = csv.writer(f)

                # 特徴量を作成してcsvファイルに書き込む
                writer.writerow(features.Features(obj_li[m], score_li[m]))

            print(score_li[m], " の特徴量作成完了")
        
        print("\n", data_path[i], "ファイル作成完了")
