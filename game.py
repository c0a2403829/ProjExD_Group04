import os
import random
import sys
import time
import pygame.mixer
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

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]: # 爆弾拡大、加速機能
    b_img = []
    bb_accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        b_img.append(bb_img)
    return b_img, bb_accs

def game_start(screen: pg.Surface):

    """
    ゲームスタート画面。
    スタート画面BGM再生。
    エンターキーでスタート。
    """
    bg = pg.image.load("fig/start.jpg")
    title_font = pg.font.SysFont("impact", 80)
    text_font = pg.font.SysFont("msgothic", 40)
    title_txt = title_font.render("Survive Kokaton", True, (35,91,200))
    text = text_font.render("Push to Enter", True, (35,91,200))

    pygame.mixer.init() #初期化
    pygame.mixer.music.load("fig/Snow_Drop.mp3") #読み込み
    pygame.mixer.music.play(-1) #スタート画面BGM再生

    while True:
        screen.blit(bg, (-570, 0))  # 背景画像貼り付け
        screen.blit(title_txt, (WIDTH//2 - title_txt.get_width()//2, HEIGHT//2 - 150)) 
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 200))  # テキスト表示
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                pygame.mixer.music.fadeout(3) #スタート画面BGM終了
                return
            
def game_clear(screen: pg.Surface):

    """
    ゲームクリア画面。
    エンターキーでゲーム終了。
    """
    bg = pg.image.load("fig/clear.jpg")
    title_font = pg.font.SysFont("impact", 90)
    text_font = pg.font.SysFont("msgothic", 50)
    title_txt = title_font.render("GAME CLEAR!!", True, (231,17,25))
    text = text_font.render("Push Enter to End", True, (231,17,25))

    pygame.mixer.init() #初期化
    pygame.mixer.music.load("fig/勝利のテーマ.mp3") #クリアBGM読み込み
    pygame.mixer.music.play(-1) #クリアBGM再生

    while True:
        screen.blit(bg, (-570, 0))  # 背景画像貼り付け
        screen.blit(title_txt, (WIDTH//2 - title_txt.get_width()//2, HEIGHT//2 - 150)) 
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 200))  # テキスト表示
        pg.display.update()
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                return


def main():
    pg.display.set_caption("生き延びろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    game_start(screen)  # スタート画面の呼び出し
    start_time = time.time()  # ゲーム開始時刻を記録

    # こうかとん初期化
    bg_img = pg.image.load("fig/campas.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()

    kk_rct.center = 300, 700

    pygame.mixer.init() #初期化
    pygame.mixer.music.load("fig/The_Beautiful_Haven_Type_I.mp3") #読み込み
    pygame.mixer.music.play(1) #ゲーム画面BGM再生
    
    clock = pg.time.Clock()
    tmr = 0
    while True:

        elapsed_time = time.time() - start_time
        survive_time = max(0, int(180 - elapsed_time)) #カウントダウン

        if survive_time <= 0:
             game_clear(screen)#ゲームクリア画面呼び出し
             time.sleep(1)
             return  # ゲーム終了
        
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        screen.blit(bg_img, [-570, 0]) 
        
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

        """
        右上にカウントダウン表示
        """
        timer_font = pg.font.SysFont("impact", 40)
        timer_txt = timer_font.render(f"Survive for {survive_time} more seconds!", True, (244,229,17))
        screen.blit(timer_txt, (70, 750))
        
        #screen.blit(bb_img, bb_rct) # 爆弾の表示
        pg.display.update()
        tmr += 1
        clock.tick(50)
        

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()