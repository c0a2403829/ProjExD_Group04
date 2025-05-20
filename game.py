import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
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
    kk_rct.center = 300, 200
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
                sum_mv[1] += mv[1] # 上下方向
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
