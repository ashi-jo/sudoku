import pygame, sys
from pygame.locals import *
from sudokuFinal import BEmain
import time

pygame.init()

OGboard = [
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

OGs = []

workingBoard = [
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


WINDOWMULTIPLIER = 5
WINDOWSIZE = 81

windowWidth = WINDOWSIZE*WINDOWMULTIPLIER
windowHeight = WINDOWSIZE*WINDOWMULTIPLIER

SQUARESIZE = (WINDOWSIZE*WINDOWMULTIPLIER)/3
CELLSIZE = SQUARESIZE/3
NUMBERSIZE = CELLSIZE/3

FPS = 10

solvedBoard = BEmain()
wrong = 0
currentGrid = {}
solved = True

screen = pygame.display.set_mode((windowWidth,455))

WHITE = (255,255,255)
BLACK = (0,0,0)
LIGHTGRAY = (200,200,200)
BLUE = (0,0,255)
DARKGRAY = (105,105,105)
RED = (255,0,0)

BOLDFONT = pygame.font.Font('freesansbold.ttf', 15)
BIGFONT = pygame.font.Font('freesansbold.ttf', 30)
# FONT = pygame.font.Font('',15)



def drawGrid():
  #draw minor lines
  for x in range(0, windowWidth, int(CELLSIZE)):
    pygame.draw.line(screen,LIGHTGRAY,(x,0),(x,windowHeight))
  for y in range(0, windowHeight,int(CELLSIZE)):
    pygame.draw.line(screen,LIGHTGRAY,(0,y),(windowWidth,y))
  #draw major lines
  for x in range(0, windowWidth, int(SQUARESIZE)):
    pygame.draw.line(screen,BLACK,(x,0),(x,windowHeight))
  for y in range(0, windowHeight+int(SQUARESIZE),int(SQUARESIZE)):
    pygame.draw.line(screen,BLACK,(0,y),(windowWidth,y))

  return None


def drawBox(mouseX, mouseY):
  if not OgPosn(mouseX,mouseY):
    boxX = ((mouseX)//CELLSIZE)*(CELLSIZE)
    boxY = ((mouseY)//CELLSIZE)*(CELLSIZE)
    pygame.draw.rect(screen, BLUE, (boxX,boxY,CELLSIZE,CELLSIZE),2)

def drawNum(mouseX,mouseY,num,color):
  boxX = ((mouseX)//CELLSIZE)*(CELLSIZE) + CELLSIZE/2
  boxY = ((mouseY)//CELLSIZE)*(CELLSIZE) + CELLSIZE/2
  numm = BOLDFONT.render(num,False,color)
  screen.blit(numm,(boxX,boxY))

def displayBoard():
  for i in range(0,9):
    for j in range(0,9):
      if OGboard[i][j] != 0:
        OGs.append([i,j])
        drawNum(j*CELLSIZE,i*CELLSIZE,str(OGboard[i][j]),BLACK)

def OgPosn(mouseX,mouseY):
  j = int((mouseX)//CELLSIZE)
  i = int((mouseY)//CELLSIZE)
  if OGboard[i][j] != 0:
    return True
  return False

def valid(mouseX,mouseY,key):
  j = int((mouseX)//CELLSIZE)
  i = int((mouseY)//CELLSIZE)
  if solvedBoard[i][j] == key:
    return True
  return False

def updateBoard(mouseX,mouseY,key):
  if not OgPosn(mouseX,mouseY):
    j = int((mouseX)//CELLSIZE)
    i = int((mouseY)//CELLSIZE)
    if valid(mouseX,mouseY,key):
      workingBoard[i][j] = key
      currentGrid[j,i] = []
      checkNum(i,j,key)
      # print(currentGrid[i,j])
      # drawNum(mouseX,mouseY,str(key),DARKGRAY)
    else:
      global wrong
      wrong = wrong + 1
      currentGrid[j,i].remove(key)

def displayUpdatedBoard(time):
  for i in range(0,9):
    for j in range(0,9):
      if OGboard[i][j] == 0 and workingBoard[i][j] !=0 :
        drawNum(j*CELLSIZE,i*CELLSIZE,str(workingBoard[i][j]),DARKGRAY)
  numm = BOLDFONT.render('X '*wrong,False,RED)
  screen.blit(numm,(0,windowHeight + NUMBERSIZE))
  timeText = BOLDFONT.render('Time: {} '.format(format_time(time)),1,RED)
  screen.blit(timeText,(windowWidth-2*CELLSIZE,windowHeight+NUMBERSIZE))
  pygame.display.update()

def initiateCells():
  fullCell = []
  for xCoord in range(0,9):
    for yCoord in range(0,9):
      currentGrid[xCoord,yCoord] = list(fullCell)
  return currentGrid

def fillCell(mouseX,mouseY,key):
  xCoord = int((mouseX)//CELLSIZE)
  yCoord = int((mouseY)//CELLSIZE)
  currentGrid[xCoord,yCoord].append(key)
  # print(currentGrid[xCoord,yCoord])

def displayOptions():
  xFactor = 0
  yFactor = 0
  for item in currentGrid:
    cellData = currentGrid[item]
    if cellData != []:
      # print(cellData)
      for number in cellData:
        if number != '':
          xFactor = ((number-1)%3)
          if number <= 3:
            yFactor = 0
          elif number <= 6:
            yFactor = 1
          else :
            yFactor = 2
          numm = BOLDFONT.render(str(number),False,LIGHTGRAY)
          screen.blit(numm,((item[0]*CELLSIZE)+(xFactor*NUMBERSIZE+2),(item[1]*CELLSIZE)+(yFactor*NUMBERSIZE+2)))

def giveRange(k):
  if k%3 == 0:
    return range(k,k+3)
  if k%3 == 1:
    return range(k-1,k+2)
  if k%3 == 2:
    return range(k-2,k+1)

def checkNum(i,j,num):
  for k in range(0,9):
      if num in currentGrid[j,k] and k != i:
        currentGrid[j,k].remove(num)
      if num in currentGrid[k,i] and k != j :
        currentGrid[k,i].remove(num)
  irange = giveRange(i)
  jrange = giveRange(j)
  for l in jrange:
    if l != j:
      for m in irange:
        if m != i:
          if num in currentGrid[m,l]:
            currentGrid[m,l].remove(num)    
  else:
    return True

def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat

# def displayOptions():
#   for key,value in currentGrid.items():
#     for val in value:
#       if val == 1:
#         xCoord = key[0] 
#         yCoord = key[1] 
#       if val == 2:
#         xCoord = key[0] + int(NUMBERSIZE)
#         yCoord = key[1] 
#       if val == 3:
#         xCoord = key[0] + int(2*NUMBERSIZE)
#         yCoord = key[1] 
#       if val == 4:
#         xCoord = key[0] 
#         yCoord = key[1] + int(NUMBERSIZE)
#       if val == 5:
#         xCoord = key[0] + int(NUMBERSIZE)
#         yCoord = key[1] + int(NUMBERSIZE)
#       if val == 6:
#         xCoord = key[0] + int(2*NUMBERSIZE)
#         yCoord = key[1] + int(NUMBERSIZE)
#       if val == 7:
#         xCoord = key[0] 
#         yCoord = key[1] + int(2*NUMBERSIZE)
#       if val == 8:
#         xCoord = key[0] + int(NUMBERSIZE)
#         yCoord = key[1] + int(2*NUMBERSIZE)
#       if val == 9:
#         xCoord = key[0] + int(2*NUMBERSIZE)
#         yCoord = key[1] + int(2*NUMBERSIZE)
#       # print(xCoord)
#       # print(yCoord)
#       numm = BOLDFONT.render(str(val),False,LIGHTGRAY)
#       screen.blit(numm,(xCoord,yCoord))


def main():
  global FPSCLOCK, screen
  FPSCLOCK = pygame.time.Clock()
  pygame.display.set_caption('SUDOKU')
  start = time.time()

  print(solvedBoard)
  initiateCells()

  mouseClicked = False
  mouseX = 0
  mouseY = 0
  
  screen.fill(WHITE)
  drawGrid()
  displayBoard()
  # currentGrid = initiateCells()
  # displayCells(currentGrid)
  running = True
  key = 0

  while running:
    playTime = round(time.time()-start)
    for event in pygame.event.get():
      if event.type == QUIT:
        running = False
        pygame.quit()
        # sys.exit()
      #mouse movement commands
      elif event.type == MOUSEBUTTONUP:
        mouseX,mouseY = event.pos
        mouseClicked = True
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_KP_1:
          key = 1
          fillCell(mouseX,mouseY,key)
        if event.key == pygame.K_KP_2:
          key = 2
          fillCell(mouseX,mouseY,key)
        if event.key == pygame.K_KP_3:
          key = 3
          fillCell(mouseX,mouseY,key)
        if event.key == pygame.K_KP_4:
          key = 4
          fillCell(mouseX,mouseY,key)
        if event.key == pygame.K_KP_5:
          key = 5
          fillCell(mouseX,mouseY,key)
        if event.key == pygame.K_KP_6:
          key = 6
          fillCell(mouseX,mouseY,key)
        if event.key == pygame.K_KP_7:
          key = 7
          fillCell(mouseX,mouseY,key)
        if event.key == pygame.K_KP_8:
          key = 8
          fillCell(mouseX,mouseY,key)
        if event.key == pygame.K_KP_9:
          key = 9
          fillCell(mouseX,mouseY,key)
        if event.key == pygame.K_KP_ENTER:
          updateBoard(mouseX,mouseY,key)
          print("Enter pressed")
    if mouseClicked :
      # print(mouseX)
      # print(mouseY)
      drawBox(mouseX,mouseY)
      
      mouseClicked = False
      # unDrawBox(mouseX,mouseY)
    #repaint screen
    screen.fill(WHITE)
    drawGrid()
    displayBoard()
    drawBox(mouseX,mouseY)
    displayUpdatedBoard(playTime)
    displayOptions()

    if workingBoard == solvedBoard:
      screen.fill(BLACK)
      won = BIGFONT.render('SOLVED!',False,RED)
      screen.blit(won,(windowHeight/2-CELLSIZE-NUMBERSIZE,windowWidth/2-CELLSIZE))
      wrongs = BIGFONT.render('with {} wrong attempts'.format(wrong),False,WHITE)
      screen.blit(wrongs,(windowHeight/2-SQUARESIZE-2*NUMBERSIZE,windowWidth/2))
      global solved
      if solved:
        total = playTime
        solved = False
      totalTime = BIGFONT.render('in {} time'.format(format_time(total)),False,WHITE)
      screen.blit(totalTime,(windowHeight/2-2*NUMBERSIZE-CELLSIZE,windowWidth/2+CELLSIZE))

    # screen.fill(BLACK)
    # won = BIGFONT.render('SOLVED!',False,RED)
    # screen.blit(won,(windowHeight/2-CELLSIZE-NUMBERSIZE,windowWidth/2-CELLSIZE))
    # wrongs = BIGFONT.render('with {} wrong attempts'.format(wrong),False,WHITE)
    # screen.blit(wrongs,(windowHeight/2-SQUARESIZE-2*NUMBERSIZE,windowWidth/2))
    # global solved
    # if solved:
    #   total = playTime
    #   solved = False
    # totalTime = BIGFONT.render('in {} time'.format(format_time(total)),False,WHITE)
    # screen.blit(totalTime,(windowHeight/2-2*NUMBERSIZE-CELLSIZE,windowWidth/2+CELLSIZE))


  #     numm = BOLDFONT.render(num,False,color)
  # screen.blit(numm,(boxX,boxY))
    

    
  
    pygame.display.update()
    FPSCLOCK.tick(FPS)



if __name__ == '__main__':
  main()


