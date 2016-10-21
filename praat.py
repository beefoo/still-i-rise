# -*- coding: utf-8 -*-

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
