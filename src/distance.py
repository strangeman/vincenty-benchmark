import geopy.distance
from ctypes import *

golib = cdll.LoadLibrary("./build/godistance.so")
golib.GoDistance.argtypes = [c_double, c_double, c_double, c_double]
golib.GoDistance.restype = c_double

rustlib_default = cdll.LoadLibrary("./build/rustdistance_default.so")
rustlib_default.rust_distance.argtypes = [c_double, c_double, c_double, c_double]
rustlib_default.rust_distance.restype = c_double

rustlib_optimized = cdll.LoadLibrary("./build/rustdistance_optimized.so")
rustlib_optimized.rust_distance.argtypes = [c_double, c_double, c_double, c_double]
rustlib_optimized.rust_distance.restype = c_double

def python_distance(coord_1, coord_2):
    return round(geopy.distance.vincenty(coord_1, coord_2).km, 4)

def go_distance(lat1, lon1, lat2, lon2):
    return golib.GoDistance(lat1, lon1, lat2, lon2)

def rust_distance_default(lat1, lon1, lat2, lon2):
    return rustlib_default.rust_distance(lat1, lon1, lat2, lon2)

def rust_distance_optimized(lat1, lon1, lat2, lon2):
    return rustlib_optimized.rust_distance(lat1, lon1, lat2, lon2)

test_cases = [
    {'coord_1': [52.2296756, 22.0122287], 'coord_2': [52.406374, 16.9251681]},
    {'coord_1': [34.2296756, 21.0122287], 'coord_2': [52.406374, 16.9251681]},
    {'coord_1': [15.2296756, 76.0122287], 'coord_2': [52.406374, 16.9251681]},
    {'coord_1': [34.2296756, 52.0122287], 'coord_2': [52.406374, 16.9251681]},
    {'coord_1': [23.2296756, 19.0122287], 'coord_2': [52.406374, 16.9251681]},
    {'coord_1': [4.2296756, 1.0122287], 'coord_2': [52.406374, 16.9251681]}]

def main():
    print("Python code")
    for case in test_cases:
        distance = python_distance((case['coord_1'][0], case['coord_1'][1]), (case['coord_2'][0], case['coord_2'][1]))
        print(distance)

    print("\nGo code")
    for case in test_cases:
        distance = go_distance(case['coord_1'][0], case['coord_1'][1], case['coord_2'][0], case['coord_2'][1])
        print(distance)

    print("\nRust code")
    for case in test_cases:
        distance = rust_distance_default(case['coord_1'][0], case['coord_1'][1], case['coord_2'][0], case['coord_2'][1])
        print(distance)

    print("\nRust code with compiler optimizations")
    for case in test_cases:
        distance = rust_distance_optimized(case['coord_1'][0], case['coord_1'][1], case['coord_2'][0], case['coord_2'][1])
        print(distance)

if __name__ == '__main__':
    main()