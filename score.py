class Score:
    def __init__(self):
        self.__title = ""
        self.__creator = ""
        self.__beat_type = [[0, 0]]
        self.__beats = [[0, 0]]
        
        self.__measure = []
        self.__alter = []
        self.__octave = []
        self.__accidental = []
        self.__note_len = []
        self.__accent = []
        self.__staccato = []
        self.__tenuto = []
        self.__strong_accent = []
        self.__staccatissimo = []
        self.__arpeggiat = []
        self.__staff = []
        self.__note_num = []
        self.__m_beat = []

    def get_title(self):
        return self.__title
    def set_title(self, title):
        self.__title = title
    title = property(get_title, set_title)

    def get_creator(self):
        return self.__creator
    def set_creator(self, creator):
        self.__creator = creator
    creator = property(get_creator, set_creator)

    def get_beat_type(self):
        return self.__beat_type
    def set_beat_type(self, beat_type):
        self.__beat_type = beat_type
    beat_type = property(get_beat_type, set_beat_type)

    def get_beats(self):
        return self.__beats
    def set_beats(self, beats):
        self.__beats = beats
    beats = property(get_beats, set_beats)

    def get_measure(self):
        return self.__measure
    def set_measure(self, measure):
        self.__measure = measure
    measure = property(get_measure, set_measure)

    def get_alter(self):
        return self.__alter
    def set_alter(self, alter):
        self.__alter = alter
    alter = property(get_alter, set_alter)

    def get_octave(self):
        return self.__octave
    def set_octave(self, octave):
        self.__octave = octave
    octave = property(get_octave, set_octave)

    def get_accidental(self):
        return self.__accidental
    def set_accidental(self, accidental):
        self.__accidental = accidental
    accidental = property(get_accidental, set_accidental)

    def get_note_len(self):
        return self.__note_len
    def set_note_len(self, note_len):
        self.__note_len = note_len
    note_len = property(get_note_len, set_note_len)

    def get_accent(self):
        return self.__accent
    def set_accent(self, accent):
        self.__accent = accent
    accent = property(get_accent, set_accent)

    def get_staccato(self):
        return self.__staccato
    def set_staccato(self, staccato):
        self.__staccato = staccato
    staccato = property(get_staccato, set_staccato)

    def get_tenuto(self):
        return self.__tenuto
    def set_tenuto(self, tenuto):
        self.__tenuto = tenuto
    tenuto = property(get_tenuto, set_tenuto)

    def get_strong_accent(self):
        return self.__strong_accent
    def set_strong_accent(self, strong_accent):
        self.__strong_accent = strong_accent
    strong_accent = property(get_strong_accent, set_strong_accent)

    def get_staccatissimo(self):
        return self.__staccatissimo
    def set_staccatissimo(self, staccatissimo):
        self.__staccatissimo = staccatissimo
    staccatissimo = property(get_staccatissimo, set_staccatissimo)

    def get_arpeggiat(self):
        return self.__arpeggiat
    def set_arpeggiat(self, arpeggiat):
        self.__arpeggiat = arpeggiat
    arpeggiat = property(get_arpeggiat, set_arpeggiat)

    def get_staff(self):
        return self.__staff
    def set_staff(self, staff):
        self.__staff = staff
    staff = property(get_staff, set_staff)

    def get_note_num(self):
        return self.__note_num
    def set_note_num(self, note_num):
        self.__note_num = note_num
    note_num = property(get_note_num, set_note_num)

    def get_m_beat(self):
        return self.__m_beat
    def set_m_beat(self, m_beat):
        self.__m_beat = m_beat
    m_beat = property(get_m_beat, set_m_beat)

    def get_measurenum(self): # 総小節数を得る
        return max(self.__measure)
