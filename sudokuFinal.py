board = [
  [5,3,0,0,7,0,0,0,0],
  [6,0,0,1,9,5,0,0,0],
  [0,9,8,0,0,0,0,6,0],
  #
  [8,0,0,0,6,0,0,0,3],
  [4,0,0,8,0,3,0,0,1],
  [7,0,0,0,2,0,0,0,6],
  #
  [0,6,0,0,0,0,2,8,0],
  [0,0,0,4,1,9,0,0,5],
  [0,0,0,0,8,0,0,7,9]
]

visited = []

def show():
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

# pick empty square
def pick():
  for i in range(0,9):
    for j in range(0,9):
      position = [i,j]
      if board[i][j] == 0 and position not in visited :
        position = [i,j]
        visited.append(position)
        return position
  return None

# try all numbers
def tryNum(i,j):
  currentNum = board[i][j]
  if currentNum != 9:
    for num in range(currentNum+1,10):
      if checkNum(i,j,num) :
        board[i][j] = num
        return True    
  board[i][j] = 0
  if board[i][j] == 0:
    backtrack(i,j)

def backtrack(i,j):
  index = visited.index([i,j])
  visited.pop(index)
  tryNum(visited[index-1][0],visited[index-1][1])


def giveRange(k):
  if k%3 == 0:
    return range(k,k+3)
  if k%3 == 1:
    return range(k-1,k+2)
  if k%3 == 2:
    return range(k-2,k+1)

def checkNum(i,j,num):
  for k in range(0,9):
      if board[i][k] == num and k != j or board[k][j] == num and k != i :
        return False
  irange = giveRange(i)
  jrange = giveRange(j)
  for l in irange:
    if l != i:
      for m in jrange:
        if m != j:
          if board[l][m] == num:
            return False     
  else:
    return True


def main():
  picked = pick()
  while picked != None:
    tryNum(picked[0],picked[1])
    picked = pick()

main()
show()
     
