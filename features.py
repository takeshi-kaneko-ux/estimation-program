import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import csv

import data # 黒鍵の特徴量を作成する際にimportする

import copy

def get_data(obj, obj_var, rest = -3):
    var_li = [[], []]
    for i in range(1, obj.get_measurenum() + 1):
        temp_var = [[], []] 
        temp_m_beat = [[], []] # 拍数
        for j in range(len(obj_var)):
            if obj.note_num[j] > rest:  # 休符は除く
                if obj.measure[j] == i:
                    if obj.staff[j] == 1:
                        temp_var[0].append(obj_var[j])
                        temp_m_beat[0].append(obj.m_beat[j])
                    elif obj.staff[j] == 2:
                        temp_var[1].append(obj_var[j])
                        temp_m_beat[1].append(obj.m_beat[j])

        for k in range(2):
            li = list(set(temp_m_beat[k]))
            li.sort()
            var_cl = []
            for _ in range(len(li)):
                var_cl.append([])
            
            for m in range(len(var_cl)):
                for n in range(len(temp_m_beat[k])):
                    if temp_m_beat[k][n] == li[m]:
                        var_cl[m].append(temp_var[k][n])
                var_cl[m].sort()

            var_li[k].append(var_cl)
    
    return var_li

def weak_beat(obj, mea, mb):
    weak = 0
    for p in range(len(obj.beats) - 1, -1, -1):
        if mea >= obj.beats[p][1]:
            if obj.beats[p][0] == 2:
                if 2 <= mb < 3:
                    weak += 1
            elif obj.beats[p][0] == 3:
                if 2 <= mb < 4:
                    weak += 1
            elif obj.beats[p][0] == 4:
                if 2 <= mb < 3 or 4 <= mb < 5:
                    weak += 1
            elif obj.beats[p][0] == 5:
                if 2 <= mb < 6:
                    weak += 1
            elif obj.beats[p][0] == 6:
                if 2 <= mb < 4 or 5 <= mb < 7:
                    weak += 1
            elif obj.beats[p][0] == 12:
                if 2 <= mb < 4 or 5 <= mb < 7 or 8 <= mb < 10 or 11 <= mb < 13:
                    weak += 1
            break
    return weak


def similarity(each_li):
    
    simi_li = []
    for i in range(len(each_li) - 1):
        a_measure = each_li[i]
        b_measure = each_li[i + 1]
        temp_a_measure = copy.deepcopy(a_measure)
        temp_b_measure = copy.deepcopy(b_measure)
        
        ope_times = 0
        max_num = 0
                
        a_len = len(temp_a_measure)
        b_len = len(temp_b_measure)
        dif_len = a_len - b_len
        for _ in range(np.abs(dif_len)):
            if dif_len > 0:
                temp_b_measure.append([0])
            elif dif_len < 0:
                temp_a_measure.append([0])
                
        for j in range(len(temp_a_measure)):
            a_note = temp_a_measure[j]
            b_note = temp_b_measure[j]

            a2_len = len(a_note)
            b2_len = len(b_note)
            dif2_len = a2_len - b2_len
            for _ in range(np.abs(dif2_len)):
                if dif2_len > 0:
                    b_note.append(0)
                elif dif2_len < 0:
                    a_note.append(0)
                    
            max_num += len(a_note)
            for k in range(len(a_note)):
                if a_note[k] != b_note[k]:
                    ope_times += 1
        
        simi_li.append(1 - (ope_times / max_num))
        
        each_li[i : i + 2] = []
        each_li.insert(i, a_measure)
        each_li.insert(i + 1, b_measure)
        

    return simi_li

def Measures(obj, score_li):
    return [obj.get_measurenum(), score_li.split("_")[0]]

def Features(obj, score_li):
    f_li = [obj.title, obj.creator]

    data_notenum = get_data(obj, obj.note_num, -1)
    data_accidental = get_data(obj, obj.accidental, -1)
    data_accent = get_data(obj, obj.accent, -1)
    data_staccato = get_data(obj, obj.staccato, -1)
    data_tenuto = get_data(obj, obj.tenuto, -1)
    data_strongaccent = get_data(obj, obj.strong_accent, -1)
    data_staccatissimo = get_data(obj, obj.staccatissimo, -1)
    data_measure = get_data(obj, obj.measure, -1)
    data_mbeat = get_data(obj, obj.m_beat, -1)
    data_notenum2 = get_data(obj, obj.note_num)
    data_notelen = get_data(obj, obj.note_len)

    for i in range(len(data_notenum)):
        each_notenum = []
        part_chord = 0
        each_blacknum = 0
        key = data.change_note()
        each_accidental = 0
        each_sign = 0 # 奏法記号の総数
        each_weaksign = 0 # 弱拍時における奏法記号の総数
        each_interval = []
        each_transition = []
        ave_transition = []
        each_measure1 = []
        each_measure2 = []
        remove_measure = []

        for j in range(len(data_notenum[i])): # 小節
            for k in range(len(data_notenum[i][j])): # 音符
                for l in range(len(data_notenum[i][j][k])): # 音符のたま
                    each_notenum.append(data_notenum[i][j][k][l])
                    
                    temp_blacknum = 0  # 黒鍵
                    for m in range(len(key)):
                        for n in range(len(key[m])):
                            if data_notenum[i][j][k][l] != key[m][n]:
                                temp_blacknum += 1
                    if temp_blacknum == 63:
                        each_blacknum += 1
                    
                    if data_accidental[i][j][k][l] > 0: # 臨時記号
                        each_accidental += 1
                    
                    if data_accent[i][j][k][l] == 1 or data_staccato[i][j][k][l] == 1 \
                        or data_tenuto[i][j][k][l] == 1 or data_strongaccent[i][j][k][l] == 1 \
                        or data_staccatissimo[i][j][k][l] == 1: # 奏法記号
                        each_sign += 1

                        each_weaksign += weak_beat(obj, data_measure[i][j][k][l], data_mbeat[i][j][k][l])
                    
                if len(data_notenum[i][j][k]) > 1: # 同拍に複数の音符があるか（和音の構成音であるか）
                    part_chord += 1
                
                each_interval.append(max(data_notenum[i][j][k]) - min(data_notenum[i][j][k])) # 音程 最大値と最小値の差
                each_transition.append(data_notenum[i][j][k])
            
            each_measure1.append(data_notenum2[i][j])
            each_measure2.append(data_notelen[i][j])
            
            if data_notenum2[i][j][0][0] == -2:
                remove_measure.append(j)
            
        
        for q in range(len(each_transition) - 1):
            max_dif = max(each_transition[q]) - max(each_transition[q + 1])
            min_dif = min(each_transition[q]) - min(each_transition[q + 1])
            ave_transition.append((np.abs(max_dif) + np.abs(min_dif)) / 2)
        
        
        f_li.append(np.std(np.array(each_notenum))) # 音域：全ての音符の鍵盤番号の標準偏差
        f_li.append(len(each_notenum) / obj.get_measurenum()) # 音符数：全ての音符数を小節数で割った値
        f_li.append(part_chord / len(each_notenum)) # 和音：全ての音符のうち和音を構成する音符数の割合
        f_li.append(each_blacknum / len(each_notenum)) # 黒鍵：全ての音符のうち黒鍵を打鍵する音符数の割合
        f_li.append(each_accidental / len(each_notenum)) # 臨時記号：全ての音符のうち臨時記号を伴う音符数の割合
        try:
            f_li.append(each_weaksign / each_sign) # 奏法記号：演奏記号を伴う音符のうち弱拍時における演奏記号を伴う音符数の割合
        except ZeroDivisionError:
            f_li.append(0)
        f_li.append(np.median(np.array(each_interval))) # 音程
        f_li.append(np.median(np.array(ave_transition))) # 移動
        for r in [each_measure1, each_measure2]: # 音の類似度、音価の類似度
            similarity_li = similarity(r)
            remove_index = []
            for s in remove_measure:
                if s != 0:
                    remove_index.append(s - 1)
                if s != len(similarity_li):
                    remove_index.append(s)
            remove_index2 = list(set(remove_index))
            remove_index2_r = sorted(remove_index2, reverse=True)
            for t in remove_index2_r:
                del similarity_li[t]
            if len(similarity_li) > 0:
                f_li.append(np.median(np.array(similarity_li)))
            else:
                f_li.append(0)
    
    group = score_li.split("_")[0] # 難易度の情報
    if group == "A":
        f_li.append(1)
    elif group == "B":
        f_li.append(2)
    elif group == "C":
        f_li.append(3)
    else:
        f_li.append(0)

    return f_li

    
