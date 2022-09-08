import numpy as np
import matplotlib.pyplot as plt


class MSD(object):
    def __init__(self) -> None:
        self.axis_dict = {"lag": 0, "N_particle": 1, "pos": -1}
        self.msd_data = 0

    def get_msd(self, position: np.ndarray, method="window", fft=True) -> np.ndarray:
        """Get MSD

        Calculate the msd data and return it with method and fft

        Args:
            position (np.ndarray):  Data of Particle's position in each lag time
            method (str, optional): default = 'window' (window or direct)
            fft (bool, optional): default = True

        Returns:
            np.ndarray: _description_
        """
        self.position = np.asarray(position, dtype=float)
        self.msd_data = 0

        if method == "direct":
            self.msd_data = self.__get_msd_direct()
        elif method == "window":
            if fft:
                self.msd_data = self.__get_msd_fft()
            else:
                self.msd_data = self.__get_msd_window()
        else:
            print(f"method can be (direct / window) : your note {method} is wrong")

        return self.msd_data

    # Direct method
    def __get_msd_direct(self) -> list[float]:
        """MSD - Direct Method

        Calculate the MSD list with linear loop with numpy function

        Time complexity : O(N**2)

        Args:
            position (np.ndarray): Data of Particle's position in each lag time
                - shape = [Number of lag, Number of particle, Coordinate data]

        Returns:
            list[float]: MSD data of each lag time
        """

        def cal_msd(diff_pos):
            return np.square(diff_pos).sum(axis=self.axis_dict["N_particle"]).mean()

        initial_position = self.position[0]
        msd = [
            cal_msd(np.subtract(current_position, initial_position))
            for current_position in self.position
        ]
        return msd

    # Window method with non-FFT
    def __get_msd_window(self):
        """MSD - Window Method with non-FFT

        Calculate the MSD list with linear loop with numpy function

        Time complexity : O(N**2)

        Args:
            position (np.ndarray): Data of Particle's position in each lag time
                - shape = [Number of lag, Number of particle, Coordinate data]

        Returns:
            list[float]: MSD data of each lag time
        """
        N, N_particle = self.position.shape[:2]
        msd_list = np.zeros((N, N_particle))
        for lag in np.arange(1, N):
            diff = self.position[lag:] - self.position[:-lag]
            sqdist = np.square(diff).sum(axis=self.axis_dict["pos"])
            msd_list[lag, :] = np.mean(sqdist, axis=self.axis_dict["lag"])
        return msd_list.mean(axis=self.axis_dict["N_particle"])

    # Window method with FFT
    def __get_msd_fft(self):
        """MSD - Window method wit FFT

        Calculate the MSD list with linear loop with numpy function

        Time complexity : O(N logN)

        Args:
            position (np.ndarray): Data of Particle's position in each lag time
                - shape = [Number of lag, Number of particle, Coordinate data]

        Returns:
            list[float]: MSD data of each lag time
        """
        N, N_particle = self.position.shape[:2]

        D = np.square(self.position).sum(axis=self.axis_dict["pos"])
        D = np.append(D, np.zeros((N, N_particle)), axis=self.axis_dict["lag"])
        Q = 2 * np.sum(D, axis=self.axis_dict["lag"])
        S_1 = np.zeros((N, N_particle))
        for m in range(N):
            Q -= D[m - 1, :] + D[N - m, :]
            S_1[m, :] = Q / (N - m)

        S_2 = self.__auto_correlation()
        return np.subtract(S_1, 2 * S_2).mean(axis=self.axis_dict["N_particle"])

    # get S2 for FFT
    def __auto_correlation(self):
        N = len(self.position)
        X = np.fft.fft(self.position, n=2 * N, axis=self.axis_dict["lag"])
        psd = X * X.conjugate()
        x = np.fft.ifft(psd, axis=self.axis_dict["lag"])
        x = x[:N].real
        x = x.sum(axis=self.axis_dict["pos"])
        n = np.arange(N, 0, -1)
        return x / n[:, np.newaxis]

    # plot the data
    def plot_msd(self, time_step=1, **kwargs):
        lagtime = len(self.position)
        if self.msd_data:
            x = np.arange(lagtime*time_step)
            y = self.msd_data
            plt.plot(x, y, **kwargs)
            plt.show()
        else:
            raise ConnectionError("Please do get_msd first")
