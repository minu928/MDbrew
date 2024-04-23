import numpy as np


def autocorrelation(data):
    data = np.asarray(data)
    nframe = data.shape[0]
    X = np.fft.fft(data, n=2 * nframe, axis=0)
    dot_X = X * X.conjugate()
    x = np.fft.ifft(dot_X, axis=0)
    x = x[:nframe].real
    x = x.mean(axis=-1)
    x /= np.arange(nframe, 0, -1)
    x /= x[0]
    return x
