# you can add imports but you should not rely on libraries that are not already provided in "requirements.txt #
from collections import deque
from heapq import heappush, heappop

import numpy as np


class TextbookStack(object):
    """A class that tracks the"""

    def __init__(self, initial_order, initial_orientations):
        assert len(initial_order) == len(initial_orientations)
        self.num_books = len(initial_order)

        for i, a in enumerate(initial_orientations):
            assert i in initial_order
            assert a == 1 or a == 0

        self.order = np.array(initial_order)
        self.orientations = np.array(initial_orientations)

    def flip_stack(self, position):
        assert position <= self.num_books

        self.order[0:position] = self.order[0:position][::-1]
        self.orientations[0:position] = np.abs(self.orientations[0:position] - 1)[
            ::-1
        ]

    def check_ordered(self):
        for idx, front_matter in enumerate(self.orientations):
            if (idx != self.order[idx]) or (front_matter != 1):
                return False

        return True

    def copy(self):
        return TextbookStack(self.order, self.orientations)

    def __eq__(self, other):
        assert isinstance(
            other, TextbookStack
        ), "equality comparison can only ba made with other __TextbookStacks__"
        return all(self.order == other.order) and all(
            self.orientations == other.orientations
        )

    def __str__(self):
        return f"TextbookStack:\n\torder: {self.order}\n\torientations:{self.orientations}"


def apply_sequence(stack, sequence):
    new_stack = stack.copy()
    for flip in sequence:
        new_stack.flip_stack(flip)
    return new_stack


# how many states got popped and expanded in the last search
# (only for the extra credit tables)
nodes_visited = 0


def a_star_search(stack):
    flip_sequence = []

    # --- v ADD YOUR CODE HERE v --- #
    global nodes_visited
    nodes_visited = 0

    num_books = stack.num_books

    # numpy arrays aren't hashable -> plain tuples of ints
    start_order = []
    start_face = []
    for i in range(0, num_books):
        start_order.append(int(stack.order[i]))
        start_face.append(int(stack.orientations[i]))
    start_state = (tuple(start_order), tuple(start_face))

    # reached_goal: book i at spot i, all facing up
    reached_goal = True
    for i in range(0, num_books):
        if start_order[i] != i:
            reached_goal = False
        if start_face[i] != 1:
            reached_goal = False

    # already sorted -> nothing to do (이미 정렬돼 있으면 끝)
    if reached_goal == True:
        return flip_sequence

    # count_bad_pairs: count neighbor pairs that are NOT a good pair
    # good pair = both face up and going up by 1,
    #          or both face down and going down by 1
    # anything else hits (a), (b), (c) or (d) -> count it once
    # one flip only changes the pair at the cut, so h drops by at most 1
    # -> admissible (never overestimates)
    mess_count = 0
    for i in range(0, num_books - 1):
        top_book = start_order[i]
        below_book = start_order[i + 1]
        top_face = start_face[i]
        below_face = start_face[i + 1]

        pair_is_good = False

        if top_face == 1 and below_face == 1:
            if below_book - top_book == 1:
                pair_is_good = True
        elif top_face == 0 and below_face == 0:
            if top_book - below_book == 1:
                pair_is_good = True

        if pair_is_good == False:
            mess_count = mess_count + 1
    start_h = mess_count

    # heap entries: (f, arrival_order, steps_taken, state)
    # arrival_order breaks ties first-come-first-served
    waiting_line = []
    arrival_order = 0

    # cheapest number of flips found so far for each state
    best_count_at = {}
    best_count_at[start_state] = 0

    # came_from[state] = (previous state, cut_spot used to get here)
    came_from = {}
    came_from[start_state] = None

    heappush(waiting_line, (0 + start_h, arrival_order, 0, start_state))

    while len(waiting_line) > 0:
        popped = heappop(waiting_line)
        steps_taken = popped[2]
        stack_rightnow = popped[3]

        nodes_visited = nodes_visited + 1

        order_now = stack_rightnow[0]
        face_now = stack_rightnow[1]

        # goal test on pop, not on push (keeps A* optimal)
        reached_goal = True
        for i in range(0, num_books):
            if order_now[i] != i:
                reached_goal = False
            if face_now[i] != 1:
                reached_goal = False

        if reached_goal == True:
            # walk back through came_from to collect the flips
            rewind_list = []
            walker = stack_rightnow
            while came_from[walker] is not None:
                previous_state = came_from[walker][0]
                used_cut = came_from[walker][1]
                rewind_list.append(used_cut)
                walker = previous_state

            # rewind_list is backwards -> copy it from the end
            i = len(rewind_list) - 1
            while i >= 0:
                flip_sequence.append(rewind_list[i])
                i = i - 1

            return flip_sequence

        # try every flip, smallest cut first
        for cut_spot in range(1, num_books + 1):
            # do_one_flip: reverse the top cut_spot books and turn each one over
            new_order = []
            new_face = []

            i = cut_spot - 1
            while i >= 0:
                new_order.append(order_now[i])
                new_face.append(1 - face_now[i])
                i = i - 1

            # the rest stays the same
            i = cut_spot
            while i < num_books:
                new_order.append(order_now[i])
                new_face.append(face_now[i])
                i = i + 1

            after_flip = (tuple(new_order), tuple(new_face))
            new_steps = steps_taken + 1

            # only keep it if it's new or strictly cheaper
            should_add = False
            if after_flip not in best_count_at:
                should_add = True
            elif new_steps < best_count_at[after_flip]:
                should_add = True

            if should_add == True:
                best_count_at[after_flip] = new_steps
                came_from[after_flip] = (stack_rightnow, cut_spot)

                # count_bad_pairs again, same rule as above
                mess_count = 0
                for i in range(0, num_books - 1):
                    top_book = new_order[i]
                    below_book = new_order[i + 1]
                    top_face = new_face[i]
                    below_face = new_face[i + 1]

                    pair_is_good = False

                    if top_face == 1 and below_face == 1:
                        if below_book - top_book == 1:
                            pair_is_good = True
                    elif top_face == 0 and below_face == 0:
                        if top_book - below_book == 1:
                            pair_is_good = True

                    if pair_is_good == False:
                        mess_count = mess_count + 1
                new_h = mess_count

                # f = g + h
                new_f = new_steps + new_h

                arrival_order = arrival_order + 1
                heappush(waiting_line, (new_f, arrival_order, new_steps, after_flip))

    return flip_sequence
    # ---------------------------- #


def weighted_a_star_search(stack, epsilon=None, N=1):
    # Weighted A* is extra credit

    flip_sequence = []
    # --- v ADD YOUR CODE HERE v --- #
    # same as a_star_search, only the priority changes:
    #   f = g + push_factor * h
    #   push_factor = 1 + epsilon - epsilon * depth / N
    # big push_factor early (greedy), shrinks to 1 deeper in (plain A*)
    global nodes_visited
    nodes_visited = 0

    num_books = stack.num_books

    # lab says epsilon = 1 and N = 2m
    # default N=1 would make push_factor negative, so swap it for 2m
    if epsilon is None:
        epsilon = 1
    if N is None or N == 1:
        N = 2 * num_books

    start_order = []
    start_face = []
    for i in range(0, num_books):
        start_order.append(int(stack.order[i]))
        start_face.append(int(stack.orientations[i]))
    start_state = (tuple(start_order), tuple(start_face))

    # reached_goal: book i at spot i, all facing up
    reached_goal = True
    for i in range(0, num_books):
        if start_order[i] != i:
            reached_goal = False
        if start_face[i] != 1:
            reached_goal = False

    if reached_goal == True:
        return flip_sequence

    # count_bad_pairs: same heuristic as A*
    mess_count = 0
    for i in range(0, num_books - 1):
        top_book = start_order[i]
        below_book = start_order[i + 1]
        top_face = start_face[i]
        below_face = start_face[i + 1]

        pair_is_good = False

        if top_face == 1 and below_face == 1:
            if below_book - top_book == 1:
                pair_is_good = True
        elif top_face == 0 and below_face == 0:
            if top_book - below_book == 1:
                pair_is_good = True

        if pair_is_good == False:
            mess_count = mess_count + 1
    start_h = mess_count

    # push_factor at depth 0 -> 1 + epsilon
    push_factor = 1 + epsilon - (epsilon * 0 / N)
    if push_factor < 1:
        push_factor = 1
    start_f = 0 + push_factor * start_h

    waiting_line = []
    arrival_order = 0

    best_count_at = {}
    best_count_at[start_state] = 0

    came_from = {}
    came_from[start_state] = None

    heappush(waiting_line, (start_f, arrival_order, 0, start_state))

    while len(waiting_line) > 0:
        popped = heappop(waiting_line)
        steps_taken = popped[2]
        stack_rightnow = popped[3]

        nodes_visited = nodes_visited + 1

        order_now = stack_rightnow[0]
        face_now = stack_rightnow[1]

        # goal test on pop
        reached_goal = True
        for i in range(0, num_books):
            if order_now[i] != i:
                reached_goal = False
            if face_now[i] != 1:
                reached_goal = False

        if reached_goal == True:
            rewind_list = []
            walker = stack_rightnow
            while came_from[walker] is not None:
                previous_state = came_from[walker][0]
                used_cut = came_from[walker][1]
                rewind_list.append(used_cut)
                walker = previous_state

            i = len(rewind_list) - 1
            while i >= 0:
                flip_sequence.append(rewind_list[i])
                i = i - 1

            return flip_sequence

        for cut_spot in range(1, num_books + 1):
            # do_one_flip
            new_order = []
            new_face = []

            i = cut_spot - 1
            while i >= 0:
                new_order.append(order_now[i])
                new_face.append(1 - face_now[i])
                i = i - 1

            i = cut_spot
            while i < num_books:
                new_order.append(order_now[i])
                new_face.append(face_now[i])
                i = i + 1

            after_flip = (tuple(new_order), tuple(new_face))
            new_steps = steps_taken + 1

            # weighted h isn't consistent, so a state may come back cheaper
            # -> strictly cheaper path re-opens it
            should_add = False
            if after_flip not in best_count_at:
                should_add = True
            elif new_steps < best_count_at[after_flip]:
                should_add = True

            if should_add == True:
                best_count_at[after_flip] = new_steps
                came_from[after_flip] = (stack_rightnow, cut_spot)

                # count_bad_pairs again
                mess_count = 0
                for i in range(0, num_books - 1):
                    top_book = new_order[i]
                    below_book = new_order[i + 1]
                    top_face = new_face[i]
                    below_face = new_face[i + 1]

                    pair_is_good = False

                    if top_face == 1 and below_face == 1:
                        if below_book - top_book == 1:
                            pair_is_good = True
                    elif top_face == 0 and below_face == 0:
                        if top_book - below_book == 1:
                            pair_is_good = True

                    if pair_is_good == False:
                        mess_count = mess_count + 1
                new_h = mess_count

                # dynamic weight at this depth
                push_factor = 1 + epsilon - (epsilon * new_steps / N)
                # past depth N it would drop below 1 -> just stay plain A*
                if push_factor < 1:
                    push_factor = 1

                # f = g + push_factor * h
                new_f = new_steps + push_factor * new_h

                arrival_order = arrival_order + 1
                heappush(waiting_line, (new_f, arrival_order, new_steps, after_flip))

    return flip_sequence

    # ---------------------------- #


if __name__ == "__main__":
    test = TextbookStack(initial_order=[3, 2, 1, 0], initial_orientations=[0, 0, 0, 0])
    output_sequence = a_star_search(test)
    correct_sequence = int(output_sequence == [4])

    new_stack = apply_sequence(test, output_sequence)
    stack_ordered = new_stack.check_ordered()

    print(f"Stack is {'' if stack_ordered else 'not '}ordered")
    print(f"Comparing output to expected traces  - \t{'PASSED' if correct_sequence else 'FAILED'}")
