import numpy as np
import matplotlib.pyplot as plt

print("Computing...")

fname = "./shared/test_tone/c000p0.bin"

f = open(fname, 'rb')
a = np.fromfile(f, dtype=np.complex64, count=100000)

# Compute FFT on the binary file
fft = np.fft.fft(a)
#print fft

# We have the matrix of fft
# Now get the magnitude
magnitude = np.absolute(fft)
#print magnitude

# Determine matrix of frequencies for computation
freqs = np.fft.fftfreq(len(a), d=3.2e-7)
#print(freqs)

# Plot FFT
plt.plot(freqs, magnitude)
plt.show()