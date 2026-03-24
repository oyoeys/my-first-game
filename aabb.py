import pygame
import sys
from sprites import load_sprite

# --- SAT (분리축 정리) 충돌 계산 수학 함수 ---
def get_axes(points):
    axes = []
    for i in range(len(points)):
        p1 = pygame.math.Vector2(points[i])
        p2 = pygame.math.Vector2(points[(i + 1) % len(points)])
        edge = p2 - p1
        normal = pygame.math.Vector2(-edge.y, edge.x)
        if normal.length() > 0:
            normal = normal.normalize()
        axes.append(normal)
    return axes

def project(points, axis):
    min_proj = float('inf')
    max_proj = float('-inf')
    for p in points:
        v = pygame.math.Vector2(p)
        proj = v.dot(axis)
        if proj < min_proj: min_proj = proj
        if proj > max_proj: max_proj = proj
    return min_proj, max_proj

def check_obb_collision(poly1, poly2):
    axes = get_axes(poly1) + get_axes(poly2)
    for axis in axes:
        min1, max1 = project(poly1, axis)
        min2, max2 = project(poly2, axis)
        if max1 < min2 or max2 < min1:
            return False
    return True

# --- Pygame 메인 로직 ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AABB(노랑)와 OBB(빨강) 충돌 비교")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 150) # AABB 충돌 시 배경색 (연한 노랑)
RED = (255, 100, 100)    # OBB 충돌 시 배경색 (연한 빨강)
GREEN = (0, 255, 0)      # OBB 테두리
RED_LINE = (255, 0, 0)   # AABB 테두리

# 1. 스프라이트 이미지 불러오기
stone_img = load_sprite("stone", (60, 60))
adventurer_img = load_sprite("adventurer", (60, 60))

# 2. 중심 좌표 및 각도 초기화
stone_center = [WIDTH // 2, HEIGHT // 2]
adv_center = [150, 150]

stone_angle = 0
adv_angle = 0
speed = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. 키보드 입력 처리
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:  adv_center[0] -= speed
    if keys[pygame.K_RIGHT]: adv_center[0] += speed
    if keys[pygame.K_UP]:    adv_center[1] -= speed
    if keys[pygame.K_DOWN]:  adv_center[1] += speed

    if keys[pygame.K_q]: adv_angle = (adv_angle + 3) % 360
    if keys[pygame.K_w]: adv_angle = (adv_angle - 3) % 360

    rot_speed = 5 if keys[pygame.K_z] else 1
    stone_angle = (stone_angle + rot_speed) % 360

    # 4. 이미지 회전 및 AABB(Rect) 계산 
    # (충돌 감지를 위해 먼저 계산합니다)
    rotated_stone = pygame.transform.rotate(stone_img, stone_angle)
    stone_rect = rotated_stone.get_rect(center=stone_center)

    rotated_adv = pygame.transform.rotate(adventurer_img, adv_angle)
    adv_rect = rotated_adv.get_rect(center=adv_center)

    # 5. OBB(초록선) 모서리 꼭짓점 계산
    hw1, hh1 = stone_img.get_width() / 2, stone_img.get_height() / 2
    corners1 = [
        pygame.math.Vector2(-hw1, -hh1), pygame.math.Vector2(hw1, -hh1),
        pygame.math.Vector2(hw1, hh1), pygame.math.Vector2(-hw1, hh1)
    ]
    obb1_points = [(stone_center[0] + p.rotate(-stone_angle).x, stone_center[1] + p.rotate(-stone_angle).y) for p in corners1]

    hw2, hh2 = adventurer_img.get_width() / 2, adventurer_img.get_height() / 2
    corners2 = [
        pygame.math.Vector2(-hw2, -hh2), pygame.math.Vector2(hw2, -hh2),
        pygame.math.Vector2(hw2, hh2), pygame.math.Vector2(-hw2, hh2)
    ]
    obb2_points = [(adv_center[0] + p.rotate(-adv_angle).x, adv_center[1] + p.rotate(-adv_angle).y) for p in corners2]

    # 6. 충돌 감지 및 배경색 변경 (우선순위: OBB > AABB > 없음)
    aabb_collision = stone_rect.colliderect(adv_rect)
    obb_collision = check_obb_collision(obb1_points, obb2_points)

    if obb_collision:
        screen.fill(RED)      # 초록선끼리 닿으면 빨강!
    elif aabb_collision:
        screen.fill(YELLOW)   # 빨간선끼리 닿으면 노랑!
    else:
        screen.fill(WHITE)    # 아무것도 안 닿으면 하양!

    # 7. 화면에 이미지 그리기
    screen.blit(rotated_stone, stone_rect.topleft)
    screen.blit(rotated_adv, adv_rect.topleft)

    # 8. 테두리 그리기
    # 빨간색 AABB 테두리 (가상의 큰 사각형)
    pygame.draw.rect(screen, RED_LINE, stone_rect, 1)
    pygame.draw.rect(screen, RED_LINE, adv_rect, 1)

    # 초록색 OBB 테두리 (실제 오브젝트에 붙은 사각형)
    pygame.draw.lines(screen, GREEN, True, obb1_points, 3)
    pygame.draw.lines(screen, GREEN, True, obb2_points, 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()