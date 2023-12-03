import numpy as np
import sys

def unwrap_1d(phase_array, discont=np.pi):
    unwrapped = np.zeros_like(phase_array)
    unwrapped[0] = phase_array[0]

    for i in range(1, len(phase_array)):
        delta = phase_array[i] - phase_array[i - 1]
        if delta > discont:
            unwrapped[i] = unwrapped[i - 1] + delta - 2 * np.pi
        elif delta < -discont:
            unwrapped[i] = unwrapped[i - 1] + delta + 2 * np.pi
        else:
            unwrapped[i] = unwrapped[i - 1] + delta

    return unwrapped

def unwrap_2d_horizontal_vertical(phase_array_2d, discont=np.pi):
    # Unwrap horizontally (row-wise)
    unwrapped_range = np.zeros_like(phase_array_2d)
    for i in range(phase_array_2d.shape[0]):
        unwrapped_range[i, :] = unwrap_1d(phase_array_2d[i, :], discont)

    # Unwrap vertically (column-wise)
    unwrapped_azimuth = np.zeros_like(phase_array_2d)
    for j in range(phase_array_2d.shape[1]):
        unwrapped_azimuth[:, j] = unwrap_1d(phase_array_2d[:, j], discont)

    # Unwrap 2D (both horizontally and vertically)
    unwrapped_2d = np.zeros_like(phase_array_2d)
    for i in range(phase_array_2d.shape[0]):
        unwrapped_2d[i, :] = unwrap_1d(unwrapped_range[i, :], discont)
    for j in range(phase_array_2d.shape[1]):
        unwrapped_2d[:, j] = unwrap_1d(unwrapped_2d[:, j], discont)

    return unwrapped_range, unwrapped_azimuth, unwrapped_2d

def main():
    # Check for command line arguments
    if len(sys.argv) != 2:
        print("Usage: python unwrap_script.py <path_to_wrapped_array.npy>")
        sys.exit(1)

    # Load the wrapped array from the provided path
    path_to_wrapped_array = sys.argv[1]
    try:
        wrapped_array = np.load(path_to_wrapped_array)
    except Exception as e:
        print(f"Error loading wrapped array: {e}")
        sys.exit(1)

    # Perform unwrapping
    unwrapped_range, unwrapped_azimuth, unwrapped_2d = unwrap_2d_horizontal_vertical(wrapped_array)

    # Save the unwrapped arrays
    np.save('unwrapped_range.npy', unwrapped_range)
    np.save('unwrapped_azimuth.npy', unwrapped_azimuth)
    np.save('unwrapped_2d.npy', unwrapped_2d)

    print("Unwrapping completed. Files saved as 'unwrapped_horizontal.npy', 'unwrapped_vertical.npy', and 'unwrapped_2d.npy'")

if __name__ == "__main__":
    main()
