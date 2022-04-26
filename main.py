#Init
import pygame,random,math
pygame.init()
FPS = 30
SCREEN_WIDTH,SCREEN_HEIGHT = 600,600
BOARD_OFFSET_HORZ, BOARD_OFFSET_VERT = 100,100
TILE_SIZE = 100
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
GOAL_COLOUR,TILE_COLOUR = (255,233,0),(25,50,75)
score = 0
game_over = False


def update_board() -> None:
    #Update board
    screen.blit(background_surf,(0,0))
    for row in range(4):
        for col in range(4):
            Board.sprites()[xy_to_pos(col,row)].update_text(board[row][col])
    
    #Draw screen
    font = pygame.font.Font(None,30)
    score_surf = font.render('Score:' + str(score),True,(255,255,255))
    screen.blit(score_surf,(0,0))

def board_to_screen_pos(x,y) -> tuple:
    return (BOARD_OFFSET_HORZ + (x * TILE_SIZE),BOARD_OFFSET_HORZ + (y * TILE_SIZE))

def add_tile():
    global board

    #Choose 2 or 4
    num = random.randint(1,10)
    num = 4 if num == 1 else 2
    left = [i for i in range(16)]

    #Find empty spaces
    for row in range(4):
        for col in range(4):
            if board[row][col] != 0:
                left.pop(left.index(xy_to_pos(col,row)))

    #No emptey spaces
    if len(left) == 0:
        return None

    #pick pos and update
    pos = pos_to_xy(left[random.randint(0,len(left) - 1)])
    board[pos[1]][pos[0]] = num
    update_board()

def check_game_over() -> bool:
    for row in range(4):
        for col in range(4):

            #0 means we can move
            if board[row][col] == 0:
                return False

            num = board[row][col]
            lst = []

            #Check if ajacent squares are the same
            if not row == 0:
                lst.append(board[row - 1][col])
            if not row == 3:
                lst.append(board[row + 1][col])
            if not col == 0:
                lst.append(board[row][col - 1])
            if not col == 3:
                lst.append(board[row][col + 1])
            
            if num in lst:
                return False

    #All falses eleminated
    return True


def xy_to_pos(x:int,y:int) -> int:
    return x + (y * 4)

def pos_to_xy(pos:int) -> tuple:
    return (pos % 4, pos // 4)

def can_move(dir:str) -> bool:
    #Check if ajacent tiles are the same or 0
    if dir == 'u':
        for row in range(1,4):
            for col in range(4):
                if board[row][col] != 0 and board[row - 1][col] in [0,board[row][col]]:
                    return True

    if dir == 'd':
        for row in range(3):
            for col in range(4):
                if board[row][col] != 0 and board[row + 1][col] in [0,board[row][col]]:
                    return True
    
    if dir == 'l':
        for row in range(4):
            for col in range(1,4):
                if board[row][col] != 0 and board[row][col - 1] in [0,board[row][col]]:
                    return True

    if dir == 'r':
        for row in range(4):
            for col in range(3):
                if board[row][col] != 0 and board[row][col + 1] in [0,board[row][col]]:
                    return True

    return False

def move_board(dir:str) -> None:
    global board,score

    if not can_move(dir):
        return None

    cols_rows = []
    for Col in range(4):
        col = []
        if dir in ['u','d']:
            #Get cols and remove 0s
            for num in range(4):
                num = board[num][Col]
                if num != 0:
                    col.append(num)
        else:
            #Get rows and remove 0s
            for num in range(4):
                num = board[Col][num]
                if num != 0:
                    col.append(num)    
        
        #Ddd 0s back
        for i in range(4-len(col)):
            if dir in ['u','l']:
                col.append(0)
            else:
                col.insert(0,0)

        cols_rows.append(col)
    
    #Check for mergeing
    if dir in ['u','l']:
        for col_row in range(4):
            for num in range(3):
                if cols_rows[col_row][num] == cols_rows[col_row][num + 1]:
                        cols_rows[col_row][num] *= 2
                        score += cols_rows[col_row][num]
                        cols_rows[col_row][num+1] = 0
    else:
        for col_row in range(3,-1,-1):
            for num in range(3,0,-1):
                if cols_rows[col_row][num] == cols_rows[col_row][num - 1]:
                        cols_rows[col_row][num] *= 2
                        score += cols_rows[col_row][num]
                        cols_rows[col_row][num-1] = 0

    #Move merged tiles into place
    for row_col in range(3,-1,-1):
        for num in range(3,-1,-1):
            if cols_rows[row_col][num] == 0:
                cols_rows[row_col].pop(num)
        for i in range(4-len(cols_rows[row_col])):
            if dir in ['u','l']:
                cols_rows[row_col].append(0)
            else:
                cols_rows[row_col].insert(0,0)

    #Update board and add new tile
    board = []
    if dir in ['u','d']:
        for num in range(4):
            row = []
            for col in range(4):
                row.append(cols_rows[col][num])
            board.append(row)
    else:
        board = cols_rows

    update_board()
    add_tile()

            
class tile(pygame.sprite.Sprite):
    def __init__(self,x:int,y:int,num:int = 0) -> None:
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE,TILE_SIZE))
        self.image.fill((156,102,40))
        self.num = num
        self.x,self.y = x,y
        self.update_text(self.num)
        self.col = TILE_COLOUR
        pos = board_to_screen_pos(x,y)
        x,y = pos[0],pos[1]
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def update_text(self,num:int) -> None:
        self.num = num
        self.set_col()

        self.image.fill(self.col)
        if num != 0:
            col = (0,0,0) if self.num < 2048 else (255,255,255) 
            font = pygame.font.Font(None,25)
            text_surf = font.render(str(num),True,col)
            self.image.blit(text_surf,((TILE_SIZE // 2) - (text_surf.get_width() // 2),(TILE_SIZE // 2) - (text_surf.get_height() // 2)))
        self.set_col()
    
    def set_col(self) -> None:
        if self.num == 0:
            self.col = TILE_COLOUR
            return None
        
        if self.num > 2048:
            self.col = (0,0,0)
            return None

        #Get how much we can change each value
        r_max = GOAL_COLOUR[0] - TILE_COLOUR[0]
        g_max = GOAL_COLOUR[1] - TILE_COLOUR[1]
        b_max = GOAL_COLOUR[2] - TILE_COLOUR[2]
        
        #Get how manny merges the tile has done vs 2048
        precentege = math.log2(self.num) / math.log2(2048)
        #Change starting col to new col by reletave precenteges
        self.col = (r_max * precentege + TILE_COLOUR[0],g_max * precentege + TILE_COLOUR[1],b_max * precentege + TILE_COLOUR[2])
    
#Init board
Board = pygame.sprite.Group()
for row in range(4):
    for col in range(4):
        Board.add(tile(col,row))
board = [[0 for col in range(4)] for row in range(4)]

class border(pygame.sprite.Sprite):
    def __init__(self, l:int,w:int,x:int,y:int) -> None:
        super().__init__()
        self.image = pygame.Surface((l,w))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(topleft = (x,y))

#Add borders
Borders = pygame.sprite.Group()
for i in range(5):
    Borders.add(border(3,400,(i * 100) + BOARD_OFFSET_HORZ,BOARD_OFFSET_VERT))
for i in range(5):
    Borders.add(border(400,3,BOARD_OFFSET_HORZ ,(i * 100) + BOARD_OFFSET_VERT))

#Background and game over
background_surf = pygame.Surface((SCREEN_HEIGHT,SCREEN_WIDTH))
background_surf.fill((179,12,43))
font = pygame.font.Font(None,100)
game_over_surf = font.render('GAME OVER!',True,(150,100,50))

add_tile()
while True:
    for event in pygame.event.get():
        #Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        #KeyUp
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            
            if event.key == pygame.K_UP:
                move_board('u')
            
            if event.key == pygame.K_DOWN:
                move_board('d')

            if event.key == pygame.K_LEFT:
                move_board('l')
            
            if event.key == pygame.K_RIGHT:
                move_board('r')

            if check_game_over():
                game_over = True

    #Frontend
    Board.draw(screen)
    Board.draw(screen)
    Borders.draw(screen)

    if game_over:
        screen.blit(game_over_surf,(SCREEN_WIDTH // 2 - (game_over_surf.get_width() // 2), SCREEN_HEIGHT // 2 - 25))

    pygame.display.update()
    clock.tick(FPS)