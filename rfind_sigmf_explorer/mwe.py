# tested on python 3.10 and 3.11
# pypi dependencies:
# numpy sigmf plotly xarray holoviews hvplot

# NOTE: This is a very memory intensive script. It will load the entire sigmf-data file
# into memory so make sure you have enough! 

from pathlib import Path
import numpy as np
import holoviews as hv
import panel as pn
hv.extension('bokeh', logo=False)
hv.output(backend="bokeh")
import sigmf
from datetime import datetime, timedelta
from datashader.colors import viridis
import hvplot.xarray # noqa
import xarray as xr


# note we are pointing at the meta file
filename = Path('/rfi-data/RFInd-calibrated-2023-05-12T20.sigmf-meta')



# the following will load some of the sigmf meta data
handle = sigmf.sigmffile.fromfile(filename.as_posix())
global_info = handle.get_global_info()

integration_time = 1/global_info[sigmf.SigMFFile.SAMPLE_RATE_KEY]
num_integrations = handle.sample_count
num_channels = handle.get_num_channels()

## Laptop ran out of memory when I tried to include this
# start_datetime = datetime.fromisoformat(handle.get_captures()[0][sigmf.SigMFFile.DATETIME_KEY])
# end_datetime = start_datetime+timedelta(seconds=num_integrations*integration_time)
# yvals = np.arange(start_datetime, end_datetime, timedelta(seconds=integration_time)).astype(datetime)
yvals = np.arange(num_integrations)*integration_time

# the following will plot an interactive waterwall of the 1 hour dataset
arr = np.memmap(filename.with_suffix(sigmf.archive.SIGMF_DATASET_EXT), shape=(num_integrations,num_channels), offset=0, dtype=np.dtype("f4"), mode='r')
arr = xr.DataArray(arr, dims=("seconds", "Hz"), coords={'seconds': yvals, "Hz": np.arange(num_channels)*2e9/num_channels})
pn.Row(arr.hvplot(width=1000, height=1000, rasterize=True, cmap=viridis, aggregator='max', cnorm='log').opts(clabel='dBm/Hz')).show()