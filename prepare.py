from bs4 import BeautifulSoup

import csv

import score
import data
import features


if __name__ == "__main__":
    score_path = ["score_name.txt", "score1a_name.txt", "score1b_name.txt", "score2a_name.txt", "score2b_name.txt", "score3_name.txt"] # 白鍵の番号が書かれてあるファイルを読み込む
    data_path = ["features.csv", "features1a.csv", "features1b.csv", "features2a.csv", "features2b.csv", "features3.csv"]
    xml_dir = ["xml/", "xml/_ANotLabel/", "xml/_ANotLabel/", "xml/_BNotLabel/", "xml/_BNotLabel/", "xml/_CNotLabel/"]

    point = [5]
    # 0: 教師ありデータ
    # 1: 教師無し初級データ前半
    # 2: 教師無し初級データ後半
    # 3: 教師無し中級データ前半
    # 4: 教師無し中級データ後半
    # 5: 教師無し上級データ
    
    # with open("data/" + "measure_num.csv", "w", encoding="utf_8_sig") as f: # 特徴量のファイルを作成
    #     writer = csv.writer(f)
    #     writer.writerow(["小節数", "難易度"])

    for i in point:
        with open("config/" + score_path[i]) as f: # 楽曲をまとめたファイルの読み込み
            scores_name = f.read()

        score_name = scores_name.splitlines() # 読み込んだファイルの1行分を取り出す
        score_li = []

        for j in range(len(score_name)): # 楽曲を「,」で区切っているため、楽曲ごとにscore_liに格納する
            s = score_name[j].split(",")
            for k in range(len(s)):
                score_li.append(s[k])

        with open("data/" + data_path[i], "w", encoding="utf_8_sig") as f: # 特徴量のファイルを作成
            writer = csv.writer(f)
            writer.writerow(["曲目", "作曲者", "音域_r", "音符数_r", "和音_r", "黒鍵_r", "臨時記号_r", "奏法記号_r", "音程_r", "移動_r",\
            "音の類似度_r", "音価の類似度_r", "音域_l", "音符数_l", "和音_l", "黒鍵_l", "臨時記号_l", "奏法記号_l", "音程_l", "移動_l",\
            "音の類似度_l", "音価の類似度_l", "難易度"])
        
        obj_li = []

        for m in range(len(score_li)):
            xml_path = xml_dir[i] + score_li[m] + ".xml"
            soup = BeautifulSoup(open(xml_path,'r').read(), "lxml") # xmlファイルの読み込み
            obj_li.append(score.Score())
            data.extract_music(obj_li[m], soup, score_li[m]) # データを取得

            with open("data/" + data_path[i], "a", encoding="utf_8_sig") as f:
                writer = csv.writer(f)
                writer.writerow(features.Features(obj_li[m], score_li[m])) # 特徴量を作成

            print(score_li[m], " の特徴量作成完了")

            # with open("data/" + "measure_num.csv", "a", encoding="utf_8_sig") as f:
            #     writer = csv.writer(f)
            #     writer.writerow(features.Measures(obj_li[m], score_li[m]))
        
        print("\n", data_path[i], "ファイル作成完了")
    
    