# -*- coding: utf-8 -*-

import math
# import re

# given a frequency, return a note in lilypond syntax
def freqToNote(freq, adjustOctave=0):
    if freq <= 0:
        # frequency <= 0 is invalid
        return "c"
    notes = ["c", "cis", "d", "dis", "e", "f", "fis", "g", "gis", "a", "ais", "b"]
    A4 = 440
    C0 = A4 * math.pow(2, -4.75)
    h = int(round(12*(math.log(freq/C0)/math.log(2))))
    octave = h / 12
    octave += adjustOctave
    octave = max(octave, 0)
    n = h % 12
    return notes[n] + ("'" * octave)

# given a list of notes with start and end,
# return a list of notes in lilypond rhythm syntax
def normalizeNotes(notes, tempo, shortestNote):
    # shortest unit in ms
    wholeNote = (60000 / tempo) * 4
    minNoteMs = wholeNote / shortestNote

    # sort notes
    notes = sorted(notes, key=lambda n: n["start"])
    # round each note to shortest note
    for i, note in enumerate(notes):
        dur = note["end"] - note["start"]
        dur = int(round(1.0 * dur / minNoteMs)) * minNoteMs
        if dur <= 0:
            print "Warning: note (%s) at %sms has duration of zero" % (note["note"], note["start"])
            dur = minNoteMs
        # notes[i]["start"] = start
        notes[i]["dur"] = dur
    # add rests
    rests = []
    for i, note in enumerate(notes):
        if i > 0:
            prev = notes[i-1]
            gap = note["start"] - prev["end"]
            dur = int(round(1.0 * gap / minNoteMs)) * minNoteMs
            if dur >= minNoteMs:
                rests.append({
                    "start": prev["end"],
                    "dur": dur,
                    "note": "r",
                    "text": ""
                })
    notes += rests
    # sort notes and rests
    notes = sorted(notes, key=lambda n: n["start"])
    # convert notes to lilypond notation
    for i, note in enumerate(notes):
        noteStr = ""
        remainder = note["dur"]
        noteDur = wholeNote
        lastMatched = False
        while noteDur >= minNoteMs:
            if remainder >= noteDur:
                noteCount = int(remainder / noteDur)
                durLabel = shortestNote/(noteDur/minNoteMs)
                # case: note is a rest; don't tie
                if note["note"] == "r":
                    noteStr += " %s%s" % (note["note"], durLabel)
                # case: many whole notes; tie together
                elif noteCount > 1:
                    for j in range(noteCount):
                        noteStr += " %s%s~" % (note["note"], durLabel)
                    # remove trailing tie and spaces
                    noteStr = noteStr.strip('~')
                    noteStr = noteStr.strip()
                    lastMatched = durLabel
                elif noteCount > 0:
                    # case: first note
                    if len(noteStr) < 1:
                        noteStr = "%s%s" % (note["note"], durLabel)
                        # case: note is half the previous note; add dot
                    elif lastMatched and lastMatched == (durLabel/2):
                        noteStr += "."
                    # case: note is more than half of previous note; tie to previous note
                    else:
                        noteStr += "~ %s%s" % (note["note"], durLabel)
                    lastMatched = durLabel
                remainder = remainder % noteDur
            noteDur /= 2
        noteStr = noteStr.strip()
        notes[i]["note"] = noteStr
    return notes

# given a list of notes, optional list of lyrics, and an optional header,
# return a string in lilypond syntax
def toString(music, lyrics, header):
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
    ly += "\\absolute {"
    ly += "\n  \\tempo 4 = %s\n " % music["tempo"]
    for i, note in enumerate(music["notes"]):
        if len(note["note"].strip()) <= 0:
            continue
        # e.g. c''4\f = C, up 2 octaves, quarter note, forte
        # e.g. c2 d8( e8 f4) = slur d-e-f
        ly += " %s" % note["note"]
    ly += ' \\bar "|."'
    ly += "\n}"

    # lyrics
    if lyrics and len(lyrics) > 0:
        ly += "\n\\addlyrics{\n "
        for i, word in enumerate(lyrics):
            text = word["text"].replace("'", "’".decode("utf-8")).encode("utf8")
            # text = re.sub(r'\W+', '', word["text"])
            ly += " %s" % text
        ly += "\n}"

    return ly
