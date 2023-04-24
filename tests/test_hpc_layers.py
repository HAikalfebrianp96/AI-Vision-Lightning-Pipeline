import random
import time
from functools import wraps

import numpy as np
import pytest
import torch

import src.models.components.layers.hypercomplex_layers as hpc_layers


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        return total_time, result
    return timeit_wrapper


def tensor_data():
    return [
        torch.zeros((100, 100)),
        torch.ones((100, 100)),
    ]


@timeit
def linear_kronecker_product1(mat_a: torch.Tensor, mat_s: torch.Tensor):
    siz1 = torch.Size(torch.tensor(mat_a.shape[-2:]) * torch.tensor(mat_s.shape[-2:]))
    res = mat_a.unsqueeze(-1).unsqueeze(-3) * mat_s.unsqueeze(-2).unsqueeze(-4)
    siz0 = res.shape[:-4]
    return torch.sum(res.reshape(siz0 + siz1), dim=0)


@timeit
def linear_kronecker_product2(in_features: int, out_features: int, n_size: int, mat_a: torch.Tensor, mat_s: torch.Tensor):
    H = torch.zeros((out_features, in_features))
    for i in range(n_size):
        H = H + torch.kron(mat_a[i], mat_s[i])
    return H


def test_kronecker_product():
    n_size = 4
    in_features = 100
    out_features = 40
    mat_a = torch.rand((n_size, n_size, n_size))
    mat_b = torch.rand((n_size, out_features//n_size, in_features//n_size))
    _, H_1 = linear_kronecker_product1(mat_a, mat_b)
    _, H_2 = linear_kronecker_product2(in_features, out_features, n_size, mat_a, mat_b)

    assert H_1.shape == H_2.shape
    assert torch.allclose(H_1, H_2)


def test_catch_phm_linear():
    _ = hpc_layers.PHMLinear(1, 1000, 100)

    with pytest.raises(Exception) as e_info:
        _ = hpc_layers.PHMLinear(3, 1000, 9)
        assert e_info == 'Input features: 1000 is not divisible by n-3'

    with pytest.raises(Exception):
        _ = hpc_layers.PHMLinear(7, 140, 9)
        assert e_info == 'Output features: 9 is not divisible by n-7'


def test_run_phm_linear():
    n_sizes = [1, 2, 3, 4, 5, 7, 9, 12]
    output_size = random.randrange(0, 1000, np.lcm.reduce(n_sizes))  # nosec B311

    for size in n_sizes:
        input_size = np.lcm.reduce(n_sizes)
        layer = hpc_layers.PHMLinear(size, input_size, output_size)

        input_tensors = [
            torch.zeros((100, input_size)),
            torch.ones((100, input_size)),
            torch.rand((100, input_size))
        ]
        for inp in input_tensors:
            _ = layer(inp)
