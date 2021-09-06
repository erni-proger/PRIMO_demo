import pygame

import sys
import os
import primary

from knife_soldier import Soldier_knife
from auto_soldier import Soldier_auto

all_sprites = pygame.sprite.Group()
military_group = pygame.sprite.Group()
ground_group = pygame.sprite.Group()
allies_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
deadly_group = pygame.sprite.Group()
effect_group = pygame.sprite.Group()
range_group = pygame.sprite.Group()


def hitting():
    hits = pygame.sprite.groupcollide(deadly_group, military_group, False, False)
    if hits:
        for key in hits:
            if key.name() == 'bullet':
                for military in hits[key]:
                    if military.team != key.team:
                        military.hit(5)
                        key.kill()
            if key.name() == 'knife':
                for military in hits[key]:
                    if military.team != key.team:
                        military.hit(1)


def moving():
    col = pygame.sprite.groupcollide(range_group, military_group, False, False)
    if col:
        for key in col:
            if key.name() == 'knife':
                for target in col[key]:
                    if key.team != target.team:
                        key.move = False
            if key.name() == 'auto':
                for target in col[key]:
                    if key.team != target.team:
                        key.move = False


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Health:
    def __init__(self, health):
        self.init_hp = health
        self.hp = health

    def updt(self, x, y):
        if self.hp / self.init_hp < 0.3:
            pygame.draw.rect(screen, (255, 0, 0),
                             (x - (0.5 * self.hp * primary.scale * 2), y + (25 * primary.scale),
                              self.hp * primary.scale * 2, 4), 1)

        elif self.hp / self.init_hp < 0.7:
            pygame.draw.rect(screen, (255, 255, 0),
                             (x - (0.5 * self.hp * primary.scale * 2), y + (25 * primary.scale),
                              self.hp * primary.scale * 2, 4), 1)
        else:
            pygame.draw.rect(screen, (0, 255, 0),
                             (x - (0.5 * self.hp * primary.scale * 2), y + (25 * primary.scale),
                              self.hp * primary.scale * 2, 4), 1)

    def __sub__(self, other):
        self.hp -= other
        return self

    def isdead(self):
        if self.hp <= 0:
            return True
        return False


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(ground_group)
        self.y = -50
        self.image = load_image('ground.png')
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.rect.move(0, self.y)


def add_soldier_knife(team):
    unit = Soldier_knife(pygame.mouse.get_pos(), 25, team, Health(50))
    all_sprites.add(unit)
    military_group.add(unit)
    deadly_group.add(unit)
    effect_group.add(unit.attack)
    range_group.add(unit)
    if team == 0:
        allies_group.add(unit)
    else:
        enemy_group.add(unit)


def add_soldier_auto(team):
    unit = Soldier_auto(pygame.mouse.get_pos(), 25, team, Health(50), (all_sprites, deadly_group))
    all_sprites.add(unit)
    military_group.add(unit)
    range_group.add(unit.range)
    effect_group.add(unit.shot)
    if team == 0:
        allies_group.add(unit)
    else:
        enemy_group.add(unit)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    ground = Ground()
    pygame.init()
    pygame.display.Info()
    current_w = pygame.display.Info().current_w
    current_h = pygame.display.Info().current_h
    size = width, height = current_w, 700
    pygame.display.set_caption('PRIMO v-0.001')
    screen = pygame.display.set_mode(size)
    background = pygame.transform.scale(load_image('bg.png'), (current_w, current_h))
    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(ground.image, (0, ground.y))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == 49:
                    add_soldier_knife(0)
                if event.key == 1073741913:
                    add_soldier_knife(1)
                if event.key == 50:
                    add_soldier_auto(0)
                if event.key == 1073741914:
                    add_soldier_auto(1)

            if event.type == pygame.QUIT:
                sys.exit()
        all_sprites.update(ground)
        effect_group.update()
        hitting()
        moving()
        all_sprites.draw(screen)
        effect_group.draw(screen)
        clock.tick(primary.FPS)
        pygame.display.flip()

    pygame.quit()
