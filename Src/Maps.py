def LoadMap(file_name: str = None, folder: str = None) -> list[list[str]]:
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

    board = []
    with open(file_name, "r") as file:
        for line in file:
            cur = line.split(", ")
            board.append([x.strip() for x in cur])

    return board


def display(board: list[list[str]], msg: str = None):
    """
    Print the maps
    """
    if msg is not None:
        print(msg)
    r, c = len(board), len(board[0])
    top_border = bytes(
        [218] + ([196] * 3 + [194]) * (c - 1) + [196] * 3 + [191]
    ).decode("cp437")
    middle_border = bytes(
        [195] + ([196] * 3 + [197]) * (c - 1) + [196] * 3 + [180]
    ).decode("cp437")
    bottom_border = bytes(
        [192] + ([196] * 3 + [193]) * (c - 1) + [196] * 3 + [217]
    ).decode("cp437")
    divider = bytes([179]).decode("cp437")

    print(top_border)
    for i in range(r):
        print(divider, end="")
        for j in range(c):
            print(f" {board[i][j]} ", end=divider)
        print()
        if i < r - 1:
            print(middle_border)
    print(bottom_border)
