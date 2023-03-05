from tqdm import trange
from .._base import *
from ..tool import spacer
import matplotlib.pyplot as plt

__all__ = ["MSD"]


# Class of Mean Square Displacement
class MSD(object):
    def __init__(self, position: NDArray, fft: bool = True):
        """MSD

        Calculate the msd data and return it with method and fft

        Parameters
        ------------
        position : NDArray
            Data of Particle's position in each frame
        fft : bool, optional
            default = True, if True the calculation in FFT, else  matrix

        ## Result of 'Mean Square Displacement'
        >>> my_msd      = MSD(position = position, fft = True)
        >>> msd_result  = my_msd.result
        """
        self.axis_dict = {"frame": 0, "N_particle": 1, "pos": -1}
        self.position = spacer.check_dimension(position, dim=3)
        self.kwrgs_trange = {"desc": " MSD  (STEP) ", "ncols": 70, "ascii": True}
        self.frame_number = self.position.shape[0]
        self.fft = fft

    @property
    def result(self) -> NDArray[np.float64]:
        """run

        Return
        ----------
        NDArray[np.float64]: result of MSD
        """
        if self.fft:
            self._result = self.__get_msd_fft()
        else:
            self._result = self.__get_msd_window()
        return self._result

    # window method with non-FFT
    def __get_msd_window(self) -> NDArray[np.float64]:
        """MSD - Window Method with non-FFT

        Calculate the MSD list with linear loop with numpy function

        Time complexity : O(N**2)

        Returns
        ----------
        NDArray[np.float64]
            MSD data of each frame
        """
        msd_list = np.zeros(self.position.shape[:2])
        for frame in trange(1, self.frame_number, **self.kwrgs_trange):
            diff_position = spacer.get_diff_position(self.position[frame:], self.position[:-frame])
            distance = self.__square_sum_position(diff_position)
            msd_list[frame, :] = np.mean(distance, axis=self.axis_dict["frame"])
        return self.__mean_msd_list(msd_list=msd_list)

    # window method with FFT
    def __get_msd_fft(self) -> NDArray[np.float64]:
        """MSD - Window method wit FFT

        Calculate the MSD list with linear loop with numpy function

        Time complexity : O(N logN)

        Returns
        ----------
        NDArray[np.float64]
            MSD data of each frame
        """
        S_1 = self.__get_S_1()
        S_2 = self.__get_S_2()
        msd_list = np.subtract(S_1, 2.0 * S_2)
        return self.__mean_msd_list(msd_list=msd_list)

    def __get_S_1(self) -> NDArray[np.float64]:
        empty_matrix = np.zeros(self.position.shape[:2])
        D = self.__square_sum_position(self.position)
        D = np.append(D, empty_matrix, axis=self.axis_dict["frame"])
        Q = 2.0 * np.sum(D, axis=self.axis_dict["frame"])
        S_1 = empty_matrix
        for m in trange(self.frame_number, **self.kwrgs_trange):
            Q -= D[m - 1, :] + D[self.frame_number - m, :]
            S_1[m, :] = Q / (self.frame_number - m)
        return S_1

    # get S2 for FFT
    def __get_S_2(self) -> NDArray[np.float64]:
        X = np.fft.fft(self.position, n=2 * self.frame_number, axis=self.axis_dict["frame"])
        dot_X = X * X.conjugate()
        x = np.fft.ifft(dot_X, axis=self.axis_dict["frame"])
        x = x[: self.frame_number].real
        x = x.sum(axis=self.axis_dict["pos"])
        n = np.arange(self.frame_number, 0, -1)
        return x / n[:, np.newaxis]

    # do square and sum about position
    def __square_sum_position(self, position_data) -> NDArray[np.float64]:
        return np.square(position_data).sum(axis=self.axis_dict["pos"])

    # do mean about msd list
    def __mean_msd_list(self, msd_list) -> NDArray[np.float64]:
        return msd_list.mean(axis=self.axis_dict["N_particle"])

    # plot the data
    def plot_result(self, time_step: float = 1, *args, **kwargs):
        if not hasattr(self, "_result"):
            self.result
        x = np.arange(0, self.frame_number * time_step, time_step)
        plt.plot(x, self._result, *args, **kwargs)
        plt.show()
