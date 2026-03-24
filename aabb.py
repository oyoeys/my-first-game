import pygame
import sys

# 1. Pygame 초기화 및 화면 설정 (800x600)
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AABB 테스트")
clock = pygame.time.Clock()

# 색상 정의 (RGB)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

# 2. 사각형(오브젝트) 생성
rect_width, rect_height = 60, 60

# 화면 중앙에 고정된 사각형
fixed_rect = pygame.Rect(
    WIDTH // 2 - rect_width // 2, 
    HEIGHT // 2 - rect_height // 2, 
    rect_width, rect_height
)

# 방향키로 이동할 사각형 (초기 위치 설정)
moving_rect = pygame.Rect(100, 100, rect_width, rect_height)
speed = 5  # 이동 속도

# 메인 게임 루프
running = True
while running:
    # 이벤트 처리 (창 닫기 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. 키보드 입력 처리 (방향키 이동)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        moving_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        moving_rect.x += speed
    if keys[pygame.K_UP]:
        moving_rect.y -= speed
    if keys[pygame.K_DOWN]:
        moving_rect.y += speed

    # 화면을 흰색으로 지우기
    screen.fill(WHITE)

    # 4. 오브젝트 그리기
    # 내부 회색 사각형
    pygame.draw.rect(screen, GRAY, fixed_rect)
    pygame.draw.rect(screen, GRAY, moving_rect)

    # AABB (빨간색 테두리, 두께 2px)
    pygame.draw.rect(screen, RED, fixed_rect, 2)
    pygame.draw.rect(screen, RED, moving_rect, 2)

    # 화면 업데이트 및 FPS 설정
    pygame.display.flip()
    clock.tick(60)

# 종료 처리
pygame.quit()
sys.exit()