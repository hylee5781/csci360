# Lab 2 Extra Credit (Problem 3): A* vs dynamically weighted A*
# this is for extra credit not the main hw
# for each m, run both searches on the stacks and record
#   - average flips
#   - average nodes visited
#   - running time
# m = 1..6 -> every possible stack (m! * 2^m)
# m = 7, 8 -> too many stacks (A* alone would take hours / days)
#            so a fixed random sample, same sample for both searches

# import
import itertools
import random
import time
import json
import matplotlib.pyplot as plt
import lab2
from lab2 import TextbookStack


# how many random stacks for the big m
SAMPLE_SIZE = 2000
# biggest m where we still try every stack
LAST_FULL_M = 6


if __name__ == "__main__":
    m_values = [1, 2, 3, 4, 5, 6, 7, 8]

    all_results = []

    for m in m_values:
        # make the list of starting stacks
        stacks_to_try = []
        if m <= LAST_FULL_M:
            # every (order, orientations) pair, m! * 2^m total
            for order in itertools.permutations(range(0, m)):
                for orientations in itertools.product([0, 1], repeat=m):
                    stacks_to_try.append((list(order), list(orientations)))
            how_chosen = "all"
        else:
            # random sample, seeded so it's the same every run
            random.seed(360 + m)
            for k in range(0, SAMPLE_SIZE):
                order = []
                for i in range(0, m):
                    order.append(i)
                random.shuffle(order)

                orientations = []
                for i in range(0, m):
                    orientations.append(random.randint(0, 1))

                stacks_to_try.append((order, orientations))
            how_chosen = "sample"

        num_stacks = len(stacks_to_try)
        print("m =", m, ":", num_stacks, "stacks (" + how_chosen + ")")

        # ---- run A* on every stack ----
        astar_total_flips = 0
        astar_total_nodes = 0
        astar_total_time = 0.0
        astar_lengths = []

        for order, orientations in stacks_to_try:
            one_stack = TextbookStack(order, orientations)

            start_clock = time.perf_counter()
            flip_sequence = lab2.a_star_search(one_stack)
            end_clock = time.perf_counter()

            # sanity check: it really got sorted
            if lab2.apply_sequence(one_stack, flip_sequence).check_ordered() == False:
                print("  !! A* not sorted:", order, orientations)

            astar_total_flips = astar_total_flips + len(flip_sequence)
            astar_total_nodes = astar_total_nodes + lab2.nodes_visited
            astar_total_time = astar_total_time + (end_clock - start_clock)
            astar_lengths.append(len(flip_sequence))

        print("  A* done")

        # ---- run weighted A* on every stack (same thing) ----
        weighted_total_flips = 0
        weighted_total_nodes = 0
        weighted_total_time = 0.0
        weighted_lengths = []

        for order, orientations in stacks_to_try:
            one_stack = TextbookStack(order, orientations)

            start_clock = time.perf_counter()
            flip_sequence = lab2.weighted_a_star_search(one_stack)
            end_clock = time.perf_counter()

            if lab2.apply_sequence(one_stack, flip_sequence).check_ordered() == False:
                print("  !! weighted A* not sorted:", order, orientations)

            weighted_total_flips = weighted_total_flips + len(flip_sequence)
            weighted_total_nodes = weighted_total_nodes + lab2.nodes_visited
            weighted_total_time = weighted_total_time + (end_clock - start_clock)
            weighted_lengths.append(len(flip_sequence))

        print("  weighted A* done")

        # how many stacks weighted A* solved with MORE flips than A*
        worse_count = 0
        for k in range(0, num_stacks):
            if weighted_lengths[k] > astar_lengths[k]:
                worse_count = worse_count + 1

        astar_result = {}
        astar_result["average_flips"] = astar_total_flips / num_stacks
        astar_result["average_nodes"] = astar_total_nodes / num_stacks
        astar_result["total_time"] = astar_total_time
        astar_result["average_time"] = astar_total_time / num_stacks

        weighted_result = {}
        weighted_result["average_flips"] = weighted_total_flips / num_stacks
        weighted_result["average_nodes"] = weighted_total_nodes / num_stacks
        weighted_result["total_time"] = weighted_total_time
        weighted_result["average_time"] = weighted_total_time / num_stacks

        one_row = {}
        one_row["m"] = m
        one_row["num_stacks"] = num_stacks
        one_row["how_chosen"] = how_chosen
        one_row["astar"] = astar_result
        one_row["weighted"] = weighted_result
        one_row["weighted_worse_count"] = worse_count
        all_results.append(one_row)

    # save numbers so the pdf can use them
    out_file = open("lab2_extra_credit_results.json", "w")
    json.dump(all_results, out_file, indent=2)
    out_file.close()

    # table 1: average flips
    print("")
    print("m | stacks | A* avg flips | weighted A* avg flips | weighted worse")
    for row in all_results:
        print(row["m"], "|", row["num_stacks"], "|",
              round(row["astar"]["average_flips"], 3), "|",
              round(row["weighted"]["average_flips"], 3), "|",
              row["weighted_worse_count"])

    # table 2: average nodes visited
    print("")
    print("m | stacks | A* avg nodes | weighted A* avg nodes")
    for row in all_results:
        print(row["m"], "|", row["num_stacks"], "|",
              round(row["astar"]["average_nodes"], 3), "|",
              round(row["weighted"]["average_nodes"], 3))

    # table 3: running time
    print("")
    print("m | A* total s | A* avg ms | weighted total s | weighted avg ms")
    for row in all_results:
        print(row["m"], "|",
              round(row["astar"]["total_time"], 6), "|",
              round(row["astar"]["average_time"] * 1000, 4), "|",
              round(row["weighted"]["total_time"], 6), "|",
              round(row["weighted"]["average_time"] * 1000, 4))

    # pull columns out for the plots
    astar_flips = []
    weighted_flips = []
    astar_nodes = []
    weighted_nodes = []
    astar_avg_ms = []
    weighted_avg_ms = []
    for row in all_results:
        astar_flips.append(row["astar"]["average_flips"])
        weighted_flips.append(row["weighted"]["average_flips"])
        astar_nodes.append(row["astar"]["average_nodes"])
        weighted_nodes.append(row["weighted"]["average_nodes"])
        astar_avg_ms.append(row["astar"]["average_time"] * 1000)
        weighted_avg_ms.append(row["weighted"]["average_time"] * 1000)

    # graded part is m = 1..5, total time over every stack
    graded_m = []
    astar_total_s = []
    weighted_total_s = []
    for row in all_results:
        if row["m"] <= 5:
            graded_m.append(row["m"])
            astar_total_s.append(row["astar"]["total_time"])
            weighted_total_s.append(row["weighted"]["total_time"])

    # figure 1: average flips
    plt.figure()
    plt.plot(m_values, astar_flips, marker="o", label="A*")
    plt.plot(m_values, weighted_flips, marker="s", label="weighted A*")
    plt.xlabel("m (number of books)")
    plt.ylabel("average number of flips")
    plt.title("average flips vs m")
    plt.legend()
    plt.savefig("lab2_average_flips.png")

    # figure 2: average nodes visited (log scale, it grows fast)
    plt.figure()
    plt.plot(m_values, astar_nodes, marker="o", label="A*")
    plt.plot(m_values, weighted_nodes, marker="s", label="weighted A*")
    plt.yscale("log")
    plt.xlabel("m (number of books)")
    plt.ylabel("average nodes visited (log scale)")
    plt.title("average nodes visited vs m")
    plt.legend()
    plt.savefig("lab2_average_nodes.png")

    # figure 3: total running time for m = 1..5 (the graded part)
    plt.figure()
    plt.plot(graded_m, astar_total_s, marker="o", label="A*")
    plt.plot(graded_m, weighted_total_s, marker="s", label="weighted A*")
    plt.xlabel("m (number of books)")
    plt.ylabel("total running time over all stacks (s)")
    plt.title("total running time vs m (m = 1..5, every stack)")
    plt.legend()
    plt.savefig("lab2_total_time.png")

    # figure 4: same thing on log scale -> straight line = exponential
    plt.figure()
    plt.plot(graded_m, astar_total_s, marker="o", label="A*")
    plt.plot(graded_m, weighted_total_s, marker="s", label="weighted A*")
    plt.yscale("log")
    plt.xlabel("m (number of books)")
    plt.ylabel("total running time (s, log scale)")
    plt.title("total running time vs m, log scale")
    plt.legend()
    plt.savefig("lab2_total_time_log.png")

    # figure 5: average time per stack, all m
    plt.figure()
    plt.plot(m_values, astar_avg_ms, marker="o", label="A*")
    plt.plot(m_values, weighted_avg_ms, marker="s", label="weighted A*")
    plt.yscale("log")
    plt.xlabel("m (number of books)")
    plt.ylabel("average time per stack (ms, log scale)")
    plt.title("average running time per stack vs m")
    plt.legend()
    plt.savefig("lab2_average_time.png")
