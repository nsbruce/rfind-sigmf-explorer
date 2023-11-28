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
import time

pn.extension(loading_indicator=True)

template = pn.template.FastListTemplate(
    title="Historical RFI explorer"
)

# pn.serve(port=9001, websocket_origin=['localhost:9001','rfi-proc-01.drao.nrc.ca:9001'])


template.main.append(
    pn.pane.Markdown("""
                    ## Important - please read!
                    
                    1. This is very memory intensive which means it's slow. So relax and enjoy the ride. Stop clicking all over the place.
                    2. Only select one file using the selector or it will not work. I'll add support for multiple files later.
                    3. This is a shared single-page application. If two people are logged on at the same time, you will see each other's selections and interacting with the plots will affect each other. So don't do that. Or at least be aware.
                    """)
)
file_selector = pn.widgets.FileSelector(directory='/data/', file_pattern='*.sigmf-meta')
template.main.append(file_selector)

load_button = pn.widgets.Button(name='Load selected data', button_type='primary', disabled=len(file_selector.value) != 1)

def toggle_load_button(event):
    load_button.disabled = len(file_selector.value) != 1
pn.bind(toggle_load_button, file_selector, watch=True)

load_spinner = pn.indicators.LoadingSpinner(value=False, size=40, name='Not currently loading new data')

plot = pn.panel(xr.DataArray(np.zeros((3,6)), dims=("seconds", "GHz"), coords={'seconds': np.arange(3), "GHz": np.arange(6)}).hvplot(width=1800, height=800, cmap='viridis'))

def load_data(event):
    selected_files = file_selector.value
    if len(selected_files) == 1:
        load_spinner.value = True
        load_spinner.name = 'Loading new data...'
        filename = Path(selected_files[0])

        handle = sigmf.sigmffile.fromfile(filename.as_posix())
        global_info = handle.get_global_info()

        integration_time = 1/global_info[sigmf.SigMFFile.SAMPLE_RATE_KEY]
        num_integrations = handle.sample_count
        num_channels = handle.get_num_channels()
        
        yvals = np.arange(num_integrations)*integration_time
        xvals = np.arange(num_channels)*2/num_channels

        arr = np.memmap(filename.with_suffix(sigmf.archive.SIGMF_DATASET_EXT), shape=(num_integrations,num_channels), offset=0, dtype=np.dtype("f4"), mode='r')
        arr = xr.DataArray(arr, dims=("seconds", "GHz"), coords={'seconds': yvals, "GHz": xvals})

        pn.pane.Alert("Data loaded.")
        load_spinner.value = False
        load_spinner.name = 'Not currently loading new data'

        plot.object = arr.hvplot(width=1800, height=800, rasterize=True, cmap=viridis, aggregator='max', cnorm='log').opts(clabel='dBm/Hz')

pn.bind(load_data, load_button, watch=True)

template.main.append(pn.Row(load_button, load_spinner))
template.main.append(plot)

template.servable()