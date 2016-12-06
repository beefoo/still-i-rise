# -*- coding: utf-8 -*-

# File is in "short" .TextGrid Praat format
# See: http://www.fon.hum.uva.nl/praat/manual/TextGrid_file_formats.html
def dataToTextGrid(data):
    dur = max([d["xmax"] for d in data])
    s = "File type = \"ooTextFile\"\n"
    s += "Object class = \"TextGrid\"\n"
    s += "\n"
    s += "0\n"
    s += "%s\n" % dur
    s += "<exists>\n"
    s += "1\n"
    s += "\"IntervalTier\"\n"
    s += "\"Text\"\n"
    s += "0\n"
    s += "%s\n" % dur
    s += "%s\n" % len(data)
    for d in data:
        s += "%s\n" % d["xmin"]
        s += "%s\n" % d["xmax"]
        s += "\"%s\"\n" % d["text"]
    return s


# File is in "short" .Pitch Praat format
# See: http://www.fon.hum.uva.nl/praat/manual/Pitch.html
def fileToPitchData(filename):

    secondsStep = None # aka dx
    secondsFirstFrame = None # aka x1

    currentFrame = None
    currentCandidate = None
    currentCandidates = None

    frames = []

    for i, line in enumerate(open(filename,'r').readlines()):
        # Main data
        if i > 9 and line:

            # initialize frame
            if currentFrame is None:
                currentFrame = {
                    "intensity": float(line),
                    "candidateCount": None,
                    "start": secondsFirstFrame + len(frames) * secondsStep,
                    "candidates": []
                }
                currentCandidate = None
                currentCandidates = []

            # retrieve # of candidates
            elif currentFrame["candidateCount"] is None:
                currentFrame["candidateCount"] = int(line)

            # initialize candidate
            elif currentCandidate is None:
                currentCandidate = {
                    "frequency": float(line),
                    "strength": None
                }

            # retrieve candidate strength
            elif currentCandidate["strength"] is None:
                currentCandidate["strength"] = float(line)
                currentFrame["candidates"].append(currentCandidate)

                # go to next frame if last candidate
                if len(currentFrame["candidates"]) >= currentFrame["candidateCount"]:
                    frames.append(currentFrame)
                    currentFrame = None

                # go to next candidate
                currentCandidate = None

        # Definitions
        elif i == 6:
            secondsStep = float(line)
        elif i == 7:
            secondsFirstFrame = float(line)

    return frames

# File is in "short" .Pitch Praat format
# See: http://www.fon.hum.uva.nl/praat/manual/PointProcess.html
def fileToPulseData(filename):
    pulses = []

    for i, line in enumerate(open(filename,'r').readlines()):
        if i > 5 and line:
            pulses.append(float(line))

    return pulses

# File is in "short" .Spectrogram Praat format
# See: http://www.fon.hum.uva.nl/praat/manual/Spectrogram.html
def fileToSpectrogramData(filename):
    props = [
        "xmin", # start time, in seconds.
        "xmax", # end time, in seconds.
        "nx", # the number of times (≥ 1).
        "dx", # time step, in seconds.
        "x1", # the time associated with the first column, in seconds. This will usually be in the range [xmin, xmax]. The time associated with the last column (i.e., x1 + (nx – 1) dx)) will also usually be in that range.
        "ymin", # lowest frequency, in Hertz. Normally 0.
        "ymax", # highest frequency, in Hertz.
        "ny", # the number of frequencies (≥ 1).
        "dy", # frequency step, in Hertz.
        "y1", # the frequency associated with the first row, in Hertz. Usually dy / 2. The frequency associated with the last row (i.e., y1 + (ny – 1) dy)) will often be ymax - dy / 2.
    ]
    startProp = 3
    startData = startProp + len(props)
    steps = []
    data = {}
    maxPower = 0

    for i, line in enumerate(open(filename,'r').readlines()):

        # Main data
        if i >= startData and line:

            # init steps
            if len(steps) <= 0:
                s = data["x1"]
                dx = data["dx"]
                for r in range(int(data["nx"])):
                    steps.append({
                        "start": s,
                        "end": s + dx,
                        "fsteps": []
                    })
                    s += dx

            # add power
            index = i - startData
            psd = float(line)
            j = int(index % data["nx"])
            steps[j]["fsteps"].append(psd)

        # Definitions
        elif i >= startProp and line:
            prop = props[i-startProp]
            data[prop] = float(line)

    data["steps"] = steps

    return data

# File is in "short" .Sound Praat format
# See: http://www.fon.hum.uva.nl/praat/manual/Sound.html
def fileToWavData(filename):

    secondsStep = None # aka dx
    secondsFirstFrame = None # aka x1
    samples = []

    for i, line in enumerate(open(filename,'r').readlines()):

        # Main data
        if i > 12 and line:
            samples.append({
                "start": secondsFirstFrame + len(samples) * secondsStep,
                "amplitude": float(line)
            })

        # Definitions
        elif i == 6:
            secondsStep = float(line)
        elif i == 7:
            secondsFirstFrame = float(line)

    return samples
