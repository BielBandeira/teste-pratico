from pygame import Rect
from pgzero.actor import Actor
import pgzrun

WIDTH = 800
HEIGHT = 600
TILE_SIZE = 64
tela_atual = 'menu'
music.play('musica')
bg = Actor('background')
entrar = Rect((200, 50), (400, 100))
volume = Rect((200, 250), (400, 100))
sair = Rect((200, 450), (400, 100))
volume_on = True
vida = 3
chave = False
ganhou = False
perdeu = False
pode_ser_atingido = True
tempo_apos_dano = 0

# Chão e plataformas
platforms = []
block1 = Actor("terrain_stone_cloud_left", (32, 568))
rect1 = Rect(block1.x - TILE_SIZE // 2, block1.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
platforms.append((block1, rect1))

block2 = Actor("terrain_stone_cloud_right", (768, 568))
rect2 = Rect(block2.x - TILE_SIZE // 2, block2.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
platforms.append((block2, rect2))

for x in range(96, 750, 64):
    middle = Actor("terrain_stone_cloud_middle", (x, 568))
    rect = Rect(middle.x - TILE_SIZE // 2, middle.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
    platforms.append((middle, rect))

block1 = Actor("terrain_stone_cloud", (480, 443))
rect1 = Rect(block1.x - TILE_SIZE // 2, block1.y - TILE_SIZE // 2, TILE_SIZE, int(TILE_SIZE * 0.1))
platforms.append((block1, rect1))

block2 = Actor("terrain_stone_cloud", (608, 379))
rect2 = Rect(block2.x - TILE_SIZE // 2, block2.y - TILE_SIZE // 2, TILE_SIZE, int(TILE_SIZE * 0.1))
platforms.append((block2, rect2))

block3 = Actor("terrain_stone_cloud", (480, 315))
rect3 = Rect(block3.x - TILE_SIZE // 2, block3.y - TILE_SIZE // 2, TILE_SIZE, int(TILE_SIZE * 0.1))
platforms.append((block3, rect3))

block4 = Actor("terrain_stone_cloud", (608, 251))
rect4 = Rect(block4.x - TILE_SIZE // 2, block4.y - TILE_SIZE // 2, TILE_SIZE, int(TILE_SIZE * 0.1))
platforms.append((block4, rect4))

block5 = Actor("terrain_stone_cloud", (480, 187))
rect5 = Rect(block5.x - TILE_SIZE // 2, block5.y - TILE_SIZE // 2, TILE_SIZE, int(TILE_SIZE * 0.1))
platforms.append((block5, rect5))

block6 = Actor("terrain_stone_cloud", (380, 143))
rect6 = Rect(block6.x - TILE_SIZE // 2, block6.y - TILE_SIZE // 2, TILE_SIZE, int(TILE_SIZE * 0.1))
platforms.append((block6, rect6))

start_x_top = 32
end_x_top = 290
for x in range(start_x_top, end_x_top, TILE_SIZE):
    middle = Actor("terrain_stone_horizontal_middle", (x, 100))
    rect = Rect(middle.x - TILE_SIZE // 2, middle.y - TILE_SIZE // 2, TILE_SIZE, int(TILE_SIZE * 0.1))
    platforms.append((middle, rect))

block_overhang_right = Actor("terrain_stone_horizontal_overhang_right", (310, 100))
rect_overhang = Rect(block_overhang_right.x - TILE_SIZE // 2, block_overhang_right.y - TILE_SIZE // 2, TILE_SIZE, int(TILE_SIZE * 0.1))
platforms.append((block_overhang_right, rect_overhang))

# Porta e chave
door = Actor("door", (32, 36))
door_rect = Rect(door.x - TILE_SIZE // 2, door.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)

key = Actor("key", (768, 504))
key_rect = Rect(key.x - TILE_SIZE // 2, key.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)

# classes
class Inimigo:
    def __init__(self, images, pos, speed, x_limits, rect_offset):
        self.frames = images
        self.index = 0
        self.timer = 0
        self.interval = 10
        self.direction = 1
        self.speed = speed
        self.actor = Actor(images[0], pos)
        self.rect_offset = rect_offset
        self.x_limits = x_limits

    def get_rect(self):
        width, height, off_x, off_y = self.rect_offset
        return Rect(self.actor.x - width // 2, self.actor.y + off_y, width, height)

    def update(self):
        self.actor.x += self.direction * self.speed
        if self.actor.x < self.x_limits[0] or self.actor.x > self.x_limits[1]:
            self.direction *= -1

        self.timer += 1
        if self.timer >= self.interval:
            self.timer = 0
            self.index = (self.index + 1) % len(self.frames)
            self.actor.image = self.frames[self.index]

    def draw(self):
        self.actor.draw()


class Heroi:
    def __init__(self, pos, rect_size, animations):
        self.actor = Actor(animations['parado'][0], pos)
        self.width, self.height, self.off_x, self.off_y = rect_size
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_force = -11
        self.on_ground = False
        self.animations = animations
        self.index = 0
        self.timer = 0
        self.interval = 20

    def get_rect(self):
        return Rect(self.actor.x - self.width // 2, self.actor.y + self.off_y, self.width, self.height)

    def update(self):
        self.velocity_y += self.gravity
        self.actor.y += self.velocity_y
        self.on_ground = False

        hero_rect = self.get_rect()
        for _, plat_rect in platforms:
            if hero_rect.colliderect(plat_rect) and self.velocity_y >= 0:
                self.actor.y = plat_rect.top - (TILE_SIZE // 2) + 1
                self.velocity_y = 0
                self.on_ground = True
                break

        if keyboard.up and self.on_ground:
            self.velocity_y = self.jump_force
        if keyboard.left:
            self.actor.x -= 5
        if keyboard.right:
            self.actor.x += 5

        self.actor.x = max(20, min(780, self.actor.x))

        self.timer += 1
        if self.timer >= self.interval:
            self.timer = 0
            if self.velocity_y < 0 or not self.on_ground:
                self.actor.image = self.animations['pulando'][0]
            elif keyboard.left or keyboard.right:
                self.index = (self.index + 1) % len(self.animations['andando'])
                self.actor.image = self.animations['andando'][self.index]
            else:
                self.index = (self.index + 1) % len(self.animations['parado'])
                self.actor.image = self.animations['parado'][self.index]

    def draw(self):
        self.actor.draw()

# objtetos do jogo
player = Heroi(
    (32, 350),
    (int(TILE_SIZE * 0.4), int(TILE_SIZE * 0.1), TILE_SIZE // -2, TILE_SIZE // 2 - int(TILE_SIZE * 0.1)),
    {
        'parado': ["character_green_front", "character_green_duck"],
        'andando': ["character_green_walk_a", "character_green_walk_b"],
        'pulando': ["character_green_jump"]
    }
)

largata1 = Inimigo(
    ["worm_ring_move_a", "worm_ring_move_b"],
    (96, 36),
    1.5,
    (96, 280),
    (TILE_SIZE, int(TILE_SIZE * 0.53), TILE_SIZE // -2, TILE_SIZE // 2 - int(TILE_SIZE * 0.53))
)

largata2 = Inimigo(
    ["worm_ring_move_a", "worm_ring_move_b"],
    (704, 504),
    1,
    (32, 768),
    (TILE_SIZE, int(TILE_SIZE * 0.8), TILE_SIZE // -2, TILE_SIZE // 2 - int(TILE_SIZE * 0.8))
)

# função para reiniciar o jogo
def reiniciar_jogo():
    global tela_atual, perdeu, ganhou, vida, chave
    tela_atual = 'menu'
    perdeu = False
    ganhou = False
    vida = 3
    chave = False
    player.actor.x = 32
    player.actor.y = 350
    largata1.actor.x = 96
    largata2.actor.x = 704

#eventos
def on_mouse_down(pos):
    global volume_on, tela_atual

    if entrar.collidepoint(pos):
        tela_atual = 'jogo'

    if volume.collidepoint(pos):
        if volume_on:
            volume_on = False
            music.pause()
        else:
            volume_on = True
            music.unpause()

    if sair.collidepoint(pos):
        exit()

#loop
def update():
    global vida, chave, ganhou, perdeu, tela_atual, pode_ser_atingido, tempo_apos_dano

    if tela_atual != 'jogo':
        return
    if perdeu or ganhou:
        return  

    player.update()
    largata1.update()
    largata2.update()
    player_rect = player.get_rect()
    largata_rect = largata1.get_rect()
    largata2_rect = largata2.get_rect()

    if (player_rect.colliderect(largata_rect) or player_rect.colliderect(largata2_rect)) and pode_ser_atingido:
        vida -= 1
        pode_ser_atingido = False
        tempo_apos_dano = 0

    if not pode_ser_atingido:
        tempo_apos_dano += 1
        if tempo_apos_dano >= 60:
            pode_ser_atingido = True

    if player_rect.colliderect(key_rect):
        chave = True

    if chave and player_rect.colliderect(door_rect) and not ganhou:
        ganhou = True
        perdeu = False
        clock.schedule_unique(reiniciar_jogo, 3)

    if vida <= 0 and not perdeu:
        perdeu = True
        ganhou = False
        clock.schedule_unique(reiniciar_jogo, 3)

def draw():
    if tela_atual == 'menu':
        bg.draw()
        screen.draw.filled_rect(entrar, "gray")
        screen.draw.text("JOGAR", center=entrar.center, fontname='pixel', fontsize=30, color="white")

        screen.draw.filled_rect(volume, "gray" if volume_on else "darkred")
        screen.draw.text("SOM", center=volume.center, fontname='pixel', fontsize=30, color="white")

        screen.draw.filled_rect(sair, "gray")
        screen.draw.text("SAIR", center=sair.center, fontname='pixel', fontsize=30, color="white")

    elif tela_atual == 'jogo':
        bg.draw()
        for bloco, rect in platforms:
            bloco.draw()
        door.draw()
        if not chave:
            key.draw()
        largata1.draw()
        largata2.draw()

        if not pode_ser_atingido:
            if (tempo_apos_dano // 5) % 2 == 0:
             player.draw()
        else:
            player.draw()

        screen.draw.text(f"Vida: {vida}", (650, 10), fontname='pixel', fontsize=15, color="gray")

    if ganhou:
     screen.draw.text("Vitoria", center=(WIDTH // 2, HEIGHT // 2), fontname='pixel', fontsize=80, color="white")
    elif perdeu:
     screen.draw.text("Derrota", center=(WIDTH // 2, HEIGHT // 2), fontname='pixel', fontsize=80, color="white")

pgzrun.go()
