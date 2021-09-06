import pygame
import primary


class Soldier_knife(pygame.sprite.Sprite):
    def __init__(self, pos, v, team, hp):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        # картинка
        self.frames = []
        self.cut_sheet(primary.load_image("soldier_knife.png"), 8, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.rect.width = self.rect.width * primary.scale
        self.rect.height = self.rect.height * primary.scale
        # обьект удара
        self.attack = Soldier_attack(self.team)
        # обьект здоровья
        self.hp = hp
        # скорость px / сек
        self.v = v
        # расстояние px / кадр
        self.px = 0
        # счетчик итераций
        self.counter = 0
        # движение
        self.move = True

    # создает список спрайтов
    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def hit(self, value):
        self.hp -= value

    def name(self):
        return 'knife'

    def update(self, ground_arg):
        self.counter += 1
        # движение или стрельба
        if self.move:
            self.px += self.v / primary.FPS
            if self.px >= 1:
                if self.team == 0:
                    self.rect = self.rect.move(self.px, 0)
                else:
                    self.rect = self.rect.move(-self.px, 0)
                self.px = 0
            # обновление спрайта
            if self.counter % 3 == 0:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        else:
            self.cur_frame = 0
            if self.counter % 20 == 0:
                self.attack.hit()

        self.move = True

        if self.counter % 25 == 0:
            self.attack.clear_hit()

        if not pygame.sprite.collide_mask(self, ground_arg):
            self.rect = self.rect.move(0, 1)
        else:
            self.rect = self.rect.move(0, -1)

        self.attack.updt(self.rect.centerx - 5, self.rect.centery)

        # картинка
        self.image = pygame.transform.scale(self.frames[self.cur_frame],
                                            (int(76 * primary.scale), int(135 * primary.scale)))
        if self.team != 0:
            self.image = pygame.transform.flip(self.image, True, False)

        # иконка здоровья
        if self.team == 0:
            self.hp.updt(self.rect.centerx - 5, self.rect.bottom)
        else:
            self.hp.updt(self.rect.centerx + 10, self.rect.bottom)

        # получение урона
        if self.hp.isdead():
            self.attack.kill()
            self.kill()


class Soldier_attack(pygame.sprite.Sprite):
    def __init__(self, team):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.image = pygame.transform.scale(primary.load_image('knife_hit.png'), (0, 0))
        self.image.fill(primary.transparent)
        self.rect = self.image.get_rect()

    def updt(self, x, y):
        if self.team == 0:
            self.rect.x = x + (60 * primary.scale)
            self.rect.y = y + (-30 * primary.scale)
        else:
            self.rect.x = x - (60 * primary.scale)
            self.rect.y = y + (-30 * primary.scale)

    def hit(self):
        self.image = pygame.transform.scale(primary.load_image('knife_hit.png'),
                                            (int(25 * primary.scale), int(60 * primary.scale)))
        if self.team != 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def clear_hit(self):
        self.image.fill(primary.transparent)
