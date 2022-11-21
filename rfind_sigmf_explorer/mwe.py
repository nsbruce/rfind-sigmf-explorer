from pathlib import Path
import numpy as np
import datashader as ds
from datashader import transfer_functions as tf
import holoviews as hv
from holoviews.operation.datashader import datashade
import panel as pn
hv.extension('bokeh', logo=False)
hv.output(backend="bokeh")
import dask.array as da
import sigmf
from datashader.colors import viridis
import hvplot.xarray # noqa
import xarray as xr

# hv.opts.defaults(hv.opts.Overlay(width=1000, height=1000, xaxis=None, yaxis=None))

filename = Path('../data/RFInd-raw-20221023T23.sigmf-meta')


# arr = da.from_array(np.memmap(filename.with_suffix(sigmf.archive.SIGMF_DATASET_EXT), shape=(4800,600000), offset=0, dtype=np.dtype("f4"), mode='r'))

# arr = np.memmap(filename.with_suffix(sigmf.archive.SIGMF_DATASET_EXT), shape=(4800,600000), offset=0, dtype=np.dtype("f4"), mode='r')
# arr = xr.DataArray(arr, dims=("x", "y"), coords={'x': np.arange(4800), "y": np.arange(600000)})
# cvs = ds.Canvas(plot_width=1000, plot_height=1000, x_range=(0, 600000), y_range=(0, 4800))
# agg = cvs.raster(arr)
# sh = tf.shade(agg, cmap=viridis)
# pn.Row(sh).show()

arr = np.memmap(filename.with_suffix(sigmf.archive.SIGMF_DATASET_EXT), shape=(4800,600000), offset=0, dtype=np.dtype("f4"), mode='r')
arr = xr.DataArray(arr, dims=("x", "y"), coords={'x': np.arange(4800), "y": np.arange(600000)})
pn.Row(arr.hvplot(width=1000, height=1000, rasterize=True)).show()


# arr = da.from_array(np.memmap(filename.with_suffix(sigmf.archive.SIGMF_DATASET_EXT), shape=(4800,600000), offset=0, dtype=np.dtype("f4"), mode='r'))

