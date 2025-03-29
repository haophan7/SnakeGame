import pygame
import sys
import random

class Snake():
    def __init__(self):
        self.length = 2
        self.positions = [((screen_width / 2), (screen_height / 2))]
        self.direction = random.choice([up, down, left, right])
        self.head_color = (255, 0, 255)
        self.body_color = (17, 24, 47)
        self.score = 0
        self.lost = False

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        if self.lost:
            return
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0]+(x*gridsize)) % screen_width), (cur[1]+(y*gridsize)) % screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.lost = True
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            if i == 0:
                r = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
                pygame.draw.rect(surface, self.head_color, r)
                pygame.draw.rect(surface, (93, 216, 228), r, 1)
            else:
                r = pygame.Rect((p[0], p[1]), (gridsize, gridsize))
                pygame.draw.rect(surface, self.body_color, r)
                pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

class Food():
    def __init__(self):
        self.position = (0, 0)
        self.orange_color = (223, 163, 49)
        self.red_color = (255, 0, 0)
        self.current_color = self.orange_color  # Màu của thức ăn hiện tại
        self.randomize_position()
        self.score = 1
        self.red_food_timer = None  # Thời gian khi thức ăn màu đỏ xuất hiện

    def randomize_position(self):
        self.position = (random.randint(0, grid_width - 1) * gridsize, random.randint(0, grid_height - 1) * gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.current_color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

    def create_red_food(self):
        self.current_color = self.red_color  # Đặt màu của thức ăn là màu đỏ
        self.score = 5  # Đặt điểm của thức ăn là 5
        self.red_food_timer = pygame.time.get_ticks()  # Ghi lại thời điểm khi thức ăn đỏ xuất hiện

    def create_orange_food(self):
        self.current_color = self.orange_color  # Đặt màu của thức ăn là màu cam
        self.randomize_position()  # Tạo vị trí mới cho thức ăn
        self.red_food_timer = None  # Đặt lại thời gian của thức ăn đỏ

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (93, 216, 228), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize, gridsize))
                pygame.draw.rect(surface, (84, 194, 205), rr)

screen_width = 480
screen_height = 480

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    pygame.display.set_caption("Snake Game")

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace", 16)

    game_over = False
    game_over_timer = 0

    orange_food_counter = 0  # Đếm số lượng viên thức ăn cam đã được ăn

    while True:
        clock.tick(10)
        snake.handle_keys()

        if not game_over:
            snake.move()

            if snake.get_head_position() == food.position:
                if food.current_color == food.orange_color:
                    snake.length += 1
                    snake.score += 1
                    orange_food_counter += 1
                    if orange_food_counter % 5 == 0:  # Mỗi khi ăn được 5 viên thức ăn màu cam
                        for _ in range(2):  # Tạo cùng lúc một viên thức ăn màu cam và một màu đỏ
                            food.create_orange_food()
                            food.create_red_food()
                    else:
                        if not food.red_food_timer:  # Nếu không có thức ăn màu đỏ hiện tại
                            food.create_orange_food()  # Tạo thức ăn màu cam mới
                elif food.current_color == food.red_color:
                    snake.length += 1
                    snake.score += food.score
                    food.create_orange_food()

            if food.red_food_timer and pygame.time.get_ticks() - food.red_food_timer >= 10000:
                food.create_orange_food()

            if snake.lost:
                game_over = True
                game_over_timer = pygame.time.get_ticks()

        drawGrid(surface)
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(snake.score), 1, (0, 0, 0))
        screen.blit(text, (5, 10))

        if game_over:
            if pygame.time.get_ticks() - game_over_timer >= 10000:  # 10 seconds
                game_over_screen(screen)
            else:
                font = pygame.font.SysFont("monospace", 36)
                label = font.render("You lost!", 1, (255, 0, 0))
                screen.blit(label, (150, 220))

        pygame.display.update()

def game_over_screen(screen):
    font = pygame.font.SysFont("monospace", 24)
    label = font.render("Do you want to play again? (Y/N)", 1, (255, 255, 0))
    screen.blit(label, (20, 225))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    main()
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()

main()
