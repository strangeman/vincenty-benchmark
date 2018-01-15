import pytest

import distance

test_cases = [
    {'coord_1': [52.2296756, 22.0122287], 'coord_2': [52.406374, 16.9251681], 'distance': 347.3727},
    {'coord_1': [34.2296756, 21.0122287], 'coord_2': [52.406374, 16.9251681], 'distance': 2045.6191},
    {'coord_1': [15.2296756, 76.0122287], 'coord_2': [52.406374, 16.9251681], 'distance': 6596.2486},
    {'coord_1': [34.2296756, 52.0122287], 'coord_2': [52.406374, 16.9251681], 'distance': 3436.2289},
    {'coord_1': [23.2296756, 19.0122287], 'coord_2': [52.406374, 16.9251681], 'distance': 3243.4761},
    {'coord_1': [4.2296756, 1.0122287], 'coord_2': [52.406374, 16.9251681], 'distance': 5538.799}]


def pedantic_benchmark(func, benchmark):
    benchmark.pedantic(func, rounds=1000, warmup_rounds=5, iterations=100)

def test_distance_python():
    for case in test_cases:
        #print(case)
        assert distance.python_distance((case['coord_1'][0], case['coord_1'][1]), (case['coord_2'][0], case['coord_2'][1])) == case['distance']

def test_benchmark_distance_python(benchmark):
    pedantic_benchmark(test_distance_python, benchmark)

def test_distance_go():
    for case in test_cases:
        #print(case)
        assert distance.go_distance(case['coord_1'][0], case['coord_1'][1], case['coord_2'][0], case['coord_2'][1]) == case['distance']

def test_benchmark_distance_go(benchmark):
    pedantic_benchmark(test_distance_go, benchmark)

def test_distance_rust_default():
    for case in test_cases:
        #print(case)
        assert distance.rust_distance_default(case['coord_1'][0], case['coord_1'][1], case['coord_2'][0], case['coord_2'][1]) == case['distance']

def test_benchmark_distance_rust_default(benchmark):
    pedantic_benchmark(test_distance_rust_default, benchmark)

def test_distance_rust_optimized():
    for case in test_cases:
        #print(case)
        assert distance.rust_distance_optimized(case['coord_1'][0], case['coord_1'][1], case['coord_2'][0], case['coord_2'][1]) == case['distance']

def test_benchmark_distance_rust_optimized(benchmark):
    pedantic_benchmark(test_distance_rust_optimized, benchmark)
