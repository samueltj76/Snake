import pygame
from random import randrange

# basic settings
RES = 736
SIZE = 32

def init_game():
    global x, y, apple, length, snake, dx, dy, score, speed_count, snake_speed
    x, y = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
    length = 1
    snake = [(x, y)]
    dx, dy = 0, 0
    score = 0
    speed_count, snake_speed = 0, 12

init_game()

dirs = {'W': True, 'S': True, 'A': True, 'D': True}
fps = 60

pygame.init()
pygame.display.set_caption('Snake 1IMA')

surface = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
font_score = pygame.font.SysFont('Arial', 26, bold=True)
font_end = pygame.font.SysFont('Arial', 66, bold=True)
font_btn = pygame.font.SysFont('Arial', 30, bold=True)
img = pygame.image.load('1.jpg').convert()

# loading snake and apple images
apple_img = pygame.image.load('apple.png').convert_alpha()
apple_img = pygame.transform.scale(apple_img, (SIZE, SIZE))

snake_head_img_original = pygame.image.load('snake_head.png').convert_alpha()
snake_head_img_original = pygame.transform.scale(snake_head_img_original, (SIZE, SIZE))

snake_body_img = pygame.image.load('snake_body.png').convert_alpha()
snake_body_img = pygame.transform.scale(snake_body_img, (SIZE, SIZE))

# sound effects
pygame.mixer.init()
eat_sound = pygame.mixer.Sound('eat.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

# closing the game
def close_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def draw_buttons():
    # again button
    try_again_btn = pygame.Rect(RES // 2 - 150, RES // 2, 300, 50)
    pygame.draw.rect(surface, pygame.Color('green'), try_again_btn)
    try_again_text = font_btn.render('TRY AGAIN', True, pygame.Color('black'))
    surface.blit(try_again_text, (RES // 2 - 80, RES // 2 + 10))

    # exit button
    exit_btn = pygame.Rect(RES // 2 - 150, RES // 2 + 70, 300, 50)
    pygame.draw.rect(surface, pygame.Color('red'), exit_btn)
    exit_text = font_btn.render('EXIT', True, pygame.Color('black'))
    surface.blit(exit_text, (RES // 2 - 30, RES // 2 + 80))

    return try_again_btn, exit_btn

def create_blurred_background():
    # Reduce the image size for a blur effect
    small_surface = pygame.transform.scale(surface, (RES // 10, RES // 10))
    # Scale it back up
    blurred_surface = pygame.transform.scale(small_surface, (RES, RES))
   
    # Darken the surface
    darken_surface = pygame.Surface((RES, RES))
    darken_surface.set_alpha(128)  # Semi-transparent black color
    darken_surface.fill(pygame.Color('black'))

    # Apply the darkening over the blurred image
    blurred_surface.blit(darken_surface, (0, 0))
    return blurred_surface

def handle_game_over():
    game_over_sound.play()  # Play the game over sound
   
    # Create a blurred and darkened background

    blurred_background = create_blurred_background()
   
    while True:
        surface.blit(blurred_background, (0, 0))  # Apply the blurred background
       
        render_end = font_end.render('GAME OVER', 1, pygame.Color('orange'))
        surface.blit(render_end, (RES // 2 - 200, RES // 3))

        # Draw the buttons and get their areas
        try_again_btn, exit_btn = draw_buttons()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if try_again_btn.collidepoint(event.pos):
                    init_game()  # Перезапуск игры
                    return
                elif exit_btn.collidepoint(event.pos):
                    pygame.quit()
                    exit()

# game
while True:
    surface.blit(img, (0, 0))

    for i, pos in enumerate(snake):
        if i == len(snake) - 1:
        
         # Set a default value for snake_head_img
            snake_head_img = snake_head_img_original

    # drawing the snake
    for i, pos in enumerate(snake):
        if i == len(snake) - 1:  # snake head
            if dx == 1:  # moving right
                snake_head_img = pygame.transform.rotate(snake_head_img_original, 270)
            elif dx == -1:  # moving left
                snake_head_img = pygame.transform.rotate(snake_head_img_original, 90)
            elif dy == 1:  # moving down
                snake_head_img = pygame.transform.rotate(snake_head_img_original, 180)
            elif dy == -1:  # moving up
                snake_head_img = snake_head_img_original  # no rotation needed for upward direction

            surface.blit(snake_head_img, pos)
        else:  # это тело змеи
            surface.blit(snake_body_img, pos)

    # drawing the apple
    surface.blit(apple_img, apple)  # display the apple image

    # drawing the score
    render_score = font_score.render(f'SCORE: {score}', 1, pygame.Color('black'))
    surface.blit(render_score, (5, 5))

    # snake movement
    speed_count += 1
    if not speed_count % snake_speed:
        x += dx * SIZE
        y += dy * SIZE
        snake.append((x, y))
        snake = snake[-length:]

    # eating the apple
    if snake[-1] == apple:
        apple = randrange(SIZE, RES - SIZE, SIZE), randrange(SIZE, RES - SIZE, SIZE)
        length += 1
        score += 1
        snake_speed -= 1
        snake_speed = max(snake_speed, 4)
        eat_sound.play()  # Play the eating sound

    # game over
    if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(snake) != len(set(snake)):
        handle_game_over()

    pygame.display.flip()
    clock.tick(fps)
    close_game()

    # controls
    key = pygame.key.get_pressed()
    if key[pygame.K_w]:
        if dirs['W']:
            dx, dy = 0, -1
            dirs = {'W': True, 'S': False, 'A': True, 'D': True}
    elif key[pygame.K_s]:
        if dirs['S']:
            dx, dy = 0, 1
            dirs = {'W': False, 'S': True, 'A': True, 'D': True}
    elif key[pygame.K_a]:
        if dirs['A']:
            dx, dy = -1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': False}
    elif key[pygame.K_d]:
        if dirs['D']:
            dx, dy = 1, 0
            dirs = {'W': True, 'S': True, 'A': False, 'D': True}

