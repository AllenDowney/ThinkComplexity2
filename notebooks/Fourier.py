""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

# importing cmath makes exp and other math functions handle
# complex numbers
from cmath import *

import numpy
import matplotlib.pyplot as pyplot


def fft(h):
    """Computes the discrete Fourier transform of the sequence h.
    Assumes that len(h) is a power of two.
    """
    N = len(h)
 
    # the Fourier transform of a single value is itself
    if N == 1: return h
 
    # recursively compute the FFT of the even and odd values
    He = fft(h[0:N:2])
    Ho = fft(h[1:N:2])
 
    # merge the half-FFTs
    i = complex(0,1)
    W = exp(2*pi*i/N)
    ws = [pow(W,k) for k in range(N)]
    H = [e + w*o for w, e, o in zip(ws, He+He, Ho+Ho)]
    return H

def psd(H, N):
    p = [Hn * Hn.conjugate() for Hn in H]
    freqs = range(N/2 + 1)
    p = [p[f].real for f in freqs]
    return freqs, p

def main(script, use_numpy=False):
    # make a signal with two sine components, f=6 and f=12
    N = 128
    t = [1.0*n/N for n in range(N)]
    h = [sin(2*pi*6*tn) + sin(2*pi*12*tn) for tn in t]

    # compute the Fourier transform
    if use_numpy:
        H = numpy.fft.fft(h)
    else:
        H = fft(h)

    # compute the power spectral density
    freqs, p = psd(H, N)

    # plot the real part
    pyplot.bar(freqs, p)
    pyplot.xlabel('frequency')
    pyplot.ylabel('amplitude')
    pyplot.show()

    # estimate the power spectral density by Welches average
    # periodogram method using the psd function provided by pylab.
    pyplot.show()

if __name__ == '__main__':
    import sys
    main(*sys.argv)

