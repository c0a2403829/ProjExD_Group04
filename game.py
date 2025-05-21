import os
import random
import sys
import time
import pygame as pg


DELTA = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }
WIDTH, HEIGHT = 600, 800
clock = pg.time.Clock()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横、縦）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True # 横、縦方向用の変数
    # 横方向判定
    if rct.left < 0 or WIDTH < rct.right: # 画面内だったら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 画面外だったら
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None: # ゲームオーバー機能
    bg_rct = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_rct,(0,0,0),(0,0,WIDTH,HEIGHT))
    bg_rct.set_alpha(150)
    screen.blit(bg_rct,[0, 0])
    fonto = pg.font.Font(None, 70)
    txt = fonto.render("Game Over",True, (255, 255, 255))
    screen.blit(txt, [450, 325])
    ck_img =pg.image.load("fig/4.png")
    screen.blit(ck_img,[400,325])
    screen.blit(ck_img,[720,325])
    pg.display.update()


class Bird:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数 xy：こうかとん画像の初期位置座標タプル
        """
        self.img = pg.image.load("fig/3.png")
        self.rct: pg.Rect = self.img.get_rect()
        self.rct.center = xy

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = __class__.imgs[tuple(sum_mv)]
        screen.blit(self.img, self.rct)


# class Player:
#     def __init__(self, x, y):
#         self.img = pg.image.load("fig/3.png")
#         self.rct: pg.Rect = self.img.get_rect()
#         self.rct.center = x,y
#         self.base_speed = 5
#         self.speed = self.base_speed
#         self.boost_timer = 0

#     def update(self):
#         # スピードアップ効果の時間管理
#         if self.boost_timer > 0:
#             self.boost_timer -= clock.get_time()
#             if self.boost_timer <= 0:
#                 self.speed = self.base_speed

#     def boost(self, duration_ms):
#         self.speed = self.base_speed * 2
#         self.boost_timer = duration_ms


class Item:
    """
    アイテムに関するクラス
    """
    def __init__(self, x, y, image_path, fall_speed=5):
        self.image = pg.transform.scale(pg.image.load(image_path).convert_alpha(),(50,45))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.active = True
        self.fall_speed = fall_speed

    def update(self):
        """アイテムを下に移動させる"""
        if self.active:
            self.rect.y += self.fall_speed

    def apply_effect(self ):
        """個別アイテムで上書きする"""
        pass

    def draw(self, surface):
        if self.active:
            surface.blit(self.image, self.rect)

class Juice(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "fig/juice.png")

    def apply_effect(self, player_rect, now, state):
        if self.active and self.rect.colliderect(player_rect):
            state["speed"] = 6
            state["boost_timer"] = now + 5000
            self.active = False

class Timer(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "fig/timer.png")

    def apply_effect(self, player_rect, now, state):
         if self.active and self.rect.colliderect(player_rect):
            state["speed"] = 0.5
            state["slow_timer"] = now + 3000
            self.active = False

class Mirror(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "fig/mirror.png")

    def apply_effect(self, player_rect, now, state):
        if self.active and self.rect.colliderect(player_rect):
            state["is_mirrored"] = True
            state["mirror_timer"] = now + 3000  # 5秒後に戻す
            self.active = False

class Shield(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "fig/shield.png")

    def apply_effect(self, player_rect, now, state):
        if self.active and self.rect.colliderect(player_rect):
            state["has_shield"] = True
            self.active = False


# class Hamburger(Item):
#     def __init__(self, x, y):
#         super().__init__(x, y, "fig/hamburger.png")

#     def apply_effect(self, player):
#         if self.active and self.rect.colliderect(player.rect):
#             print("Healed!")
#             self.active = False


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # こうかとん初期化
    bg_img = pg.image.load("fig/campas.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 700
    items = []
    # 状態管理用の辞書（ブースト/鈍足/ミラーなど共通）
    state = {
    "speed": 3,
    "boost_timer": 0,
    "slow_timer": 0,
    "is_mirrored": False,
    "mirror_timer": 0,
    "has_shield": False
}

    # 定期出現用のタイマー
    SPAWN_INTERVAL = 3000
    last_spawn_time = pg.time.get_ticks()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        now = pg.time.get_ticks()
         # 一定時間後に速度を元に戻す
        if state["boost_timer"] != 0 and now > state["boost_timer"]:
            state["speed"] = 3
            state["boost_timer"] = 0
        if state["slow_timer"] != 0 and now > state["slow_timer"]:
            state["speed"] = 3
            state["slow_timer"] = 0
        if state["mirror_timer"] != 0 and now > state["mirror_timer"]:
            state["is_mirrored"] = False
            state["mirror_timer"] = 0
        # 一定時間ごとにランダムなアイテムを生成
        if now - last_spawn_time > SPAWN_INTERVAL:
            x = random.randint(0, WIDTH - 50)
            # 確率に応じて選択
            r = random.random()  # 0〜1の乱数を取得
            if r < 0.45:
                item = Juice(x, -40)
            elif r < 0.85:
                item = Timer(x, -40)
            elif r < 0.95:
                item = Mirror(x, -40)
            else:
                item = Shield(x, -40)
            items.append(item)
            # elif item_type == 'hamburger':
            #     items.append(Hamburger(x, -40))
            last_spawn_time = now
    
        # こうかとんの操作
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] * state["speed"]# 左右方向
                if state["is_mirrored"]:
                    sum_mv[0] = -sum_mv[0]  # 反転
        kk_rct.move_ip(sum_mv) # 移動
        if check_bound(kk_rct) != (True, True): # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面内に戻す
        screen.blit(kk_img, kk_rct)

        if state["has_shield"]:
            # s_img = pg.transform.scale(pg.image.load("fig/shield.png").convert_alpha(),(50,45))
            # s_rct = s_img.get_rect()
            # screen.blit(s_img, s_rct)
            font = pg.font.Font(None, 40)
            txt = font.render("SHIELD ON", True, (255, 255, 0))
            screen.blit(txt, (10, 10))

        for item in items:
            item.update()
            item.apply_effect(kk_rct, now, state)
            item.draw(screen)
        items = [item for item in items if item.rect.y < HEIGHT and item.active]

        pg.display.update()
        tmr += 1
        clock.tick(50)
        

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
