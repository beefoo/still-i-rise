# Perform "Sound: To Spectrogram..." function on .wav file
# Outputs .Spectrogram short text files
#
# Docs:
#   http://www.fon.hum.uva.nl/praat/manual/Sound__To_Spectrogram___.html
#   https://github.com/praat/praat/blob/ed740fb665317111707b2713d5822075e6345706/fon/praat_Sound.cpp#L2044

form Get spectrogram data from sound file
  # Filenames
  text Sound_file sound.wav
  text Spectrogram_file data/sound.Spectrogram
  # Spectrogram analysis parameters
  positive Window_length 0.005
  positive Maximum_frequency 5000.0
  positive Time_step 0.002
  positive Frequency_step 20.0
  text Window_shape Gaussian
endform

# Check if the spectrogram file exists:
if fileReadable (spectrogram_file$)
  # pause The file 'spectrogram_file$' already exists! Do you want to overwrite it?
  filedelete 'spectrogram_file$'
endif

# Open sound file
Read from file... 'sound_file$'

# Get the name of the sound object:
sound_name$ = selected$ ("Sound", 1)

# Select sound file and do spectrogram analysis
select Sound 'sound_name$'
To Spectrogram... window_length maximum_frequency time_step frequency_step 'window_shape$'

# Save as short text file
select Spectrogram 'sound_name$'
Save as short text file... 'spectrogram_file$'

# Remove the spectrogram and sound objects
select Spectrogram 'sound_name$'
plus Sound 'sound_name$'
Remove
