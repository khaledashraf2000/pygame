import pygame

# initialize
pygame.init()
pygame.display.set_caption("Minimal Pong")
ICON = pygame.image.load("assets/icon.png")
pygame.display.set_icon(ICON)

# constants
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60
BORDER = 20

# loading assets
BAT_IMG = pygame.image.load("assets/bat_img.png")
BALL_IMG = pygame.image.load("assets/ball_img.png")
FONT = pygame.font.Font("assets/PressStart2P.ttf", 30)


class Player:
    def __init__(self, x, y):
        self.score = 0
        self.x = x
        self.y = y
        self.dy = 0

    def draw(self):
        WINDOW.blit(BAT_IMG, (self.x, self.y))

    def move_up(self):
        self.dy = -6

    def move_down(self):
        self.dy = 6

    def move(self):
        # restrict movement
        if HEIGHT - BORDER - 75 > self.y + self.dy > 0 + BORDER:
            self.y += self.dy

    def stop(self):
        self.dy = 0


class Ball:
    def __init__(self, player_1: Player, player_2: Player):
        self.player_1 = player_1
        self.player_2 = player_2
        self.x = WIDTH / 2 - 20 / 2
        self.y = HEIGHT / 2 - 20 / 2
        self.dx = -4
        self.dy = -4

    def draw(self):
        WINDOW.blit(BALL_IMG, (self.x, self.y))

    def bounce(self):
        # bouncing top and bottom
        if self.y <= 0 + BORDER or self.y + 20 >= HEIGHT - BORDER:
            self.dy *= -1

        # bouncing off bats
        if (self.player_1.y <= self.y <= self.player_1.y + (75 - 10) and
            0 + BORDER + 20 < self.x <= self.player_1.x + 30) or \
                (self.player_2.y <= self.y <= self.player_2.y + (75 - 10) and
                 WIDTH - BORDER - 20 > self.x + 20 >= self.player_2.x):
            self.dx *= -1
        # didn't bounce off bat
        elif self.x < 0 + BORDER or self.x > WIDTH - BORDER - 20:
            # add score
            if self.get_court(self) == 'L':
                self.player_2.score += 10
            else:
                self.player_1.score += 10
            # reset ball to default position
            self.x = WIDTH / 2 - 20 / 2
            self.y = HEIGHT / 2 - 20 / 2

    def move(self):
        self.y += self.dy
        self.x += self.dx

    @staticmethod
    def get_court(self):
        if 0 < self.x < WIDTH / 2:
            return 'L'
        else:
            return 'R'


def main():
    player_1 = Player(0 + BORDER, int(HEIGHT / 2 - 75 / 2))
    player_2 = Player(WIDTH - 30 - BORDER, int(HEIGHT / 2 - 75 / 2))
    ball = Ball(player_1, player_2)
    run = True

    def draw_score():
        score_1_label = FONT.render(str(player_1.score), True, (80, 80, 80))
        WINDOW.blit(score_1_label, (0 + BORDER + 185 - (30 * len(str(player_1.score))) / 2, BORDER + 270))
        score_2_label = FONT.render(str(player_2.score), True, (80, 80, 80))
        WINDOW.blit(score_2_label, (WIDTH - BORDER - 185 - (30 * len(str(player_1.score))) / 2, BORDER + 270))

    def draw_screen():
        WINDOW.fill((15, 15, 15))
        pygame.draw.rect(WINDOW, (17, 17, 17), (BORDER, BORDER, WIDTH - 2 * BORDER, HEIGHT - 2 * BORDER))
        draw_score()
        player_1.draw()
        player_2.draw()
        ball.draw()
        pygame.display.update()

    def update_objects():
        player_1.move()
        player_2.move()
        ball.bounce()
        ball.move()

    while run:
        draw_screen()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # player 1 move
                if event.key == pygame.K_UP:
                    player_2.move_up()
                if event.key == pygame.K_DOWN:
                    player_2.move_down()

                # player 2 move
                if event.key == pygame.K_w:
                    player_1.move_up()
                if event.key == pygame.K_s:
                    player_1.move_down()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_2.stop()
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player_1.stop()

            if event.type == pygame.QUIT:
                run = False

        CLOCK.tick(FPS)
        update_objects()


main()
