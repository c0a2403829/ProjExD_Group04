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
survive_time = 0
 # 変数survive_timeは他のメンバーが作成するため後で削除

class Bomb: # 本来は壁が降ってくるが他のメンバーの担当のため衝突判定の代用(マージ時に消す)
    """
    爆弾に関するクラス
    """
    def __init__(self, color: tuple[int, int, int], rad: int):
        """
        引数に基づき爆弾円Surfaceを生成する
        引数1 color：爆弾円の色タプル
        引数2 rad：爆弾円の半径
        """
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)

    def update(self, screen: pg.Surface):
        screen.blit(self.img, self.rct)


class Gameover:
    """
    黒い画面にGame Overの文字とこうかとんを表示
    その後画面を少しsleepさせる
    """
    def __init__(self):
        self.bl_img = pg.Surface((WIDTH*2,HEIGHT*2)) #黒い画面を描画
        self.bl_img.set_alpha(200)
        pg.draw.rect(self.bl_img,(0, 0, 0),pg.Rect(0,0,WIDTH,HEIGHT))
        self.bl_rct = self.bl_img.get_rect()
        self.bl_rct.center = (WIDTH,HEIGHT)

        self.fonto = pg.font.Font(None, 200) # 文字列表示
        self.txt = self.fonto.render("Game Over",True, (255, 255, 255))

        self.time_fonto = pg.font.Font(None, 50) # 文字列表示
        self.time_txt = self.time_fonto.render(f"{survive_time} seconds left",True, (255, 255, 255)) 

        self.kk_img1 = pg.image.load("fig/8.png") # こうかとん(左)表示 
        self.kk_img1 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
        self.kk_rct1 = self.kk_img1.get_rect()
        self.kk_rct1.center = 135, HEIGHT/2+30

        self.kk_img2 = pg.image.load("fig/8.png") # こうかとん(右)表示 
        self.kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
        self.kk_rct2 = self.kk_img1.get_rect()
        self.kk_rct2.center = 1000, HEIGHT/2+30
        

    def update(self,screen: pg.Surface):
        screen.blit(self.bl_img,self.bl_rct)
        screen.blit(self.txt, [180,HEIGHT/2-20])
        screen.blit(self.time_txt, [410,500])
        screen.blit(self.kk_img1, self.kk_rct1)
        screen.blit(self.kk_img2, self.kk_rct2)
        pg.display.update()
        time.sleep(5)


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect
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



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    gameover = Gameover()

    # こうかとん初期化
    bg_img = pg.image.load("fig/campas.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    obj_wall1 = [Bomb((255, 0, 0), 10)]
    obj_wall2 = [Bomb((255, 255, 0), 10)]
    obj_wall3 = [Bomb((255, 255, 255), 10)]
  
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
       
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] # 左右方向
                sum_mv[1] += mv[1] # 上下方向
        
        for wall1 in obj_wall1:
            if kk_rct.colliderect(wall1.rct): # 壁1に合った判定確認
                pg.mixer.music.load("fig/打撃4.mp3") #  壁1に当たったときの音を鳴らす
                pg.mixer.music.play(loops=0, start=0.0)
                gameover.update(screen)  
                return
        for wall1 in obj_wall1:
            wall1.update(screen)

        for wall2 in obj_wall2:
            if kk_rct.colliderect(wall2.rct): # 壁2に合った判定確認
                pg.mixer.music.load("fig/打撃4.mp3") # 壁2に当たったときの音を鳴らす
                pg.mixer.music.play(loops=0, start=0.0)
                gameover.update(screen)  
                return
        for wall2 in obj_wall2:
            wall2.update(screen)

        for wall3 in obj_wall3:
            if kk_rct.colliderect(wall3.rct): # 壁3に合った判定確認
                pg.mixer.music.load("fig/打撃4.mp3") # 壁3に当たったときの音を鳴らす
                pg.mixer.music.play(loops=0, start=0.0)
                gameover.update(screen) 
                return
        for wall3 in obj_wall3:
            wall3.update(screen)

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
