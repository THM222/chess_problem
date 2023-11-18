import argparse
from enum import Enum
from pprint import pprint
import copy


class PieceType(Enum):
  QUEEN = 1
  ROOK = 2
  BISHOP = 3 
  KING = 4
  KNIGHT = 5


EMPTY = ' '


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--width", "-w", help="width of the board", type=int)
  parser.add_argument("--length", "-l", help="length of the board", type=int)
  parser.add_argument("--kings", "-k", help="number of kings", type=maximum_2, default=0)
  parser.add_argument("--queens", "-q", help="number of queens", type=maximum_2, default=0)
  parser.add_argument("--rooks", "-r", help="number of rooks", type=maximum_4, default=0)
  parser.add_argument("--bishops", "-b", help="number of bishops", type=maximum_4, default=0)
  parser.add_argument("--knights", "-n", help="number of bishops", type=maximum_4, default=0)
  args = parser.parse_args()
  return args


def maximum_2(n):
  n_int = int(n)
  if n_int < 0 or n_int > 2:
    print("Value must be between 0 and 2")
    exit(1)
  return n_int


def maximum_4(n):
  n_int = int(n)
  if n_int < 0 or n_int > 4:
    print("Value must be between 0 and 4")
    exit(1)
  return n_int


def contains_piece(board, row, col):
  try:
    if board[row][col] and board[row][col] != EMPTY:
      return True
  except:
    print(f"failed for row {row}, col {col}")
    pprint(board)
    raise
  return False


def is_empty_row(board, row_num):
  for i in range(len(board[row_num])):
    if board[row_num][i] and board[row_num][i] != EMPTY:
      return False
  return True 


def is_empty_column(board, col_num):
  for i in range(len(board)):
    if board[i][col_num] and board[i][col_num] != EMPTY:
      return False
  return True


def empty_row(board, row_num):
  for i in range(len(board[row_num])):
    board[row_num][i] = EMPTY


def empty_column(board, col_num):
  for i in range(len(board)):
    board[i][col_num] = EMPTY


def is_empty_diagonals(board, row, col):
  max_cols = len(board[0])
  max_rows = len(board)
  for n in range(-max_rows, max_rows):
    if (row+n >= 0 and col+n >= 0 and row+n < max_rows and col+n < max_cols):
      if contains_piece(board, row+n, col+n):
        return False

    if (row+n >= 0 and col-n >= 0 and row+n < max_rows and col-n < max_cols):
      if contains_piece(board, row+n, col-n):
        return False

  for n in range(-max_cols, max_cols):
    if (row+n >= 0 and col+n >= 0 and row+n < max_rows and col+n < max_cols):
      if contains_piece(board, row+n, col+n):
        return False

    if (row-n >= 0 and col+n >= 0 and row-n < max_rows and col+n < max_cols):
      if contains_piece(board, row-n, col+n):
        return False

  return True


def empty_diagonals(board, row, col):
  max_cols = len(board[0])
  max_rows = len(board)
  for n in range(-max_rows, max_rows):
    if (row+n >= 0 and col+n >= 0 and row+n < max_rows and col+n < max_cols):
      board[row+n][col+n] = EMPTY

    if (row+n >= 0 and col-n >= 0 and row+n < max_rows and col-n < max_cols):
      board[row+n][col-n] = EMPTY


  for n in range(-max_cols, max_cols):
    if (row+n >= 0 and col+n >= 0 and row+n < max_rows and col+n < max_cols):
      board[row+n][col+n] = EMPTY

    if (row-n >= 0 and col+n >= 0 and row-n < max_rows and col+n < max_cols):
      board[row-n][col+n] = EMPTY


def place_bishop(i, j, max_i, max_j, board):
  if board[i][j]:
    return False

  if not is_empty_diagonals(board, i, j):
    return False

  empty_diagonals(board, i, j)
  board[i][j] = 'B'

  return True


def place_queen(i, j, max_i, max_j, board):
  if (
    board[i][j]
    or not is_empty_row(board, i)
    or not is_empty_column(board, j)
    or not is_empty_diagonals(board, i, j)
  ):
    return False

  empty_row(board, i)
  empty_column(board, j)
  empty_diagonals(board, i, j)
  board[i][j] = 'Q'

  return True


def place_knight(i, j, max_i, max_j, board):
  if (
    board[i][j]
    or (i+2 < max_i and j+1 < max_j and contains_piece(board, i+2, j+1))
    or (i-2 >= 0    and j+1 < max_j and contains_piece(board, i-2, j+1))
    or (i+2 < max_i and j-1 >= 0    and contains_piece(board, i+2, j-1))
    or (i-2 >= 0    and j-1 >= 0    and contains_piece(board, i-2, j-1))
    or (i+1 < max_i and j+2 < max_j and contains_piece(board, i+1, j+2))
    or (i-1 >= 0    and j+2 < max_j and contains_piece(board, i-1, j+2))
    or (i+1 < max_i and j-2 >= 0    and contains_piece(board, i+1, j-2))
    or (i-1 >= 0    and j-2 >= 0    and contains_piece(board, i-1, j-2))
  ):
    return False

  if i+2 < max_i and j+1 < max_j:
    board[i+2][j+1] = EMPTY
  if i-2 >= 0    and j+1 < max_j:
    board[i-2][j+1] = EMPTY
  
  if i+2 < max_i and j-1 >= 0   :
    board[i+2][j-1] = EMPTY
  if i-2 >= 0    and j-1 >= 0   :
    board[i-2][j-1] = EMPTY
  
  if i+1 < max_i and j+2 < max_j:
    board[i+1][j+2] = EMPTY
  if i-1 >= 0    and j+2 < max_j:
    board[i-1][j+2] = EMPTY
  
  if i+1 < max_i and j-2 >= 0   :
    board[i+1][j-2] = EMPTY
  if i-1 >= 0    and j-2 >= 0   :
    board[i-1][j-2] = EMPTY
  
  board[i][j] = 'N'
  return True


def place_rook(i, j, board):
  if (
    board[i][j]
    or not is_empty_row(board, i)
    or not is_empty_column(board, j)
  ):
    return False

  empty_row(board, i)
  empty_column(board, j)
  board[i][j] = 'R'
  return True


def place_king(i, j, max_i, max_j, board):
  if (
    board[i][j]
    or (i+1 < max_i and contains_piece(board, i+1, j))
    or (i-1 >= 0    and contains_piece(board, i-1, j))
    or (j+1 < max_j and contains_piece(board, i, j+1))
    or (j-1 >= 0    and contains_piece(board, i, j-1))
    or (i+1 < max_i and j+1 < max_j and contains_piece(board, i+1, j+1))
    or (i-1 >= 0    and j+1 < max_j and contains_piece(board, i-1, j+1))
    or (i+1 < max_i and j-1 >= 0    and contains_piece(board, i+1, j-1))
    or (i-1 >= 0    and j-1 >= 0    and contains_piece(board, i-1, j-1))
  ):
    return False
  
  if i+1 < max_i:
    board[i+1][j] = EMPTY
  if i-1 >= 0:
    board[i-1][j] = EMPTY
  
  if j+1 < max_j:
    board[i][j+1] = EMPTY
  if j-1 >= 0:
    board[i][j-1] = EMPTY

  if i+1 < max_i and j+1 < max_j:
    board[i+1][j+1] = EMPTY
  if i-1 >= 0    and j+1 < max_j:
    board[i-1][j+1] = EMPTY
  
  if i+1 < max_i and j-1 >= 0:
    board[i+1][j-1] = EMPTY
  if i-1 >= 0    and j-1 >= 0:
    board[i-1][j-1] = EMPTY
  
  board[i][j] = 'K'
  return True


def place_piece_at(x, y, width, length, board, piece_type):
  match piece_type:
    case PieceType.ROOK:
      return place_rook(x, y, board)
    case PieceType.KING:
      return place_king(x, y, width, length, board)
    case PieceType.KNIGHT:
      return place_knight(x, y, width, length, board)
    case PieceType.BISHOP:
      return place_bishop(x, y, width, length, board)
    case PieceType.QUEEN:
      return place_queen(x, y, width, length, board)
    case _:
      return True


def place(board, piece, width, length, free_spaces):
  new_boards = []
  for x in range(width):
    for y in range(length):
      new_board = copy.deepcopy(board)
      valid = place_piece_at(x, y, width, length, new_board, piece)
      if valid:
        new_boards.append(new_board)

  return new_boards


def place_all(pieces, rows, columns):
  free_spaces = rows * columns
  empty_board = [ [ None ]*columns for i in range(rows)]
  valid_boards = [ empty_board ]

  for piece in pieces:
    valid_boards_after_adding_piece = []
    for board in valid_boards:
      updated_boards = place(board, piece, rows, columns, free_spaces)
      valid_boards_after_adding_piece += updated_boards
    valid_boards = copy.deepcopy(valid_boards_after_adding_piece)
    free_spaces -= 1

  return valid_boards


def solve(rows, columns, num_kings, num_queens, num_bishops, num_rooks, num_knights):
  pieces = []
  pieces += [ PieceType.KING for _ in range(num_kings) ]
  pieces += [ PieceType.ROOK for _ in range(num_rooks) ]
  pieces += [ PieceType.BISHOP for _ in range(num_bishops) ]
  pieces += [ PieceType.QUEEN for _ in range(num_queens) ]
  pieces += [ PieceType.KNIGHT for _ in range(num_knights) ]

  all_boards = place_all(pieces, rows, columns)
  all_unique_boards = {str(x).replace("None", "' '") for x in all_boards}

  pprint(all_unique_boards)
  print(len(all_unique_boards))


if __name__ == '__main__':
  args = parse_args()

  columns, rows = args.width, args.length
  num_kings = args.kings
  num_queens = args.queens
  num_rooks = args.rooks
  num_bishops = args.bishops
  num_knights = args.knights

  if (num_kings+num_queens+num_bishops+num_rooks+num_knights) >= columns*rows:
    print("No valid solutions because number of pieces is greater than or equal to the size of the board")
    exit(1)

  solve(rows, columns, num_kings, num_queens, num_bishops, num_rooks, num_knights)



