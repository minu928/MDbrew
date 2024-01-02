import numpy as np


def autocorrelation(data):
    data = np.asarray(data)
    N_frame = data.shape[0]
    # Do FFT
    X = np.fft.fft(data, n=2 * N_frame, axis=0)
    dot_X = X * X.conjugate()
    # Do iFFT
    x = np.fft.ifft(dot_X, axis=0)
    x = x[:N_frame].real
    x = x.sum(axis=-1)
    n = np.arange(N_frame, 0, -1)
    return x / n[:, np.newaxis]
