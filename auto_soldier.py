import pygame
import primary


class Soldier_auto(pygame.sprite.Sprite):
    def __init__(self, pos, v, team, hp, bullet_groups):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        # картинка
        self.frames = []
        self.cut_sheet(primary.load_image("soldier_auto.png"), 8, 1)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.rect.width = self.rect.width * primary.scale
        self.rect.height = self.rect.height * primary.scale
        # обьект выстрела и пули
        self.shot = Soldier_shot(self.team)
        self.bullet_groups = bullet_groups
        # обьект дистанции выстрела
        self.range = Range(600, self.team, 'auto')
        # обьект здоровья
        self.hp = hp
        # скорость px / сек
        self.v = v
        # расстояние px / кадр
        self.px = 0
        # счетчик итераций
        self.counter = 0

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

    def update(self, ground_arg):
        self.counter += 1
        # обновление дистанции выстрела
        self.range.update(self.rect.centerx, self.rect.centery)
        # движение или стрельба
        if self.range.move:
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
            if self.counter % 25 == 0:
                self.shot.shoot()
                if self.team == 0:
                    bullet = Soldier_bullet(
                        (self.rect.centerx + (70 * primary.scale), self.rect.centery + (-17 * primary.scale)),
                        self.team)
                    for group in self.bullet_groups:
                        group.add(bullet)
                else:
                    bullet = Soldier_bullet(
                        (self.rect.centerx - (70 * primary.scale), self.rect.centery + (-17 * primary.scale)),
                        self.team)
                    for group in self.bullet_groups:
                        group.add(bullet)
            else:
                self.shot.clear_shoot()

        self.range.move = True

        if not pygame.sprite.collide_mask(self, ground_arg):
            self.rect = self.rect.move(0, 1)
        else:
            self.rect = self.rect.move(0, -1)

        self.shot.updt(self.rect.centerx - 5, self.rect.centery)

        # картинка
        self.image = pygame.transform.scale(self.frames[self.cur_frame],
                                            (int(100 * primary.scale), int(135 * primary.scale)))
        if self.team != 0:
            self.image = pygame.transform.flip(self.image, True, False)

        # иконка здоровья
        if self.team == 0:
            self.hp.updt(self.rect.centerx - 5, self.rect.bottom)
        else:
            self.hp.updt(self.rect.centerx + 10, self.rect.bottom)

        # получение урона
        if self.hp.isdead():
            self.shot.kill()
            self.kill()


class Soldier_shot(pygame.sprite.Sprite):
    def __init__(self, team):
        pygame.sprite.Sprite.__init__(self)
        self.team = team
        self.image = pygame.transform.scale(primary.load_image('soldier_shot.png'),
                                            (int(10 * 2.3 * primary.scale), int(10 * primary.scale)))
        self.image.fill(primary.transparent)
        self.rect = self.image.get_rect()

    def updt(self, x, y):
        if self.team == 0:
            self.rect.x = x + (70 * primary.scale)
            self.rect.y = y + (-17 * primary.scale)
        else:
            self.rect.x = x - (55 * primary.scale)
            self.rect.y = y + (-17 * primary.scale)

    def shoot(self):
        self.image = pygame.transform.scale(primary.load_image('soldier_shot.png'),
                                            (int(15 * 2.3 * primary.scale), int(20 * primary.scale)))
        if self.team != 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def clear_shoot(self):
        self.image.fill(primary.transparent)


class Soldier_bullet(pygame.sprite.Sprite):
    def __init__(self, pos, team):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(primary.load_image('soldier_bullet.png'),
                                            (int(10 * 2.3 * primary.scale), int(10 * primary.scale)))
        self.team = team
        if self.team != 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]

        # скорость px / сек
        self.v = 1000
        # расстояние px / кадр
        self.px = self.v / primary.FPS

    def name(self):
        return 'bullet'

    def update(self, ground_arg):
        if self.team == 0:
            self.rect = self.rect.move(self.px, 0)
        else:
            self.rect = self.rect.move(-self.px, 0)

        if self.rect.right < 0 or self.rect.x > 1536 or pygame.sprite.collide_mask(self, ground_arg):
            self.kill()


class Range(pygame.sprite.Sprite):
    def __init__(self, rng, team, nm):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((int(rng * primary.scale), 2))
        self.rect = self.image.get_rect()
        self.team = team
        self.nm = nm
        self.move = True

    def update(self, x, y):
        self.rect.y = y
        if self.team == 0:
            self.rect.x = x
        else:
            self.rect.x = x - self.rect.width

    def name(self):
        return self.nm
