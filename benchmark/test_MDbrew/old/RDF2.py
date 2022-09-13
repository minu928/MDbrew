import numpy as np
from tqdm import trange
import matplotlib.pyplot as plt


class RDF:
    def __init__(self, a: np.array, b: np.array, system_size: np.array) -> None:
        """init

        Args:
            a (np.array): [lag time, N_particle, dim]
            b (np.array): [lag time, N_particle, dim]
            box_size (np.array): [[-lx, lx], [-ly, ly], [-lz, lz]]
        """
        self.a = np.asarray(a)
        self.b = np.asarray(b)
        self.systme_size = np.asarray(system_size)[:, 1]
        self.box_length = self.systme_size * 2
        self.lag_number = self.a.shape[0]
        self.a_number = self.a.shape[1]
        self.b_number = self.b.shape[1]
        self.b_number_density = self.b_number / np.prod(self.box_length)

    # Main function for Get rdf from a and b, [lag time, N_particle, dim]
    def get_rdf(self, resolution: int = 200):
        self.resolution = resolution
        self.r_max = np.min(self.systme_size)
        self.dr = self.r_max / resolution
        self.histo_method = self.__check_method()
        self.hist_data = np.zeros(self.resolution)
        for lag in trange(self.lag_number, desc=" RDF  (STEP) ", ascii=True):
            self.unit_a = self.a[lag, :, :]
            self.unit_b = self.b[lag, :, :]
            self.histo_method()
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

    # Check a == b
    def __check_method(self):
        if self.a is self.b:
            # print("Single Case")
            self.count_num = 2
            return self.__get_hist_single
        else:
            # print("Binary Case\n")
            self.count_num = 1
            return self.__get_hist_binary

    # Get histogram data in single case
    def __get_hist_single(self):
        for idx, a_position in enumerate(self.unit_a[:-1]):
            for b_position in self.unit_b[idx + 1 :]:
                self.__update_hist_data(a_position, b_position)

    # Get histogram data in binary case
    def __get_hist_binary(self):
        for a_position in self.unit_a:
            for b_position in self.unit_b:
                self.__update_hist_data(a_position, b_position)

    # Update the hist_data
    def __update_hist_data(self, a_position: list[float], b_position: list[float]):
        r = self.__get_distance(a_position, b_position)
        idx_hist = int(r / self.dr)
        if 0 < idx_hist < self.resolution:
            self.hist_data[idx_hist] += self.count_num

    # Get the distance with checking PBC
    def __get_distance(self, a, b) -> float:
        delta_coordinates = np.abs(np.subtract(a, b))
        delta_coordinates = self.__check_pbc(delta_coordinates)
        r = np.sqrt(np.sum(np.square(delta_coordinates)))
        return r

    # Check the PBC
    def __check_pbc(self, delta_coordinates) -> np.array:
        for dim, box_length in enumerate(self.box_length):
            if delta_coordinates[dim] > self.systme_size[dim]:
                delta_coordinates[dim] = box_length - delta_coordinates[dim]
        return delta_coordinates

    # Calculate the Density Function
    def __cal_g_r(self):
        g_r = np.zeros(self.resolution)
        for i in range(1, self.resolution):
            r_i = i * self.dr
            g_r[i] = self.hist_data[i] / (r_i * r_i)
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
