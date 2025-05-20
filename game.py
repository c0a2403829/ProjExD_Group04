import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 600, 800
DELTA = { # 辞書の作成
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}
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

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]: # 爆弾拡大、加速機能
    b_img = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        b_img.append(bb_img)
    return b_img, bb_accs
"""
def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    kk_dict = {
        (0, -5): kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 270, 0.9),
        (+5, -5): kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 315, 0.9),
        (+5, 0): kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),
    }
    if sum_mv == [0, -5]:
        return
"""

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # こうかとん初期化
    bg_img = pg.image.load("fig/campas.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 700
    """
    # 爆弾初期化
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5 # 爆弾の速度
    """
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        """
         # 爆弾の拡大、加速
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_img.set_colorkey((0, 0, 0))

         # こうかとんRectと爆弾Rectが重なっていたら
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            time.sleep(5)
            return
        """
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] # 左右方向
                #sum_mv[1] += mv[1] # 上下方向
        """"
        if key_lst[pg.K_UP]:
            sum_mv[1] -= 5
        if key_lst[pg.K_DOWN]:
            sum_mv[1] += 5
        if key_lst[pg.K_LEFT]:
            sum_mv[0] -= 5
        if key_lst[pg.K_RIGHT]:
            sum_mv[0] += 5
        """

        kk_rct.move_ip(sum_mv) # こうかとんの移動
        if check_bound(kk_rct) != (True, True): # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面内に戻す
        screen.blit(kk_img, kk_rct)
        """"""
        # #bb_rct.move_ip(avx, avy) # 爆弾の移動 
        # yoko, tate = check_bound(bb_rct)
        # if not yoko: # 左右どちらかにはみ出ていたら
        #     vx *= -1
        # if not tate: # 上下どちらかにはみ出ていたら
        #     vy *= -1
        
        #screen.blit(bb_img, bb_rct) # 爆弾の表示
        pg.display.update()
        tmr += 1
        clock.tick(50)
        

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
# import os
# import random
# import sys
# import time
# import pygame as pg


# WIDTH = 650  # ゲームウィンドウの幅
# HEIGHT = 110  # ゲームウィンドウの高さ
# NUM_OF_BOMBS = 5  # 爆弾の個数
# os.chdir(os.path.dirname(os.path.abspath(__file__)))


# class Bird:
#     """
#     ゲームキャラクター（こうかとん）に関するクラス
#     """
#     delta = {  # 押下キーと移動量の辞書
#         pg.K_UP: (0, -5),
#         pg.K_DOWN: (0, +5),
#         pg.K_LEFT: (-5, 0),
#         pg.K_RIGHT: (+5, 0),
#     }
#     img0 = pg.transform.rotozoom(pg.image.load("fig/campus.jpg"), 0, 0.9)
#     img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
#     imgs = {  # 0度から反時計回りに定義
#         (+5, 0): img,  # 右
#         (+5, -5): pg.transform.rotozoom(img, 45, 0.9),  # 右上
#         (0, -5): pg.transform.rotozoom(img, 90, 0.9),  # 上
#         (-5, -5): pg.transform.rotozoom(img0, -45, 0.9),  # 左上
#         (-5, 0): img0,  # 左
#         (-5, +5): pg.transform.rotozoom(img0, 45, 0.9),  # 左下
#         (0, +5): pg.transform.rotozoom(img, -90, 0.9),  # 下
#         (+5, +5): pg.transform.rotozoom(img, -45, 0.9),  # 右下
#     }

#     def __init__(self, xy: tuple[int, int]):
#         """
#         こうかとん画像Surfaceを生成する
#         引数 xy：こうかとん画像の初期位置座標タプル
#         """
#         self.img = __class__.imgs[(+5, 0)]
#         self.rct: pg.Rect = self.img.get_rect()
#         self.rct.center = xy

#     def change_img(self, num: int, screen: pg.Surface):
#         """
#         こうかとん画像を切り替え，画面に転送する
#         引数1 num：こうかとん画像ファイル名の番号
#         引数2 screen：画面Surface
#         """
#         self.img = pg.transform.rotozoom(pg.image.load(f"fig/{num}.png"), 0, 0.9)
#         screen.blit(self.img, self.rct)

#     def update(self, key_lst: list[bool], screen: pg.Surface):
#         """
#         押下キーに応じてこうかとんを移動させる
#         引数1 key_lst：押下キーの真理値リスト
#         引数2 screen：画面Surface
#         """
#         sum_mv = [0, 0]
#         for k, mv in __class__.delta.items():
#             if key_lst[k]:
#                 sum_mv[0] += mv[0]
#                 sum_mv[1] += mv[1]
#         self.rct.move_ip(sum_mv)
#         if check_bound(self.rct) != (True, True):
#             self.rct.move_ip(-sum_mv[0], -sum_mv[1])
#         if not (sum_mv[0] == 0 and sum_mv[1] == 0):
#             self.img = __class__.imgs[tuple(sum_mv)]
#         screen.blit(self.img, self.rct)

      
# def main():
#     pg.display.set_caption("たたかえ！こうかとん")
#     screen = pg.display.set_mode((WIDTH, HEIGHT))    
#     bg_img = pg.image.load("fig/campus.jpg")
#     bird = Bird((300, 200))
#     tmr = 0
#     while True:
        
        
#         pg.display.update()


# if __name__ == "__main__":
#     pg.init()
#     main()
#     pg.quit()
#     sys.exit()
