import numpy as np
import timeit


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

    # recursion
    left = quicksort(left)
    right = quicksort(right)
    return left + [pivot] + right


def main():
    l = np.random.randint(low=1, high=100, size=12)
    target = np.random.choice(l, 1)[0]
    print(f'Randomly generated list of size {len(l)}')
    idx, steps, sorted_list = binary_search(search_space=list(l), target=target, ordered=False)
    print(f'target={target}, idx={idx}, list[idx]={l[idx]} found in {steps} steps.')


if __name__ == '__main__':
    main()

    #print(timeit.timeit(test_sorting(quicksort), number=100))
