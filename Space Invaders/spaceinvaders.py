import pygame

# initialize
pygame.init()

# constants
WIDTH, HEIGHT = 800, 600
BORDER = 30
FPS = 60

# create the screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font("assets/PressStart2P.ttf", 15)

# loading assets
ICON = pygame.image.load("assets/icon.jpg")
PLAYER_IMG = pygame.image.load("assets/player_img.png")
INVADER_IMG = pygame.image.load("assets/invader_img.png")
LASER_IMG = pygame.image.load("assets/bullet_img.png")

# adding title and logo
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(ICON)

score = 0
player_x = 400 - 64 / 2
player_y = 425 - 64 / 2
player_dx = 0
player_dy = 0
invader_x = 0 + BORDER
invader_y = 30 + BORDER
invader_dx = 0.2
invader_dy = 0
bullet_x = player_x
bullet_y = player_y
bullet_dx = 0
bullet_dy = -0.7
player_alive = True
invader_alive = True
running = True
shoot = False
clock = pygame.time.Clock()


def show_score():
    score_label = FONT.render(str(score), True, (255, 255, 255))
    SCREEN.blit(score_label, (750 - 15 * len(str(score)), BORDER))


def draw_player(x, y):
    SCREEN.blit(PLAYER_IMG, (x, y))


def draw_invader(x, y):
    SCREEN.blit(INVADER_IMG, (x, y))


def draw_bullet(x, y):
    SCREEN.blit(LASER_IMG, (x, y))


while running:
    SCREEN.fill((15, 15, 15))
    show_score()
    for event in pygame.event.get():
        # move handling
        if event.type == pygame.KEYDOWN:
            # move to the left
            if event.key == pygame.K_LEFT:
                player_dx = -0.3
            # move to the right
            if event.key == pygame.K_RIGHT:
                player_dx = 0.3
            # move up
            if event.key == pygame.K_UP:
                player_dy = -0.3
            # move down
            if event.key == pygame.K_DOWN:
                player_dy = 0.3
        if event.type == pygame.KEYUP:
            # stop
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_dx = 0
            if event.key == pygame.K_UP or pygame.K_DOWN:
                player_dy = 0

            # shoot
            if event.key == pygame.K_SPACE:
                bullet_x = player_x
                bullet_y = player_y
                shoot = True

        # quit handling
        if event.type == pygame.QUIT:
            running = False

    # check boundaries
    # player movement
    if 0 + BORDER < player_x + player_dx < 800 - 64 - BORDER:
        player_x += player_dx
    if 425.0 - 64 / 2 - BORDER < player_y + player_dy < 600 - 64 - BORDER:
        player_y += player_dy

    # invader movement
    if 0 + BORDER < invader_x + invader_dx < 800 - 64 - BORDER:
        invader_x += invader_dx
    else:
        invader_y += 20
        invader_dx = -invader_dx

    # collision
    if invader_y - 32 < bullet_y < invader_y + 32 and invader_x - 32 < bullet_x < invader_x + 32:
        invader_x = 0 + BORDER
        invader_y = 30 + BORDER
        score += 10

    # collision with player
    if invader_y < player_y < invader_y + 64 and invader_x < player_x < invader_x + 64:
        player_alive = False

    if invader_alive:
        draw_invader(invader_x, invader_y)
    if player_alive:
        draw_player(player_x, player_y)
    if shoot and bullet_y > 0:
        bullet_y += bullet_dy
        draw_bullet(bullet_x, bullet_y)
        if bullet_y <= 0:
            bullet_y = player_y
            bullet_x = player_x
            shoot = False

    pygame.display.update()
