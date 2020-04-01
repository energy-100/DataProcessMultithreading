
import sys
from time import time
from functools import reduce

import numpy as np
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from IPython.core.interactiveshell import InteractiveShell

import pycuda
import pycuda.autoinit
import pycuda.driver as drv
from pycuda import gpuarray
from pycuda.elementwise import ElementwiseKernel
from pycuda.scan import InclusiveScanKernel
from pycuda.reduction import ReductionKernel

def simple_speed_test():
    host_data = np.float32(np.random.random(50000000))

    t1 = time()
    host_data_2x = host_data * np.float32(2)
    t2 = time()

    print(f'total time to compute on CPU: {t2 - t1}')

    device_data = gpuarray.to_gpu(host_data)

    t1 = time()
    device_data_2x = device_data * np.float32(2)
    t2 = time()

    from_device = device_data_2x.get()

    print(f'total time to compute on GPU: {t2 - t1}')
    print(f'Is the host computation the same as the GPU computation? : {np.allclose(from_device, host_data_2x)}')


simple_speed_test()