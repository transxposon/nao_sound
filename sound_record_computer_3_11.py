import time
import sounddevice as sd
import scipy.io.wavfile as wav
import os
import threading


def list_devices():
    """
    Available audio devices are listed for easier microphone picking
    """
    print("Available audio devices:")
    devices = sd.query_devices()
    for idx, device in enumerate(devices):
        print("{}: {}, {} ({} in, {} out)".format(
            idx,
            device['name'],
            device['hostapi'],
            device['max_input_channels'],
            device['max_output_channels']
        ))


def wait_for_stop_signal(stop_event):
    """
    When user presses 's' and Enter, stops the other function.

    Args:
        stop_event (threading.Event): The event object to signal stopping.
    """
    input("Press 's' and Enter to stop recording.\n")
    stop_event.set()


def record_audio(file_name, device, sample_rate=16000):
    """
    Record audio until the user presses 's' and Enter, and save it as a WAV file.

    Args:
        file_name (str): Name of the WAV file (without extension).
        device (int): Audio input device index.
        sample_rate (int, opt): Sampling rate in Hz, default 16000.
    """
    try:
        sd.default.device = (device, None)  # input device only

        print("Using device {}: {}".format(device, sd.query_devices()[device]['name']))

        output_file = os.path.join(os.getcwd(), file_name + ".wav")

        print("Recording audio. Press 's' and Enter to stop...")

        stop_event = threading.Event()

        # threading for stopping
        stop_thread = threading.Thread(target=wait_for_stop_signal, args=(stop_event,))
        stop_thread.start()

        # recording
        # sd.rec() requires preallocated duration
        # here the default is an hour
        start_time = time.time()
        audio_data = sd.rec(int(3600 * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        stop_event.wait()
        end_time = time.time()

        print("\nStopping recording...")
        sd.stop()

        elapsed_time = end_time - start_time
        actual_samples = int(elapsed_time * sample_rate)
        audio_data = audio_data[:actual_samples]  # trim before saving

        print("Saving audio to:", output_file)
        wav.write(output_file, sample_rate, audio_data)
        print("Audio file saved at:", output_file)

    except Exception as e:
        print("Error while recording audio:", e)


if __name__ == "__main__":

    list_devices()

    try:
        device_index = int(input("Enter the device index for recording: "))
        file_name = input("Enter the desired file name (without .wav extension): ")

        record_audio(file_name, device_index)

    except ValueError:
        print("Invalid input. Please enter numeric values for device index.")
