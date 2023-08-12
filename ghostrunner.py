import pygame
import random
import pygame.font 
import sys
pygame.init()

easter_egg = 0
pygame.mixer.music.load("assets/background_song.mp3")
pygame.mixer.music.play(-1)  # Play in an infinite loop
score_taken_sound = pygame.mixer.Sound("assets/score_taken.wav")
coin_sound = pygame.mixer.Sound("assets/coin.wav")
font_path = "assets/font.ttf"
score = 0
screen_width = 800
screen_height = 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
border_size = 5
font = pygame.font.Font(font_path, 36)  # Choose font and size
background_color = (0, 0, 0)
button_color = (255, 255, 255)
background_image = pygame.image.load("assets/background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

BAT_SPEED = 3


class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/ghost.png")
        self.original_image_mirror = pygame.image.load("assets/ghost_mirror.png")
        self.scale_factor = 4
        self.image = pygame.transform.scale(self.original_image, (16 * self.scale_factor, 16 * self.scale_factor))
        self.rect = self.image.get_rect()
        self.rect.center = (100, screen_height // 1.1)
        self.speed = 6

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if self.rect.left - self.speed >= border_size:
                self.rect.x -= self.speed
                self.image = pygame.transform.scale(self.original_image_mirror, (16 * self.scale_factor, 16 * self.scale_factor))
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if self.rect.right + self.speed <= screen_width - border_size:
                self.rect.x += self.speed
                self.image = pygame.transform.scale(self.original_image, (16 * self.scale_factor, 16 * self.scale_factor))
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if self.rect.top - self.speed >= border_size:
                self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if self.rect.bottom + self.speed <= screen_height - border_size:
                self.rect.y += self.speed
         

def start_game():
    global game_started
    game_started = True

class Bat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/bat.gif")  # Load bat image
        self.image = pygame.transform.scale(self.image, (64, 32))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))
        self.speed = BAT_SPEED  # Add random speed to each bat
        self.direction_x = random.choice([-1, 1])  # Randomly choose left or right direction
        self.direction_y = random.choice([-1, 1])  # Randomly choose up or down direction

    def update(self):
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.speed * self.direction_y
        
        # Check for collision with screen edges and change direction
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.direction_x *= -1  # Change x direction when hitting screen edge
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.direction_y *= -1  # Change y direction when hitting screen edge
            
        # Ensure the bat stays within the screen bounds
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, screen_height - self.rect.height))

bats = pygame.sprite.Group()
for _ in range(5):
    bat = Bat()
    bats.add(bat)

class Gravestone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/gravestone.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))

gravestones = pygame.sprite.Group()
for _ in range(3):
    gravestone = Gravestone()
    gravestones.add(gravestone)

my_sprite = Ghost()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    my_sprite.update()


    screen.blit(background_image, (0, 0))
    screen.blit(my_sprite.image, my_sprite.rect.topleft)

    for gravestone in gravestones:
        screen.blit(gravestone.image, gravestone.rect.topleft)

    # Check for collision with gravestones
    gravestones_hit = pygame.sprite.spritecollide(my_sprite, gravestones, True)
    for _ in gravestones_hit:
        new_gravestone = Gravestone()
        score += 1
        BAT_SPEED += 0.01  # Increase bat speed
        coin_sound.play()  # Play the coin sound effect        
        gravestones.add(new_gravestone)
    
    for bat in bats:
        bat.speed = BAT_SPEED
        bat.update()
        screen.blit(bat.image, bat.rect.topleft)
    
    # Check for collision with bats
        if my_sprite.rect.colliderect(bat.rect):
            score -= 10
            bat.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))  # Reposition the bat
            score_taken_sound.play()  # Play the collision sound effect
    
    # Easter egg logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_t]:
            easter_egg = 1
        if easter_egg == 1 and keys[pygame.K_o]:
            easter_egg = 2
        if easter_egg == 2 and keys[pygame.K_m]:
            easter_egg = 3
        if easter_egg == 3 and keys[pygame.K_a]:
            easter_egg = 4
        if easter_egg == 4 and keys[pygame.K_s]:
            easter_egg = 0
            score += 150


    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, screen_width, border_size))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, screen_height - border_size, screen_width, border_size))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, border_size, screen_height))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screen_width - border_size, 0, border_size, screen_height))
    if score < 0:
        score = 0
    if score < 33:
        text = font.render(f"Score = {score}", True, (255, 255, 255))
    if score >= 50:
        text = font.render(f"Score = {score}★", True, (255, 255, 255))
    if score >= 100:
        text = font.render(f"Score = {score}★★", True, (255, 255, 255))
    if score >= 200:
        text = font.render(f"Score = {score}★★★", True, (255, 255, 255))

    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 20))
    clock.tick(60)  # Control the frame rate
    pygame.display.update()

pygame.quit()
