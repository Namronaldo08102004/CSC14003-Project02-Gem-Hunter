def flatten(pos: tuple[int, int], n: int) -> int:
    """
    Convert to 1D index count from 1 (cannot use 0 in pysat-CNF)
    Args:
        pos (tuple[int, int]): location
        n (int): the width of the map

    Returns:
        int: 1D index
    """
    return (pos[0]) * n + pos[1] + 1


def unflatten(pos: int, n: int) -> tuple[int, int]:
    """
    Convert 1D index back to 2D index
    """
    return (pos - 1) // n, (pos - 1) % n


class Board:
    def __init__(self, file_name: str = None, folder: str = None):
        self.board = []
        self.assign = set()
        self.unassign = set()
        self.rows, self.cols = 0, 0
        if file_name is not None:
            self.load_map(file_name, folder)

    def load_map(self, file_name: str = None, folder: str = None):
        """
        Load the map from a file
        Args:
            file_name (str, optional). Defaults to None.
            folder (str, optional): Sub-folder. Defaults to None.

        Returns:
            list[list[str]]: the board
        """
        if file_name is None:
            file_name = "map.txt"
        if folder is not None:
            file_name = folder + "/" + file_name
        self.file_name = file_name

        with open(file_name, "r") as file:
            for line in file:
                cur = line.split(", ")
                self.board.append([x.strip() for x in cur])
        self.rows, self.cols = len(self.board), len(self.board[0])
        self.get_assigned_unassigned()

    def get_assigned_unassigned(self):
        """
        Get assigned and unassigned cells
        """
        self.assign = set()
        self.unassign = set()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != "_":
                    self.assign.add((i, j))
                else:
                    self.unassign.add((i, j))

    def get_neighbors(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Find all the neighbors of a cell that is unassigned
        Args:
            pos (tuple[int, int]): location

        Returns:
            list[tuple[int, int]]: neighbors that are not assigned
        """
        x, y = pos
        neighbors = []
        move = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dx, dy in move:
            if (x + dx, y + dy) in self.unassign:
                neighbors.append((x + dx, y + dy))
        return neighbors

    def load_solution(self, model: list[int]):
        """
        Load the solution from the model
        Args:
            model (list[int]): the model
        """
        for i in model:
            if i > 0:
                x, y = unflatten(i, self.cols)
                self.board[x][y] = "T"
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == "_":
                    self.board[i][j] = "G"
    def export_solution(self, file_name: str = None):
        if not file_name:
            file_name = self.file_name[:-4] + "_solution.txt"
        with open(file_name, "w") as file:
            for row in self.board:
                file.write(", ".join(row) + "\n")
        
    def display(self, msg: str = None):
        """
        Print the maps
        """
        if msg is not None:
            print(msg)

        top_border = bytes(
            [218] + ([196] * 3 + [194]) * (self.cols - 1) + [196] * 3 + [191]
        ).decode("cp437")
        middle_border = bytes(
            [195] + ([196] * 3 + [197]) * (self.cols - 1) + [196] * 3 + [180]
        ).decode("cp437")
        bottom_border = bytes(
            [192] + ([196] * 3 + [193]) * (self.cols - 1) + [196] * 3 + [217]
        ).decode("cp437")
        divider = bytes([179]).decode("cp437")

        print(top_border)
        for i in range(self.rows):
            print(divider, end="")
            for j in range(self.cols):
                print(f" {self.board[i][j]} ", end=divider)
            print()
            if i < self.rows - 1:
                print(middle_border)
        print(bottom_border)
