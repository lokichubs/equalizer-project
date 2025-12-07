# Exploring MEMS Microphone Characteristics and Constructing an Equalizer to Apply Audio Effects
A project that characterizes an I2S MEMS microphone through flicker noise analysis and frequency response measurements, then applies digital signal processing techniques to implement a telephone effect equalizer.

## Project Overview
This project demonstrates comprehensive characterization of a MEMS microphone and validates its application in real-time audio processing. The study includes:
- **Flicker noise (1/f noise) analysis** using 12-hour silent recordings to determine noise floor and corner frequency
- **Frequency response measurement** across the audible spectrum (20 Hz - 20 kHz) using swept-sine methodology
- **Digital equalizer implementation** applying cascaded 4th-order Butterworth bandpass filters to create a telephone effect (300 Hz - 3.4 kHz)

Data is collected via I2S digital interface on a Raspberry Pi 4B and processed using Python with NumPy, SciPy, and Matplotlib for comprehensive spectral analysis.

## Hardware Used

- [Raspberry Pi 4B](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/)
- [SPH0645LM4H I2S MEMS Microphone](https://www.knowles.com/docs/default-source/model-downloads/sph0645lm4h-b-datasheet-rev-c.pdf)
- 10kΩ Resistor (pull-up for I2S lines)
- Breadboard and jumper wires
- MicroSD card (for data storage)
- Computer speakers (for frequency sweep playback)
- Closable box (for noise isolation during flicker noise recording)

## Software Requirements

### For Raspberry Pi (Data Collection)
```bash
conda env create -f rpi.yml
conda activate env-rpi
```

### For PC (Analysis & Processing)
```bash
conda env create -f pc.yml
conda activate env-pc
```
## Usage

### 1. Flicker Noise Characterization

**On Raspberry Pi:**
```bash
cd src/flicker_noise
python record_flicker_noise.py
# Records 12 hours of silence at 8 kHz sampling rate
# Output: data/recorded_flicker_noise_mono.wav
```
**On PC:**
```bash
cd src/flicker_noise
jupyter notebook flicker_noise_analysis.ipynb
# Calculates PSD using Welch's method
# Identifies corner frequency and noise floor
# Generates log-log plot with 1/f reference line
```

### 2.  Frequency Response Measurement

**On PC (Generate Sweep Signal):**
```bash
cd src/frequency_sweep
python pc_freq_sweep.py
# Creates linear chirp: 20 Hz → 20 kHz over 10 seconds
# Output: data/linear_sweep_gen.wav
```

**On Raspberry Pi (Record Response):**
```bash
cd src/frequency_sweep
# Play linear_sweep_gen.wav on computer speakers
python record_freq_sweep.py
# Records microphone response at 48 kHz
# Output: data/recorded_sweep. wav
```

**On PC (Analyze Response):**
```bash
cd src/frequency_sweep
jupyter notebook freq_sweep_analysis.ipynb
# Applies Gaussian smoothing to PSD
# Performs octave band analysis
# Plots frequency response and octave band powers
```

### 3.  Telephone Effect Equalizer

**On Raspberry Pi (Record Test Audio):**
```bash
cd src/equalizer
# Play "Thriller" or other test audio on speakers
python record_sample.py
# Records 15 seconds at 48 kHz
# Output: data/recorded_sample_mono.wav
```

**On PC (Apply Filter):**
```bash
cd src/equalizer
python equalizer.py
# Designs cascaded 4th-order Butterworth filters:
#   - High-pass: 300 Hz cutoff
#   - Low-pass: 3.4 kHz cutoff
jupyter notebook equalizer_analysis.ipynb
# Applies filter and normalizes output
# Output: data/telephone_effect.wav
# The sliders can be adjusted to acheive any cut off - not just the telephone affect
```
## My Results

- Full analysis and results available in [Documentation/Final_Report.pdf](Documentation/Final_Report.pdf)
- IEEE Transactions format with comprehensive discussion of methods, results, and error analysis

## References

[1] Analog Devices, "Understanding and eliminating 1/f noise," *Analog Dialogue*.  [Online]. Available: https://www. analog.com/en/resources/analog-dialogue/articles/understanding-and-eliminating-1-f-noise. html

[2] A. V. Oppenheim and R.  W. Schafer, *Discrete-Time Signal Processing*, 3rd ed. Upper Saddle River, NJ: Prentice Hall, 2009.

[3] P. Welch, "The use of fast Fourier transform for the estimation of power spectra: A method based on time averaging over short, modified periodograms," *IEEE Trans. Audio Electroacoust. *, vol. 15, no. 2, pp. 70–73, Jun. 1967.

[4] S. Butterworth, "On the theory of filter amplifiers," *Wireless Engineer*, vol. 7, pp. 536–541, Oct. 1930.

[5] Knowles Electronics, "SPH0645LM4H-B datasheet: Digital MEMS microphone," *Knowles Acoustics*, 2016.  [Online]. Available: https://www.knowles.com/docs/default-source/model-downloads/sph0645lm4h-b-datasheet-rev-c.pdf

[6] V. Välimäki and J. D. Reiss, "All about audio equalization: Solutions and frontiers," *Applied Sciences*, vol. 6, no. 5, p. 129, May 2016.

[7] U. Zölzer, Ed., *DAFX: Digital Audio Effects*, 2nd ed. Chichester, UK: Wiley, 2011.

**Author:** Lokesh Sriram  
**Project Repository:** [github.com/lokichubs/equalizer-project](https://github.com/lokichubs/equalizer-project)