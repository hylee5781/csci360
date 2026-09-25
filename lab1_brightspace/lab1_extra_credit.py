# Lab 1 Extra Credit (Problem 3): exhaustive analysis for n = 1..5.
# this is for extra credit not the main hw
# for every possible initial stack of each n, i'mg oing to run BFS and DFS
# and then
# average the number of flips
# AND also the number of nodes traversed

# import
import itertools
from collections import deque
import matplotlib.pyplot as plt
from lab1 import TextbookStack


def bfs_with_node_count(stack):
    # same BFS as lab1.py
    # but also counts nodes traversed
    # 약간 헷갈리는게
    # 노드 수 = 탐색하면서 방문한 서로 다른 state 개수 근데 이따 돌아오기
    start_state = (tuple(stack.order), tuple(stack.orientations))
    been_there = {start_state}

    if stack.check_ordered():
        return [], len(been_there)

    # lets name them correctly
    pending_tbd = deque()
    pending_tbd.append((stack, []))

    while pending_tbd:
        stack_rightnow, path_sofar_used = pending_tbd.popleft()

        # increase
        for point_here in range(1, stack_rightnow.num_books + 1):
            new_stack = stack_rightnow.copy()
            new_stack.flip_stack(point_here)
            new_state = (tuple(new_stack.order), tuple(new_stack.orientations))

            # pass
            if new_state in been_there:
                continue
            been_there.add(new_state)

            # add
            new_path = path_sofar_used + [point_here]

            if new_stack.check_ordered():
                return new_path, len(been_there)

            pending_tbd.append((new_stack, new_path))

    # need to return here
    return [], len(been_there)


def dfs_with_node_count(stack):
    # same DFS as lab1.py
    # but need to count nodes traversed
    start_state = (tuple(stack.order), tuple(stack.orientations))
    been_there = {start_state}

    # order check
    if stack.check_ordered():
        return [], len(been_there)

    # save
    backup = [(stack, [])]

    while backup:
        stack_rightnow, path_sofar_used = backup.pop()

        for point_here in range(1, stack_rightnow.num_books + 1):
            new_stack = stack_rightnow.copy()
            new_stack.flip_stack(point_here)
            new_state = (tuple(new_stack.order), tuple(new_stack.orientations))

            # pass
            if new_state in been_there:
                continue
            been_there.add(new_state)

            new_path = path_sofar_used + [point_here]

            # return new
            if new_stack.check_ordered():
                return new_path, len(been_there)

            backup.append((new_stack, new_path))

    # return
    return [], len(been_there)


def all_initial_stacks(n):
    # every possible (order, orientations) pair, 2^n * n! total
    # come back here later
    # make empty first
    all_stacks = []
    for order in itertools.permutations(range(n)):
        for orientations in itertools.product([0, 1], repeat=n):
            all_stacks.append((list(order), list(orientations)))
    return all_stacks


def average_flips_and_nodes(search_function_with_count, n_values):
    # exhaustive average, per n, of flips & nodes traversed
    average_flips_list = []
    average_nodes_list = []

    for n in n_values:
        # set it to 0 first
        total_flips = 0
        total_nodes = 0
        all_stacks = all_initial_stacks(n)

        for order, orientations in all_stacks:
            one_stack = TextbookStack(order, orientations)
            flip_sequence, node_count = search_function_with_count(one_stack)
            total_flips = total_flips + len(flip_sequence)
            total_nodes = total_nodes + node_count

        num_stacks = len(all_stacks)
        average_flips_list.append(total_flips / num_stacks)
        average_nodes_list.append(total_nodes / num_stacks)
        # print it here
        print(f"  n={n} done ({num_stacks} stacks)")

    return average_flips_list, average_nodes_list


if __name__ == "__main__":
    n_values = [1, 2, 3, 4, 5]

    print("running BFS over all stacks...")
    bfs_average_flips, bfs_average_nodes = average_flips_and_nodes(bfs_with_node_count, n_values)

    print("running DFS over all stacks...")
    dfs_average_flips, dfs_average_nodes = average_flips_and_nodes(dfs_with_node_count, n_values)

    print("\nn values:", n_values)
    print("BFS average flips:", bfs_average_flips)
    print("BFS average nodes:", bfs_average_nodes)
    print("DFS average flips:", dfs_average_flips)
    print("DFS average nodes:", dfs_average_nodes)

    # table required by the assignment
    print("\nn | BFS avg flips | BFS avg nodes | DFS avg flips | DFS avg nodes")
    for i, n in enumerate(n_values):
        print(f"{n} | {bfs_average_flips[i]:.3f} | {bfs_average_nodes[i]:.3f} | "
              f"{dfs_average_flips[i]:.3f} | {dfs_average_nodes[i]:.3f}")

    # this is gonna be
    # figure 1: BFS average flips vs n
    plt.figure()
    plt.plot(n_values, bfs_average_flips, marker="o")
    plt.xlabel("n (number of books)")
    plt.ylabel("average number of flips")
    plt.title("BFS: average flips vs n")
    plt.savefig("bfs_average_flips.png")

    # here it is 
    # figure 2: DFS average flips vs n
    plt.figure()
    plt.plot(n_values, dfs_average_flips, marker="o")
    plt.xlabel("n (number of books)")
    plt.ylabel("average number of flips")
    plt.title("DFS: average flips vs n")
    plt.savefig("dfs_average_flips.png")
