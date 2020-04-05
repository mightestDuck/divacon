import sys
import timeit
import numpy as np
import matplotlib.pyplot as plt
from typing import Callable


def binary_search(search_space: list, target: int, ordered: bool = False) -> (int, int, list):
    if not ordered:
        search_space = mergesort(list(search_space))

    i_low = 0
    i_high = len(search_space) - 1
    i_mid = int(i_high/2)

    steps = 0
    while search_space[i_mid] != target:
        if target > search_space[i_mid]:
            i_low = i_mid + 1
        else:
            i_high = i_mid - 1
        i_mid = int((i_high - i_low)/2) + i_low
        steps += 1
        print(f'{steps} | {search_space[i_low]} < {search_space[i_mid]} < {search_space[i_high]}')
    return i_mid, steps, search_space


def mergesort(l: list) -> list:
    if len(l) <= 1:  # recursion escape condition
        return l

    # divide
    left = mergesort(l[0:int(len(l)/2)])
    right = mergesort(l[int(len(l)/2): len(l)])

    # merge
    l = []
    while len(left) > 0 and len(right) > 0:
        if left[0] <= right[0]:
            l.append(left[0])
            left = left[1:]
        else:
            l.append(right[0])
            right = right[1:]
    if len(left) > 0:
        l += left
    else:
        l += right
    return l


def quicksort(l: list) -> list:
    # pivot is the first on the right, should be the median
    if len(l) < 1:  # recursion escape condition
        return l

    # partitioning
    pivot = l[-1]
    left, right = [], []
    for e in l[:-1]:
        if e <= pivot:
            left += [e]
        else:
            right += [e]

    # conquering
    left = quicksort(left)
    right = quicksort(right)
    return left + [pivot] + right


def test_sorting(f: Callable, l_len: int):
    l = np.random.randint(low=1, high=100, size=l_len)
    return f(l)


def plot(ys: list, x: list, title: str = None, labels=list, xlab: str = None, ylab: str = None):
    fig, ax = plt.subplots()
    for y, label in zip(ys, labels):
        ax.plot(x,  y, '-', label=label)

    ax.set_xscale('log'), ax.set_yscale('log')
    plt.xlabel(xlab), plt.ylabel(ylab)
    plt.title(title)
    plt.legend()
    plt.show()


def main():
    l = np.random.randint(low=1, high=100, size=12)
    target = np.random.choice(l, 1)[0]
    print(f'Randomly generated list of size {len(l)}')
    idx, steps, sorted_list = binary_search(search_space=list(l), target=target, ordered=False)
    print(f'target={target}, idx={idx}, list[idx]={l[idx]} found in {steps} steps.')


if __name__ == '__main__':
    sys.setrecursionlimit(10 ** 6)
    fs = [f.__name__ for f in [quicksort, mergesort]]
    lengths = [int(10**i) for i in np.linspace(1, 5, 20)]
    print(f'lengths: {lengths}')
    results = {}
    for cnt, f in enumerate(fs):
        print(f'{cnt}/{len(fs)} Evaluation of {f} started.')
        try:
            results[f]
        except Exception:
            results[f] = []
        for l in lengths:
            print(f'Testing {f} for len(list)={l}.')
            results[f].append(timeit.timeit(stmt=f'test_sorting(f={f}, l_len={l})', globals=globals(), number=100))
    plot(x=lengths, ys=[results[f] for f in fs], labels=fs,
         title='average sorting time',
         xlab='log(list length)',
         ylab='time in s')
