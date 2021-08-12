import numpy as np


class GPS_L1CA(object):

    def __init__(self):
        # G1 polynomial = X^10 + X^3 + 1
        # G2 polynomial = X^10 + X^9 + X^8 + X^6 + X^3 + X^2 + 1
        self.rf_freq = int(10.23 * 154 * 10e6)  # L1 Frequency (Hz) (1575.42 MHz)
        self.G1_initial = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.bool)
        self.G2_initial = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], dtype=np.bool)
        self.CA_code_count = int(1023)
        self.CA_code_rate = 1023000  # Code clock rate (MHz)
        self.CA_code_period = 1 / self.CA_code_rate  # Code period (s)
        self.SV_ID = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                               25, 26, 27, 28, 29, 30, 31, 32, 66, 67, 68, 69])
        self.PRN = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                             26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37])
        self.PRN_delay = np.array([5, 6, 7, 8, 17, 18, 139, 140, 141, 251, 252, 254, 255, 256, 257, 258, 469, 470, 471,
                                   472, 473, 474, 509, 512, 513, 514, 515, 516, 859, 860, 861, 862, 950, 947, 948, 950])
        self.SBAS_PRN = np.array([120, 121, 122, 123, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137,
                                  138, 140, 141, 143, 144, 147, 148, 183, 193])
        self.SBAS_delay = np.array([145, 175, 52, 21, 235, 886, 657, 634, 762, 355, 1012, 176, 603, 130, 359, 595,
                                    68, 386, 456, 499, 307, 127, 118, 163, 144, 339])
        self.SBAS_initial = np.array([0o1106, 0o1241, 0o0267, 0o0232, 0o1076, 0o1764, 0o0717, 0o1532, 0o1250, 0o0341,
                                      0o0551, 0o0520, 0o1731, 0o0706, 0o1216, 0o0740, 0o1007, 0o0450, 0o1653, 0o1411,
                                      0o1312, 0o1060, 0o0355, 0o0335, 0o1562, 0o0727])
        self.G1_register = np.zeros(10, dtype=np.bool)
        self.G2_register = np.zeros(10, dtype=np.bool)
        self.G1 = np.zeros(1023, dtype=np.bool)
        self.G2 = np.zeros(1023, dtype=np.bool)

    def create_G1_G2(self, PRN):
        self.G1_register = self.G1_initial
        if PRN > 119:
            idx = int(np.where(self.SBAS_PRN == PRN)[0])
            initial = '{0:010b}'.format(self.SBAS_initial[idx])
            for i in range(len(initial)):
                self.G2_initial[i] = int(initial[i])
            self.G2_register = self.G2_initial
            delay = self.SBAS_delay[idx]

            # TODO: SBAS calc doesn't meet standard 'first 10 chips'

        else:
            idx = int(np.where(self.PRN == PRN)[0])
            self.G2_register = self.G2_initial
            delay = self.PRN_delay[idx]

        for shift in range(self.CA_code_count):
            self.G1[shift] = self.G1_register[9]
            self.G2[shift] = self.G2_register[9]

            G1_fb = self.G1_register[9] ^ self.G1_register[2]
            G2_fb = self.G2_register[9] ^ self.G2_register[8] ^ self.G2_register[7] ^ self.G2_register[5] ^ \
                    self.G2_register[2] ^ self.G2_register[1]

            self.G1_register = np.roll(self.G1_register, 1)
            self.G2_register = np.roll(self.G2_register, 1)

            self.G1_register[0] = G1_fb
            self.G2_register[0] = G2_fb

        self.G2 = np.roll(self.G2, delay)
        G_code = np.bitwise_xor(self.G1, self.G2)
        return G_code

    def G_code_sampled(self, PRN, fs, doppler):
        G_code_sampled = np.zeros(int(fs / 1000), dtype=np.complex)  # Samples for 1ms
        samples_per_code = fs / self.CA_code_rate
        G_code = self.create_G1_G2(PRN)

        for i in range(len(G_code)):
            cur_count = round(i * samples_per_code)
            next_count = round((i + 1) * samples_per_code)
            if G_code[i]:
                G_code_sampled[cur_count:next_count] = np.complex(0, 1)
            else:
                G_code_sampled[cur_count:next_count] = np.complex(0, -1)

        print(G_code[-10:])
        print(G_code_sampled[-50:])




