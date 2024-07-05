import copy

# Reference
# https://norvig.com/sudoku.html

EXAMPLE_PUZZLE = """
400000805
030000000
000700000
020000060
000080400
000010000
000603070
500200000
104000000"""

EASY_PUZZLE = '100200300400500600700800900000000000000000000000000000000000000000000000000000000'

GRID_SIZE = 9
BOX_SIZE = 3

class Solver():

    def __init__(this):
        pass

    def display(this, puzzle):
        row = 0
        while row < GRID_SIZE:
            col = 0
            while col < GRID_SIZE:
                char = str(puzzle[row * GRID_SIZE + col])
                if char == "0":
                    char = " "
                print(char + " ", end="")
                if (col + 1) % BOX_SIZE == 0 and col != GRID_SIZE - 1:
                    print("|", end="")
                col += 1
            print("")
            if (row + 1) % BOX_SIZE == 0 and row != GRID_SIZE - 1:
                print("------+------+------")
            row += 1

    def puzzle_from_string(s):
        s = s.replace("\n", "")
        puzzle = [int(s[i]) for i in range(GRID_SIZE * GRID_SIZE)]
        return puzzle


    def get_neighbors(this, number):
        assert(0 <= number < GRID_SIZE * GRID_SIZE)
        row = number // GRID_SIZE
        col = number % GRID_SIZE
        boxcol = col // BOX_SIZE
        boxrow = row // BOX_SIZE
        neighbors = {row * GRID_SIZE + i for i in range(GRID_SIZE)}
        neighbors.update([col + GRID_SIZE * i for i in range(GRID_SIZE)])
        for j in range(BOX_SIZE):
            for i in range(BOX_SIZE):
                neighbors.add(i * GRID_SIZE + j + boxcol * BOX_SIZE + boxrow * BOX_SIZE * GRID_SIZE)
        neighbors.discard(number)
        return neighbors

    def solve_recursive(this, sorted_poss, depth=0):

        sorted_poss = {k: v for k, v in sorted(sorted_poss.items(), key=lambda item: len(item[1]))}

        for k in sorted_poss:
            v = sorted_poss[k]
            if len(v) == 0:
                #print("that broke the puzzle...")
                return -1
            if len(v) == 1:
                digit = v[0]
                neighbors = this.get_neighbors(k)
                for n in neighbors:
                    if digit in sorted_poss[n]:
                        sorted_poss[n].remove(digit)
                        if len(sorted_poss[n]) < 1:
                            return -1
        
        sorted_poss = {k: v for k, v in sorted(sorted_poss.items(), key=lambda item: len(item[1]))}

        for k in sorted_poss:
            v = sorted_poss[k]
            if len(v) > 1:
                f = 0
                while f < len(v):
                    fix = copy.deepcopy(sorted_poss)
                    digit = sorted_poss[k][f]
                    fix[k] = [digit]
                    #print(" " * depth + "putting " + str(digit) + " in position " + str(k))
                    solution = this.solve_recursive(fix, depth + 1)
                    if solution != -1:
                        return solution
                    f+= 1
                return -1

        # No bifurcations. puzzle is solved.
        print("Found a solution!")
        return sorted_poss
    

    def solve(this, puzzle):
        # Prepare possibilities
        possibilities = [[0] for i in range(GRID_SIZE * GRID_SIZE)]
        for i in range(GRID_SIZE * GRID_SIZE):
            if puzzle[i] == 0:
                possibilities[i] = [i+1 for i in range(GRID_SIZE)]
            else:
                possibilities[i] = [puzzle[i]]
        poss_dict = {i: possibilities[i] for i in range(len(possibilities))}
        sorted_poss = {k: v for k, v in sorted(poss_dict.items(), key=lambda item: len(item[1]))}
        solved_poss = this.solve_recursive(sorted_poss)

        solved = [solved_poss[i][0] for i in range(GRID_SIZE * GRID_SIZE)]
        return solved


solver = Solver()

result = input("Paste in a sudoku puzzle (or leave blank for default):\n")
puzzle_string = result if result != "" else EXAMPLE_PUZZLE
puzzle = Solver.puzzle_from_string(puzzle_string)
solver.display(puzzle)
solved_puzzle = solver.solve(puzzle)
solver.display(solved_puzzle)
