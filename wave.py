import numpy as np  
from PIL import Image  # Pillow Image Processing Library
from scipy.io import wavfile  # Audio file I/O library
from tkinter import filedialog  # Opens and Saves Files

# Define image dimensions
height = 800
width = 400
size = (width, height)

# Prompt user to select a JPEG image file
image = filedialog.askopenfilename()  
data = Image.open(image)
data = data.resize(size)

# Convert the image to a numerical array
array = np.array(data, dtype='float')


# Convert the image to grayscale using standard conversion formula
# (0.2989*R + 0.5870*G + 0.1140*B)
grayscale = 0.2989 * array[:, :, 0] + \
                  0.5870 * array[:, :, 1] + \
                  0.1140 * array[:, :, 2]

# Normalize the grayscale image data
grayscale /= np.max(grayscale)

# Flip the grayscale image data vertically
flipped = np.flip(grayscale, axis=0)

# Generate random phase data
phase = np.random.randn(height, width)
phase *= 23
phase = np.exp(1j * phase)

# Manipulate the grayscale image data with phase data
mod = flipped * phase

# Concatenate manipulated image data with its flipped version
concat = np.concatenate((np.flip(mod, axis=1), mod), axis=1)

# Perform inverse Fourier transform along horizontal axis
inverse = np.fft.ifftshift(concat, axes=1)
inverse = np.fft.ifft(inverse, axis=1)

# Flatten matrix into 1D vector
flat = inverse.flatten()

# Normalize data to -1 to 1 range
norm = flat / np.max(flat)

# Scale data to int16 range (-32768 to 32767)
scaled = np.multiply(norm, 32767)

# Create 2-channel waveform
wave = np.array([scaled, scaled]).T.astype(np.int16)

# Prompt user to save the waveform as a WAV file
fileTypes = [('WAV File', '*.wav')]
output = filedialog.asksaveasfilename(filetypes=fileTypes, defaultextension=fileTypes)

# Define sampling frequency
samplingFrequency = 24000

# Write the waveform data to a WAV file
wavfile.write(output, int(round(samplingFrequency)), wave)
