from pathlib import Path
from sigmf_loader import load_sigmf_full
import numpy as np
import plotly.express as px
import pandas as pd

arr = load_sigmf_full(Path('data/RFInd-raw-20221209T16.sigmf-meta'))
        # shape=(4800, 600000),

maxHr = np.max(arr, axis=0)
assert len(maxHr) == 600000


minHr = np.min(arr, axis=0)
meanHr = np.mean(arr, axis=0)
medianHr = np.median(arr, axis=0)

df = pd.DataFrame({'max': maxHr, 'min': minHr, 'mean': meanHr, 'median': medianHr})

fig = px.line(df)
fig.show()

df.to_csv('jonas.csv')
