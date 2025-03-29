import pygame
import random
import sys
import pygame.display
import time
import os

# Các hằng số
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (205, 133, 63)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
TEAL = (0, 128, 128)
YELLOW = (255, 215, 0)
GRAY = (128, 128, 128)
ROYAL = (65, 105, 225)
ORANGE = (255, 165, 79)

# Khởi tạo biến high score
high_score = 0

# Hàm vẽ rắn
def draw_snake(surface, snake):
    # Vẽ đầu con rắn
    pygame.draw.rect(surface, ORANGE, (snake[0][0], snake[0][1], CELL_SIZE, CELL_SIZE))
    # Vẽ mắt
    pygame.draw.circle(surface, BLACK, (snake[0][0] + 5, snake[0][1] + 5), 2)
    pygame.draw.circle(surface, BLACK, (snake[0][0] + 15, snake[0][1] + 5), 2)
    # Vẽ lưỡi con rắn
    pygame.draw.rect(surface, RED, (snake[0][0] + 5, snake[0][1] + 10, 10, 4))
    # Vẽ thân con rắn
    for segment in snake[1:]:
        pygame.draw.rect(surface, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    # Vẽ các đốt trên lưng con rắn
    for segment in snake[1:]:
        pygame.draw.circle(surface, ROYAL, (segment[0] + CELL_SIZE // 2, segment[1] + CELL_SIZE // 2), 4)

# Hàm vẽ thức ăn
def draw_food(surface, food_positions, orange_positions, black_food=False):
    for food in food_positions:
        pygame.draw.rect(surface, BLUE, (food[0], food[1], CELL_SIZE, CELL_SIZE))
    for orange in orange_positions:
        pygame.draw.rect(surface, YELLOW, (orange[0], orange[1], CELL_SIZE, CELL_SIZE))
    if black_food and food_positions:
        pygame.draw.rect(surface, BLACK, (food_positions[0][0], food_positions[0][1], CELL_SIZE, CELL_SIZE))

# Tạo thức ăn mới
def create_food(snake, obstacles):
    while True:
        food_position = [random.randrange(0, SCREEN_WIDTH, CELL_SIZE), random.randrange(40, SCREEN_HEIGHT, CELL_SIZE)]
        # Kiểm tra xem vị trí thức ăn mới có trùng với snake hoặc obstacles không
        if food_position not in snake and food_position not in obstacles:
            return food_position

# Khoảng cách giữa hai điểm
def distance(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

# Kiểm tra va chạm
def check_collision(snake, obstacles):
    # Kiểm tra va chạm với các phần tử trong snake
    if len(snake) != len(set(map(tuple, snake))):
        return True
    # Kiểm tra va chạm với các chướng ngại vật
    for obstacle in obstacles:
        if snake[0] == obstacle:
            return True
    return False

# Hàm vẽ chướng ngại vật
def draw_obstacles(screen, obstacles):
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle[0], obstacle[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, TEAL, obstacle_rect)

# Kiểm tra điều kiện khi con rắn đạt tốc độ bằng 10
def check_speed_limit(snake, food_positions, orange_positions, FPS):
    if FPS == 10:
        return True
    else:
        return False

# Hiển thị thông báo và xử lý việc chơi lại
def display_message(screen, message, score):
    global high_score
    font = pygame.font.SysFont("monospace", 36)
    text = font.render(message, True, GRAY)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(10000)

    if score > high_score:
        high_score = score

    # Ẩn điểm số và điểm cao
    screen.fill(WHITE)
    pygame.display.flip()

    text = font.render("Do you want to play again? (Y/N)", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    # Chuyển sang màn hình mới (file campaign.py)
                    pygame.quit()
                    import campaign
                    campaign.main()
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

# Hàm kiểm tra xem con rắn có đi vào thành màu đen không
def check_win_condition(snake, obstacles):
    return snake[0] in obstacles

# Hàm hiển thị thông báo chiến thắng
def display_victory_message(screen, score):
    font = pygame.font.SysFont("monospace", 36)
    text1 = font.render("Congratulations! You won Level 4!", True, GRAY)
    text2 = font.render("Your Score Is: " + str(score), True, GRAY)

    text_rect1 = text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    text_rect2 = text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)

    pygame.display.flip()
    return pygame.time.get_ticks()  # Trả về thời điểm hiện tại khi thông báo được hiển thị

# Hàm main
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Xenzia")
    icon = pygame.image.load("snake.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()
    orange_start_time = pygame.time.get_ticks()

    running = True
    while running:
        # Khởi tạo con rắn ở giữa màn hình với độ dài là 2
        snake = [[SCREEN_WIDTH // 2 + CELL_SIZE, SCREEN_HEIGHT // 2], [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]]
        direction = None

        # Khởi tạo danh sách obstacles
        obstacles_left = [[220, y] for y in range(40, SCREEN_HEIGHT - 340, CELL_SIZE)]
        obstacles_left2 = [[0, y] for y in range(40, SCREEN_HEIGHT - 380, CELL_SIZE)]
        obstacles_right = [[SCREEN_WIDTH - 260, y] for y in range(380, SCREEN_HEIGHT, CELL_SIZE)]
        obstacles_top = [[x, 40] for x in range(0, SCREEN_WIDTH - 720, CELL_SIZE)]
        obstacles_top2 = [[x, 40] for x in range(160, SCREEN_WIDTH - 160, CELL_SIZE)]
        obstacles_center = [[x, 260] for x in range(0, SCREEN_WIDTH - 360, CELL_SIZE)]
        obstacles_center2 = [[x, SCREEN_HEIGHT - 340] for x in range(540, SCREEN_WIDTH, CELL_SIZE)]
        obstacles_center3 = [[x, SCREEN_HEIGHT - 240] for x in range(0, SCREEN_WIDTH, CELL_SIZE)]
        obstacles = obstacles_top + obstacles_left + obstacles_right + obstacles_left2 + obstacles_top2 + obstacles_center + obstacles_center2 + obstacles_center3
        draw_obstacles(screen, obstacles)

        food_positions = [create_food(snake, obstacles)]
        orange_positions = []

        food_eaten_count = 0
        score = 0  # Điểm số ban đầu
        displaying_message = False
        speed_up_counter = 0  # Biến để đếm số lượng thức ăn đã ăn
        FPS = 5  # Đặt tốc độ ban đầu
        snake_started_moving = False  # Biến để kiểm tra xem con rắn đã bắt đầu di chuyển chưa
        black_food_eaten = 0  # Biến để theo dõi số lượng thức ăn đen đã ăn

        # Hiển thị điểm số và điểm cao từ đầu
        screen.fill(WHITE)
        font = pygame.font.SysFont("monospace", 24)
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (10, 10))
        high_score_text = font.render("High Score: " + str(high_score), True, BLACK)
        screen.blit(high_score_text, (SCREEN_WIDTH - 220, 10))

        # Hiển thị tốc độ
        speed_text = font.render("Speed: " + str(FPS), True, BLACK)
        screen.blit(speed_text, (SCREEN_WIDTH // 2 - 90, 10))

        # Hiển thị con rắn
        draw_snake(screen, snake)

        # Hiển thị thức ăn
        draw_food(screen, food_positions, orange_positions, check_speed_limit(snake, food_positions, orange_positions, FPS))

        # Hiển thị dòng kẻ ngang dưới score và high_score.txt
        pygame.draw.rect(screen, BLACK, (0, 38, SCREEN_WIDTH, 2))

        # Hiển thị chướng ngại vật
        draw_obstacles(screen, obstacles)

        pygame.display.flip()

        while not direction:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        direction = event.key

        if not running:
            break

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and direction != pygame.K_RIGHT:
                        direction = pygame.K_LEFT
                    elif event.key == pygame.K_RIGHT and direction != pygame.K_LEFT:
                        direction = pygame.K_RIGHT
                    elif event.key == pygame.K_UP and direction != pygame.K_DOWN:
                        direction = pygame.K_UP
                    elif event.key == pygame.K_DOWN and direction != pygame.K_UP:
                        direction = pygame.K_DOWN

            if not running:
                break

            if direction is not None and not displaying_message:
                if not snake_started_moving:
                    snake_started_moving = True

                keys = pygame.key.get_pressed()
                if direction == pygame.K_LEFT and direction != pygame.K_RIGHT:
                    new_head = [snake[0][0] - CELL_SIZE, snake[0][1]]
                elif direction == pygame.K_RIGHT and direction != pygame.K_LEFT:
                    new_head = [snake[0][0] + CELL_SIZE, snake[0][1]]
                elif direction == pygame.K_UP and direction != pygame.K_DOWN:
                    new_head = [snake[0][0], snake[0][1] - CELL_SIZE]
                    if new_head[1] <= 30:
                        new_head[1] = SCREEN_HEIGHT - CELL_SIZE
                elif direction == pygame.K_DOWN and direction != pygame.K_UP:
                    new_head = [snake[0][0], snake[0][1] + CELL_SIZE]
                    if new_head[1] >= SCREEN_HEIGHT:
                        new_head[1] = 40

                if new_head[0] >= SCREEN_WIDTH:
                    new_head[0] = 0
                elif new_head[0] < 0:
                    new_head[0] = SCREEN_WIDTH - CELL_SIZE
                elif new_head[1] >= SCREEN_HEIGHT:
                    new_head[1] = 0
                elif new_head[1] < 0:
                    new_head[1] = SCREEN_HEIGHT - CELL_SIZE

                snake.insert(0, new_head)

                if check_collision(snake, obstacles):
                    displaying_message = True
                    if not display_message(screen, "You lost! Your Score Is: " + str(score), score):
                        running = False
                    break

                if snake[0] in food_positions:
                    food_positions.remove(snake[0])
                    score += 1  # Cộng điểm khi ăn thức ăn đỏ
                    food_eaten_count += 1
                    if check_speed_limit(snake, food_positions, orange_positions, FPS):
                        # Nếu con rắn đạt tốc độ bằng 10 thì không tạo thức ăn mới nữa
                        black_food_eaten += 1
                        if black_food_eaten >= 1:
                            # Nếu con rắn đi vào thành màu đen, hiển thị thông báo và đợi 10 giây trước khi đóng cửa sổ
                            displaying_message = True
                            start_time = display_victory_message(screen, score)  # Lưu thời điểm khi thông báo được hiển thị
                            while pygame.time.get_ticks() - start_time < 10000:  # Vòng lặp để đợi 10 giây
                                pass
                            screen.fill(WHITE)  # Xóa thông báo khỏi màn hình
                            pygame.display.flip()
                            if not display_message(screen, "You win!", score):
                                running = False
                            break
                    else:
                        if food_eaten_count % 5 == 0:
                            # Tăng tốc độ sau mỗi 5 viên thức ăn
                            FPS += 1
                            orange_positions.append(create_food(snake, obstacles))
                            food_positions.append(create_food(snake, obstacles))
                            orange_start_time = pygame.time.get_ticks()
                        else:
                            food_positions.append(create_food(snake, obstacles))
                elif snake[0] in orange_positions:
                    orange_positions.remove(snake[0])
                    score += 5  # Cộng điểm khi ăn thức ăn cam
                else:
                    snake.pop()

                if orange_positions and pygame.time.get_ticks() - orange_start_time >= 5000:
                    orange_positions = []

                screen.fill(WHITE)
                pygame.draw.rect(screen, BLACK, (0, 38, SCREEN_WIDTH, 2))
                draw_snake(screen, snake)
                draw_food(screen, food_positions, orange_positions,
                          check_speed_limit(snake, food_positions, orange_positions, FPS))

                # Kiểm tra xem con rắn có đi vào thành màu đen không
                if check_speed_limit(snake, food_positions, orange_positions, FPS) and snake[0] in obstacles:
                    # Nếu con rắn đi vào thành màu đen, hiển thị thông báo và đợi 10 giây trước khi đóng cửa sổ
                    displaying_message = True
                    start_time = display_victory_message(screen, score)  # Lưu thời điểm khi thông báo được hiển thị
                    while pygame.time.get_ticks() - start_time < 10000:  # Vòng lặp để đợi 10 giây
                        pass
                    screen.fill(WHITE)  # Xóa thông báo khỏi màn hình
                    pygame.display.flip()
                    if not display_message(screen, "You win!", score):
                        running = False
                    break

                score_text = font.render("Score: " + str(score), True, BLACK)
                screen.blit(score_text, (10, 10))
                high_score_text = font.render("High Score: " + str(high_score), True, BLACK)
                screen.blit(high_score_text, (SCREEN_WIDTH - 220, 10))
                speed_text = font.render("Speed: " + str(FPS), True, BLACK)
                screen.blit(speed_text, (SCREEN_WIDTH // 2 - 90, 10))
                obstacles_left = [[220, y] for y in range(40, SCREEN_HEIGHT - 340, CELL_SIZE)]
                obstacles_left2 = [[0, y] for y in range(40, SCREEN_HEIGHT - 380, CELL_SIZE)]
                obstacles_right = [[SCREEN_WIDTH - 260, y] for y in range(380, SCREEN_HEIGHT, CELL_SIZE)]
                obstacles_top = [[x, 40] for x in range(0, SCREEN_WIDTH - 720, CELL_SIZE)]
                obstacles_top2 = [[x, 40] for x in range(160, SCREEN_WIDTH - 160, CELL_SIZE)]
                obstacles_center = [[x, 260] for x in range(0, SCREEN_WIDTH - 360, CELL_SIZE)]
                obstacles_center2 = [[x, SCREEN_HEIGHT - 340] for x in range(540, SCREEN_WIDTH, CELL_SIZE)]
                obstacles_center3 = [[x, SCREEN_HEIGHT - 240] for x in range(0, SCREEN_WIDTH, CELL_SIZE)]
                obstacles = obstacles_top + obstacles_left + obstacles_right + obstacles_left2 + obstacles_top2 + obstacles_center + obstacles_center2 + obstacles_center3
                draw_obstacles(screen, obstacles)

                pygame.display.flip()

                clock.tick(FPS)

            else:
                displaying_message = False
                screen.fill(WHITE)
                pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
