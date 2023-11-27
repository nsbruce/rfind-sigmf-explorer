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
filename = Path('/data/RFInd-calibrated-2023-11-26T18.sigmf-meta')
filename1 = Path('/data/RFInd-calibrated-2023-11-27T18.sigmf-meta')



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
xvals = np.arange(num_channels)*2/num_channels

# the following will plot an interactive waterwall of the 1 hour dataset
arr = np.memmap(filename.with_suffix(sigmf.archive.SIGMF_DATASET_EXT), shape=(num_integrations,num_channels), offset=0, dtype=np.dtype("f4"), mode='r')
arr = xr.DataArray(arr, dims=("seconds", "GHz"), coords={'seconds': yvals, "GHz": xvals})
arr1 = np.memmap(filename1.with_suffix(sigmf.archive.SIGMF_DATASET_EXT), shape=(num_integrations,num_channels), offset=0, dtype=np.dtype("f4"), mode='r')
arr1 = xr.DataArray(arr1, dims=("seconds", "GHz"), coords={'seconds': yvals, "GHz": xvals})

column = pn.Column()
column.append(pn.pane.Markdown('# RFI comparison'))
row = pn.Row()
row.append(pn.Column('Sun. Nov. 26',  arr.hvplot(width=800, height=800, rasterize=True, cmap=viridis, aggregator='max', cnorm='log', clim=(5 * 10**-18, 5 * 10**-12))))
row.append(pn.Column('Mon. Nov. 27', arr1.hvplot(width=800, height=800, rasterize=True, cmap=viridis, aggregator='max', cnorm='log', clim=(5 * 10**-18, 5 * 10**-12)).opts(clabel='dBm/Hz')))

column.append(row)
column.show(port=9000, websocket_origin=['localhost:9000','rfi-proc-01.drao.nrc.ca:9000'])