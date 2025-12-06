import subprocess
import soundfile as sf
import numpy as np

# Run in command line:
# pscp hp@10.0.0.204:/home/hp/Desktop/16722_Project/recorded_flicker_noise_mono.wav "C:\Users\HP\Desktop\Equalizer_Project\src\flicker_noise\data"

SAMPLE_RATE = 8000        # I2S MEMS mic sample rate
CHANNELS = 1               # mono
FORMAT = "S32_LE"          # 32-bit signed integer (best for I2S MEMS)
RECORD_SECONDS = 3600*12
DEVICE = "plughw:3"        # matches your CLI example
FINAL_WAV = "recorded_flicker_noise_mono.wav"

print("============================================")
print("       I2S MONO RECORDING STARTING")
print(f" Sample rate : {SAMPLE_RATE} Hz")
print(f" Channels    : {CHANNELS}")
print(f" Format      : {FORMAT} (32-bit integer)")
print(f" Device      : {DEVICE}")
print(f" Output WAV  : {FINAL_WAV}")
print("============================================\n")

subprocess.run([
    "arecord",
    "-D", DEVICE,
    "-c", str(CHANNELS),
    "-r", str(SAMPLE_RATE),
    "-f", FORMAT,
    "-t", "wav",
    "-d", str(RECORD_SECONDS),
    FINAL_WAV
])

print("\nRecording finished.")

audio, sr = sf.read(FINAL_WAV)
print(f"Loaded audio shape: {audio.shape}, sample rate: {sr}")
print(f"Audio dtype: {audio.dtype}")

if audio.dtype == np.int32:
    audio = audio.astype(np.float32) / 2147483648.0  # 2^31
    print(f"Converted to float32, range: [{audio.min():.6f}, {audio.max():.6f}]")

# Save final mono float WAV ready for EQ
sf.write(FINAL_WAV, audio, sr, subtype='FLOAT')
print("Done! Final mono float WAV saved and ready for EQ:", FINAL_WAV)
