import numpy as np
from PIL import Image
from tkinter import filedialog, Tk, Scale, Button, HORIZONTAL, Label
import matplotlib.pyplot as plt
from scipy.io import wavfile
import pygame
import logging

# Initialize pygame mixer
pygame.mixer.init()

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

globalWave = None 
Fs = 24000

def generate_spectrogram(freq):
    global globalWave, Fs
    logging.debug("Generating spectrogram with frequency: {}".format(freq))
    
    plt.close()

    # Resize image to match desired dimensions
    resized_img = data.resize((400, 800))
    logging.debug("Image resized to 400x800 pixels.")

    # Convert the resized image to a numerical array
    array = np.array(resized_img, dtype='float')

    # Convert the image to grayscale using standard conversion formula
    grayscale = 0.2989 * array[:, :, 0] + \
                0.5870 * array[:, :, 1] + \
                0.1140 * array[:, :, 2]
    logging.debug("Image converted to grayscale.")

    # Normalize the grayscale image data
    grayscale /= np.max(grayscale)

    # Flip the grayscale image data vertically
    flipped = np.flip(grayscale, axis=0)

    # Generate random phase data
    phase = np.random.randn(800, 400)
    phase *= (freq * 100000)
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
    logging.debug("Waveform generated.")

    # Update the sampling frequency based on the slider value
    Fs = int(24000 * (freq / 20))
    logging.debug("Sampling frequency set to: {}".format(Fs))

    globalWave = wave

    # Display the Spectrogram
    plt.specgram(wave[:, 0], Fs=Fs, vmin=scale.get(), vmax=40)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Time (s)')
    plt.title('Spectrogram')
    plt.colorbar(label='Power/Frequency (dB/Hz)')
    plt.show()

def play_waveform():
    global globalWave, Fs
    logging.debug("Attempting to play waveform.")
    if globalWave is not None:
        # Create Sound object from waveform
        audio = pygame.mixer.Sound(buffer=globalWave.tobytes())
        pygame.mixer.stop()  # Stop any currently playing sounds
        audio.play()  # Play the .wav audio
        logging.debug("Waveform is playing.")
    else:
        logging.error("No waveform loaded. Cannot play audio.")

def stop_waveform():
    logging.debug("Stopping audio playback.")
    pygame.mixer.stop()

# Initialize Tkinter window
root = Tk()
root.title("Spectrometer App")
root.geometry("300x200")  # Resize the GUI window

# Create a scale (slider) widget
scale = Scale(root, from_=1, to=40, orient=HORIZONTAL, label="Frequency", command=generate_spectrogram)
scale.set(20)  # Set initial frequency
scale.pack()

# Load image
image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
data = Image.open(image_path)

# Create buttons
generate_button = Button(root, text="Generate Spectrogram", command=lambda: generate_spectrogram(scale.get()))
generate_button.pack()

play_button = Button(root, text="Play .wav File", command=play_waveform)
play_button.pack()

stop_button = Button(root, text="Stop Playing", command=stop_waveform)
stop_button.pack()

# Run the Tkinter event loop
root.mainloop()
