import numpy as np
import time
import zlib
import rp_annot as rpa

def test_compress():
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
        assert np.array_equal(test_array, rpa.reconstruct_from_diff_coords(get_diff_coords(test_array), len(test_array)))


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
    np_payload1d = np_payload.reshape(-1)
    payload_len = len(np_payload1d)

    t = time.time()
    for i in range(100):
        np_payload_diff_coords = rpa.get_diff_coords(np_payload1d)
    compress_time = (time.time() - t) / 100

    t = time.time()
    for i in range(100):
        np_payload1d =  rpa.reconstruct_from_diff_coords(np_payload_diff_coords, payload_len)
    decompress_time = (time.time() - t) / 100

    payload_bytes = np_payload.tobytes()
    t = time.time()
    for i in range(100):
        z_compressed_data = zlib.compress(payload_bytes, 1)
    z_compressed_time = (time.time() - t) / 100

    t = time.time()
    for i in range(100):
        data = zlib.decompress(z_compressed_data)
    z_decompress_time = (time.time() - t) / 100

    print('time to compress is ', z_compressed_time / compress_time, 'faster than zlib')
    print('time to decompress is ', z_decompress_time / decompress_time, 'faster than zlib')
    print('compressed size is ', len(z_compressed_data) / len(np_payload_diff_coords_bytes), 'smaller than zlib')


if __name__ == '__main__':
    test_get_diff_array()
    test_compress()
    #test_with_larger_payload()
