import numpy as np

x = np.random.rand(1e6)
q25, q50, q75 = np.percentile(x, [25,50,75])