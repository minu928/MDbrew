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
        """
        Radial Distribution Function
        you can get result from RDF.result

        Parameters
        ----------
        a : NDArray
            Position data  ||  shape : [frame, N_particle, dim]
        b : NDArray
            Position data  ||  shape : [frame, N_particle, dim]
        system_size : [[-lx, lx], [-ly, ly], [-lz, lz]]
            System size of data
        layer_depth : int, optional
            how many layer do you set, 0 means with PBC (one box) other layered, by default 0
        r_max : float, optional
            you can input the max radius else None means 'calculate max(system_size)', by default None
        resolution : int, optional
            resolution of dr, by default 1000

        Result of Radial Density Function, Coordination Number
        ------------------------------------------------------------
        >>> my_rdf     = RDF(a = a_position, b= b_position, system_size=system_size)
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

        self.r_max = np.max(self.system_size) * (2.0 * self.layer_depth + 1.0) if r_max is None else r_max
        self.resolution = resolution
        self.dr = self.r_max / self.resolution
        self.hist_data = None
        self.radii = np.linspace(0.0, self.r_max, self.resolution)

    @property
    def result(self):
        if self.hist_data is None:
            self._cal_hist_data()
        return self.__cal_rdf_from_hist_data()

    @property
    def cn(self):
        if self.hist_data is None:
            self._cal_hist_data()
        return self.__cal_cn_from_hist_data()

    # Function for get hist
    def _cal_hist_data(self):
        self.hist_data = np.zeros(self.resolution)
        self.__apply_boundary_condition = self.__set_boundary_condition()
        kwrgs_trange = {"desc": " RDF  (STEP) ", "ncols": 70, "ascii": True}
        for frame in trange(self.frame_number, **kwrgs_trange):
            a_unit = self.a[frame, ...].astype(np.float64)
            b_unit = self.b[frame, ...].astype(np.float64)
            a_unit = np.tile(a_unit[:, None, :], (1, self.b_number, 1))
            b_unit = np.tile(b_unit[None, :, :], (self.a_number, 1, 1))
            diff_position = get_diff_position(a_unit, b_unit)
            diff_position = self.__apply_boundary_condition(diff_position)
            distance = get_distance(diff_position=diff_position, axis=-1)
            idx_hist = self.__cal_idx_histogram(distance=distance)
            value, count = np.unique(idx_hist, return_counts=True)
            self.hist_data[value] += count

    # select the mode with Boundary Layer
    def __set_boundary_condition(self):
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
        return diff_position[..., np.newaxis, :] + self.layer

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
    def __cal_idx_histogram(self, distance) -> NDArray[np.int64]:
        idx_hist = (distance / self.dr).astype(np.int64)
        return idx_hist[np.where((0 < idx_hist) & (idx_hist < self.resolution))]

    # Calculate the Density Function
    def __cal_rdf_from_hist_data(self) -> NDArray[np.float64]:
        r_i = self.radii[1:]
        g_r = np.append(0.0, self.hist_data[1:] / np.square(r_i))
        factor = np.array(
            4.0 * np.pi * self.dr * self.frame_number * self.a_number * self.b_number,
            dtype=np.float64,
        )
        box_volume = np.prod(self.box_length, dtype=np.float64)
        return g_r * box_volume / factor

    # Function for get coordinate number
    def __cal_cn_from_hist_data(self):
        self.n = self.hist_data / (self.frame_number * self.a_number)
        return np.cumsum(self.n)
