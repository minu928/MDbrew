from tqdm import trange
from .._base import *
from ..tool.spacer import *

__all__ = ["RDF"]

# Calculate and Plot the RDF
class RDF:
    def __init__(
        self,
        a: NDArray,
        b: NDArray,
        system_size: NDArray,
        layer_depth: int = 0,
        r_max: float = None,
        resolution: int = 1000,
    ):
        """RDF

        Args:
            a (NDArray): [frame, N_particle, dim]
            b (NDArray): [frame, N_particle, dim]
            system_size (NDArray): [[-lx, lx], [-ly, ly], [-lz, lz]]

        Kwargs:
            r_max (float): you can input the max radius else None means 'calculate max(system_size)'
            resolution (int): resolution of dr
            layer_depth (int) : how many layer do you set, 0 means with PBC (one box) other layered

        ## Result of Radial Density Function, Coordination Number
        >>> my_rdf     = RDF(a_position, b_position, system_size)
        >>> rdf_result = my_rdf.result
        >>> cn_result  = my_rdf.cn
        """
        self.a = check_dimension(a, dim=3)
        self.b = check_dimension(b, dim=3)

        self.system_size = check_dimension(system_size, dim=2)[:, 1]
        self.box_length = self.system_size * 2.0

        self.layer_depth = layer_depth
        self.layer = self.__make_layer()
        self.is_layered = layer_depth

        self.frame_number = self.a.shape[0]
        self.a_number, self.b_number = self.a.shape[1], self.b.shape[1]

        self.r_max = self.__set_r_max(r_max)
        self.resolution = resolution
        self.dr = self.r_max / self.resolution

        self.run()

    # run the class
    def run(self):
        """run

        Function for calculate the rdf, cn.

        Returns:
            list[NDArray] : [radii, result, cn]
        """
        self._get_hist()
        self._get_radii()
        self._get_result()
        self._get_cn()
        return [self.radii, self.result, self.cn]

    # Function for get hist
    def _get_hist(self) -> NDArray[np.float64]:
        self.hist_data = np.zeros(self.resolution)
        self.__apply_boundary = self.__set_boundary_mode()
        kwrgs_trange = {"desc": " RDF  (STEP) ", "ncols": 70, "ascii": True}
        for frame in trange(self.frame_number, **kwrgs_trange):
            self.a_unit = self.a[frame, ...].astype(np.float64)
            self.b_unit = self.b[frame, ...].astype(np.float64)
            self.__make_histogram()

    # Function for get rdf
    def _get_result(self) -> NDArray[np.float64]:
        self.result = self.__get_g_r()

    # Function for get radii data
    def _get_radii(self) -> NDArray[np.float64]:
        self.radii = np.linspace(0.0, self.r_max, self.resolution)

    # Function for get coordinate number
    def _get_cn(self) -> NDArray[np.float64]:
        self.n = self.hist_data / (self.frame_number * self.a_number)
        self.cn = np.cumsum(self.n)

    # make a histogram
    def __make_histogram(self):
        for b_line in self.b_unit:
            diff_position = get_diff_position(self.a_unit, b_line)
            diff_position = self.__apply_boundary(diff_position=diff_position)
            distance = get_distance(diff_position=diff_position, axis=-1)
            idx_hist = self.__get_idx_histogram(distance=distance)
            value, count = np.unique(idx_hist, return_counts=True)
            self.hist_data[value] += count

    # select the mode with Boundary Layer
    def __set_boundary_mode(self):
        if self.is_layered:
            return self.__add_layer
        else:
            return self.__check_pbc

    # set the pbc only consider single system
    def __check_pbc(self, diff_position) -> NDArray[np.float64]:
        diff_position = np.abs(diff_position)
        return np.where(
            diff_position > self.system_size,
            self.box_length - diff_position,
            diff_position,
        )

    # set the pbc with 27 system
    def __add_layer(self, diff_position) -> NDArray[np.float64]:
        return diff_position[:, np.newaxis, :] + self.layer

    # Make a 3D layer_idx
    def __make_layer(self) -> NDArray[np.float64]:
        list_direction = []
        idx_direction_ = range(-self.layer_depth, self.layer_depth + 1)
        for i in idx_direction_:
            for j in idx_direction_:
                for k in idx_direction_:
                    list_direction.append([i, j, k])
        return np.array(list_direction) * self.box_length

    # get idx for histogram
    def __get_idx_histogram(self, distance) -> NDArray[np.int64]:
        idx_hist = (distance / self.dr).astype(np.int64)
        return idx_hist[np.where((0 < idx_hist) & (idx_hist < self.resolution))]

    # Calculate the Density Function
    def __get_g_r(self) -> NDArray[np.float64]:
        r_i = self.radii[1:]
        g_r = np.append(0.0, self.hist_data[1:] / np.square(r_i))
        factor = np.array(
            4.0 * np.pi * self.dr * self.frame_number * self.a_number * self.b_number,
            dtype=np.float64,
        )
        box_volume = np.prod(self.box_length, dtype=np.float64)
        return g_r * box_volume / factor

    def __set_r_max(self, r_max) -> np.float64:
        if r_max is not None:
            return r_max
        else:
            return max(self.system_size) * (2.0 * self.layer_depth + 1.0)

    # Plot the g(r) with radii datas
    def plot_result(self, bins: int = 1, *args, **kwrgs):
        x = self.radii[::bins]
        y = self.result[::bins]
        plt.plot(x, y, *args, **kwrgs)
        plt.xlabel("r")
        plt.ylabel("g(r)")
        plt.hlines(1.0, 0, self.r_max + 1, colors="black", linestyles="--")
        plt.plot()

    # Plot the cn with radii data
    def plot_cn(self, *args, **kwrgs):
        plt.plot(self.radii, self.cn, *args, **kwrgs)
        plt.xlabel("r")
        plt.ylabel("cn")
        plt.plot()
