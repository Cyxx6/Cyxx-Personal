# SUDOKU 

#!/usr/bin/env python3
import random
import copy
import sys
from typing import List, Tuple, Optional

Grid = List[List[int]]

# -----------------------------
# Core Sudoku engine
# -----------------------------
def find_empty(grid: Grid) -> Optional[Tuple[int, int]]:
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                return r, c
    return None

def is_valid(grid: Grid, r: int, c: int, val: int) -> bool:
    if any(grid[r][x] == val for x in range(9)):  # row
        return False
    if any(grid[x][c] == val for x in range(9)):  # col
        return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    for rr in range(br, br + 3):
        for cc in range(bc, bc + 3):
            if grid[rr][cc] == val:
                return False
    return True

def solve_backtrack(grid: Grid) -> bool:
    empty = find_empty(grid)
    if not empty:
        return True
    r, c = empty
    nums = list(range(1, 10))
    random.shuffle(nums)
    for n in nums:
        if is_valid(grid, r, c, n):
            grid[r][c] = n
            if solve_backtrack(grid):
                return True
            grid[r][c] = 0
    return False

def count_solutions(grid: Grid, cap: int = 2) -> int:
    count = 0
    def dfs(g: Grid):
        nonlocal count
        if count >= cap:
            return
        empty = find_empty(g)
        if not empty:
            count += 1
            return
        r, c = empty
        for n in range(1, 10):
            if is_valid(g, r, c, n):
                g[r][c] = n
                dfs(g)
                if count >= cap:
                    return
                g[r][c] = 0
    work = [row[:] for row in grid]
    dfs(work)
    return count

def generate_full_grid() -> Grid:
    grid = [[0] * 9 for _ in range(9)]
    def fill():
        empty = find_empty(grid)
        if not empty:
            return True
        r, c = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        for n in nums:
            if is_valid(grid, r, c, n):
                grid[r][c] = n
                if fill():
                    return True
                grid[r][c] = 0
        return False
    fill()
    return grid

def make_puzzle(difficulty: str = "normal") -> Tuple[Grid, Grid]:
    if difficulty == "easy":
        target_clues = random.randint(46, 55)
    elif difficulty == "hard":
        target_clues = random.randint(28, 35)
    else:
        target_clues = random.randint(36, 45)
    full = generate_full_grid()
    solution = [row[:] for row in full]
    puzzle = [row[:] for row in full]
    positions = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(positions)
    def clues_count(g: Grid) -> int:
        return sum(1 for r in range(9) for c in range(9) if g[r][c] != 0)
    for (r, c) in positions:
        if clues_count(puzzle) <= target_clues:
            break
        r2, c2 = 8 - r, 8 - c
        saved1, saved2 = puzzle[r][c], puzzle[r2][c2]
        if saved1 == 0 and saved2 == 0:
            continue
        puzzle[r][c] = 0
        puzzle[r2][c2] = 0
        if count_solutions(puzzle, cap=2) != 1:
            puzzle[r][c] = saved1
            puzzle[r2][c2] = saved2
    if count_solutions(puzzle, cap=2) != 1:
        return make_puzzle(difficulty)
    return puzzle, solution

# -----------------------------
# UI helpers
# -----------------------------
def print_board(grid: Grid, fixed_mask: List[List[bool]] = None):
    sep = "─" * 25
    print("    1 2 3   4 5 6   7 8 9")
    print("  ┌" + sep + "┐")
    for r in range(9):
        line = []
        for c in range(9):
            v = grid[r][c]
            cell = "." if v == 0 else str(v)
            line.append(cell)
        row_label = chr(ord('A') + r)
        row_str = " ".join(line[0:3]) + " │ " + " ".join(line[3:6]) + " │ " + " ".join(line[6:9])
        print(f"{row_label} │ {row_str} │")
        if r in (2, 5):
            print("  │ " + " ".join(["-"] * 7) + "   " + " ".join(["-"] * 7) + "   " + " ".join(["-"] * 7) + " │")
    print("  └" + sep + "┘")

def coords_from_user(token: str) -> Optional[Tuple[int, int]]:
    token = token.strip().upper()
    if len(token) != 2:
        return None
    row_char, col_char = token[0], token[1]
    if row_char < 'A' or row_char > 'I':
        return None
    if col_char < '1' or col_char > '9':
        return None
    r = ord(row_char) - ord('A')
    c = int(col_char) - 1
    return r, c

def parse_command(s: str):
    parts = s.strip().split()
    if not parts:
        return None, ()
    cmd = parts[0].lower()
    if cmd in ("quit", "exit"):
        return "quit", ()
    if cmd == "help":
        return "help", ()
    if cmd == "show":
        return "show", ()
    if cmd == "check":
        return "check", ()
    if cmd == "restart":
        return "restart", ()
    if cmd == "new":
        return "new", ()
    if cmd == "hint":
        return "hint", ()
    if cmd == "set" and len(parts) == 3:
        pos = coords_from_user(parts[1])
        if pos is None:
            return None, ()
        try:
            val = int(parts[2])
        except ValueError:
            return None, ()
        if not (1 <= val <= 9):
            return None, ()
        return "set", (pos[0], pos[1], val)
    if cmd == "clear" and len(parts) == 2:
        pos = coords_from_user(parts[1])
        if pos is None:
            return None, ()
        return "clear", (pos[0], pos[1])
    return None, ()

def board_equal(a: Grid, b: Grid) -> bool:
    for r in range(9):
        for c in range(9):
            if a[r][c] != b[r][c]:
                return False
    return True

def compute_fixed_mask(puzzle: Grid) -> List[List[bool]]:
    return [[puzzle[r][c] != 0 for c in range(9)] for r in range(9)]

def find_single_candidate(grid: Grid) -> Optional[Tuple[int, int, int]]:
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                candidates = [n for n in range(1, 10) if is_valid(grid, r, c, n)]
                if len(candidates) == 1:
                    return r, c, candidates[0]
    return None

# -----------------------------
# Game loop
# -----------------------------
def new_game(difficulty="normal") -> Tuple[Grid, Grid, Grid, List[List[bool]]]:
    puzzle, solution = make_puzzle(difficulty)
    current = [row[:] for row in puzzle]
    fixed = compute_fixed_mask(puzzle)
    return puzzle, solution, current, fixed

def print_help():
    print(
"""Commands:
  set <pos> <val>     e.g., set B5 7
  clear <pos>         e.g., clear H9
  hint                fill a safe single-candidate cell
  check               report any mistakes vs. Sudoku rules
  show                print board
  restart             reset to original puzzle
  new                 start a new normal puzzle
  quit / exit         leave
  help                show this help
Positions use A–I for rows and 1–9 for columns; '.' are empty cells.
"""
    )

def main():
    random.seed()
    difficulty = "normal"
    puzzle, solution, current, fixed = new_game(difficulty)
    print("\n=== Sudoku 9x9 — Normal Difficulty ===")
    print_help()
    print_board(current, fixed)

    while True:
        try:
            s = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        cmd, args = parse_command(s)
        if cmd is None:
            print("Unrecognized command. Type 'help'.")
            continue

        if cmd in ("quit", "exit"):
            print("Goodbye!")
            return

        if cmd == "help":
            print_help()

        elif cmd == "show":
            print_board(current, fixed)

        elif cmd == "restart":
            current = [row[:] for row in puzzle]
            print("Puzzle reset.")
            print_board(current, fixed)

        elif cmd == "new":
            puzzle, solution, current, fixed = new_game("normal")
            print("\nNew NORMAL puzzle:")
            print_board(current, fixed)

        elif cmd == "check":
            if all(current[r][c] != 0 for r in range(9) for c in range(9)):
                if board_equal(current, solution):
                    print("ALLAH BIGGEST")
                else:
                    print("Board is full, but not correct.")
            else:
                print("Board not yet complete.")

        elif cmd == "hint":
            sc = find_single_candidate(current)
            if sc:
                r, c, v = sc
                if not fixed[r][c]:
                    current[r][c] = v
                    print(f"Hint: {chr(ord('A')+r)}{c+1} → {v}")
                    print_board(current, fixed)
            else:
                empties = [(r, c) for r in range(9) for c in range(9) if current[r][c] == 0]
                if empties:
                    r, c = random.choice(empties)
                    current[r][c] = solution[r][c]
                    print(f"Revealed: {chr(ord('A')+r)}{c+1} → {solution[r][c]}")
                    print_board(current, fixed)

        elif cmd == "set":
            r, c, v = args
            if fixed[r][c]:
                print("That cell is fixed and cannot be changed.")
                continue
            if not is_valid(current, r, c, v):
                print("wrong input bitch")
                continue
            current[r][c] = v
            print_board(current, fixed)
            if all(current[r][c] != 0 for r in range(9) for c in range(9)) and board_equal(current, solution):
                print("ALLAH BIGGEST")

        elif cmd == "clear":
            r, c = args
            if fixed[r][c]:
                print("That cell is fixed and cannot be cleared.")
            else:
                current[r][c] = 0
                print_board(current, fixed)

if __name__ == "__main__":
    try:
        main()
    except RecursionError:
        print("Recursion error, try again.")
        sys.exit(1)
