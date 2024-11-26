import sys
# Append the path where naoqi is located
sys.path.append('/Users/princess/Downloads/pynaoqi-python2.7-2.8.6.23-mac64-20191127_144231/lib/python2.7/site-packages')

import os
from naoqi import ALProxy
import time
import threading
import scipy.io.wavfile as wav
import numpy as np

# ssh ended up being necessary, unsure if the reason is my mac or what
sshpass_path = "/opt/homebrew/bin"
if sshpass_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + sshpass_path

# Fixed path on the robot for storage
ROBOT_FILE_PATH = "/home/nao/recordings/microphones/nao_audio.wav"


def wait_for_stop_signal(stop_event):
    """
    User presses 's' and Enter to stop recording.

    Args:
        stop_event (threading.Event): Event object to signal stopping.
    """
    raw_input("Press 's' and Enter to stop recording.\n")
    stop_event.set()


def trim_audio(input_path, output_path, duration, sample_rate=16000):
    """
    Trim the recorded audio to the actual duration and save it locally.
    (Because we create a defined length at the start!)

    Args:
        input_path (str): Path to the input WAV file.
        output_path (str): Path to the output WAV file.
        duration (float): Actual recording duration in seconds.
        sample_rate (int, opt): Sampling rate in Hz (default: 16000).
    """
    try:
        print "Trimming the audio file to the actual duration..."

        sample_rate, audio_data = wav.read(input_path)

        actual_samples = int(duration * sample_rate)
        trimmed_audio = audio_data[:actual_samples]

        wav.write(output_path, sample_rate, trimmed_audio)
        print "Trimmed audio file saved at:", output_path
    except Exception as e:
        print "Error while trimming audio:", e


def record_nao_sound(NAO_IP, PORT=9559, password="nao"):
    """
    Record audio from NAO's microphones and save it locally after transferring from the robot.
    Sample rate is 16000 Hz.

    Args:
        NAO_IP (str): Robot IP address.
        PORT (int, opt): Robot port number (default: 9559).
        password (str, opt): Password for the NAO robot (default: "nao").
    """


    # choose filename
    file_name = raw_input("Enter the file name (without .wav extension): ")
    local_file = os.path.abspath(file_name + ".wav")

    audio_recorder = ALProxy("ALAudioRecorder", NAO_IP, PORT)

    print "Starting audio recording on the robot..."
    print "Press 's' and Enter to stop the recording."

    # recording settings
    channels = [0, 0, 1, 0]  # Front microphone
    sample_rate = 16000
    audio_format = "wav"

    os.system("sshpass -p '{}' ssh nao@{} 'mkdir -p /home/nao/recordings/microphones'".format(password, NAO_IP))

    stop_event = threading.Event()

    stop_thread = threading.Thread(target=wait_for_stop_signal, args=(stop_event,))
    stop_thread.start()

    # start recording
    start_time = time.time()
    audio_recorder.startMicrophonesRecording(ROBOT_FILE_PATH, audio_format, sample_rate, channels)
    stop_event.wait()
    audio_recorder.stopMicrophonesRecording()
    end_time = time.time()

    print "\nRecording complete. Audio saved on the robot at:", ROBOT_FILE_PATH


    print "Verifying file on the robot..."
    file_check = os.system("sshpass -p '{}' ssh nao@{} 'test -e {}'".format(password, NAO_IP, ROBOT_FILE_PATH))
    if file_check != 0:
        print "Error: Audio file not found on the robot!"
        return

    # Transfer the file to the local machine
    print "Transferring audio file to your local machine..."
    scp_command = "sshpass -p '{}' scp nao@{}:{} {}".format(password, NAO_IP, ROBOT_FILE_PATH, local_file)
    transfer_result = os.system(scp_command)
    if transfer_result != 0:
        print "Error: Failed to transfer the audio file!"
        return

    # remove empty bits
    duration = end_time - start_time
    trimmed_file = local_file.replace(".wav", "_trimmed.wav")
    trim_audio(local_file, trimmed_file, duration, sample_rate)

    # Delete the untrimmed file
    try:
        os.remove(local_file)
        print "Deleted the original untrimmed file to save space:", local_file
    except OSError as e:
        print "Error while deleting untrimmed file:", e

    print "Final trimmed audio file saved locally at:", trimmed_file


if __name__ == "__main__":

    NAO_IP = "192.168.0.131"
    PORT = 9559

    record_nao_sound(NAO_IP, PORT)
