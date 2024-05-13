import numpy as np
from PIL import Image
from tkinter import filedialog, Tk, Scale, Button, HORIZONTAL, Label, messagebox
import matplotlib.pyplot as plt
from scipy.io import wavfile
import pygame
import logging

# Initialize pygame mixer
pygame.mixer.init()

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

globalWave = None 
Fs = 24000
data = None  # Initialize data as None to ensure it's checked

def generate_spectrogram(freq):
    global globalWave, Fs, data
    if data is None:
        logging.error("No image loaded. Please load an image first.")
        messagebox.showerror("Error", "No image loaded. Please load an image first.")
        return
    
    logging.info(f"Generating spectrogram with frequency: {freq}")

    plt.close()

    # Process the image
    resized_img = data.resize((400, 800))
    array = np.array(resized_img, dtype='float')
    grayscale = 0.2989 * array[:, :, 0] + 0.5870 * array[:, :, 1] + 0.1140 * array[:, :, 2]
    grayscale /= np.max(grayscale)
    flipped = np.flip(grayscale, axis=0)

    # Manipulate the image data for spectrogram generation
    phase = np.random.randn(800, 400) * (freq * 100000)
    phase = np.exp(1j * phase)
    phase = np.resize(phase, (800, 400))
    mod = flipped * phase
    concat = np.concatenate((np.flip(mod, axis=1), mod), axis=1)
    inverse = np.fft.ifftshift(concat, axes=1)
    inverse = np.fft.ifft(inverse, axis=1)
    flat = inverse.flatten()
    norm = flat / np.max(flat)
    scaled = np.int16(norm * 32767)
    wave = np.column_stack((scaled, scaled))

    Fs = int(24000 * (freq / 20))
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
    if globalWave is None:
        logging.error("No waveform loaded. Cannot play audio.")
        return
    
    logging.info("Playing waveform.")
    audio = pygame.mixer.Sound(buffer=globalWave.tobytes())
    pygame.mixer.stop()
    audio.play()

def stop_waveform():
    logging.info("Stopping audio playback.")
    pygame.mixer.stop()

# Initialize Tkinter window
root = Tk()
root.title("Spectrometer App")
root.geometry("300x200")

def load_image():
    global data
    image_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
    if image_path:
        data = Image.open(image_path)
        logging.info(f"Image loaded: {image_path}")
    else:
        logging.info("Image loading canceled.")

load_button = Button(root, text="Load Image", command=load_image)
load_button.pack()

scale = Scale(root, from_=1, to=40, orient=HORIZONTAL, label="Frequency")
scale.set(20)
scale.pack()

generate_button = Button(root, text="Generate Spectrogram", command=lambda: generate_spectrogram(scale.get()))
generate_button.pack()

play_button = Button(root, text="Play .wav File", command=play_waveform)
play_button.pack()

stop_button = Button(root, text="Stop Playing", command=stop_waveform)
stop_button.pack()

root.mainloop()
