import os
import time
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650

DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5, 0),
    
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向にはみ出でいたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向にはみ出ていたら
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    go_img = pg.Surface((WIDTH, HEIGHT))#背景画像作成
    pg.draw.rect(go_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(200)
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over",
                       True, (255, 255, 255))#gameoverフォント作成
    go_img.blit(txt, [400, 300])#テキストを1のsurfacelit
    go_kk_img = pg.image.load("fig/8.png")
    go_img.blit(go_kk_img, [340, 290])#こうかとん画像を1のsurfaceにblit
    go_img.blit(go_kk_img, [720, 290])
    screen.blit(go_img, [0, 0])
    pg.display.update()
    time.sleep(5)
    return go_img

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    # bb_img = pg.Surface((20,20))#空のサーフェイス
    # pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    # bb_img.set_colorkey((0, 0, 0)) #四隅を削除
    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)#爆弾横座標
    bb_rct.centery = random.randint(0, HEIGHT)#爆弾縦座標
    
    #演習2：途中まで実装
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):#こうかとんと爆弾の衝突判定
            return gameover(screen)# ゲームオーバー

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        avx = vx * bb_accs[min(tmr//500, 9)]
        avy = vy * bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] #横方向
                sum_mv[1] += mv[1] #縦方向
        #if key_lst[pg.K_UP]:
         #   sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
         #   sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
         #   sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
         #   sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct) #爆弾描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
