import pygame
import sys
import random # 추가
import math   # 추가

pygame.init()
screen = pygame.display.set_mode((400, 400)) # 400x400으로 변경
pygame.display.set_caption("My First Pygame")

WHITE = (0, 0, 0) # 배경색(검정)
BLUE = (255, 0, 0) # 원색(빨강)
# 추가된 설정들
SQUARE_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 255)
GO_COLOR = (255, 255, 0)

# 원 및 시스템 변수 추가
circle_x, circle_y = 200, 200
score = 0
game_over = False
last_eat_time = pygame.time.get_ticks()
squares = []

# 폰트 및 타이머 추가
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 60)
SPAWN_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_EVENT, 1500) # 1.5초 생성

clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks() # 시간 측정 추가
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 네모 생성 로직 추가
        if not game_over and event.type == SPAWN_EVENT:
            while True:
                nx, ny = random.randint(0, 390), random.randint(0, 390)
                if math.sqrt((circle_x-nx)**2 + (circle_y-ny)**2) > 100:
                    squares.append([nx, ny, current_time])
                    break

    # 게임 로직 추가 (오버 체크, 이동, 충돌)
    if not game_over:
        if current_time - last_eat_time > 5000: game_over = True
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: circle_y -= 7
        if keys[pygame.K_s]: circle_y += 7
        if keys[pygame.K_a]: circle_x -= 7
        if keys[pygame.K_d]: circle_x += 7

        rem = []
        for sq in squares:
            dist = math.sqrt((circle_x-sq[0])**2 + (circle_y-sq[1])**2)
            if dist < 100:
                score += 1
                last_eat_time = current_time
            elif current_time - sq[2] < 500:
                rem.append(sq)
        squares = rem

    screen.fill(WHITE)
    
    # 그리기 작업
    for sq in squares:
        pygame.draw.rect(screen, SQUARE_COLOR, (sq[0], sq[1], 10, 10))
    
    pygame.draw.circle(screen, BLUE, (circle_x, circle_y), 100, 10)

    # UI 추가
    fps_txt = font.render(f"FPS: {round(clock.get_fps())}", True, TEXT_COLOR)
    screen.blit(fps_txt, (10, 10))
    sc_txt = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(sc_txt, (300, 10))
    
    if game_over:
        msg = large_font.render("GAME OVER", True, GO_COLOR)
        screen.blit(msg, msg.get_rect(center=(200, 200)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()