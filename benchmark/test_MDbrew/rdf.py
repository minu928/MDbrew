from tqdm import trange
from .tools import *

# Calculate and Plot the RDF
class RDF:
    def __init__(
        self,
        a: NDArray,
        b: NDArray,
        system_size: NDArray,
        r_max: float = None,
        resolution: int = 1000,
        pbc: str = "single",
    ):
        """init

        Args:
            a (NDArray): [lag time, N_particle, dim]
            b (NDArray): [lag time, N_particle, dim]
            system_size (NDArray): [[-lx, lx], [-ly, ly], [-lz, lz]]

        Kwargs:
            r_max (float): you can input the max radius else None means 'calculate max(system_size)'
            resolution (int): resolution of dr
            pbc (str) : you can choose "single" or "layer"

        ## Result of Radial Density Function, Coordination Number
        >>> my_rdf     = RDF(a_position, b_position, system_size)
        >>> rdf_result = my_rdf.result
        >>> cn_result  = my_rdf.cn
        """
        self.a = check_dimension(a, dim=3)
        self.b = check_dimension(b, dim=3)
        self.system_size = check_dimension(system_size, dim=2)[:, 1]
        self.box_length = self.system_size * 2.0
        self.lag_number = self.a.shape[0]
        self.a_number, self.b_number = self.a.shape[1], self.b.shape[1]
        self.r_max = self.__set_r_max(r_max)
        self.resolution = resolution
        self.dr = float(self.r_max / self.resolution)
        self.pbc = pbc
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
        self._get_rdf()
        self._get_cn()
        return [self.radii, self.result, self.cn]

    # Function for get hist
    def _get_hist(self) -> NDArray[np.float64]:
        self.hist_data = np.zeros(self.resolution)
        self.__check_pbc = self.__set_pbc_style()
        kwrgs_trange = {"desc": " RDF  (STEP) ", "ncols": 70, "ascii": True}
        for lag in trange(self.lag_number, **kwrgs_trange):
            self.a_unit = self.a[lag, ...].astype(np.float64)
            self.b_unit = self.b[lag, ...].astype(np.float64)
            self.__make_histogram()

    # Function for get rdf
    def _get_rdf(self) -> NDArray[np.float64]:
        self.result = self.__get_g_r()

    # Function for get radii data
    def _get_radii(self) -> NDArray[np.float64]:
        self.radii = np.linspace(0.0, self.r_max, self.resolution)

    # Function for get coordinate number
    def _get_cn(self) -> NDArray[np.float64]:
        self.n = self.hist_data / (self.lag_number * self.a_number)
        self.cn = np.cumsum(self.n)

    # make a histogram
    def __make_histogram(self):
        for b_line in self.b_unit:
            diff_position = self.__get_diff_position(target=b_line)
            diff_position = self.__check_pbc(diff_position=diff_position)
            distance = self.__get_distance(diff_position=diff_position)
            idx_hist = self.__get_idx_histogram(distance=distance)
            value, count = np.unique(idx_hist, return_counts=True)
            self.hist_data[value] += count

    # get position difference
    def __get_diff_position(self, target) -> NDArray[np.float64]:
        return np.abs(np.subtract(self.a_unit, target, dtype=np.float64))

    def __is_pbc_single(self) -> bool:
        pbc_list = ["single", "layer"]
        if not self.pbc in pbc_list:
            raise ValueError(f"pbc <- (single) or (layer) : your Value {self.pbc} is wrong")
        else:
            if self.pbc == "single":
                return True
            else:
                return False

    def __set_pbc_style(self) -> object:
        if self.__is_pbc_single:
            return self.__set_pbc_single

        else:
            self.layer = self.__make_first_layer()
            return self.__set_pbc_layer

    # set the pbc only consider single system
    def __set_pbc_single(self, diff_position) -> NDArray[np.float64]:
        return np.where(
            diff_position > self.system_size,
            self.box_length - diff_position,
            diff_position,
        )

    # set the pbc with 27 system
    def __set_pbc_layer(self, diff_position) -> NDArray[np.float64]:
        return diff_position[:, np.newaxis, :] + self.layer

    # Make a first layer
    def __make_first_layer(self) -> NDArray[np.float64]:
        return self.__make_direction_idx() * self.box_length

    # Make a 3D layer_idx
    def __make_direction_idx(self):
        list_direction = []
        idx_direction_ = [-1, 0, 1]
        for i in idx_direction_:
            for j in idx_direction_:
                for k in idx_direction_:
                    list_direction.append([i, j, k])
        return np.array(list_direction)

    # get distance from different of position
    def __get_distance(self, diff_position) -> NDArray[np.float64]:
        return np.sqrt(np.sum(np.square(diff_position), axis=-1))

    # get idx for histogram
    def __get_idx_histogram(self, distance) -> NDArray[np.int64]:
        idx_hist = (distance / self.dr).astype(np.int64)
        return idx_hist[np.where((0 < idx_hist) & (idx_hist < self.resolution))]

    # Calculate the Density Function
    def __get_g_r(self) -> NDArray[np.float64]:
        r_i = self.radii[1:]
        g_r = np.append(0.0, self.hist_data[1:] / np.square(r_i))
        factor = np.array(
            4.0 * np.pi * self.dr * self.lag_number * self.a_number * self.b_number,
            dtype=np.float64,
        )
        box_volume = np.prod(self.box_length, dtype=np.float64)
        return g_r * box_volume / factor

    def __set_r_max(self, r_max) -> np.float64:
        if r_max is not None:
            return r_max
        else:
            box_max_radius = max(self.system_size)
            if self.__is_pbc_single:
                return box_max_radius
            else:
                return box_max_radius * 3.0

    # Plot the g(r) with radii datas
    def plot_g_r(self, bins: int = 1, *args, **kwrgs):
        x = self.radii[::bins]
        y = self.g_r[::bins]
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
