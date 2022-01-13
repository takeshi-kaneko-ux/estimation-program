# estimation-program

## 手順
1 特徴量を作成する　→ 2 推定する

### 1 特徴量を作成する
1. 教師ありデータとして使用するピアノ曲のMusicXMLファイルを用意する。同様に、教師なしデータとして使用するピアノ曲のMusicXMLファイルを用意する。そして、難易度を推定したいピアノ曲のMusicXMLファイルを用意する。
2. xml/Sディレクトリ内に、1.の教師ありデータとして使用するMusicXmlファイルを格納する。xml/Uディレクトリ内に、1.の教師なしデータとして使用するMusicXmlファイルを格納する。そして、xml/Nディレクトリ内に、1.の難易度を推定したピアノ曲のMusicXMLファイルを格納する。
3. configディレクトリに、教師ありデータとして使用するxmlファイル名がまとめられたテキストファイル（score_nameS.txt）と教師なしデータとして使用するxmlファイル名がまとめられたテキストファイル（score_nameU.txt）、そして難易度を推定したいピアノ曲のxmlファイル名がまとめられたテキストファイル（score_nameN.txt）を作成する。詳細は、score_name_sample.txtを参照。
4. プログラムのディレクトリ構造は下図のようになる。
5. ターミナル上でestimation-programディレクトリに移動し、**python prepare.py**と入力して実行する。しばらくすると、特徴量が作成され、csvファイルがdataディレクトリ内に保存される。
<img width="668" alt="ディレクトリ構造" src="https://user-images.githubusercontent.com/66774255/149289720-744ecd44-2f36-4207-9176-6600e393b82e.png">


### 2 推定する
1. estimation.pyファイルを開く。
2. 半教師あり学習を行う場合はflag変数をTrueに、教師あり学習を行う場合はflag変数をFalseに設定する。
3. 半教師あり学習を行う場合は閾値label_thetaを0.33から0.9の間で設定する。
4. num1とnum2の変数は、分類学習を行う際に必要となるrandom_stateの値を設定するものである。任意の数値を設定する。
5. 最後に、ターミナル上でestimation-programディレクトリに移動し、**python estimation.py**と入力して実行する。実行後、難易度を推定したいピアノ曲の推定結果が出力される。また、推定時に使用した学習モデルの精度（F値）も合わせて出力される。

## 作成者
KANEKO Takeshi
