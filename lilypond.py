# -*- coding: utf-8 -*-

def lily(music, lyrics, header):
    ly = ""

    # header
    if header:
        ly += "\\header {"
        ly += "\n  title=\"%s\"" % header["title"]
        if "subtitle" in header:
            ly += "\n  subtitle=\"%s\"" % header["subtitle"]
        if "composer" in header:
            ly += "\n  composer=\"%s\"" % header["composer"]
        if "arranger" in header:
            ly += "\n  arranger=\"%s\"" % header["arranger"]
        if "copyright" in header:
            ly += "\n  copyright=\"%s\"" % header["copyright"]
        ly += "\n}\n"

    # music
    ly += "\\relative %s {" % music["relative"]
    ly += "  \\tempo 4 = %s" % music["tempo"]
    for i, measure in enumerate(music["measures"]):
        ly += "\n "
        for j, note in enumerate(measure):
            octave = "'" * note["octave"]
            if len(note["dynamics"]) > 0:
                note["dynamics"] = "\\" + note["dynamics"]
            # e.g. c''4\f~ = C, up 2 octaves, quarter note, forte, tie to next note
            # e.g. c2 d8( e8 f4) = slur d-e-f
            ly += " " + note["note"] + octave + note["duration"] + note["dynamics"] + note["ties"] + note["slur"]
    ly += ' \\bar "|."'
    ly += "\n}"

    # lyrics
    if len(lyrics) > 0:
        ly += "\n\\addlyrics{"
        for i, measure in enumerate(lyrics):
            ly += "\n"
            for j, word in enumerate(measure):
                ly += " %s" % word["word"]
        ly += "\n}"

    return ly
