import numpy as np
from tqdm import trange, tqdm
from ..spatial import spacer
from ..main.brewery import Brewery
from ..tool.colorfont import color


# Class of Mean Square Displacement
class MSD(object):
    axis_dict = {"frame": 0, "N_particle": 1, "pos": -1}
    kwrgs_trange = {
        "desc": f"[ {color.font_cyan}BREW{color.reset} ]  #{color.font_green}MSD{color.reset} ",
        "ncols": 60,
        "ascii": True,
    }
    kwrgs_pos = {
        "desc": f"[ {color.font_cyan}BREW{color.reset} ]  #{color.font_green}POS{color.reset} ",
        "ncols": 60,
        "ascii": True,
    }

    def __init__(self, position, fft: bool = True, dtype: str = float, do_unwrap: bool = False):
        """MSD

        Calculate the msd data and return it with method and fft

        Parameters
        ------------
        position
            Data of Particle's position in each frame
        fft : bool, optional
            default = True, if True the calculation in FFT, else  matrix

        ## Result of 'Mean Square Displacement'
        >>> my_msd      = MSD(position = position, fft = True)
        >>> msd_result  = my_msd.result
        """
        self.position = position
        self._dtype = dtype
        self._do_unwrap = do_unwrap
        self._fft = fft

    def run(self, start: int = 0, end: int = None, step: int = 1):
        """run

        Return
        ----------
        NDArray[np.float64]: result of MSD
        """
        if type(self.position) == Brewery:
            if self._do_unwrap:
                self.position.move_frame(start)
                unwrapped_position = self.position.coords[None, :]
                pre_position = self.position.coords
                pos_range = tqdm(self.position.frange(start=start + 1, end=end, step=step), **self.kwrgs_pos)
                for _ in pos_range:
                    this_position = self.position.coords
                    up, ixyz = spacer.unwrap_position(
                        pre_position=pre_position,
                        position=this_position,
                        box=self.position.box_size,
                        ixyz=ixyz,
                        return_ixyz=True,
                    )
                    pre_position = this_position.copy()
                    unwrapped_position = np.concatenate([unwrapped_position, up[None, :]], axis=0)
                self.position = unwrapped_position.copy()
            else:
                pos_range = tqdm(self.position.frange(start=start, end=end, step=step), **self.kwrgs_pos)
                self.position = np.array([self.position.coords for _ in pos_range], dtype=self._dtype)
        else:
            self.position = spacer.check_dimension(self.position, dim=3)
        self.frame_number = self.position.shape[0]
        if self._fft:
            self._result = self.__get_msd_fft()
        else:
            self._result = self.__get_msd_window()
        return self

    @property
    def result(self):
        if not hasattr(self, "_result"):
            self.run()
        return self._result

    # window method with non-FFT
    def __get_msd_window(self):
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
    def __get_msd_fft(self):
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

    def __get_S_1(self):
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
    def __get_S_2(self):
        X = np.fft.fft(self.position, n=2 * self.frame_number, axis=self.axis_dict["frame"])
        dot_X = X * X.conjugate()
        x = np.fft.ifft(dot_X, axis=self.axis_dict["frame"])
        x = x[: self.frame_number].real
        x = x.sum(axis=self.axis_dict["pos"])
        n = np.arange(self.frame_number, 0, -1)
        return x / n[:, np.newaxis]

    # do square and sum about position
    def __square_sum_position(self, position_data):
        return np.square(position_data).sum(axis=self.axis_dict["pos"])

    # do mean about msd list
    def __mean_msd_list(self, msd_list):
        return msd_list.mean(axis=self.axis_dict["N_particle"])
