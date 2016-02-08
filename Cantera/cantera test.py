

import cantera as ct 
import numpy as np
import matplotlib.pyplot as mplt

gas= ct.Solution('gri30.xml')
gas.TP = 1200, 101325
gas()

