# import math
# from pathlib import Path

import numpy as np
import numpy.typing as npt
# import plotly.graph_objects as go
import datashader as ds
# import plotly.express as px
from datashader import transfer_functions as tf, reductions as rd
import xarray as xr
import holoviews as hv
from holoviews.operation.datashader import rasterize, shade, datashade
import panel as pn
from bokeh.plotting import show
hv.extension('bokeh', logo=False)
hv.output(backend="bokeh")

# class BigSpectrogram():
#     def __init__(self, arr) -> None:
#         self.da = da
#     def points(self, x_range, y_range):
#         print(x_range, y_range)
#         data = self.arr.sel(x=slice(*x_range), y=slice(*y_range)).compute()
#         image = hv.Image(data)
#         return image

#     def view(self, **kwargs):
#         range_xy = hv.streams.RangeXY(x_range=(0, 4800), y_range=(0, 600000))
#         points = hv.DynamicMap(self.points, streams=[range_xy])
#         agg = rasterize(points)
#         return agg


def plot_interactive_waterfall(arr: npt.NDArray[np.float64]) -> None:
    # this just kills the process
    # arr = xr.DataArray(arr, dims=("x", "y"), coords={'x':np.arange(4800), "y":np.arange(600000)})
    # spectrogram = BigSpectrogram(arr)
    # pn.Row(spectrogram.view()).show(port=37921)


    arr = xr.DataArray(arr, dims=("x", "y"), coords={'x': np.arange(4800), "y": np.arange(600000)})
    cvs = ds.Canvas(plot_width=1000, plot_height=1000, x_range=(0, 4800), y_range=(0, 4800))
    agg = cvs.raster(arr)
    sh = tf.shade(agg)
    pn.Row(sh).show(port=37921)

    # arr = xr.DataArray(arr, dims=("x", "y"), coords={'x':np.arange(4800), "y":np.arange(600000)})
    # print('have arr')
    # pts = hv.Image(arr)
    # print("have pts")
    # # pts = hv.GridSpace(arr)
    # sh = datashade(pts)
    # print('have shade')
    # pn.Row(sh).show(port=37921)





