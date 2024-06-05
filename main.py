import pygame
import sys
import random

# 화면에 레벨을 표시함
def draw_level():
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile == '#':
                pygame.draw.rect(screen, (0, 0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))
            elif tile == '.':
                pygame.draw.circle(screen, (255, 0, 0), (x * tile_size + tile_size // 2, y * tile_size + tile_size // 2), tile_size // 4)
            elif tile == '$':
                pygame.draw.rect(screen, (0, 255, 0), (x * tile_size, y * tile_size, tile_size, tile_size))

#화면에 플레이어를 표시함
def draw_player():
    pygame.draw.circle(screen, (0, 0, 255), (player_pos[0] * tile_size + tile_size // 2, player_pos[1] * tile_size + tile_size // 2), tile_size // 2)

#플레이어의 이동을 정의
def move_player(dx, dy):
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    
    if level[new_y][new_x] in " .":
        # player가 있던 자리 공백으로 변환
        level[player_pos[1]] = level[player_pos[1]][:player_pos[0]] + " " + level[player_pos[1]][player_pos[0]+1:]
        #player 이동
        player_pos[0] = new_x
        player_pos[1] = new_y
        level[player_pos[1]] = level[player_pos[1]][:player_pos[0]] + "@" + level[player_pos[1]][player_pos[0]+1:]
    elif level[new_y][new_x] == '$':
        box_new_x = new_x + dx
        box_new_y = new_y + dy
        if level[box_new_y][box_new_x] in " .":
            # 상자 이동
            level[new_y] = level[new_y][:new_x] + ' ' + level[new_y][new_x+1:]
            level[box_new_y] = level[box_new_y][:box_new_x] + '$' + level[box_new_y][box_new_x+1:]
            level[player_pos[1]] = level[player_pos[1]][:player_pos[0]] + " " + level[player_pos[1]][player_pos[0]+1:]
            player_pos[0] = new_x
            player_pos[1] = new_y
            level[player_pos[1]] = level[player_pos[1]][:player_pos[0]] + "@" + level[player_pos[1]][player_pos[0]+1:]

############################################################ For Test ############################################################

# 맵 데이터
level = []
player_pos = [0, 0]
goal_count = 0

# 맵 타일 종류
WALL = '#'
FLOOR = ' '
PLAYER = '@'
BOX = '$'
GOAL = '.'
BOX_ON_GOAL = '*'
PLAYER_ON_GOAL = '+'

def create_empty_map(width, height):
    return [[WALL if x == 0 or x == width - 1 or y == 0 or y == height - 1 else FLOOR for x in range(width)] for y in range(height)]

def place_player_and_goals(map_data, num_goals):
    global player_pos
    free_spaces = [(y, x) for y, row in enumerate(map_data) for x, tile in enumerate(row) if tile == FLOOR]
    random.shuffle(free_spaces)

    # 플레이어 위치 선정
    print(str(type(player_pos)) + "place_player_and_goals")
    temp_pos = list(free_spaces.pop())
    player_pos[0] = temp_pos[0]
    player_pos[1] = temp_pos[1]
    print(str(type(player_pos)) + "place_player_and_goals")
    map_data[player_pos[0]][player_pos[1]] = PLAYER

    # 목표 지점 선정
    goals = []
    for _ in range(num_goals):
        goal_pos = free_spaces.pop()
        map_data[goal_pos[0]][goal_pos[1]] = GOAL
        goals.append(goal_pos)
    for i in map_data:
        print(i)
    return player_pos, goals

def is_adjacent_to_wall(y, x, map_data):
    """Check if the position (y, x) is adjacent to a wall."""
    adjacent_positions = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
    return any(map_data[ny][nx] == WALL for ny, nx in adjacent_positions)

def place_boxes(map_data, goals):
    global goal_count
    
    free_spaces = [(y, x) for y, row in enumerate(map_data) for x, tile in enumerate(row) if tile == FLOOR and not is_adjacent_to_wall(y, x, map_data)]
    for i in map_data:
        print(i)
    print(free_spaces)
    random.shuffle(free_spaces)

    for goal in goals:
        box_pos = free_spaces.pop()
        map_data[box_pos[0]][box_pos[1]] = BOX
        goal_count += 1
    
    for i in map_data:
        print(i)
    return map_data

def generate_sokoban_map(width, height, num_goals):
    global player_pos
    while True:
        map_data = create_empty_map(width, height)
        print(str(type(player_pos)) + "generate_sokoban_map")
        player_pos, goals = place_player_and_goals(map_data, num_goals)
        print(str(type(player_pos)) + "generate_sokoban_map")
        map_data = place_boxes(map_data, goals)
        return map_data, player_pos
    
level, player_pos = generate_sokoban_map(10,10,3)
for i in level:
    print(i)
print(player_pos)
#############################################################################################################################


# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sokoban")

# 색상 설정
WHITE = (255, 255, 255)

# 이미지 로드
player_image = pygame.image.load('player.png')
wall_image = pygame.image.load('wall.png')
box_image = pygame.image.load('box.png')
goal_image = pygame.image.load('goal.png')
floor_image = pygame.image.load('floor.png')

# 맵 데이터
level = [
    "#######",
    "#     #",
    "#.$ # #",
    "# @   #",
    "#######"
]

#목표 개수 설정
n_goal = 1

# 타일 크기 설정
tile_size = 100

# 플레이어 위치 찾기
player_pos = [0, 0]
for y, row in enumerate(level):
    for x, tile in enumerate(row):
        if tile == '@':
            player_pos = [x, y]
print(player_pos)

def run():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_player(0, -1)
                elif event.key == pygame.K_DOWN:
                    move_player(0, 1)
                elif event.key == pygame.K_LEFT:
                    move_player(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    move_player(1, 0)
        
        screen.fill(WHITE)
        draw_level()
        draw_player()
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    run()