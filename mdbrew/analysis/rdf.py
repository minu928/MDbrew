import numpy as np
from typing import Type
from tqdm import trange, tqdm
from mdbrew.main.brewery import Brewery
from mdbrew.tool.colorfont import color
from mdbrew.tool.space import calculate_diff_position, calculate_distance, check_dimension


# Calculate and Plot the RDF
class RDF(object):
    def __init__(
        self,
        a_coords,
        b_coords,
        box=None,
        r_max: float = None,
        resolution: int = 1000,
        dtype: type = float,
    ):
        if isinstance(a_coords, Brewery) and isinstance(b_coords, Brewery):
            self.instance_rdf = BreweryRDF(a=a_coords, b=b_coords, box=box, r_max=r_max, resolution=resolution, dtype=dtype)
        else:
            self.instance_rdf = NormalRDF(a=a_coords, b=b_coords, box=box, r_max=r_max, resolution=resolution, dtype=dtype)

    def run(self, start=0, end=None, step=1):
        self.instance_rdf.run(start=start, end=end, step=step)
        return self

    @property
    def result(self):
        if self.instance_rdf.hist_data is None:
            self.run()
        return self.instance_rdf._cal_rdf()

    @property
    def cn(self):
        if self.instance_rdf.hist_data is None:
            self.run()
        return self.instance_rdf._cal_cn()

    @property
    def radii(self):
        if self.instance_rdf.radii is None:
            self.instance_rdf.radii = np.linspace(0, self.instance_rdf.r_max, self.instance_rdf.resolution + 1)
        return self.instance_rdf.radii


class InterfaceRDF(object):
    kwrgs_trange = {
        "desc": f"[ {color.font_cyan}BREW{color.reset} ]  #{color.font_green}RDF{color.reset} ",
        "ncols": 60,
        "ascii": True,
    }
    hist_data = None
    radii = None

    def __init__(
        self,
        a,
        b,
        box=None,
        r_max: float = None,
        resolution: int = 1000,
        dtype: str = float,
    ):
        self.r_max = np.max(self.box) * 0.5 if r_max is None else r_max
        self.resolution = resolution
        self._dtype = dtype

    def run(self, start=0, end=None, step=1):
        pass

    def _unit_run(self, a_unit, b_unit, box_unit):
        diff_position = calculate_diff_position(a_unit[:, None, :], b_unit[None, :, :])
        diff_position = self._check_pbc(diff_position=diff_position, box=box_unit)
        distance = calculate_distance(diff_position=diff_position, axis=-1)
        each_hist, dr_arr = np.histogram(distance, bins=self.resolution, range=(0, self.r_max))
        self.frame_num += 1
        self.hist_data += each_hist
        self.gr[1:] += each_hist[1:] / np.square(dr_arr[1:-1]) * np.prod(box_unit)

    # set the pbc only consider single system
    def _check_pbc(self, diff_position, box):
        diff_position = np.abs(diff_position)
        return np.where(diff_position > 0.5 * box, box - diff_position, diff_position)

    # Calculate the Density Function
    def _cal_rdf(self):
        dr = self.r_max / self.resolution
        factor = 4.0 * np.pi * dr * self.frame_num * self.a_number * self.b_number
        return self.gr / factor

    # Function for get coordinate number
    def _cal_cn(self):
        self.n = self.hist_data / (self.frame_num * self.a_number)
        return np.cumsum(self.n)


class BreweryRDF(InterfaceRDF):
    def __init__(
        self,
        a: Type[Brewery],
        b: Type[Brewery],
        box=None,
        r_max: float = None,
        resolution: int = 1000,
        dtype: type = float,
    ):
        self.a = a.reorder()
        self.b = b.reorder()
        self.a_number = a.atom_num
        self.b_number = b.atom_num
        self.is_box_input = box is not None
        self.box = a.box_size if box is None else box
        assert len(self.box), "plz set box"
        super().__init__(self.a, self.b, self.box, r_max, resolution, dtype)

    def run(self, start=0, end=None, step=1):
        self.frame_num = 0
        self.gr = np.zeros(self.resolution)
        self.hist_data = np.zeros(self.resolution)
        frange = self._make_frange(start=start, end=end, step=step)
        for idx in tqdm(frange, **self.kwrgs_trange):
            a_unit = self.a.coords
            b_unit = self.b.coords
            box_unit = self._make_box(self.box, idx)
            self._unit_run(a_unit=a_unit, b_unit=b_unit, box_unit=box_unit)

    def _make_frange(self, start=0, end=None, step=1):
        kwrgs = {"start": start, "end": end, "step": step}
        if self.a is self.b:
            return self.a.frange(**kwrgs)
        return zip(self.a.frange(**kwrgs), self.b.frange(**kwrgs))

    def _make_box(self, box, idx):
        if not self.is_box_input:
            return np.array(self.a.box_size)
        box = np.array(box)
        assert idx[0] == idx[1], "Reset Error"  # idx = (0, 0), (1, 1), ...
        return box if box.ndim == 1 else box[idx[0]]


class NormalRDF(InterfaceRDF):
    def __init__(
        self,
        a,
        b,
        box=None,
        r_max: float = None,
        resolution: int = 1000,
        dtype: type = float,
    ):
        self.a = check_dimension(a, dim=3, dtype=dtype)
        self.b = check_dimension(b, dim=3, dtype=dtype)
        self.a_number = self.a.shape[1]
        self.b_number = self.b.shape[1]
        self.box = self._make_box(box=box)
        super().__init__(a, b, box, r_max, resolution, dtype)

    def run(self, start=0, end=None, step=1):
        self.frame_num = 0
        self.gr = np.zeros(self.resolution)
        self.hist_data = np.zeros(self.resolution)
        # self.frame_num = self.a.shape[0] if end is None else end - start + 1
        for frame in trange(start=start, stop=end, step=step, **self.kwrgs_trange):
            a_unit = self.a[frame, ...]
            b_unit = self.b[frame, ...]
            box_unit = self.box[frame]
            self._unit_run(a_unit=a_unit, b_unit=b_unit, box_unit=box_unit)

    def _make_box(self, box):
        frame_num = len(self.a)
        box_frame = len(box)
        if frame_num != box_frame:
            if box_frame != 1:
                raise ValueError(f"Check your box shape, total frame: {frame_num} != box frame: {box_frame}")
            return np.tile(box, (frame_num, 1))
        return box
