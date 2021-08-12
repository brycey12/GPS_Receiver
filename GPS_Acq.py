import numpy as np
import matplotlib.pyplot as plt
import GPS_Numbers


def create_fft(IQ, start, stop):
    sample_freq = 4000000
    sample_time = 1 / sample_freq
    time_points = np.arange(start, stop, sample_time)
    time_points = time_points[0:-1]
    fft_result = np.fft.fft(IQ) / len(IQ)
    fft_result = fft_result[range(int(len(IQ) / 2))]

    sample_count = len(IQ)
    values = np.arange(int(sample_count / 2))
    time_period = sample_count / sample_freq
    freqs = values / time_period

    figure, ax = plt.subplots(2, 1)
    ax[0].plot(IQ.real)
    ax[0].plot(IQ.imag)
    ax[1].plot(freqs, abs(fft_result.real))
    plt.show()


if __name__ == '__main__':
    fs = 4000000
    L1CA = GPS_Numbers.GPS_L1CA()
    L1CA.G_code_sampled(20, fs, 0)

    # filename = 'C:\\Python Projects\\GPS\\GPS_Receiver\\Data\\2013_04_04_GNSS_SIGNAL_at_CTTC_SPAIN.dat'
    # data = np.fromfile(filename, count=100000, dtype='int16')
    # I_data = data[0:80000:2]
    # Q_data = data[1:80000:2]
    # IQ_data = I_data + (1j * Q_data)
    #
    # create_fft(IQ_data[0:4000], 0, 0.001)

