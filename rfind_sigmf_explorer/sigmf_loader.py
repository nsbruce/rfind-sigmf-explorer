import math
from datetime import datetime
from pathlib import Path

import dask.array as da
import numpy as np
import numpy.typing as npt
import sigmf  # type: ignore
from sigmf import SigMFFile


def load_sigmf_chunk(path: Path, start_ts: int, end_ts: int) -> npt.NDArray[np.float64]:
    handle = sigmf.sigmffile.fromfile(path.as_posix())
    global_info = handle.get_global_info()
    int_time = 1/global_info[SigMFFile.SAMPLE_RATE_KEY]
    file_start_ts = datetime.fromisoformat(
        handle.get_captures()[0][SigMFFile.DATETIME_KEY]
        ).timestamp()
    start_idx = int(math.floor((start_ts - file_start_ts)/int_time))
    num_samples = int(math.ceil((end_ts - start_ts)/int_time))
    d = handle.read_samples(start_idx, num_samples)
    return np.array(d, dtype=np.float64)


def load_sigmf_full(path: Path) -> npt.NDArray[np.float64]:
    handle = sigmf.sigmffile.fromfile(path.as_posix())
    # global_info = handle.get_global_info()
    # int_time = 1/global_info[SigMFFile.SAMPLE_RATE_KEY]
    d = handle.read_samples()
    return np.array(d, dtype=np.float64)


def load_sigmf_dask(path: Path):
    data = da.from_array(np.memmap(path.with_suffix(sigmf.archive.SIGMF_DATASET_EXT), shape=(4800,600000), offset=0, dtype=np.dtype("f4"), mode='r'))
    return data
