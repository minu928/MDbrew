import numpy as np
from tqdm import tqdm, trange

# Calculate and Plot the RDF
class RDF:
    def __init__(self, a: np.array, b: np.array, box_size: np.array) -> None:
        """RDF

        Class for calculate and plot the radial distribution function

        Args:
            a   (np.ndarray)  :   first molecule position data [x, y, z]
            b   (np.ndarray)  :   second molecule position data [x, y, z]
            box_size (np.ndarray) : size data of box [lx, ly, lz]
        """
        self.a = a
        self.b = b
        self.box_size = box_size
        self.a_number = self.a.shape[0]
        self.b_number = self.b.shape[0]

        self.PROGRESS_BAR_LENGTH = 70

    def get_rdf(self, resolution: int = 200):
        """Get RDF

        Function for calculate the RDF

        Args:
            resolution          (int)   :   set your resolution
            number_of_config    (int)   :   how much your simulation results

        Returns:
            radii   (np.ndarray)    :   data for x
            g_r     (np.ndarray)    :   each point's density
        """
        self.resolution = resolution
        self.r_max = min(self.box_size) / 2
        self.dr = self.r_max / resolution
        self.hist_data = np.zeros(resolution)

        if self.__check_single():
            self.__get_hist_single()
        else:
            self.__get_hist_binary()
        self.__cal_g_r()
        return self.g_r

    def get_radii(self) -> np.ndarray:
        """Get Radii

        return the radii data

        Returns:
            np.ndarray: raddii data
        """
        self.radii = self.__cal_radii()
        return self.radii

    # Check a == b
    def __check_single(self) -> bool:
        if self.a is self.b or self.a == self.b:
            print("\nSingle Case\n")
            self.count_num = 2
            return True
        else:
            print("\nBinary Case\n")
            self.count_num = 1
            return False

    # Get histogram data in single case
    def __get_hist_single(self):
        print("STEP : Make Hist Data in single case")
        for idx, a_position in enumerate(
            tqdm(self.a[:-1], ncols=self.PROGRESS_BAR_LENGTH)
        ):
            for b_position in self.b[idx:]:
                self.__update_hist_data(a_position, b_position)

    # Get histogram data in binary case
    def __get_hist_binary(self):
        print("STEP : Make Hist Data in binary case")
        for a_position in tqdm(self.a, ncols=self.PROGRESS_BAR_LENGTH):
            for b_position in self.b:
                self.__update_hist_data(a_position, b_position)

    # Update the hist_data
    def __update_hist_data(self, a_position: list[float], b_position: list[float]):
        r = self.__get_distance(a_position, b_position)
        idx_hist = int(r / self.dr)
        if 0 < idx_hist < self.resolution:
            self.hist_data[idx_hist] += self.count_num

    # Get the distance with checking PBC
    def __get_distance(self, a, b) -> float:
        """Distance (radius)

        Calculate distance between a & b with Periodic Boundary Layer

        Args:
            a, b        (np.ndarray) : position that we want to calculate radius

        Returns:
            float64 : radius between a and b
        """
        delta_coordinates = np.abs(a - b)
        delta_coordinates = self.__check_pbc(delta_coordinates)
        r = np.sqrt(np.sum(delta_coordinates * delta_coordinates))
        return r

    # Check the PBC
    def __check_pbc(self, delta_coordinates) -> np.array:
        """Check PBC

        Check delta_coordinates has a value that is larger than box_size

        Args:
            delta_coordinates   (np.ndarray) : distance data between each dimensions
            box_size            (np.ndarray) : size of simulation

        Returns:
            np.ndarray : value checked delta_coordinates with Periodic Boudary Layer
        """
        for dim, box_length in enumerate(self.box_size):
            if delta_coordinates[dim] * 2 > box_length:
                delta_coordinates[dim] = box_length - delta_coordinates[dim]
        return delta_coordinates

    # Calculate the Density Function
    def __cal_g_r(self):
        g_r = np.zeros(self.resolution)
        print("STEP : Make the g(r)")
        for i in trange(1, self.resolution, ncols=self.PROGRESS_BAR_LENGTH):
            r_i = i * self.dr
            g_r[i] = self.hist_data[i] / (r_i * r_i)
        b_number_density = self.b_number / np.prod(self.box_size)
        denomiator = 4 * np.pi * self.a_number * b_number_density * self.dr
        self.g_r = g_r / denomiator

    # Calculate the radii data
    def __cal_radii(self):
        return np.linspace(0, self.r_max, self.resolution)

    # Plot the g(r) with radii data
    def plot_g_r(self):
        import matplotlib.pyplot as plt

        try:
            plt.plot(self.radii, self.g_r, "k-")
            plt.xlabel("r")
            plt.ylabel("g(r)")
            plt.hlines(1.0, 0, self.r_max, colors="red", linestyles="--")
            plt.plot()
        except:
            raise Exception("get_g_r first")

    # Set the PROGRESS_BAR_LENGTH
    def set_progress_bar_length(self, width=70):
        self.PROGRESS_BAR_LENGTH = width
        print(f"Progress bar length is changed into {width}")

    # get histogramm data
    def get_histogram_data(self):
        return self.hist

    # set g(r)
    def set_g_r(self, g_r: np.ndarray):
        self.g_r = g_r
