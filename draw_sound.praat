# Draws waveform, spectrogram, F0 curve and TextGrid.
# Adapted from: https://www.uvic.ca/humanities/linguistics/assets/docs/praat/draw-waveform-sgram-f0.praat
# http://www.helsinki.fi/~lennes/praat-scripts/public/save_phonetic_transcription_example.praat

form Input
  # files
  text sound_file sound.wav
  text text_file sound.TextGrid
  text output_file sound.eps

  # For view
  sentence xaxis Time (s)
  sentence yaxis Frequency (Hz)
  positive time_maj_unit 0.5
  positive time_min_unit 0.1
  positive width 8 # right boundary of figure (specify width)

  # For spectrogram
  positive window_length 0.005
  positive maximum_frequency 5000.0
  positive time_step 0.002
  positive frequency_step 20.0
  text window_shape Gaussian

  # For pitch
  boolean draw_pitch no
  positive pitch_floor 75
  positive max_candidates 15
  text very_accurate off
  positive silence_threshold 0.03
  positive voicing_threshold 0.45
  positive octave_cost 0.01
  positive octave_jump_cost 0.35
  positive voiced_cost 0.14
  positive pitch_ceiling 600
endform

# Open sound file
Read from file... 'sound_file$'

# Get the name of the sound object:
sound_name$ = selected$ ("Sound", 1)

# Select sound file and do spectrogram analysis
select Sound 'sound_name$'
To Spectrogram... 'window_length' 'maximum_frequency' 'time_step' 'frequency_step' 'window_shape$'

# Specify font type size, color
Times
Font size... 15
Black

# Define size and position of waveform (by specifying grid coordinates)
# Viewport... left_viewport_horiz right_viewport_horiz top_viewport_verti bottom_viewport_verti
Viewport... 0 'width' 0 2

# Draw waveform
select Sound 'sound_name$'
Draw... 0 0 0 0 no curve

# Define size and position of spectrogram
Viewport... 0 'width' 1 5

# Draw spectrogram
select Spectrogram 'sound_name$'
Paint... 0 0 0 0 100 yes 50 6 0 no

# Select sound file and do pitch analysis
if draw_pitch = 1
  select Sound 'sound_name$'
  To Pitch (ac)... time_step pitch_floor max_candidates very_accurate silence_threshold voicing_threshold octave_cost octave_jump_cost voiced_cost pitch_ceiling

  select Pitch 'sound_name$'

  # first as a thick white line
  Line width... 15
  White
  Draw... 0 0 'pitch_floor' 'pitch_ceiling' no

  # then as a thin black line
  Line width... 4
  Black
  Draw... 0 0 'pitch_floor' 'pitch_ceiling' no
endif

# Label x axis
# Text bottom... yes 'xaxis$'
# Marks bottom every... 1 'time_min_unit' no yes no
# Marks bottom every... 1 'time_maj_unit' yes yes no

# Define size and position of TextGrid
Viewport... 0 'width' 1 5.75

# Draw TextGrid
Read from file... 'text_file$'
# Get the name of the TextGrid object:
text_name$ = selected$ ("TextGrid", 1)
select TextGrid 'text_name$'
Draw... 0 0 yes yes no

# Define size and position of inner box
Viewport... 0 'width' 0 5.75

# Draw inner box
Black
Draw inner box

# Write to eps file
Write to EPS file... 'output_file$'
# Save as PNG file...

# Remove objects from Praat objects list
select Spectrogram 'sound_name$'
plus Sound 'sound_name$'
Remove
