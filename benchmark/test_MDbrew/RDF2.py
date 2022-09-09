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
            box_size (np.array): [[-lx, lx], [-ly, ly], [-lz, lz]]
        """
        self.a = np.asarray(a, dtype=np.float64)
        self.b = np.asarray(b, dtype=np.float64)
        self.system_size = np.asarray(system_size, dtype=np.float64)[:, 1]
        self.box_length = self.system_size * 2
        self.lag_number = self.a.shape[0]
        self.a_number = self.a.shape[1]
        self.b_number = self.b.shape[1]
        self.b_number_density = self.b_number / np.prod(self.box_length)

        self.over_ = []

    # Main function for Get rdf from a and b, [lag time, N_particle, dim]
    def get_rdf(self, resolution: int = 10000):
        self.resolution = resolution
        self.r_max = np.min(self.system_size).astype(np.float64)
        self.dr = (self.r_max / self.resolution).astype(np.float64)
        self.hist_data = np.zeros(self.resolution)
        kwrgs_trange = {"desc": " RDF  (STEP) ", "ncols": 70, "ascii": True}
        for lag in trange(self.lag_number, **kwrgs_trange):
            self.unit_a = self.a[lag, :, :].astype(np.float64)
            self.unit_b = self.b[lag, :, :].astype(np.float64)
            # self.__get_hist_new()
            self.__get_hist_bye()
        self.g_r = self.__cal_g_r()
        return self.g_r

    # Function for get radii data
    def get_radii(self) -> np.ndarray:
        self.radii = np.linspace(0, self.r_max, self.resolution)
        return self.radii

    # Function for get coordinate number
    def get_CN(self) -> np.ndarray:
        self.n = self.hist_data / (self.lag_number * self.a_number)
        self.cn = np.cumsum(self.n)
        return self.cn

    def __get_hist_new(self):
        for shift in range(1, self.b_number):
            b = np.roll(self.unit_b, shift, axis=0)
            #
            diff_position = np.abs(np.subtract(self.unit_a, b))
            diff_position = np.where(
                diff_position > self.system_size,
                self.box_length - diff_position,
                diff_position,
            )
            r = np.sqrt(np.sum(np.square(diff_position), axis=-1))
            idx_hist = (r * self.resolution / self.r_max).astype(np.int64)
            self.over_.append(idx_hist[np.where(idx_hist > self.resolution)])
            idx_hist = idx_hist[np.where((0 < idx_hist))]
            idx_hist = idx_hist[np.where((idx_hist < self.resolution))]
            self.hist_data[idx_hist] += 1

    def __get_hist_bye(self):
        for b_line in self.unit_b:
            b = np.tile(b_line, (self.a_number, 1))
            diff_position = np.abs(np.subtract(self.unit_a, b))
            diff_position = np.where(
                diff_position > self.system_size,
                self.box_length - diff_position,
                diff_position,
            )
            r = np.sqrt(np.sum(np.square(diff_position), axis=-1))
            idx_hist = (r * self.resolution / self.r_max).astype(np.int64)
            self.over_.append(idx_hist[np.where(idx_hist > self.resolution)])
            idx_hist = idx_hist[np.where((0 < idx_hist))]
            idx_hist = idx_hist[np.where((idx_hist < self.resolution))]
            self.hist_data[idx_hist] += 1

    # Calculate the Density Function
    def __cal_g_r(self):
        r_i = np.arange(1, self.resolution) * self.dr
        g_r = np.append(0, self.hist_data[1:] / np.square(r_i))
        self.factor = 4 * np.pi * self.b_number_density * self.dr
        denominator = self.factor * self.lag_number * self.a_number
        return g_r / denominator

    # Plot the g(r) with radii data
    def plot_g_r(self, *args, **kwrgs):
        try:
            plt.plot(self.get_radii(), self.g_r, *args, **kwrgs)
            plt.xlabel("r")
            plt.ylabel("g(r)")
            plt.hlines(1.0, 0, self.r_max, colors="red", linestyles="--")
            plt.plot()
        except:
            raise Exception("get_g_r first")
