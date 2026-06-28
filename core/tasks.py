import math
import time


def compute_primes(n: int) -> dict:
    """
    Find all primes upto n using Sieve of Eratosthenes.
    Pure CPU work- for demonstrating process isolation.
    """
    start = time.perf_counter()

    sieve = bytearray([1]) * (n + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))

    primes = [i for i, v in enumerate(sieve) if v]
    elapsed = time.perf_counter() - start

    return {
        "count": len(primes),
        "largest": primes[-1] if primes else None,
        "elapsed_seconds": round(elapsed, 4),
    }


def fibonacci(n: int) -> dict:
    """Compute nth Fibonacci number iteratively."""
    start = time.perf_counter()

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    elapsed = time.perf_counter() - start
    return {
        "n": n,
        "result": a,
        "elapsed_seconds": round(elapsed, 4),
    }


def matrix_multiply(size: int) -> dict:
    """Multiply two random size×size matrices manually (no numpy)."""
    import random

    start = time.perf_counter()

    A = [[random.random() for _ in range(size)] for _ in range(size)]
    B = [[random.random() for _ in range(size)] for _ in range(size)]
    C = [[0.0] * size for _ in range(size)]

    for i in range(size):
        for j in range(size):
            for k in range(size):
                C[i][j] += A[i][k] * B[k][j]

    elapsed = time.perf_counter() - start
    return {
        "matrix_size": f"{size}x{size}",
        "elapsed_seconds": round(elapsed, 4),
    }


TASK_REGISTRY: dict[str, callable] = {
    "compute_primes": compute_primes,
    "fibonacci": fibonacci,
    "matrix_multiply": matrix_multiply,
}
