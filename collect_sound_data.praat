# Perform "To Pitch (ac)" function on .wav file
# http://www.fon.hum.uva.nl/praat/manual/Sound__To_Pitch__ac____.html
# https://github.com/praat/praat/blob/ed740fb665317111707b2713d5822075e6345706/fon/praat_Sound.cpp#L1923
# Ref:
#   https://depts.washington.edu/phonlab/resources/getDurationPitchFormants.praat
#   http://www.acsu.buffalo.edu/~cdicanio/scripts/Pitch_Dynamics_2.praat
#   https://sites.google.com/site/speechrate/Home/praat-script-syllable-nuclei-v2
#   http://web.uvic.ca/~tyoon/resource/vq.praat

form Get pitch data from sound file
  text Sound_file sound.wav
  text Pitch_file data/sound.Pitch
  text Pulse_file data/sound.PointProcess
  # Pitch analysis parameters
  positive Time_step 0.01
  positive Pitch_floor 80
  positive Max_candidates 4
  text Very_accurate on
  positive Silence_threshold 0.03
  positive Voicing_threshold 0.3
  # To more strongly favour recruitment of high-frequency candidates, increase this value. Default: 0.01
  positive Octave_cost 0.001
  # To decrease the number of large frequency jumps, increase this value. Default: 0.35
  positive Octave_jump_cost 0.3
  # To decrease the number of voiced/unvoiced transitions, increase this value. Default: 0.14
  positive Voiced_cost 0.2
  positive Pitch_ceiling 180
endform

# Check if the pitch file exists:
if fileReadable (pitch_file$)
  # pause The file 'pitch_file$' already exists! Do you want to overwrite it?
  filedelete 'pitch_file$'
endif

# Check if the pulse file exists:
if fileReadable (pulse_file$)
  # pause The file 'pulse_file$' already exists! Do you want to overwrite it?
  filedelete 'pulse_file$'
endif

# Open sound file
Read from file... 'sound_file$'

# Get the name of the sound object:
sound_name$ = selected$ ("Sound", 1)

# Select sound file and do pitch analysis
select Sound 'sound_name$'
To Pitch (ac)... time_step pitch_floor max_candidates very_accurate silence_threshold voicing_threshold octave_cost octave_jump_cost voiced_cost pitch_ceiling

# Save as short text file
select Pitch 'sound_name$'
Save as short text file... 'pitch_file$'

# Create Point Process
select Sound 'sound_name$'
plus Pitch 'sound_name$'
To PointProcess (cc)

# Save as short text file
Save as short text file... 'pulse_file$'

# Remove the Pulse, Pitch, and sound objects
select Pitch 'sound_name$'
plus Sound 'sound_name$'
Remove
