from mdbrew.main.interface import OpenerInterface


atomic_dict = {
    "pdbtype": [0, 4],
    "idx": [6, 11],
    "atom": [12, 16],
    "indicator": [16, 17],
    "resname": [17, 20],
    "chain": [21, 22],
    "resid": [22, 26],
    "rescode": [26, 27],
    "x": [30, 38],
    "y": [38, 46],
    "z": [46, 54],
    "occupancy": [54, 60],
    "temp_factor": [60, 66],
    "seg_id": [72, 76],
    "element": [76, 78],
    "charge": [78, 80],
}


class pdbOpener(OpenerInterface):
    ending_num_for_pdb = None
    is_column_updated = False
    fmt: str = "pdb"

    def __init__(self, path: str, *args, **kwrgs) -> None:
        super().__init__(path, *args, **kwrgs)
        self.path = path
        self.skip_head = 2
        self.column = []
        super().gen_db()

    def _make_one_frame_data(self, file):
        first__loop_line = file.readline()
        assert "REMARK" in first__loop_line
        second_loop_line = file.readline()
        self.box_size = [float(box_length) for box_length in second_loop_line.split()[1:4]]
        one_frame_data = []
        self.total_line_num = 3
        if self.ending_num_for_pdb is None:
            while True:
                line = file.readline()
                if "END" in line:
                    break
                self.total_line_num += 1
                ##############################
                split_line = self.apply_atom_type(line)
                #############################
                one_frame_data.append(split_line)
                self.ending_num_for_pdb = int(split_line[1])
                self.is_column_updated = True
        else:
            self.total_line_num += self.ending_num_for_pdb
            one_frame_data = [self.apply_atom_type(file.readline()) for _ in range(self.ending_num_for_pdb)]
            file.readline()
        return one_frame_data

    def apply_atom_type(self, line):
        data_list = []
        for key, idxes in atomic_dict.items():
            data = line[idxes[0] : idxes[1]].strip()
            if data:
                data_list.append(data)
                if not self.is_column_updated:
                    self.column.append(key)
        return data_list
