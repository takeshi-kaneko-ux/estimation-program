import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

import csv

# 半教師あり学習を実行->True, 教師あり学習を実行->False
flag = True

# 閾値
label_theta = 0.9

# 設定
num1 = 0
num2 = 1

# 教師ありデータがまとめられたcsvファイル
file_name1 = "data/featuresS.csv"

# 教師なしデータがまとめられたcsvファイル
file_name2 = "data/featuresU.csv"

# 新規データがまとめられたcsvファイル
file_name3 = "data/featuresN.csv"


# データ読み込み、データフレーム作成
DF = pd.read_csv(file_name1)
x = DF[["音域_r", "音符数_r", "和音_r", "黒鍵_r", "臨時記号_r", "奏法記号_r", 
        "音程_r", "移動_r", "音の類似度_r", "音価の類似度_r", 
        "音域_l", "音符数_l", "和音_l", "黒鍵_l", "臨時記号_l", "奏法記号_l",
        "音程_l", "移動_l", "音の類似度_l", "音価の類似度_l"]]
y = DF["難易度"]

DF3 = pd.read_csv(file_name3)
x3 = DF3[["音域_r", "音符数_r", "和音_r", "黒鍵_r", "臨時記号_r", "奏法記号_r", 
        "音程_r", "移動_r", "音の類似度_r", "音価の類似度_r", 
        "音域_l", "音符数_l", "和音_l", "黒鍵_l", "臨時記号_l", "奏法記号_l",
        "音程_l", "移動_l", "音の類似度_l", "音価の類似度_l"]]

# データ分割
X_train, X_test, y_train, y_test = train_test_split(x.values, y.values, random_state=num1)

# 学習モデルの作成
rf = RandomForestClassifier(n_estimators=100, criterion="gini", max_features="auto", bootstrap="true", random_state=num2)

# 学習
rf.fit(X_train, y_train)

if not flag: # 教師あり学習で学習したモデルrfで推定
    # 学習モデルの評価
    y_test_pred = rf.predict(X_test)
    score = f1_score(y_test, y_test_pred, average="macro")

    # 新規データの難易度を推定
    y_pred = rf.predict(x3.values)

else: # 半教師あり学習で学習したモデルrf2で推定
    # 教師なしデータを読み込む
    DF2 = pd.read_csv(file_name2)
    x2 = DF2[["音域_r", "音符数_r", "和音_r", "黒鍵_r", "臨時記号_r", "奏法記号_r", 
        "音程_r", "移動_r", "音の類似度_r", "音価の類似度_r", 
        "音域_l", "音符数_l", "和音_l", "黒鍵_l", "臨時記号_l", "奏法記号_l",
        "音程_l", "移動_l", "音の類似度_l", "音価の類似度_l"]]
    y2 = DF2["難易度"]

    # 教師無しデータの難易度を推定
    X2 = x2.values
    y2_pred = rf.predict(X2)

    # 推定結果の確信度
    y2_proba = np.max(rf.predict_proba(X2), axis=1)

    # 確信度が閾値を超えた結果を取り出す
    y2_ex = X2[np.where(y2_proba > label_theta)]
    y2_pred_add = y2_pred[np.where(y2_proba > label_theta)]

    # 学習データの追加
    X_train = np.insert(X_train, -1, y2_ex, axis=0)
    y_train = np.insert(y_train, -1, y2_pred_add, axis=0)

    # 学習モデルの作成
    rf2 = RandomForestClassifier(n_estimators=100, criterion="gini", max_features="auto", bootstrap="true", random_state=num2)

    # 再度学習
    rf2.fit(X_train, y_train)

    # 学習モデル評価
    y_test_pred2 = rf2.predict(X_test)
    score = f1_score(y_test, y_test_pred2, average="macro")

    # 新規データの難易度を推定
    y_pred = rf2.predict(x3.values)

# 新規データがまとめられたファイルを再度読み込み
with open(file_name3, "r") as f:
    r = csv.reader(f)
    line = [row for row in r]

# 新規データの難易度を推定した結果を出力
print("難易度推定の結果")
for i in range(y_pred.size):
    result = ""
    if y_pred[i] == 1:
        result = "初級"
    elif y_pred[i] == 2:
        result = "中級"
    elif y_pred[i] == 3:
        result = "上級"
    print("{}({})：{}".format(line[i + 1][0], line[i + 1][1], result))
print("\n--------\n今回実行した学習モデルの精度：{}".format(round(score, 5)))
