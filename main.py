import pygame
import sys

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

# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sokoban")

# 색상 설정
WHITE = (255, 255, 255)

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