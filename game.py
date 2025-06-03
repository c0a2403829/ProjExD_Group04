import os
import random
import sys
import time
import pygame.mixer
import pygame as pg


WIDTH, HEIGHT = 600, 800
clock = pg.time.Clock()
WALL_SPEED = 3

DELTA = { # 辞書の作成
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Gameover:
    """
    黒い画面にGame Overの文字とこうかとんを表示
    その後画面を少しsleepさせる
    """
    def __init__(self,survive_time):
        self.bl_img = pg.Surface((WIDTH*2,HEIGHT*2)) #黒い画面を描画
        self.bl_img.set_alpha(200)
        pg.draw.rect(self.bl_img,(0, 0, 0),pg.Rect(0,0,WIDTH,HEIGHT))
        self.bl_rct = self.bl_img.get_rect()
        self.bl_rct.center = (WIDTH,HEIGHT)

        self.fonto = pg.font.Font(None, 60) # 文字列表示
        self.txt = self.fonto.render("Game Over",True, (255, 255, 255))

        self.time_fonto = pg.font.Font(None, 50) # 文字列表示
        self.time_txt = self.time_fonto.render(f"{survive_time}seconds left",True, (255, 255, 255)) 

        self.kk_img1 = pg.image.load("fig/8.png") # こうかとん(左)表示 
        self.kk_img1 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
        self.kk_rct1 = self.kk_img1.get_rect()
        self.kk_rct1.center = 135, HEIGHT/2+30

        self.kk_img2 = pg.image.load("fig/8.png") # こうかとん(右)表示 
        self.kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
        self.kk_rct2 = self.kk_img1.get_rect()
        self.kk_rct2.center = 470, HEIGHT/2+30
        
    def update(self,screen: pg.Surface):
        screen.blit(self.bl_img,self.bl_rct)
        screen.blit(self.txt, [180,HEIGHT/2-20])
        screen.blit(self.time_txt, [170,500])
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
            state["speedup"] = True
            state["speed"] = 2
            state["boost_timer"] = now + 5000
            self.active = False

class Timer(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "fig/timer.png")

    def apply_effect(self, player_rect, now, state):
         if self.active and self.rect.colliderect(player_rect):
            state["speed"] = 0.4
            state["slow_timer"] = now + 3000
            self.active = False

class Mirror(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "fig/mirror.png")

    def apply_effect(self, player_rect, now, state):
        if self.active and self.rect.colliderect(player_rect):
            state["is_mirrored"] = True
            state["mirror_timer"] = now + 4000  # 4秒後に戻す
            self.active = False

class Shield(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "fig/shield.png")

    def apply_effect(self, player_rect, now, state):
        if self.active and self.rect.colliderect(player_rect):
            state["has_shield"] = True
            state["shield_timer"] = now + 8000
            self.active = False

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


class Wall:
    def __init__(self, x, y, image_path, form="obj_wall1", speed=WALL_SPEED, walls=[]):
        """
        シンプルな画像一枚と縦に二枚重ねたとき横に二枚並べたときの三種類の大きさ調整
        画像の情報取得
        基本情報の設定
        壁同士が重ならない位置に壁を配置
        """
        self.image = pg.image.load(image_path)
        
        if form == "obj_wall1":
            self.image = pg.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 4))
        elif form == "obj_wall2":
            self.image = pg.transform.scale(self.image, (self.image.get_width() // 8, self.image.get_height() // 4))
            self.rect = self.image.get_rect()
            self.rect.height *= 2
            self.rect.centery -= self.image.get_height() // 2
        elif form == "obj_wall3":
            self.image = pg.transform.scale(self.image, (self.image.get_width() // 4, self.image.get_height() // 8))
            self.rect = self.image.get_rect()
            self.rect.width *= 2
            self.rect.centerx -= self.image.get_width() // 2

        self.form = form
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.topleft = self.safe_position(x, y, walls)
    
    def safe_position(self, x, y, walls):
        """
        壁同士の出力場所の重複を防止
        coolliderect(a)はaと座標が重なったらループを抜ける、
        抜けた場合ランダムに座標を付けなおす
        戻り値：ランダムなx,y座標
        """
        trying = 100
        for i in range(trying):
            tr_rect = self.rect.copy()
            tr_rect.topleft = (x, y)
            coll = False
            for w in walls:
                if tr_rect.colliderect(w.rect):
                    coll = True
                    break
            if not coll:
                return x, y
            x = random.randint(0,WIDTH - self.rect.width)
            y = random.randint(-500, -50)
        return x, y
    
    def move(self, walls):
        """
        壁の位置を下に下げていき画面外に消えたときに画面上部のランダムな位置からまた落ち始める
        """
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.topleft = self.safe_position(random.randint(0, WIDTH - self.rect.width), random.randint(-500, -50), walls)

    def draw(self, screen):
        """
        wall2,wall3をそれぞれ、画像を縦、横に並べたものにする
        """
        screen.blit(self.image, self.rect)     


def main():
    pg.display.set_caption("生き延びろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    game_start(screen)  # スタート画面の呼び出し
    start_time = time.time()  # ゲーム開始時刻を記録

    # こうかとん初期化
    sum_mv = [0,0]
    bg_img = pg.image.load("fig/campas.jpg")    
    kk_img0 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_img = kk_img0 if sum_mv[0] >= 0 else pg.transform.flip(kk_img0, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 700
    reverse_icon = pg.image.load("fig/reverse.png").convert_alpha()
    reverse_icon = pg.transform.scale(reverse_icon, (40, 40))
    shield_icon = pg.image.load("fig/shield.png").convert_alpha()
    shield_icon = pg.transform.scale(shield_icon, (35, 35))
    barrier_img = pg.transform.scale(pg.image.load("fig/barrier.png"), (90, 80)) 
    items = []

    # 状態管理用の辞書（ブースト/鈍足/ミラーなど共通）
    state = {
    "speedup": False,
    "speed": 0.8,
    "boost_timer": 0,
    "slow_timer": 0,
    "is_mirrored": False,
    "mirror_timer": 0,
    "has_shield": False,
    "shield_timer": 0,
}

    # 定期出現用のタイマー
    SPAWN_INTERVAL = 3000
    last_spawn_time = pg.time.get_ticks()

    pygame.mixer.init() #初期化
    pygame.mixer.music.load("fig/The_Beautiful_Haven_Type_I.mp3") #読み込み
    pygame.mixer.music.play(1) #ゲーム画面BGM再生
    
    walls =[]
    wall_type = ["obj_wall1", "obj_wall2", "obj_wall3"]
    random.shuffle(wall_type)
    for i in range(4):  #壁の枚数を設定
        walls.append(Wall(random.randint(0, WIDTH), random.randint(-500, -50), "fig/wall.png", wall_type[i % len(wall_type)], walls=walls))
        # 壁枚数分のwallオブジェクトを生成し、ランダムな壁をwallsリストに追加

    clock = pg.time.Clock()
    tmr = 0
  
    scale=0.9
    kk_base_img=pg.image.load("fig/3.png")
    kk_img = pg.transform.rotozoom(kk_base_img, 0, scale)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 700
    
    clock = pg.time.Clock()
    tmr = 0
    speed = 1 

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
   
        now = pg.time.get_ticks()

        screen.blit(bg_img, [-570, 0]) 
        for wall1 in walls:
            if kk_rct.colliderect(wall1.rect): # 壁1に合った判定確認
                if state["has_shield"] == False:
                    pg.mixer.music.load("fig/打撃4.mp3") #  壁1に当たったときの音を鳴らす
                    pg.mixer.music.play(loops=0, start=0.0)
                    game.update(screen)  
                    return

        elapsed_sec = tmr // 50
        scale = 0.9 + 0.2 * (elapsed_sec // 20)  # 10秒ごとにサイズアップ
        kk_img = pg.transform.rotozoom(kk_base_img, 0, scale)
        kk_rct = kk_img.get_rect(center=kk_rct.center) 
        speed = 1 + elapsed_sec // 20

        # こうかとんの操作  
        kk_rct.move_ip(sum_mv) # こうかとんの移動
        if check_bound(kk_rct) != (True, True): # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面内に戻す
        screen.blit(kk_img, kk_rct)

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

        # 一定時間後に速度を元に戻す
        if state["boost_timer"] != 0 and now > state["boost_timer"]:
            state["speed"] = 0.8
            state["boost_timer"] = 0
            state["speedup"] = False
        if state["slow_timer"] != 0 and now > state["slow_timer"]:
            state["speed"] = 0.8
            state["slow_timer"] = 0
        if state["mirror_timer"] != 0 and now > state["mirror_timer"]:
            state["is_mirrored"] = False
            state["mirror_timer"] = 0
        if state["shield_timer"] != 0 and now > state["shield_timer"]:
            state["has_shield"] = False
            state["shield_timer"] = 0

        """
        右上にカウントダウン表示
        """
        timer_font = pg.font.SysFont("impact", 40)
        timer_txt = timer_font.render(f"Survive for {survive_time} more seconds!", True, (244,229,17))
        screen.blit(timer_txt, (70, 200))

        game = Gameover(survive_time)

        # スピードアップ中効果トンをこうかとんを赤くする
        draw_img = kk_img.copy()
        if state["speedup"] == True:  # 速度アップ中
            red_overlay = pg.Surface(kk_img.get_size())
            red_overlay.fill((120, 0, 0))  # 赤色成分
            draw_img.blit(red_overlay, (0, 0), special_flags=pg.BLEND_RGB_ADD)
        screen.blit(draw_img, kk_rct)

        # スロウ中に画面を暗くする 
        if state["speed"] < 0.8:        
            overlay = pg.Surface((WIDTH, HEIGHT))
            overlay.fill((0, 80, 255))
            overlay.set_alpha(40)    # 透明度
            screen.blit(overlay, (0, 0))
        
        # 反転中にアイコンを表示する
        if state["is_mirrored"]:
            screen.blit(reverse_icon, (10, 10))
        if state["mirror_timer"] > now:
            font = pg.font.Font(None, 40)
            remain = (state["mirror_timer"] - now) // 1000
            txt = font.render(f"{remain}", True, (255,255,255))
            screen.blit(txt, (50, 40))

        # シールド発動中、バリアとシールドアイコン表示
        if state["has_shield"]:
             screen.blit(shield_icon, (WIDTH - 45, 10))
             barrier_rect = barrier_img.get_rect(center=kk_rct.center)
             screen.blit(barrier_img, barrier_rect)

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

        for item in items:
            item.update()
            item.apply_effect(kk_rct, now, state)
            item.draw(screen)
        items = [item for item in items if item.rect.y < HEIGHT and item.active]

        for wall in walls:
            wall.move(walls)
            wall.draw(screen)
            
        pg.display.update()
        tmr += 1
        clock.tick(50)
        

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
