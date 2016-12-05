# Draws waveform, spectrogram, F0 curve and TextGrid.
# Adapted from: https://www.uvic.ca/humanities/linguistics/assets/docs/praat/draw-waveform-sgram-f0.praat

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
  positive right_bound 8 # right boundary of figure (specify width)

  # For spectrogram
  positive window_length 0.005
  positive maximum_frequency 5000.0
  positive time_step 0.002
  positive frequency_step 20.0
  text window_shape Gaussian

  # for pitch
  # boolean draw_pitch no
endform

# Open sound file
Read from file... 'sound_file$'

# Get the name of the sound object:
sound_name$ = selected$ ("Sound", 1)

# Select sound file and do spectrogram analysis
select Sound 'sound_name$'
To Spectrogram... 'window_length' 'maximum_frequency' 'time_step' 'frequency_step' 'window_shape$'

# Define size and position of waveform (by specifying grid coordinates)
Viewport... 0 'right_bound' 0 2

# Draw waveform
select Sound 'sound_name$'
Draw... 0 0 0 0 no curve

# Define size and position of spectrogram
Viewport... 0 'right_bound' 1 5

# Draw spectrogram
select Spectrogram 'sound_name$'
Paint... 0 0 0 0 100 yes 50 6 0 no

# Label x axis
# Text bottom... yes 'xaxis$'
# Marks bottom every... 1 'time_min_unit' no yes no
# Marks bottom every... 1 'time_maj_unit' yes yes no

# Write to eps file
Write to EPS file... 'output_file$'

# Remove objects from Praat objects list
select Spectrogram 'sound_name$'
plus Sound 'sound_name$'
Remove
