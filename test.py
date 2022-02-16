import numpy as np
import os
import time
import zlib
import rp_annot as rpa

def test_reconstruct():
    for test_array in [
            [0, 0, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1]
        ]:
        test_array = np.array(test_array).astype(bool)
        assert np.array_equal(test_array, rpa.reconstruct_from_diff_coords(rpa.get_diff_coords(test_array), len(test_array)))


def test_get_diff_array():
    for test_array in [
            [0, 0, 1, 1, 0],
            [1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0]
        ]:
        test_array = np.array(test_array)
        assert np.array_equal(test_array, rpa.reconstruct_from_diff_array(rpa.get_diff_array(test_array)))


def test_with_larger_payload():
    np_payload = np.load('test_data/payload.npy')
    np_payload = np_payload.astype(bool)
    np_payload1d = np_payload.reshape(-1).astype(bool)
    payload_len = len(np_payload1d)

    t = time.time()
    for i in range(100):
        np_payload_diff_coords = rpa.get_diff_coords(np_payload1d)
    print('rpa.get_diff_coords: total time for 100', time.time() - t)
    compress_time = (time.time() - t) / 100

    t = time.time()
    for i in range(100):
        np_payload1d =  rpa.reconstruct_from_diff_coords(np_payload_diff_coords, payload_len)
    decompress_time = (time.time() - t) / 100

    payload_bytes = np.load('test_data/payload.npy').tobytes()
    t = time.time()
    for i in range(100):
        z_compressed_data = zlib.compress(payload_bytes, 1)
    print('zlib.compress: total time for 100', time.time() - t)
    z_compressed_time = (time.time() - t) / 100

    t = time.time()
    for i in range(100):
        data = zlib.decompress(z_compressed_data)
    z_decompress_time = (time.time() - t) / 100

    rp_annot_bytes = np_payload_diff_coords.tobytes()

    print('time to compress is ', round(compress_time, 3), 'which is',
          round(z_compressed_time / compress_time,  3), 'faster than zlib')
    print('time to decompress is ', round(decompress_time, 9), 'which is', 
          round(z_decompress_time / decompress_time, 3), 'faster than zlib')
    print('compressed size is ', len(rp_annot_bytes), 'which is',
          round(len(z_compressed_data) / len(rp_annot_bytes), 2), 'smaller than zlib')


def test_compress():
    np_1d_bool_array = np.zeros(100000, dtype=bool)
    np_1d_bool_array[20000:50000] = True
    compressed = rpa.compress(np_1d_bool_array)
    decompressed =  rpa.decompress(compressed, len(np_1d_bool_array))
    assert np.array_equal(np_1d_bool_array, decompressed)

if __name__ == '__main__':
    
    test_get_diff_array()
    test_reconstruct()
    test_compress()

    if os.path.isfile('test_data/payload.npy'):
        test_with_larger_payload()
    print('pass')
