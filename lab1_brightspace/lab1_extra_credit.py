# Lab 1 Extra Credit: average number of flips vs n, for BFS and DFS.
# 이 파일은 채점 대상인 lab1.py 가 아니라 추가 분석용 스크립트임.

import random
import matplotlib.pyplot as plt
from lab1 import TextbookStack, breadth_first_search, depth_first_search


def average_flips_by_n(search_function, n_values, num_samples):
    # returns avg flips for each n
    average_flips_list = []

    for n in n_values:
        total_flips = 0

        for sample_num in range(num_samples):
            # make one random stack of size n
            random_order = list(range(n))
            random.shuffle(random_order)
            random_orientations = [random.randint(0, 1) for i in range(n)]

            random_stack = TextbookStack(random_order, random_orientations)

            # run the search, count its flips
            flip_sequence = search_function(random_stack)
            total_flips = total_flips + len(flip_sequence)

        # average over all samples for this n
        average_flips = total_flips / num_samples
        average_flips_list.append(average_flips)

    return average_flips_list


if __name__ == "__main__":
    random.seed(0)  # same random stacks every run

    n_values = [1, 2, 3, 4, 5, 6]
    num_samples = 20

    bfs_average_flips = average_flips_by_n(breadth_first_search, n_values, num_samples)
    dfs_average_flips = average_flips_by_n(depth_first_search, n_values, num_samples)

    print("n values:", n_values)
    print("BFS average flips:", bfs_average_flips)
    print("DFS average flips:", dfs_average_flips)

    # figure 1: BFS
    plt.figure()
    plt.plot(n_values, bfs_average_flips, marker="o")
    plt.xlabel("n (number of books)")
    plt.ylabel("average number of flips")
    plt.title("BFS: average flips vs n")
    plt.savefig("bfs_average_flips.png")

    # figure 2: DFS
    plt.figure()
    plt.plot(n_values, dfs_average_flips, marker="o")
    plt.xlabel("n (number of books)")
    plt.ylabel("average number of flips")
    plt.title("DFS: average flips vs n")
    plt.savefig("dfs_average_flips.png")
