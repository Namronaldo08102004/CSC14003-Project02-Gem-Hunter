def get_assigned_unassigned(board: list[list[str]]):
    """
    Go through the map and find the assigned and unassigned cells
    Args:
        board (list[list[str]]): the map

    Returns:
        assign (dict[tuple[int, int], str]): assigned cells, location - value, the value isn't convert to int yet
        unassign (set[tuple[int, int]]): locations of unassigned cells
    """
    assign: dict[tuple[int, int], str] = {}
    unassign: set[tuple[int, int]] = set()

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != "_":
                assign[(i, j)] = board[i][j]
            else:
                unassign.add((i, j))
    
    return assign, unassign

def flatten(pos: tuple[int, int], n: int) -> int:
    """
    Convert to 1D index count from 1 (cannot use 0 in pysat-CNF)
    Args:
        pos (tuple[int, int]): location
        n (int): the width of the map

    Returns:
        int: 1D index
    """
    return (pos[0]) * n + pos[1] +1
def unflatten(pos: int, n: int) -> tuple[int, int]:
    """
    Convert 1D index back to 2D index
    """
    return (pos - 1) // n, (pos - 1) % n

def get_neighbors(pos: tuple[int, int], unassign: set[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Find all the neighbors of a cell that is unassigned
    Args:
        pos (tuple[int, int]): location
        unassign (set[tuple[int, int]]): locations of unassigned cells

    Returns:
        list[tuple[int, int]]: neighbors that are not assigned
    """
    x, y = pos
    neighbors = []
    move = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    for dx, dy in move:
        if (x + dx, y + dy) in unassign:
            neighbors.append((x + dx, y + dy))
    
    return neighbors
