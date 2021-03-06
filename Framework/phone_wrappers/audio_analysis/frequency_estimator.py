from __future__ import division
from numpy.fft import rfft
from numpy import argmax, mean, diff, log
import numpy
from matplotlib.mlab import find
from scipy.signal import blackmanharris, fftconvolve
from time import time
import sys
try:
    import soundfile as sf
except ImportError:
    from scikits.audiolab import flacread

# from parabolic import parabolic
# import parabolic as parabolic
import parabolic


def freq_from_crossings(sig, fs):
    """
    Estimate frequency by counting zero crossings
    """
    # Find all indices right before a rising-edge zero crossing
    indices = find((sig[1:] >= 0) & (sig[:-1] < 0))

    # Naive (Measures 1000.185 Hz for 1000 Hz, for instance)
    # crossings = indices

    # More accurate, using linear interpolation to find intersample
    # zero-crossings (Measures 1000.000129 Hz for 1000 Hz, for instance)
    crossings = [i - sig[i] / (sig[i+1] - sig[i]) for i in indices]

    # Some other interpolation based on neighboring points might be better.
    # Spline, cubic, whatever

    return fs / mean(diff(crossings))


def freq_from_fft(sig, fs):
    """
    Estimate frequency from peak of FFT
    """
    # Compute Fourier transform of windowed signal
    windowed = sig * blackmanharris(len(sig))
    f = rfft(windowed)

    # Find the peak and interpolate to get a more accurate peak
    i = argmax(abs(f))  # Just use this for less-accurate, naive version
    true_i = parabolic.parabolic(log(abs(f)), i)[0]

    # Convert to equivalent frequency
    return fs * true_i / len(windowed)


def freq_from_autocorr(sig, fs):
    """
    Estimate frequency using autocorrelation
    """
    # Calculate autocorrelation (same thing as convolution, but with
    # one input reversed in time), and throw away the negative lags
    corr = fftconvolve(sig, sig[::-1], mode='full')
    corr = corr[len(corr)//2:]

    # Find the first low point
    d = diff(corr)
    start = find(d > 0)[0]

    # Find the next peak after the low point (other than 0 lag).  This bit is
    # not reliable for long signals, due to the desired peak occurring between
    # samples, and other peaks appearing higher.
    # Should use a weighting function to de-emphasize the peaks at longer lags.
    peak = argmax(corr[start:]) + start
    px, py = parabolic.parabolic(corr, peak)

    return fs / px


def freq_from_HPS(self, sig, fs):
    """
    Estimate frequency using harmonic product spectrum (HPS)

    """
    windowed = sig * blackmanharris(len(sig))

    from pylab import subplot, plot, log, copy, show

    # harmonic product spectrum:
    c = abs(rfft(windowed))
    maxharms = 8
    subplot(maxharms, 1, 1)
    plot(log(c))
    for x in range(2, maxharms):
        a = copy(c[::x])  # Should average or maximum instead of decimating
        # max(c[::x],c[1::x],c[2::x],...)
        c = c[:len(a)]
        i = argmax(abs(c))
        true_i = parabolic.parabolic(abs(c), i)[0]
        print('Pass %d: %f Hz' % (x, fs * true_i / len(windowed)))
        c *= a
        subplot(maxharms, 1, x)
        plot(log(c))
    show()

filename = sys.argv[1]

print('Reading file "%s"\n' % filename)
# try:
# signal, fs = sf.read(filename, dtype='int16', channels=1)
signal, fs = sf.read(filename, format='RAW', samplerate=16000, channels=1, subtype='PCM_16')
# except NameError:
    # signal, fs, enc = flacread(filename)

# fs = 160000
# signal = numpy.memmap(filename, dtype='h', mode='r')    
    
print('Calculating frequency from FFT:',)
start_time = time()
print('%f Hz' % freq_from_fft(signal, fs))
print('Time elapsed: %.3f s\n' % (time() - start_time))

print('Calculating frequency from zero crossings:',)
start_time = time()
print('%f Hz' % freq_from_crossings(signal, fs))
print('Time elapsed: %.3f s\n' % (time() - start_time))

print('Calculating frequency from autocorrelation:',)
start_time = time()
print('%f Hz' % freq_from_autocorr(signal, fs))
print('Time elapsed: %.3f s\n' % (time() - start_time))

# print('Calculating frequency from harmonic product spectrum:')
# start_time = time()
# freq_from_HPS(signal, fs)
# print('Time elapsed: %.3f s\n' % (time() - start_time))
