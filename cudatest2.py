# coding: utf-8
import pycuda.autoinit
import pycuda.driver as cuda
import pycuda.gpuarray as gpuarray
import numpy


d_array = numpy.random.randn(5, 5) # 0～1の乱数が入った5x5の倍制度配列を生成
s_array = d_array.astype(numpy.float32) # 配列を単精度に変換（GPUは単精度演算の方が早い）

gpu = gpuarray.to_gpu(s_array) # GPUのメモリー領域を確保しデータを渡す
result = (2 * gpu).get() # 格納されているデータを2倍して結果を取得


# 演算前の値を表示
for x in s_array:
    for xx in x:
        print("{: f}".format(xx), end="\t")
    print("")

print("")

# 演算後の値を表示（乱数が2倍されている）
for y in result:
    for yy in y:
        print("{: f}".format(yy), end="\t")
    print("")