import numpy as np
import soundfile as sf

# ==============================
# PARAMETERS
# ==============================
duration = 10         # 10 seconds (short & clean)
fs = 48000
f_start = 20
f_end = 20000
amplitude = 0.5

# Time array
t = np.linspace(0, duration, int(fs * duration), endpoint=False)

# Linear sweep frequency at each time
freq_t = f_start + (f_end - f_start) * (t / duration)

# Generate sweep using phase = integral of frequency
phase = 2 * np.pi * np.cumsum(freq_t) / fs

sweep = amplitude * np.sin(phase)

# Save WAV
sf.write("linear_sweep_gen.wav", sweep, fs)
print("Generated: linear_sweep.wav")
print("Play with Windows or VLC.")
