import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
DELTA = { # 辞書の作成
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

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # こうかとん初期化
    bg_img = pg.image.load("fig/campas.jpg")   
    scale=0.9
    kk_base_img=pg.image.load("fig/3.png")
    kk_img = pg.transform.rotozoom(kk_base_img, 0, scale)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 550, 500
    
    clock = pg.time.Clock()
    tmr = 0
    speed = 1 
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        #右上の時間表示count up (以下四文、消していいよ)
        font = pg.font.Font(None, 50) 
        elapsed_time = tmr // 50 
        time_text = font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))  
        screen.blit(time_text, (50, 30))

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] # 左右方向
                sum_mv[1] += mv[1] # 上下方向
        sum_mv[0] *= speed
        sum_mv[1] *= speed

        elapsed_sec = tmr // 50
        scale = 0.9 + 0.2 * (elapsed_sec // 20)  # 10秒ごとにサイズアップ
        kk_img = pg.transform.rotozoom(kk_base_img, 0, scale)
        kk_rct = kk_img.get_rect(center=kk_rct.center) 
        

        # obj_wall1 = pg.transform.rotozoom(obj_base_wall1, 0, scale)
        # obj_wall2 = pg.transform.rotozoom(obj_base_wall2, 0, scale)
        # obj_wall3 = pg.transform.rotozoom(obj_base_wall3, 0, scale)
        # obj_wall1_rect = obj_wall1.get_rect(center=obj_wall1_rect.center) 
        # obj_wall2_rect = obj_wall2.get_rect(center=obj_wall2_rect.center) 
        # obj_wall3_rect = obj_wall3.get_rect(center=obj_wall3_rect.center) 

        speed = 1 + elapsed_sec // 10

    

        kk_rct.move_ip(sum_mv) # こうかとんの移動
        if check_bound(kk_rct) != (True, True): # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面内に戻す
        screen.blit(kk_img, kk_rct)
      
      
        
       
        
        pg.display.update()
        tmr += 1
        clock.tick(50)
        

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
