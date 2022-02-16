import numpy as np


def reconstruct_from_diff_array(diff_array):
    reconstructed = np.zeros(diff_array.shape[0])
    cur_val = 0
    for i, d in enumerate(diff_array):
        if d != 0:
            if cur_val == 0:
                cur_val = 1
            else:
                cur_val = 0
        reconstructed[i] = cur_val
    return reconstructed


def reconstruct_from_diff_coords(diff_coords, length):
    reconstructed = np.zeros(length, dtype=bool)
    pair_idx = 0
    diff_coords_len =  len(diff_coords)
    while pair_idx < len(diff_coords):
        from_idx = diff_coords[pair_idx]
        if pair_idx + 1 > diff_coords_len - 1:
            # if we have gone over the edge. Just set the last 1 to 1.
            reconstructed[from_idx:] = 1
        else:
            # otherwise take the to_idx from the diff_coords
            to_idx = diff_coords[pair_idx + 1]
            reconstructed[from_idx:to_idx] = 1
        pair_idx += 2
    return reconstructed


def get_diff_array(original):
    # https://stackoverflow.com/questions/32195525/how-to-np-roll-faster
    diff_array = np.bitwise_xor(original,  np.roll(original, 1))
    # We assume difference is from 0.
    # if 0 was at the start of original, then it should be at the start of the diff array
    diff_array[0] = original[0]
    return diff_array

def get_diff_coords(original):
    diff_array = get_diff_array(original)
    coords = np.where(diff_array)
    return coords[0]


def decompress(compressed, length):
    diff_coords = np.frombuffer(compressed, dtype='int64')
    return reconstruct_from_diff_coords(diff_coords, length)


def compress(original):
    return get_diff_coords(original).tobytes()
