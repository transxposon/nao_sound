# nao_sound

two programs to record sound from your local microphone and nao robot. 

# **Audio Recording Utilities**

This repository contains two Python programs for recording audio:
1. **Recording from a local microphone using `sounddevice` and `scipy.io.wavfile`**
2. **Recording audio from a NAO robot and saving it locally**

---

## **Features**

### Program 1: Local Microphone Audio Recorder
- Records audio using a microphone connected to your computer.
- Allows you to choose the microphone from available audio devices.
- Stops recording when you press `s` and trims the audio to the actual recorded length.
- Saves the recording as a WAV file in the current working directory.

### Program 2: NAO Robot Audio Recorder
- Records audio from a NAO robot's front microphone.
- Transfers the audio file from the robot to your local machine.
- Stops recording when you press `s` and trims the audio to the actual recorded length.
- -Saves the recording as a WAV file in the current working directory.

---

## **Setup Instructions**

### **Prerequisites**

- Python 2.7 (required for compatibility with NAOqi)
- Libraries:
  - `os`
  - `time`
  - `threading`
  - `sys`
  - `sounddevice`
  - `scipy`
  - `numpy`
  - `sshpass`

- NAOqi Python SDK (download and include in your project)
- A NAO robot connected to your network (for the second program)

### **Installing Dependencies**

```bash
pip install os time threading sys sounddevice scipy.io.wavfile numpy 
brew install sshpass  # macOS users
sudo apt-get install sshpass  # Ubuntu/Debian users
