# for data transformation
import numpy as np
# for visualizing the data
import matplotlib.pyplot as plt
# for opening the media file
import scipy.io.wavfile as wavfile

Fs, aud = wavfile.read('car.wav')
# select left channel only
aud = aud[:,0]
# trim the first 125 seconds
first = aud[:int(Fs*125)]

powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(first, Fs=Fs)

# Orient Correctly
updown = np.transpose(powerSpectrum)
flipped_spectrum = np.flipud(updown)

# Display the flipped spectrogram
plt.imshow(flipped_spectrum, aspect='auto', extent=[time[0], time[-1], frequenciesFound[0], frequenciesFound[-1]])
plt.xlabel('Frequency (Hz)')
plt.ylabel('Time (s)')
plt.title('Spectrogram')
plt.colorbar(label='Power/Frequency (dB/Hz)')
plt.show()

# Reference to display spectrogram
# https://dolby.io/blog/beginners-guide-to-visualizing-audio-as-a-spectogram-in-python/
