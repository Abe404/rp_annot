# rp-annot
Minimal compression library for sparse or contiguous 1D numpy boolean arrays.

Only depends on numpy

## Install 
The latest version is available via PyPI (https://pypi.org/project/rp-annot) 
 
> pip install rp-annot

## Example usage
```python
import rp_annot as rpa
import numpy as np

np_1d_bool_array = np.zeros(100000, dtype=bool)
np_1d_bool_array[20000:50000] = True
compressed = rpa.compress(np_1d_bool_array) # 16 bytes
decompressed =  rpa.decompress(compressed, len(np_1d_bool_array))
assert np.array_equal(np_1d_bool_array, decompressed)
```
