# 462-Image-Processing-Project

  The initial proposal of the project is to create a simplistic UI that transforms an image input into a Spectrogram that can be read and played as a .wav file. We call it, the Spectrometer App. Based on a given image it will generate spectrograms that changes depending on a slider that adjusts the frequency from 0 to 40.

#### Packages Used
- NumPy
- PIL (Python Imaging Library)
- Tkinter
- Matplotlib
- Pygame
- ~~OpenCV~~

#### Code Functionality
* Allows users to select an image file (.jpg, .png, ,jpeg) from their system
  * Event handling allows for buttons to be deactivated and provide a warning until their conditions are met
    * Example, *Generate Spectrogram* cannot be pressed until *Load Image*
![image](https://github.com/nickdero10/462-Image-Processing-Project/assets/122575719/e97b9489-1681-40d2-a7f8-3623c5ad02c3)

    * Event Error Handling Snippets
![image](https://github.com/nickdero10/462-Image-Processing-Project/assets/122575719/d32cdb5d-cac8-4376-bb10-ea1f8f3fd19e)
![image](https://github.com/nickdero10/462-Image-Processing-Project/assets/122575719/f84f52f4-5819-47b3-a5ab-a4f0024ce3d2)
![image](https://github.com/nickdero10/462-Image-Processing-Project/assets/122575719/e9aeb3ee-2264-4eef-bd45-9cdac5f6d173)
![image](https://github.com/nickdero10/462-Image-Processing-Project/assets/122575719/b2be095f-13df-45ef-b95a-4676df81c94d)

  



## Group Contributions
John
* GUI state functionality/visual additions, event logging and handling, troubleshooting Spectrogram and GUI code
* Attempted Visual Studio Implementation/OpenCV implementation in python, not functional enough to be submitted
* README/REPORT
Nick
* Project Idea
* Initial Spectrogram Code, GUI and troubleshooting
* Spectrogram Code and GUI base logic
* README/REPORT
