import pygame
import subprocess
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
screen_width = 800
screen_height = 600

# Màu sắc
white = (255, 255, 255)
black = (0, 0, 0)

# Tạo cửa sổ
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Home")

# Font
font = pygame.font.Font(None, 60)

# Hàm vẽ text ở giữa màn hình
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Xử lý sự kiện khi click chuột
            mouse_pos = pygame.mouse.get_pos()
            if classic_button_rect.collidepoint(mouse_pos):
                # Xử lý khi click nút Classic
                subprocess.Popen([sys.executable, 'classic.py'])
            elif campaign_button_rect.collidepoint(mouse_pos):
                # Xử lý khi click nút Campaign
                subprocess.Popen([sys.executable, 'campaign.py'])
            elif quit_button_rect.collidepoint(mouse_pos):
                # Xử lý khi click nút Quit
                pygame.quit()
                sys.exit()

    # Xóa màn hình
    screen.fill(white)

    # Vẽ tiêu đề Main Menu
    draw_text("Main Menu", font, black, screen, screen_width // 2, 100)

    # Vẽ nút Classic
    classic_button = pygame.Rect(screen_width // 2 - 100, 200, 200, 50)
    classic_button_rect = pygame.draw.rect(screen, black, classic_button)
    draw_text("Classic", font, white, screen, screen_width // 2, 225)

    # Vẽ nút Campaign
    campaign_button = pygame.Rect(screen_width // 2 - 100, 300, 200, 50)
    campaign_button_rect = pygame.draw.rect(screen, black, campaign_button)
    draw_text("Campaign", font, white, screen, screen_width // 2, 325)

    # Vẽ nút Quit
    quit_button = pygame.Rect(screen_width // 2 - 100, 400, 200, 50)
    quit_button_rect = pygame.draw.rect(screen, black, quit_button)
    draw_text("Quit", font, white, screen, screen_width // 2, 425)

    # Cập nhật màn hình
    pygame.display.flip()

# Kết thúc Pygame
pygame.quit()
