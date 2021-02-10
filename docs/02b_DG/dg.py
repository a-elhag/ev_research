## Part 0: Import
import sys
sys.path.insert(0, '/home/alkubuntu/Documents/research/ev_research')

import numpy as np
from src.generate_dg import GenerateDG

## Part 1: Using GenerateDG
dg_gen = GenerateDG('src/data/db/dg.db')
dg_gen.monte(10)

dg_gen.data_gen.shape

dg_gen.plot(years = 10)
## Part 2:
