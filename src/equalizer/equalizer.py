from tkinter import *
from tkinter import ttk
import numpy as np
import scipy.signal as signal
import threading
import sounddevice as sd
import soundfile as sf
from tkinter import filedialog
import os


window = Tk()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 500
window_height = 550
x_window = int((screen_width - window_width) / 2)
y_window = int((screen_height - window_height) / 2)

window.geometry(f"{window_width}x{window_height}+{x_window}+{y_window}")
window.title("Bandpass Filter (High-Pass + Low-Pass)")

status = StringVar(window)
status.set("No file loaded")
file_path = "data/recorded_sample_mono.wav"  # Default file path
apply_filter = BooleanVar(value=False)  # Toggle for applying filter

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)


def open_file():
    global file_path
    file_path = filedialog.askopenfilename(
        defaultextension=".wav",
        filetypes=[("Wave Files", "*.wav")],
        initialdir="data"
    )
    if file_path:
        status.set(f"File loaded: {os.path.basename(file_path)}")
        print(f"Selected file: {file_path}")


def play_audio():
    print(f"\n{'='*50}")
    print(f"Playing file: {file_path}")
    
    try:
        # Load audio file
        audio, sr = sf.read(file_path)
        
        # Print detailed audio information
        print(f"{'='*50}")
        print(f"AUDIO FILE INFORMATION:")
        print(f"{'='*50}")
        print(f"Shape: {audio.shape}")
        print(f"Sample rate: {sr} Hz")
        print(f"Data type: {audio.dtype}")
        print(f"Duration: {len(audio) / sr:.2f} seconds")
        print(f"Channels: 1 (Mono)" if audio.ndim == 1 else f"Channels: {audio.shape[1]}")
        print(f"{'='*50}\n")
        
        # Apply bandpass filter (high-pass + low-pass) if enabled
        if apply_filter.get():
            # Get frequency range from sliders
            low_freq = low_cutoff_slider.get()
            high_freq = high_cutoff_slider.get()
            
            print(f"Applying bandpass filter ({low_freq} Hz - {high_freq} Hz)...")
            print(f"  Step 1: High-pass filter (cut below {low_freq} Hz)")
            print(f"  Step 2: Low-pass filter (cut above {high_freq} Hz)")
            
            order = 4  # Filter order
            nyquist = 0.5 * sr
            
            # Step 1: Apply HIGH-PASS filter (removes frequencies below low_freq)
            normal_low = low_freq / nyquist
            b_high, a_high = signal.butter(order, normal_low, btype='high', analog=False)
            audio = signal.lfilter(b_high, a_high, audio)
            
            # Step 2: Apply LOW-PASS filter (removes frequencies above high_freq)
            normal_high = high_freq / nyquist
            b_low, a_low = signal.butter(order, normal_high, btype='low', analog=False)
            audio = signal.lfilter(b_low, a_low, audio)
            
            # Normalize to prevent clipping
            max_val = np.max(np.abs(audio))
            if max_val > 0:
                audio = audio / max_val * 0.95
            
            # Save filtered audio
            output_file = "data/telephone_effect.wav"
            sf.write(output_file, audio, sr)
            print(f"✓ Filtered audio saved to: {output_file}")
            
            print(f"Filter applied! Only frequencies between {low_freq}-{high_freq} Hz remain.")
            status.set(f"Playing & Saved: {low_freq}-{high_freq} Hz")
        else:
            status.set("Playing original audio")
        
        # Play audio
        sd.play(audio, sr)
        
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        status.set(f"Error: File not found")
    except Exception as e:
        print(f"Error: {e}")
        status.set(f"Error: {e}")


def stop_audio():
    sd.stop()
    status.set("Audio stopped")
    print("Audio stopped")


def on_slider_change(value):
    """Update info label when sliders change"""
    low_val = low_cutoff_slider.get()
    high_val = high_cutoff_slider.get()
    info_label.config(text=f"Pass frequencies between {low_val} Hz and {high_val} Hz")


# Buttons and controls
ttk.Button(window, text="Open File", command=open_file, width=20).pack(pady=10)

# Checkbutton for enabling/disabling filter
ttk.Checkbutton(window, text="Apply Bandpass Filter", 
                variable=apply_filter).pack(pady=10)

# Frequency range sliders
slider_frame = Frame(window, padx=20)
slider_frame.pack(pady=10)

Label(slider_frame, text="Low Cutoff (High-Pass)", font=("Arial", 10, "bold")).pack()
low_cutoff_slider = Scale(slider_frame, from_=20, to=5000, orient=HORIZONTAL,
                          length=400, resolution=10, command=on_slider_change)
low_cutoff_slider.set(300)  # Default: cut below 300 Hz
low_cutoff_slider.pack(pady=5)

Label(slider_frame, text="High Cutoff (Low-Pass)", font=("Arial", 10, "bold")).pack(pady=(15,0))
high_cutoff_slider = Scale(slider_frame, from_=500, to=15000, orient=HORIZONTAL,
                           length=400, resolution=10, command=on_slider_change)
high_cutoff_slider.set(3400)  # Default: cut above 3400 Hz
high_cutoff_slider.pack(pady=5)

# Play/Stop buttons
ttk.Button(window, text="Play", command=play_audio, width=20).pack(pady=5)
ttk.Button(window, text="Stop", command=stop_audio, width=20).pack(pady=5)

# Status and info labels
ttk.Label(window, textvariable=status, font=("Arial", 10)).pack(pady=10)
info_label = Label(window, text="Pass frequencies between 300 Hz and 3000 Hz", 
                   font=("Arial", 8), foreground="gray")
info_label.pack(pady=5)

# Save info label
Label(window, text="Filtered audio auto-saves to: data/filtered_audio.wav", 
      font=("Arial", 7), foreground="blue").pack(pady=5)

window.mainloop()