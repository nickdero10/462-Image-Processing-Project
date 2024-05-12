import numpy as np
from PIL import Image
from tkinter import filedialog, Tk, Scale, Button, HORIZONTAL
import matplotlib.pyplot as plt
from scipy.io import wavfile

def generate_spectrogram(freq):
    plt.close()

    # Resize image to match desired dimensions
    resized_img = data.resize((400, 800))

    # Convert the resized image to a numerical array
    array = np.array(resized_img, dtype='float')

    # Convert the image to grayscale using standard conversion formula
    grayscale = 0.2989 * array[:, :, 0] + \
                      0.5870 * array[:, :, 1] + \
                      0.1140 * array[:, :, 2]

    # Normalize the grayscale image data
    grayscale /= np.max(grayscale)

    # Flip the grayscale image data vertically
    flipped = np.flip(grayscale, axis=0)

    # Generate random phase data
    phase = np.random.randn(800, 400)
    phase *= freq
    phase = np.exp(1j * phase)

    # Resize phase to match image dimensions
    phase = np.resize(phase, (800, 400))

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

    Fs = 24000

    aud = wave[:,0]

    # trim the first 125 seconds
    first = aud[:int(Fs*125)]

    powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(first, Fs=Fs, vmin=scale.get(), vmax=100)

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

# Initialize Tkinter window
root = Tk()
root.title("Frequency Slider")

# Create a scale (slider) widget
scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, label="Frequency", command=generate_spectrogram)
scale.set(50)  # Set initial frequency
scale.pack()

# Load image
image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
data = Image.open(image_path)

# Create a button to generate the spectrogram
generate_button = Button(root, text="Generate Spectrogram", command=lambda: generate_spectrogram(scale.get()))
generate_button.pack()

# Run the Tkinter event loop
root.mainloop()
