PIECE_INFO = {
  "I": {
    "color": "#00FFFF",
    "rotations": [
      [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
      ],
      [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0]
      ],
      [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0]
      ],
      [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 0, 0]
      ]
    ],
    "kick_index": 1
  },
  "O": {
    "color": "#FFFF00",
    "rotations": [
      [
        [1, 1],
        [1, 1]
      ],
      [
        [1, 1],
        [1, 1]
      ],
      [
        [1, 1],
        [1, 1]
      ],
      [
        [1, 1],
        [1, 1]
      ]
    ],
    "kick_index": 2
  },
  "T": {
    "color": "#800080",
    "rotations": [
      [
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
      ],
      [
        [0, 1, 0],
        [0, 1, 1],
        [0, 1, 0]
      ],
      [
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0]
      ],
      [
        [0, 1, 0],
        [1, 1, 0],
        [0, 1, 0]
      ]
    ],
    "kick_index": 0
  },
  "S": {
    "color": "#00FF00",
    "rotations": [
      [
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
      ],
      [
        [0, 1, 0],
        [0, 1, 1],
        [0, 0, 1]
      ],
      [
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 0]
      ],
      [
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0]
      ]
    ],
    "kick_index": 0
  },
  "Z": {
    "color": "#FF0000",
    "rotations": [
      [
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
      ],
      [
        [0, 0, 1],
        [0, 1, 1],
        [0, 1, 0]
      ],
      [
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 1]
      ],
      [
        [0, 1, 0],
        [1, 1, 0],
        [1, 0, 0]
      ]
    ],
    "kick_index": 0
  },
  "L": {
    "color": "#FF7F00",
    "rotations": [
      [
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
      ],
      [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
      ],
      [
        [0, 0, 0],
        [1, 1, 1],
        [1, 0, 0]
      ],
      [
        [1, 1, 0],
        [0, 1, 0],
        [0, 1, 0]
      ]
    ],
    "kick_index": 0
  },
  "J": {
    "color": "#0000FF",
    "rotations": [
      [
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
      ],
      [
        [0, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
      ],
      [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 1]
      ],
      [
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]
      ]
    ],
    "kick_index": 0
  }
}

KICK_TABLE = [
  [
    [
      [[0, 0]],
      [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
      [[0, 0], [0, 1], [1, 1], [-1, 1], [1, 0], [-1, 0]],
      [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]
    ],
    [
      [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
      [[0, 0]],
      [[0, 0], [1, 0], [1, -1], [0, 2], [1, 2]],
      [[0, 0], [1, 0], [1, 2], [1, 1], [0, 2], [0, 1]]
    ],
    [
      [[0, 0], [0, -1], [-1, -1], [1, -1], [-1, 0], [1, 0]],
      [[0, 0], [-1, 0], [-1, 1], [0, -2], [-1, -2]],
      [[0, 0]],
      [[0, 0], [1, 0], [1, 1], [0, -2], [1, -2]]
    ],
    [
      [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
      [[0, 0], [-1, 0], [-1, 2], [-1, 1], [0, 2], [0, 1]],
      [[0, 0], [-1, 0], [-1, -1], [0, 2], [-1, 2]],
      [[0, 0]]
    ]
  ],
  [
    [
      [[0, 0]],
      [[0, 0], [1, 0], [-2, 0], [-2, -1], [1, 2]],
      [[0, 0], [0, 1], [1, 1], [-1, 1], [1, 0], [-1, 0]],
      [[0, 0], [-1, 0], [2, 0], [2, -1], [-1, 2]]
    ],
    [
      [[0, 0], [-1, 0], [2, 0], [-1, -2], [2, 1]],
      [[0, 0]],
      [[0, 0], [-1, 0], [2, 0], [-1, 2], [2, -1]],
      [[0, 0], [1, 0], [1, 2], [1, 1], [0, 2], [0, 1]]
    ],
    [
      [[0, 0], [0, -1], [-1, -1], [1, -1], [-1, 0], [1, 0]],
      [[0, 0], [-2, 0], [1, 0], [-2, 1], [1, -2]],
      [[0, 0]],
      [[0, 0], [2, 0], [-1, 0], [2, 1], [-1, -2]]
    ],
    [
      [[0, 0], [1, 0], [-2, 0], [1, -2], [-2, 1]],
      [[0, 0], [-1, 0], [-1, 2], [-1, 1], [0, 2], [0, 1]],
      [[0, 0], [1, 0], [-2, 0], [1, 2], [-2, -1]],
      [[0, 0]]
    ]
  ],
  [
    [
      [[0, 0]],
      [[0, 0]],
      [[0, 0]],
      [[0, 0]]
    ],
    [
      [[0, 0]],
      [[0, 0]],
      [[0, 0]],
      [[0, 0]]
    ],
    [
      [[0, 0]],
      [[0, 0]],
      [[0, 0]],
      [[0, 0]]
    ],
    [
      [[0, 0]],
      [[0, 0]],
      [[0, 0]],
      [[0, 0]]
    ]
  ]
]

# board = [["N"] * 10 for _ in range(40)]


def boardToString(board):
  boardStr = ""

  for row in board:
    boardStr += "".join(row)
    boardStr += "\n"

  return boardStr

# print(boardToString())

import numpy as np
def isValid(board, piece, px, py, r):
  rMatrix = PIECE_INFO[piece]["rotations"][r]
  # print(board)
  # print('x',len(rMatrix))
 
  for dy in range(len(rMatrix)):
    # print('y', len(rMatrix[dy]))
    for dx in range(len(rMatrix[dy])):
      x = px + dx
      y = py + dy
      # print('x', x, 'y', y)
      if rMatrix[dy][dx] == 1 and (x < 0 or x >= 10 or y < 0 or y >= 40 or board[y][x] != "N"):
        return False
  
  return True

def getRotationResult(board, piece, px, py, r, rot):
  newR = r + rot
  while newR < 0: newR += 4
  while newR >= 4: newR -= 4
  kicks = KICK_TABLE[PIECE_INFO[piece]["kick_index"]][r][newR]

  for dx, dy in kicks:
    if isValid(board, piece, px+dx, py-dy, newR): # dy in kick table is pos for up, but needs to be reversed cus top board row is index 0
      return (px+dx, py-dy, newR, True)
  
  return (px, py, r, False)

# returns if a board is valid or not
def isTerminal(board, piece, px, py, r):
  return not isValid(board, piece, px, py+1, r)

# if type= False, board is a (40,10) of int and piece is a char. If type = True, board is a (400,) numpy array and piece is an int
def getAllBoardStates(board, piece, TYPE):
  if TYPE:
    inv_vocab = {0:"N", 1:"G", 2:"I", 3:"O", 4:"T", 5:"S", 6:"Z", 7:"J", 8:"L"}
    board = mod_board_matrix_to_helper(board)
    piece = inv_vocab[piece]
  stack = [(3 if piece != "O" else 4, 0, 0)]
  terminal_states = set()
  seen = set()
  moves = [(1, 0), (-1, 0), (0, 1)] # (0, 1) is move down, since top row is index 0
  rotations = [1, -1, 2]

  while stack:
    curr = stack.pop()

    if curr in seen:
      continue

    seen.add(curr)
    px, py, r = curr

    if isTerminal(board, piece, px, py, r):
      terminal_states.add(curr)
    
    for dx, dy in moves:
      if isValid(board, piece, px + dx, py + dy, r):
        stack += [(px + dx, py + dy, r)]
    
    for rot in rotations:
      newX, newY, newR, valid = getRotationResult(board, piece, px, py, r, rot)

      if valid:
        stack += [(newX, newY, newR)]
  # print('len seen', len(seen))
  # print('terminal states', terminal_states)
  # print('len terminal states', len(terminal_states))
  return terminal_states


def clearLines(board):
    # board is list of rows, index 0 = bottom
    new_board = [row for row in board if any(cell == "N" for cell in row)]
    
    # add empty rows at the BOTTOM (index 0) to replace cleared lines
    cleared = 40 - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, ["N"] * 10)
    
    return new_board

def getBoardString(board, piece, px, py, r):
    board_copy = [row[:] for row in board]
    
    rMatrix = PIECE_INFO[piece]["rotations"][r]

    for dy in range(len(rMatrix)):
        for dx in range(len(rMatrix[dy])):
            if rMatrix[dy][dx] == 1:
                x = px + dx
                y = py + dy
                board_copy[y][x] = piece
    
    board_copy = clearLines(board_copy)  # apply line clears after placement
    
    boardStr = ""
    for row in board_copy:
        boardStr = "".join(row) + boardStr
    
    return boardStr

def getBoardMatrix(boardStr):
  boardArr = []

  for r in range(40):
    row = []

    for c in range(10):
      i = 10 * r + c
      row += [boardStr[i]]
    
    boardArr.insert(0, row)
  
  return boardArr

def mod_board_matrix_to_helper(board_matrix):
    inv_vocab = {0:"N", 1:"G", 2:"I", 3:"O", 4:"T", 5:"S", 6:"Z", 7:"J", 8:"L"}
    # print(board_matrix)
    thing= board_matrix.reshape(40, 10).tolist()
    thing2=[[inv_vocab[cell] for cell in row] for row in thing]
    return thing2[::-1]

# gets the numpy array for a board
def getBoardArray(board, piece, px, py, r):
    vocab = {"N":0,"G":1,"I":2,"O":3,"T":4,"S":5,"Z":6,"J":7,"L":8}
    board_str = getBoardString(board, piece, px, py, r)
    return np.array([vocab[c] for c in board_str], dtype=np.int32)

# returns all numpy arrays for a set of states



init_board = getBoardMatrix("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
init_piece = "I"
# print(isValid(init_board, init_piece, 7, 37, 1))
# print(boardToString(init_board))
# states = getAllBoardStates(init_board, init_piece, False)
# print(states)
# boardStrings = []


# for px, py, r in states:
#   boardStrings += [getBoardString(init_board, init_piece, px, py, r)]

# boardStrings = sorted(list(set(boardStrings)))
# print(len(sorted(boardStrings)))
# for x in range(10):
#   print(boardStrings[x])

# import json

# with open("states.json", "w") as f:
#     json.dump(list(states), f)

# with open("boardStrings.json", "w") as f:
#     json.dump(boardStrings, f)


