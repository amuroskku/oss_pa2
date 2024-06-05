import pygame
import sys
import random
from collections import deque

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 1000
screen_height = 1000
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
box_on_goal_image = pygame.image.load('box_with_x.png')

# 타일 크기 설정
tile_size = 100

# 맵 타일 종류
WALL = '#'
FLOOR = ' '
PLAYER = '@'
BOX = '$'
GOAL = '.'
BOX_ON_GOAL = '*'
PLAYER_ON_GOAL = '+'

# 방향 벡터
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# 게임 상태
STATE_MENU = 0
STATE_GAME = 1
STATE_CONTROLS = 2
game_state = STATE_MENU

# 맵 데이터
level = []
player_pos = [0, 0]
goal_count = 0

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

def draw_level(map_data):
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            screen.blit(floor_image, (x * tile_size, y * tile_size))
            if tile == WALL:
                screen.blit(wall_image, (x * tile_size, y * tile_size))
            elif tile == GOAL:
                screen.blit(goal_image, (x * tile_size, y * tile_size))
            elif tile == BOX:
                screen.blit(box_image, (x * tile_size, y * tile_size))
            elif tile == BOX_ON_GOAL:
                screen.blit(box_on_goal_image, (x * tile_size, y * tile_size))

def draw_player():
    screen.blit(player_image, (player_pos[0] * tile_size, player_pos[1] * tile_size))

def move_player(dx, dy):
    global level
    global goal_count
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    
    if level[new_y][new_x] in " .":
        # player가 있던 자리 공백으로 변환
        for i in level:
            print(i)
        print(level[player_pos[1]][:player_pos[0]])
        print(level[player_pos[1]][player_pos[0]+1:])
        level[player_pos[1]][player_pos[0]] = " "
        #player 이동
        player_pos[0] = new_x
        player_pos[1] = new_y
        level[player_pos[1]][player_pos[0]] = "@"
    elif level[new_y][new_x] == '$':
        box_new_x = new_x + dx
        box_new_y = new_y + dy
        if level[box_new_y][box_new_x] in " .":
            level[new_y][new_x] = ' '
            level[player_pos[1]][player_pos[0]] = " "
            player_pos[0] = new_x
            player_pos[1] = new_y
            level[player_pos[1]][player_pos[0]] = "@"
            # 상자 이동
            if level[box_new_y][box_new_x] == " ":
                level[box_new_y][box_new_x] = '$'
            elif level[box_new_y][box_new_x] == ".":
                level[box_new_y][box_new_x] = '*'
                goal_count -= 1

def is_win():
    global goal_count
    if goal_count == 0:
        font = pygame.font.SysFont(None, 100)
        text = font.render("YOU WIN!", True, (255, 0, 0))
        screen.blit(text, (screen_width // 2 - 200, screen_height // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2000)  # 2초간 대기
        reset_game()  # 게임 초기화 함수 호출

def reset_game():
    global level, player_pos, previous_moves
    level, player_pos = generate_sokoban_map(10, 10, 3)
    previous_moves.clear()  # 이전 행동 기록 초기화

previous_moves = deque()

def show_menu():
    font = pygame.font.SysFont(None, 50)
    text = ["Press Enter To Start Game","To See How To Play, Press H"]
    label = []
    position = [screen_width // 2 - 200, screen_height // 2 - 50]
    for line in text:
        label.append(font.render(line, True, (255, 0, 0)))
    for line in range(len(label)):
        screen.blit(label[line],(position[0],position[1]+(line*50)+(15*line)))
    pygame.display.flip()

def show_controls():
    font = pygame.font.SysFont(None, 32)
    text = ["                                                              Sokoban Rules","1. Objective: Push all the boxes into the holes.", "2. Winning Condition: Fill all the holes with boxes to win.", "3. New Map: A new map will be generated automatically a few seconds after you win.", "                                              To return to main menu, Press 'Esc'"]
    label = []
    position = [screen_width // 2 - 460, screen_height // 2 - 250]
    for line in text:
        label.append(font.render(line, True, (255, 0, 0)))
    for line in range(len(label)):
        screen.blit(label[line],(position[0],position[1]+(line*50)+(15*line)))
    pygame.display.flip()

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == STATE_MENU:
                if event.key == pygame.K_RETURN:  # Enter 키를 눌러 게임 시작
                    level, player_pos = generate_sokoban_map(10, 10, 3)
                    game_state = STATE_GAME
                elif event.key == pygame.K_h:  # H 키를 눌러 조작법 안내
                    game_state = STATE_CONTROLS
            elif game_state == STATE_CONTROLS:
                if event.key == pygame.K_ESCAPE:  # ESC 키를 눌러 메뉴로 돌아감
                    game_state = STATE_MENU
            elif game_state == STATE_GAME:
                if event.key == pygame.K_ESCAPE:  # ESC 키를 눌러 메뉴로 돌아감
                    game_state = STATE_MENU
                elif event.key == pygame.K_UP:
                    move_player(0, -1)
                    is_win()
                elif event.key == pygame.K_DOWN:
                    move_player(0, 1)
                    is_win()
                elif event.key == pygame.K_LEFT:
                    move_player(-1, 0)
                    is_win()
                elif event.key == pygame.K_RIGHT:
                    move_player(1, 0)
                    is_win()

    screen.fill(WHITE)
    if game_state == STATE_MENU:
        show_menu()
    elif game_state == STATE_CONTROLS:
        show_controls()
    elif game_state == STATE_GAME:
        draw_level(level)
        draw_player()
        pygame.display.flip()

pygame.quit()
sys.exit()
