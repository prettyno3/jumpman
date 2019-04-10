import pandas as pd
import numpy as np
from ggplot import *


df = pd.DataFrame({
    "x": np.random.normal(0, 10, 1000),
    "y": np.random.normal(0, 10, 1000),
    "z": np.random.normal(0, 10, 1000)
})
df = pd.melt(df)

ggplot(aes(x='value', color='variable'), data=df) + \
    geom_histogram()