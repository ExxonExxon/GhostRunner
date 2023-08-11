import pygame
import random
import pygame.font 
pygame.init()

score = 0
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
border_size = 5
font = pygame.font.Font(None, 36)  # Choose font and size

background_image = pygame.image.load("background.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

class Ghost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("ghost.png")
        self.original_image_mirror = pygame.image.load("ghost_mirror.png")
        self.scale_factor = 4
        self.image = pygame.transform.scale(self.original_image, (16 * self.scale_factor, 16 * self.scale_factor))
        self.rect = self.image.get_rect()
        self.rect.center = (100, screen_height // 1.1)
        self.speed = 0.51

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

class Gravestone(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("gravestone.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))

class AIGhost(pygame.sprite.Sprite):
    def __init__(self, target):
        super().__init__()
        self.original_image = pygame.image.load("ai_ghost.png")
        self.scale_factor = 4
        self.image = pygame.transform.scale(self.original_image, (16 * self.scale_factor, 16 * self.scale_factor))
        self.rect = self.image.get_rect()
        self.target = target  # The target is the player-controlled ghost
        # Additional attributes for AI logic

gravestones = pygame.sprite.Group()
for _ in range(10):
    gravestone = Gravestone()
    gravestones.add(gravestone)

my_sprite = Ghost()
ai_ghost = AIGhost(Ghost)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
        gravestones.add(new_gravestone)
    
    # Check for collision with AI ghost
    if pygame.sprite.collide_rect(Ghost, ai_ghost):
        # Reset game elements and restart the game
        score = 0
        Ghost.rect.center = (100, screen_height // 1.1)
        ai_ghost.rect.center = (random.randint(0, screen_width), random.randint(0, screen_height))

    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, screen_width, border_size))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, screen_height - border_size, screen_width, border_size))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(0, 0, border_size, screen_height))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screen_width - border_size, 0, border_size, screen_height))
    text = font.render(f"Score = {score}", True, (255, 255, 255))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2, 20))
    pygame.display.update()

pygame.quit()
