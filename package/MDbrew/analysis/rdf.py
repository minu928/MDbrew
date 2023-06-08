import numpy as np
from tqdm import trange, tqdm
from ..main.brewery import Brewery
from ..tool.spacer import *
from ..tool.colorfont import color


# Calculate and Plot the RDF
class RDF(object):
    kwrgs_trange = {
        "desc": f"[ {color.font_cyan}BREW{color.reset} ]  #{color.font_green}RDF{color.reset} ",
        "ncols": 60,
        "ascii": True,
    }

    def __init__(
        self,
        a,
        b,
        box_size=None,
        layer: int = 0,
        r_max: float = None,
        resolution: int = 1000,
        dtype: str = "float32",
    ):
        if type(a) == Brewery:
            self.is_Brewery_type = True
            self.a = a.reorder()
            self.b = b.reorder()
            self.a_number = a.atom_num
            self.b_number = b.atom_num
            self.box_size = a.box_size if box_size is None else box_size
            assert len(self.box_size), "plz set box_size"
        else:
            self.is_Brewery_type = False
            self.a = check_dimension(a, dim=3, dtype=dtype)
            self.b = check_dimension(b, dim=3, dtype=dtype)
            self.a_number = self.a.shape[1]
            self.b_number = self.b.shape[1]
            self.box_size = box_size

        self._dtype = dtype
        self.box_size = np.array(self.box_size, dtype=dtype)
        self.half_box_size = self.box_size * 0.5

        self.layer_depth = layer
        self.layer = self.__make_layer()

        self.resolution = resolution
        self.r_max = np.max(self.half_box_size) * (2.0 * self.layer_depth + 1.0) if r_max is None else r_max
        self.dr = self.r_max / self.resolution

        self.hist_data = None
        self.radii = np.linspace(0.0, self.r_max, self.resolution)

    def run(self, start=0, end=None, step=1):
        if self.is_Brewery_type:
            self._cal_hist_data_with_generator(start=start, end=end, step=step)
        else:
            self._cal_hist_data_with_iterator(start=start, end=end, step=step)
        return self

    @property
    def result(self):
        if self.hist_data is None:
            self.run()
        return self.__cal_rdf_from_hist_data()

    @property
    def cn(self):
        if self.hist_data is None:
            self.run()
        return self.__cal_cn_from_hist_data()

    # Function for get hist
    def _cal_hist_data_with_iterator(self, start=0, end=None, step=1):
        self.hist_data = np.zeros(self.resolution)
        _apply_boundary_condition = self.__set_boundary_condition()
        self.frame_num = self.a.shape[0] if end is None else end - start + 1
        for frame in trange(start=start, stop=end, step=step, **self.kwrgs_trange):
            a_unit = self.a[frame, ...]
            b_unit = self.b[frame, ...]
            diff_position = get_diff_position(a_unit[:, None, :], b_unit[None, :, :])
            diff_position = _apply_boundary_condition(diff_position=diff_position)
            distance = get_distance(diff_position=diff_position, axis=-1)
            idx_hist = self.__cal_idx_histogram(distance=distance)
            value, count = np.unique(idx_hist, return_counts=True)
            self.hist_data[value] += count

    # Function for get hist
    def _cal_hist_data_with_generator(self, start=0, end=None, step=1):
        self.hist_data = np.zeros(self.resolution)
        _apply_boundary_condition = self.__set_boundary_condition()
        frange = (
            self.a.frange(start=start, end=end, step=step)
            if self.a is self.b
            else zip(self.a.frange(start=start, end=end, step=step), self.b.frange(start=start, end=end, step=step))
        )
        frame_num = 0
        for _ in tqdm(frange, **self.kwrgs_trange):
            frame_num += 1
            a_unit = self.a.coords
            b_unit = self.b.coords
            diff_position = get_diff_position(a_unit[:, None, :], b_unit[None, :, :])
            diff_position = _apply_boundary_condition(diff_position=diff_position)
            distance = get_distance(diff_position=diff_position, axis=-1)
            idx_hist = self.__cal_idx_histogram(distance=distance)
            value, count = np.unique(idx_hist, return_counts=True)
            self.hist_data[value] += count
        self.frame_num = frame_num

    # select the mode with Boundary Layer
    def __set_boundary_condition(self):
        return self.__add_layer if self.layer_depth else self.__check_pbc

    # set the pbc only consider single system
    def __check_pbc(self, diff_position):
        diff_position = np.abs(diff_position)
        return np.where(
            diff_position > self.half_box_size,
            self.box_size - diff_position,
            diff_position,
        )

    # set the pbc with 27 system
    def __add_layer(self, diff_position):
        return diff_position[..., np.newaxis, :] + self.layer

    # Make a 3D layer_idx
    def __make_layer(self):
        list_direction = []
        idx_direction_ = range(-self.layer_depth, self.layer_depth + 1)
        for i in idx_direction_:
            for j in idx_direction_:
                for k in idx_direction_:
                    list_direction.append([i, j, k])
        return np.array(list_direction) * self.box_size

    # get idx for histogram
    def __cal_idx_histogram(self, distance):
        idx_hist = (distance / self.dr).astype("int32")
        return idx_hist[np.where((0 < idx_hist) & (idx_hist < self.resolution))]

    # Calculate the Density Function
    def __cal_rdf_from_hist_data(self):
        r_i = self.radii[1:]
        g_r = np.append(0.0, self.hist_data[1:] / np.square(r_i))
        factor = np.array(
            4.0 * np.pi * self.dr * self.frame_num * self.a_number * self.b_number,
            dtype=self._dtype,
        )
        box_volume = np.prod(self.box_size, dtype=self._dtype)
        return g_r * box_volume / factor

    # Function for get coordinate number
    def __cal_cn_from_hist_data(self):
        self.n = self.hist_data / (self.frame_num * self.a_number)
        return np.cumsum(self.n)
