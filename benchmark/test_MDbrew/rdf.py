import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt

# Calculate and Plot the RDF
class RDF:
    def __init__(self, a: np.array, b: np.array, system_size: np.array) -> None:
        """init

        Args:
            a (np.array): [lag time, N_particle, dim]
            b (np.array): [lag time, N_particle, dim]
            system_size (np.array): [[-lx, lx], [-ly, ly], [-lz, lz]]
        """
        self.a = np.asarray(a, dtype=np.float64)
        self.b = np.asarray(b, dtype=np.float64)
        self.system_size = np.asarray(system_size, dtype=np.float64)[:, 1]
        self.box_length = self.system_size * 2.0
        self.lag_number = self.a.shape[0]
        self.a_number = self.a.shape[1]
        self.b_number = self.b.shape[1]

    # Main function for Get rdf from a and b, [lag time, N_particle, dim]
    def get_rdf(self, r_max: float, resolution: int = 10000):
        self.r_max = r_max
        self.resolution = resolution
        self.dr = float(self.r_max / self.resolution)
        self.hist_data = np.zeros(self.resolution)
        kwrgs_trange = {"desc": " RDF  (STEP) ", "ncols": 70, "ascii": True}
        for lag in trange(self.lag_number, **kwrgs_trange):
            self.a_unit = self.a[lag, :, :].astype(np.float64)
            self.b_unit = self.b[lag, :, :].astype(np.float64)
            self.__make_histogram()
        self.g_r = self.__get_g_r()
        return self.g_r

    # Function for get radii data
    def get_radii(self) -> np.ndarray:
        self.radii = np.linspace(0.0, self.r_max, self.resolution)
        return self.radii

    # Function for get coordinate number
    def get_CN(self) -> np.ndarray:
        self.n = self.hist_data / (self.lag_number * self.a_number)
        self.cn = np.cumsum(self.n)
        return self.cn

    # make a histogram
    def __make_histogram(self):
        for b_line in self.b_unit:
            b_tile = np.tile(b_line, (self.a_number, 1))
            diff_position = self.__get_diff_position(target=b_tile)
            checked_position = self.__check_PBC(diff_position=diff_position)
            distance = self.__get_distance(diff_position=checked_position)
            idx_hist = self.__get_idx_histogram(distance=distance)
            self.hist_data[idx_hist] += 1.0

    # check the diiferent of position
    def __check_PBC(self, diff_position):
        return np.where(
            diff_position > self.system_size,
            np.abs(self.box_length - diff_position),
            diff_position,
        )

    # get position difference
    def __get_diff_position(self, target):
        return np.abs(np.subtract(self.a_unit, target, dtype=np.float64))

    # get distance from different of position
    def __get_distance(self, diff_position):
        return np.sqrt(np.sum(np.square(diff_position), axis=-1))

    # get idx for histogram
    def __get_idx_histogram(self, distance):
        idx_hist = (distance / self.dr).astype(np.int64)
        return idx_hist[np.where((0 < idx_hist) & (idx_hist < self.resolution))]

    # Calculate the Density Function
    def __get_g_r(self):
        r_i = self.get_radii()[1:]
        g_r = np.append(0.0, self.hist_data[1:] / np.square(r_i))
        factor = np.array(4.0 * np.pi * self.b_number * self.dr, dtype=np.float64)
        factor *= np.array(self.lag_number * self.a_number, dtype=np.float64)
        box_volume = np.prod(self.box_length, dtype=np.float64)
        return g_r * box_volume / factor

    # Plot the g(r) with radii datas
    def plot_g_r(self, bins: int = 1, *args, **kwrgs):
        try:
            x = self.radii[::bins]
            y = self.g_r[::bins]
            plt.plot(x, y, *args, **kwrgs)
            plt.xlabel("r")
            plt.ylabel("g(r)")
            plt.hlines(1.0, 0, self.r_max + 1, colors="black", linestyles="--")
            plt.plot()
        except:
            raise Exception("get_g_r first")

    # Plot the cn with radii data
    def plot_cn(self, *args, **kwrgs):
        try:
            plt.plot(self.radii, self.cn, *args, **kwrgs)
            plt.xlabel("r")
            plt.ylabel("cn")
            plt.plot()
        except:
            raise Exception("get_cn first")
