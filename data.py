def change_note():
    key_path = "config/key.txt"  # 鍵盤ファイルの読み込み
    with open(key_path) as f:
        notes = f.read()
    note = notes.splitlines()
    key_li = []
    for i in range(len(note)):
        temp_li = []
        if not note[i].find("#"):
            continue
        n = note[i].split(",")
        for j in range(len(n)):
            temp_li.append(int(n[j]))
        key_li.append(temp_li)
        
    return key_li

def get_data(obj, soup, score_li):
    obj.title = soup.find("work-title").string
    obj.creator = soup.find("identification").creator.string

    measure = 0 # 小節数
    beat_count = 1

    for m in soup.find_all("measure"): # 1小節

        measure += 1   # 小節数をカウントする
        m_beat = 1     # 小節内の拍数 measure-beat　初期設定は1　（第1拍からカウント）
        tmp_m_beat = 0

        if m.attributes.divisions:
            divisions = int(m.attributes.divisions.string) # 拍の基準値

        if m.attributes.time:
            beat_type_temp = int(m.attributes.time.find("beat-type").string) # 1拍とする音符
            beats_temp = int(m.attributes.time.beats.string) # 拍子

        if (obj.beat_type[beat_count - 1][0] != beat_type_temp or obj.beats[beat_count - 1][0] != beats_temp):
            obj.beat_type.append([beat_type_temp, measure])
            obj.beats.append([beats_temp, measure])
            beat_count += 1

        adj = 1.0  # 音価を求めるために変数を用意
        if obj.beat_type[-1][0] == 8:
            adj = 2.0
        elif obj.beat_type[-1][0] == 2:
            adj = 0.5

        for nb in m.find_all({"note", "backup"}):
            
            if nb.name == "backup":
                m_beat -= int(nb.duration.string) / divisions * adj

            if nb.name == "note": # 音符または休符の情報を取り出す
                alter = 0
                octave = 0
                accidental = 0 #　臨時記号
                note_len = 0
                accent, staccato, tenuto, strong_accent, staccatissimo, arpeggiat = 0, 0, 0, 0, 0, 0 
                staff = int(nb.staff.string)
                note_num = 0

                if nb.grace: # 装飾音は飛ばす
                    continue

                if nb.duration:
                    note_len = int(nb.duration.string) / divisions * adj  # 音価を求める

                if not nb.chord: # 和音の構成音でなければ
                    m_beat += tmp_m_beat

                if nb.notations:
                    if nb.notations.articulations:
                        if nb.notations.articulations.accent:
                            accent = 1
                        if nb.notations.articulations.staccato:
                            staccato = 1
                        if nb.notations.articulations.tenuto:
                            tenuto = 1
                        if nb.notations.articulations.find("strong-accent"):
                            strong_accent = 1
                        if nb.notations.articulations.staccatissimo:
                            staccatissimo = 1
                
                    if nb.notations.arpeggiat:
                        arpeggiat = 1
                
                if nb.accidental:
                    if nb.accidental.string == "sharp":
                        accidental = 1
                    elif nb.accidental.string == "flat":
                        accidental = 2
                    elif nb.accidental.string == "natural":
                        accidental = 3
                    elif nb.accidental.string == "double-sharp":
                        accidental = 4
                    elif nb.accidental.string == "flat-flat":
                        accidental = 5

                if nb.pitch: # 音符である場合、[小節数, 現在の拍数、音名、半音階的変化、音高、臨時記号、演奏記号（6個）、使用する手]の情報を取り出す
                    octave = int(nb.pitch.octave.string)
                    
                    step_li = ["C", "D", "E", "F", "G", "A", "B"]
                    search_row = int(nb.pitch.octave.string)
                    search_column = 0
                    for i in range(7):
                        if step_li[i] == nb.pitch.step.string:
                            search_column = i
                    note_num = change_note()[search_row][search_column]                    

                    if nb.pitch.alter: # 半音階的変化がある場合
                        alter = nb.pitch.alter.string
                        note_num = note_num + int(nb.pitch.alter.string)
                      
                if nb.rest: # 休符
                    alter = 10
                    octave = -1
                    accidental = -1
                    accent = staccato = tenuto = strong_accent = staccatissimo = arpeggiat = -1
                    if obj.beat_type[-1][0] == 8:
                        if note_len == 0.015625:
                            note_num = -2
                        else:
                            note_num = -1
                    elif obj.beat_type[-1][0] == 2:
                        if note_len == 0.00390625:
                            note_num = -2
                        else:
                            note_num = -1
                    elif obj.beat_type[-1][0] == 4:
                        if note_len == 0.0078125:
                            note_num = -2
                        else:
                            note_num = -1
                
                # Scoreクラスのインスタンスの属性値をセットする
                obj.measure.append(measure)
                obj.alter.append(alter)
                obj.octave.append(octave)
                obj.accidental.append(accidental)
                obj.note_len.append(note_len)
                obj.accent.append(accent)
                obj.staccato.append(staccato)
                obj.tenuto.append(tenuto)
                obj.strong_accent.append(strong_accent)
                obj.staccatissimo.append(staccatissimo)
                obj.arpeggiat.append(arpeggiat)
                obj.staff.append(staff)
                obj.note_num.append(note_num)
                obj.m_beat.append(m_beat)

                if nb.duration: # 装飾音はdurationないので飛ばす
                    tmp_m_beat = int(nb.duration.string) / divisions * adj

    
    obj.beat_type.remove([0, 0])
    obj.beats.remove([0, 0])
