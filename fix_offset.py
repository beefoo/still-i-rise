# -*- coding: utf-8 -*-

import json

data = {}
with open('data/and_still_i_rise_aligned.json') as f:
    data = json.load(f)

transcript = data["transcript"]
transcriptLen = len(transcript)

offset = 0
for i, entry in enumerate(data["words"]):
    word = entry["word"]
    wordLen = len(word)

    offsetEnd = offset+wordLen
    substr = transcript[offset:offsetEnd]
    while substr != word and offsetEnd < transcriptLen:
        offset += 1
        offsetEnd += 1
        substr = transcript[offset:offsetEnd]

    data["words"][i]["startOffset"] = offset
    data["words"][i]["endOffset"] = offsetEnd
    offset = offsetEnd + 1

with open('data/and_still_i_rise_aligned_fixed.json', 'w') as f:
    json.dump(data, f, indent=2)
