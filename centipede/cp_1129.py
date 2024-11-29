#------------------------------------------
# title: Centipede
# author: sanbunnoichi
# desc: ATARI7800's Centipede clone
# site: https://github.com/sanbunno-ichi/cp
# license: MIT
# version: 1.0
#
#更新履歴
#2024,xx.xx 公開

#飽きてきたので一旦保留・・・

#[残作業]
#(済)一番下の段にキノコは置かない
#ステージ１０あたりから、つながるムカデは５匹、それ以外は１匹ずつに出現する
#そのごつながるムカデの数は１匹ずつへっていき最後はみな１匹ずつの出現に変わる
#最後の１匹になってしばらくすると両側から１匹ずつ現れる
#ステージ変わったら色変え（cidにオフセット加算）
#効果音入れ

#2024.11.29 クモの動き
#2024.11.26 スコア作成
#2024.11.25 ステージクリア、ゲームオーバー表記
#2024.11.25 残機表記
#2024.11.25 ステージクリアの作成
#2024.11.24 ノミとサソリの動き暫定作成
#2024.11.24 タイトルからゲームオーバーまでの流れ作成
#2024.11.24 ヒットチェック組み込み
#2024.11.22 プレイヤーとプレイヤーの弾
#2024.11.22 ムカデ胴体の動き
#2024.11.21 ムカデ先頭＆キノコの動き
#2024.11.17 作成開始
#------------------------------------------
#ATARI7800のCENTIPEDEのキャラを使用
#ゲーム内挙動
#サソリが通過したキノコを毒キノコに変える
#ノミは下からDOWN_AREA段目以下にはキノコを置かない？
#プレイヤーがやられると、ダメージ受けたキノコはすべて元に戻る、毒キノコの毒もなくなる（普通のキノコに変わる
#蜘蛛はHITされる位置で得点が変わる上から（300,600,900はある？
#------------------------------------------
import pyxel

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192

CSIZE = 8

XSIZE = ( SCREEN_WIDTH // CSIZE )
YSIZE = ( SCREEN_HEIGHT // CSIZE )
DOWN_AREA = 6		#プレイヤー移動エリア（下から？段目までの意味）


TITLE_X = SCREEN_WIDTH//2 - (0xf8//2)
TITLE_Y = 0x30
TITLE_XSIZE = 0xf8

SCORE_KETA = 6

#-----------------------------------------------------------------
#[workass]変数
WORK_TOP			=	0
WORK_END			=	0x1000
_ass = WORK_TOP
GWK = [WORK_TOP for _ass in range(WORK_END)]	#変数管理(RAM領域)

game_adv			=	WORK_TOP+0x00		#game_control number

G_TITLE				=	0
G_GAME				=	1
G_GAMEOVER			=	2
G_CLEAR				=	3

game_subadv			=	WORK_TOP+0x01		#game_control sub-number

GS_INIT				=	0
GS_MAIN				=	1
GS_WAIT				=	2
GS_RESTART			=	3

stage_number		=	WORK_TOP+0x02		#0～
score				=	WORK_TOP+0x03		#スコア（最大６桁）
highscore			=	WORK_TOP+0x04		#ハイスコア（最大６桁）
rest_number			=	WORK_TOP+0x05		#残機
move_speed			=	WORK_TOP+0x06		#ムカデ移動スピード
wait_counter		=	WORK_TOP+0x07		#汎用カウンタ
sasori_timer		=	WORK_TOP+0x08		#サソリ出現タイマー
nomi_timer			=	WORK_TOP+0x09		#ノミ出現タイマー
sasori_adv			=	WORK_TOP+0x0a		#サソリ制御
nomi_stage_max		=	WORK_TOP+0x0b		#各ステージノミ出現最大数

PTAMA_WORK			=	WORK_TOP+0x20		#画面内一発
PTAMA_MAX			=	1

PLY_WORK			=	WORK_TOP+0x30
cid					=	0x00		#ID番号
ccond				=	0x01		#状態フラグ
#状態フラグ内訳
F_LIVE				=	0x80		#[bit7]生(1)死(0)
F_HIT				=	0x40		#[bit6]ヒット(1)
F_STOP				=	0x20		#[bit5]停止（ムカデ）
F_VMOVE				=	0x10		#[bit4]縦移動中(1)（ムカデ）
F_HMOVE				=	0x08		#[bit3]横移動中(1/0=RIGHT/LEFT)（ムカデ）
F_DIR				=	0x04		#[bit2]移動方向(1/0=UP/DOWN)
F_DOKU				=	0x02		#[bit1]毒キノコに当たった（ムカデ）
F_HEAD				=	0x01		#[bit0]先頭(1)

cxpos				=	0x02		#X座標
cypos				=	0x03		#Y座標
cxspd				=	0x04		#X移動スピード
cyspd				=	0x05		#Y移動スピード
canum				=	0x06		#アニメ番号
cacnt				=	0x07		#アニメカウンタ
caspd				=	0x08		#アニメスピードカウンタ
cwait				=	0x09		#汎用カウンタ

cmukade				=	0x0a		#接合元id（ムカデ用）
cjoin				=	0x0b		#接合先id（ムカデ用）
csavecnt			=	0x0c		#位置情報記憶カウンタ（ムカデ用）
cmpat				=	0x0c		#移動パターン番号（クモ用）
cmcnt				=	0x0d		#移動カウンタ
cmnum				=	0x0e
cstep				=	0x0f

CWORK_SIZE			=	0x10		#各種キャラクタワークサイズ

KUMO_WORK			=	WORK_TOP+0x40
KUMO_MAX			=	1	#4

NOMI_WORK			=	WORK_TOP+0x80
NOMI_MAX			=	8

SASORI_WORK			=	WORK_TOP+0x100
SASORI_MAX			=	1				#画面上１匹だけ

MUKADE_WORK			=	WORK_TOP+0x200	#最大12個（PTAMA_WORK + (CWORK_SIZE*PTAMA_MAX))
MUKADE_MAX			=	12

SCREEN_WORK			=	WORK_TOP+0x300	#キノコ配置等に使用
SCREEN_MAX			=	XSIZE * YSIZE	#画面分のエリアを設定：画面内すべてのキャラ数(画面全部で32x24=0x300)

SAVE_WORK			=	WORK_TOP+0x600	#ムカデ用接合するための位置記憶（MUKADE_MAX*SINGLE_SAVE_MAX*4(cond,x,y,?)）
SINGLE_SAVE_MAX		=	16
SAVE_PARTS			=	4
#移動スピード１として１６回分（８ドット）の座標と状態（F_VMOVE+F_HMOVE+F_DIR+F_DOKU）を記憶しておく（足りなければ増やす）
#接合先の座標から接合元の座標を取得してセット・・・を繰り返す

#次_WORK			=	WORK_TOP+0xa00

#-----------------------------------------------------------------
#キャラクタテーブル
#-----------------------------------------------------------------
IDMAX = 0x44
ctbl = [
	# u,    v,    us,   vs
	[ 0x08, 0x00, 0x08, 0x08 ],		#0x00 プレイヤー
	[ 0x10, 0x00, 0x01, 0x05 ],		#0x01 プレイヤーの弾
	[ 0x00, 0x08, 0x08, 0x08 ],		#0x02 ムカデ頭左向き1-1
	[ 0x00, 0x10, 0x08, 0x08 ],		#0x03 ムカデ頭左向き1-2
	[ 0x00, 0x18, 0x08, 0x08 ],		#0x04 ムカデ頭左向き1-3
	[ 0x08, 0x08, 0x08, 0x08 ],		#0x05 ムカデ頭下向き2-1
	[ 0x08, 0x10, 0x08, 0x08 ],		#0x06 ムカデ頭下向き2-2
	[ 0x08, 0x18, 0x08, 0x08 ],		#0x07 ムカデ頭下向き2-3
	[ 0x10, 0x08, 0x08, 0x08 ],		#0x08 ムカデ胴左向き1-1
	[ 0x10, 0x10, 0x08, 0x08 ],		#0x09 ムカデ胴左向き1-2
	[ 0x10, 0x18, 0x08, 0x08 ],		#0x0a ムカデ胴左向き1-3
	[ 0x00, 0x20, 0x08, 0x08 ],		#0x0b キノコ1 damage0
	[ 0x08, 0x20, 0x08, 0x08 ],		#0x0c キノコ2 damage1
	[ 0x00, 0x28, 0x08, 0x08 ],		#0x0d キノコ3 damage2
	[ 0x08, 0x28, 0x08, 0x08 ],		#0x0e キノコ4 damage3
	[ 0x10, 0x60, 0x08, 0x08 ],		#0x0f 毒キノコ1 damage0
	[ 0x10, 0x68, 0x08, 0x08 ],		#0x10 毒キノコ2 damage1
	[ 0x10, 0x70, 0x08, 0x08 ],		#0x11 毒キノコ3 damage2
	[ 0x10, 0x78, 0x08, 0x08 ],		#0x12 毒キノコ4 damage3
	[ 0x00, 0x30, 0x12, 0x08 ],		#0x13 蜘蛛1
	[ 0x00, 0x38, 0x12, 0x08 ],		#0x14 蜘蛛2
	[ 0x00, 0x40, 0x12, 0x08 ],		#0x15 蜘蛛3
	[ 0x00, 0x48, 0x12, 0x08 ],		#0x16 蜘蛛4
	[ 0x00, 0x50, 0x0a, 0x08 ],		#0x17 ノミ1
	[ 0x0a, 0x50, 0x0a, 0x08 ],		#0x18 ノミ2
	[ 0x00, 0x58, 0x0a, 0x08 ],		#0x19 ノミ3
	[ 0x0a, 0x58, 0x0a, 0x08 ],		#0x1a ノミ4
	[ 0x00, 0x60, 0x10, 0x10 ],		#0x1b サソリ1
	[ 0x00, 0x70, 0x10, 0x10 ],		#0x1c サソリ2
	[ 0x00, 0x80, 0x10, 0x10 ],		#0x1d サソリ3
	[ 0x00, 0x90, 0x10, 0x10 ],		#0x1e サソリ4
	[ 0x00, 0xc0, 0xf8, 0x20 ],		#0x1f タイトル下
	[ 0x00, 0xe0, 0xf8, 0x20 ],		#0x20 タイトル上
	[ 0x58, 0xa0, 0x60, 0x08 ],		#0x21 ATARIロゴ
	[ 0x50, 0xa0, 0x08, 0x08 ],		#0x22 EXTEND

	[ 0x00, 0xa0, 0x08, 0x08 ],		#0x23 スコアフォント0
	[ 0x08, 0xa0, 0x08, 0x08 ],		#0x24 スコアフォント1
	[ 0x10, 0xa0, 0x08, 0x08 ],		#0x25 スコアフォント2
	[ 0x18, 0xa0, 0x08, 0x08 ],		#0x26 スコアフォント3
	[ 0x20, 0xa0, 0x08, 0x08 ],		#0x27 スコアフォント4
	[ 0x28, 0xa0, 0x08, 0x08 ],		#0x28 スコアフォント5
	[ 0x30, 0xa0, 0x08, 0x08 ],		#0x29 スコアフォント6
	[ 0x38, 0xa0, 0x08, 0x08 ],		#0x2a スコアフォント7
	[ 0x40, 0xa0, 0x08, 0x08 ],		#0x2b スコアフォント8
	[ 0x48, 0xa0, 0x08, 0x08 ],		#0x2c スコアフォント9

	[ 0x00, 0xa8, 0x08, 0x08 ],		#0x2d ハイスコアフォント0
	[ 0x08, 0xa8, 0x08, 0x08 ],		#0x2e ハイスコアフォント1
	[ 0x10, 0xa8, 0x08, 0x08 ],		#0x2f ハイスコアフォント2
	[ 0x18, 0xa8, 0x08, 0x08 ],		#0x30 ハイスコアフォント3
	[ 0x20, 0xa8, 0x08, 0x08 ],		#0x31 ハイスコアフォント4
	[ 0x28, 0xa8, 0x08, 0x08 ],		#0x32 ハイスコアフォント5
	[ 0x30, 0xa8, 0x08, 0x08 ],		#0x33 ハイスコアフォント6
	[ 0x38, 0xa8, 0x08, 0x08 ],		#0x34 ハイスコアフォント7
	[ 0x40, 0xa8, 0x08, 0x08 ],		#0x35 ハイスコアフォント8
	[ 0x48, 0xa8, 0x08, 0x08 ],		#0x36 ハイスコアフォント9

	[ 0x00, 0xb8, 0x08, 0x08 ],		#0x37 出現スコアフォント0
	[ 0x08, 0xb8, 0x08, 0x08 ],		#0x38 出現スコアフォント1
	[ 0x10, 0xb8, 0x08, 0x08 ],		#0x39 出現スコアフォント2
	[ 0x18, 0xb8, 0x08, 0x08 ],		#0x3a 出現スコアフォント3
	[ 0x20, 0xb8, 0x08, 0x08 ],		#0x3b 出現スコアフォント4
	[ 0x28, 0xb8, 0x08, 0x08 ],		#0x3c 出現スコアフォント5
	[ 0x30, 0xb8, 0x08, 0x08 ],		#0x3d 出現スコアフォント6
	[ 0x38, 0xb8, 0x08, 0x08 ],		#0x3e 出現スコアフォント7
	[ 0x40, 0xb8, 0x08, 0x08 ],		#0x3f 出現スコアフォント8
	[ 0x48, 0xb8, 0x08, 0x08 ],		#0x40 出現スコアフォント9

	[ 0x10, 0x80, 0x08, 0x08 ],		#0x41 ムカデ胴下向き2-1
	[ 0x10, 0x88, 0x08, 0x08 ],		#0x42 ムカデ胴下向き2-2
	[ 0x10, 0x90, 0x08, 0x08 ],		#0x43 ムカデ胴下向き2-3
	]
#-----------------------------------------------------------------
#キャラクタセット
#	X座標, Y座標, id番号, hrev水平反転, _vrev垂直反転
#-----------------------------------------------------------------
def cput( _xp, _yp, _id, _hrev = 0, _vrev = 0 ):
	_hrev = _hrev * (-2) + 1	#0/1→1/-1
	_vrev = _vrev * (-2) + 1	#0/1→1/-1
	pyxel.blt( _xp, _yp, 0, ctbl[_id][0], ctbl[_id][1], ctbl[_id][2] * _hrev, ctbl[_id][3] * _vrev, colkey = 0 )

#-----------------------------------------------------------------
#アニメテーブル（内容はキャラクタID、７パターン以上は別途・・・
#-----------------------------------------------------------------
ANIMMAX = 0x0e
atbl = [[0 for i in range(10)] for j in range(ANIMMAX)]
atbl = [
	#hv_rev:bit0=hrev, bit1=vrev
	#spd,hv_rev,p1,,,0xff(終端)（spd=0はアニメ無し）
	[ 2, 0x0, 0x02, 0x03, 0x02, 0x04, 0xff, 0xff, 0xff ],	#0x00 ムカデ頭左向き
	[ 2, 0x0, 0x08, 0x09, 0x08, 0x0a, 0xff, 0xff, 0xff ],	#0x01 ムカデ胴左向き
	[ 2, 0x1, 0x02, 0x03, 0x02, 0x04, 0xff, 0xff, 0xff ],	#0x02 ムカデ頭右向き
	[ 2, 0x1, 0x08, 0x09, 0x08, 0x0a, 0xff, 0xff, 0xff ],	#0x03 ムカデ胴右向き
	[ 2, 0x0, 0x05, 0x06, 0x05, 0x07, 0xff, 0xff, 0xff ],	#0x04 ムカデ頭下向き
	[ 2, 0x0, 0x41, 0x42, 0x41, 0x43, 0xff, 0xff, 0xff ],	#0x05 ムカデ胴下向き
	[ 2, 0x2, 0x05, 0x06, 0x05, 0x07, 0xff, 0xff, 0xff ],	#0x06 ムカデ頭上向き
	[ 2, 0x2, 0x41, 0x42, 0x41, 0x43, 0xff, 0xff, 0xff ],	#0x07 ムカデ胴上向き
	[ 3, 0x0, 0x1b, 0x1d, 0x1e, 0x1c, 0xff, 0xff, 0xff ],	#0x08 サソリ左向き
	[ 3, 0x1, 0x1b, 0x1d, 0x1e, 0x1c, 0xff, 0xff, 0xff ],	#0x09 サソリ右向き
	[ 3, 0x0, 0x13, 0x14, 0x15, 0x16, 0xff, 0xff, 0xff ],	#0x0a 蜘蛛
	[ 3, 0x0, 0x17, 0x19, 0x18, 0x1a, 0xff, 0xff, 0xff ],	#0x0b ノミ
	[ -1, 0x0, 0x0b, 0x0c, 0x0d, 0x0e, 0xff, 0xff, 0xff ],	#0x0c キノコ
	[ -1, 0x0, 0x0f, 0x10, 0x11, 0x12, 0xff, 0xff, 0xff ],	#0x0d 毒キノコ
	]

#アニメ番号
ACNT_HV		= 1
ACNT_OFFSET	= 2
ANUM_MUKADE_LEFT	= 0x0
ANUM_BODY_LEFT		= 0x1
ANUM_MUKADE_RIGHT	= 0x2
ANUM_BODY_RIGHT		= 0x3
ANUM_MUKADE_DOWN	= 0x4
ANUM_BODY_DOWN		= 0x5
ANUM_MUKADE_UP		= 0x6
ANUM_BODY_UP		= 0x7
ANUM_SASORI_LEFT	= 0x8
ANUM_SASORI_RIGHT	= 0x9
ANUM_KUMO			= 0xa
ANUM_NOMI			= 0xb
ANUM_KINOKO			= 0xc
ANUM_DOKUKINOKO		= 0xd

#-----------------------------------------------------------------
#アニメーション制御
#	_flag	0:通常ループ実行
#			1:終端で終了（戻り値1で終了）
#			2:終端から逆実行、最初に戻って終了（戻り値1で終了）
#-----------------------------------------------------------------
#ここではパターン番号、パターンスピードでパターンカウントを変化させるだけ
#なので、描画時に
#	_id = atbl[GWK[_wk+canum]][GWK[_wk+cacnt]+ACNT_OFFSET(2)]
#として指定する
#-----------------------------------------------------------------
#hv_revの指定方法：
#	_h = 0
#	_v = 0
#	if( atbl[GWK[_wk+canum]][ACNT_HV] & 0x01 ):
#		_h = 1
#	if( atbl[GWK[_wk+canum]][ACNT_HV] & 0x02 ):
#		_v = 1
#	cput( GWK[MUKADE_WORK + cxpos], GWK[MUKADE_WORK + cypos], _id, _h, _v )
#-----------------------------------------------------------------
def anim_control( _wk, _flag ):
	#アニメ番号有り
	if( GWK[_wk+canum] < ANIMMAX ):

		if( atbl[GWK[_wk+canum]][0] < 0 ):
			#アニメスピードでアニメしない（パターン番号直接指定）
			return(1)

		GWK[_wk+caspd] += 1
		#アニメスピード超えた？
		if( GWK[_wk+caspd] >= atbl[GWK[_wk+canum]][0] ):
			GWK[_wk+caspd] = 0

			if( _flag == 0 ):
				GWK[_wk+cacnt] += 1
				#アニメ終端？
				if( atbl[GWK[_wk+canum]][GWK[_wk+cacnt]+ACNT_OFFSET] == 0xff ):
					GWK[_wk+cacnt] = 0
					return (1)
			elif( _flag == 1 ):
				GWK[_wk+cacnt] += 1
				#アニメ終端？
				if( atbl[GWK[_wk+canum]][GWK[_wk+cacnt]+ACNT_OFFSET] == 0xff ):
					GWK[_wk+cacnt] -= 1		#終端前に戻す
					return (1)
			elif( _flag == 2 ):
				GWK[_wk+cacnt] -= 1
				#アニメ始端？
				if( GWK[_wk+cacnt] < 0 ):
					GWK[_wk+cacnt] = 0
					return (1)
	return (0)

#---------------------------------------------------------------------------------------------------
#スコアセット
#	_type = 0 : 通常スコア
#	_type = 1 : ハイスコア
#---------------------------------------------------------------------------------------------------
def set_score( _xp, _yp, _score, _type ):

	str_score = str(_score)

	_id = 0x00
	_codelist = list( str_score )
	for i in range( len( str_score ) ):
		_id = ord( _codelist[i] )
		if( _type == 0 ):
			_id = _id - 0x0d	#0x23
		else:
			_id = _id - 0x03	#0x2d

		pyxel.blt( _xp + (i*8), _yp, 0, ctbl[_id][0], ctbl[_id][1], ctbl[_id][2], ctbl[_id][3], 0 )

	if( _type == 0 ):
		#残機表示
		_id = 0x22
		rest_xpos = len( str_score )*8
		for i in range( GWK[rest_number] ):
			pyxel.blt( _xp + rest_xpos + (i*8), _yp, 0, ctbl[_id][0], ctbl[_id][1], ctbl[_id][2], ctbl[_id][3], 0 )

#-----------------------------------------------------------------
#スコア加算
#-----------------------------------------------------------------
def add_score(_p):
	GWK[score] += _p
	if( GWK[highscore] < GWK[score] ):
		GWK[highscore] = GWK[score]

#-----------------------------------------------------------------
#スコア表示
#-----------------------------------------------------------------
def score_draw():
	#スコア
	set_score( 0x08, 0x00, GWK[score], 0 )
	#ハイスコア
	set_score( 0x60, 0x00, GWK[highscore], 1 )

#-----------------------------------------------------------------
#キノコ以外の敵初期化
#-----------------------------------------------------------------
def other_enemy_clear():
	for _cnt in range( KUMO_MAX * CWORK_SIZE ):
		GWK[KUMO_WORK + _cnt] = 0
	for _cnt in range( NOMI_MAX * CWORK_SIZE ):
		GWK[NOMI_WORK + _cnt] = 0
	for _cnt in range( SASORI_MAX * CWORK_SIZE ):
		GWK[SASORI_WORK + _cnt] = 0
	for _cnt in range( MUKADE_MAX * CWORK_SIZE ):
		GWK[MUKADE_WORK + _cnt] = 0
	for _cnt in range( MUKADE_MAX * SINGLE_SAVE_MAX * SAVE_PARTS ):
		GWK[SAVE_WORK + _cnt] = 0

#-----------------------------------------------------------------
#キノコ初期化
#-----------------------------------------------------------------
def kinoko_init():
	if( GWK[game_adv] == G_TITLE ):
		#タイトル
		pass

	else:
		#ゲーム
		for _cnt in range( 32 ):
			_xp = pyxel.rndi( 1, XSIZE - 1 )
			_yp = pyxel.rndi( 1, YSIZE - DOWN_AREA )
			GWK[SCREEN_WORK + ( _yp * XSIZE + _xp ) ] = 0x0b		#キノコ
	
#-----------------------------------------------------------------
#キノコ制御
#-----------------------------------------------------------------
def kinoko_control():
	pass

#-----------------------------------------------------------------
#ノミ制御
#	落下場所はランダム
#	ランダム位置にキノコを置いていく
#	一度に連続して４～６匹出現することもある（同時ではない）
#	ステージ進むと連続数が増える？
#	ステージごとに出現するノミの数を決める（１から８くらい？
#-----------------------------------------------------------------
def nomi_control():

	for _cnt in range( GWK[nomi_stage_max] ):
		_wk = NOMI_WORK + ( _cnt * CWORK_SIZE )
		if( ( GWK[_wk + ccond] & F_LIVE ) == 0 ):
			#print("NOMI set", _cnt)
			GWK[_wk + cwait] -= 1
			if( GWK[_wk + cwait] < 0 ):
				#次回の出現タイマーセット
				GWK[_wk + cwait] = pyxel.rndi( ( 1000 // (GWK[stage_number]+1) ), 1500 )
				GWK[_wk + ccond] = F_LIVE
				GWK[_wk + cid] = 0x17
				_app_X = pyxel.rndi( 2, ( SCREEN_WIDTH // CSIZE ) ) + 1
				GWK[_wk + cxpos ] = _app_X * CSIZE
				GWK[_wk + cypos] = -0x10
				GWK[_wk + canum] = ANUM_NOMI

				GWK[_wk + cacnt] = 0
				GWK[_wk + cxspd] = 0
				GWK[_wk + cyspd] = 4
					
		else:
			GWK[_wk + cypos] += GWK[_wk + cyspd]
			if( GWK[_wk + cypos] > SCREEN_HEIGHT ):
				GWK[_wk + ccond] = 0

			else:
				_chk = pyxel.rndi( 0,10 )
				if( _chk < 2 ):
					#最下段には置かない
					if( ( GWK[_wk + cypos] // CSIZE ) < ( YSIZE-1 ) ):
						_wk = SCREEN_WORK + ( GWK[_wk + cypos] // CSIZE ) * XSIZE + ( GWK[_wk + cxpos] // CSIZE )
						if( GWK[_wk] == 0 ):
							#ノーマルキノコを置く
							GWK[_wk] = 0x0b

#-----------------------------------------------------------------
#ノミ初期設定
#-----------------------------------------------------------------
def nomi_stage_max_set():
	GWK[nomi_stage_max] = GWK[stage_number] + 1
	if( GWK[nomi_stage_max] > NOMI_MAX ):
		GWK[nomi_stage_max] = NOMI_MAX

	for _cnt in range( GWK[nomi_stage_max] ):
		_wk = NOMI_WORK + ( _cnt * CWORK_SIZE )
		GWK[_wk + cwait] = pyxel.rndi( ( 1000 // (GWK[stage_number]+1) ), 2000 )

	
#-----------------------------------------------------------------
#サソリ制御
#	出現Yは画面中央より上でランダム
#	進む先にキノコがあったら毒キノコに変える
#-----------------------------------------------------------------
def sasori_control():

	if( GWK[sasori_adv] == 0 ):

		#出現タイマー
		GWK[sasori_timer] -= 1
		if( GWK[sasori_timer] < 0 ):
		
			#print("SASORI set")
			#次の出現タイマーセット
			sasori_timer_set()

			_app_Y = pyxel.rndi( 2, ( SCREEN_HEIGHT//CSIZE )//2 )
			GWK[SASORI_WORK + ccond] = F_LIVE
			GWK[SASORI_WORK + cid] = 0x1d
			GWK[SASORI_WORK + cypos ] = _app_Y * CSIZE
	
			if( pyxel.frame_count & 0x01 ):
				GWK[SASORI_WORK + cxpos] = SCREEN_WIDTH
				GWK[SASORI_WORK + canum] = ANUM_SASORI_LEFT
			else:
				GWK[SASORI_WORK + cxpos] = -0x10
				GWK[SASORI_WORK + canum] = ANUM_SASORI_RIGHT

			GWK[SASORI_WORK + cacnt] = 0
			GWK[SASORI_WORK + cxspd] = 2
			GWK[SASORI_WORK + cyspd] = 0
			
			GWK[sasori_adv] = 1

	if( GWK[sasori_adv] == 1 ):
		if( GWK[SASORI_WORK + ccond] & F_LIVE ):
			if( GWK[SASORI_WORK + canum] == ANUM_SASORI_LEFT ):
				GWK[SASORI_WORK + cxpos] -= GWK[SASORI_WORK + cxspd]
				if( GWK[SASORI_WORK + cxpos] < -0x10 ):
					GWK[SASORI_WORK + ccond] = 0
					GWK[sasori_adv] = 0
			else:
				GWK[SASORI_WORK + cxpos] += GWK[SASORI_WORK + cxspd]
				if( GWK[SASORI_WORK + cxpos] > SCREEN_WIDTH ):
					GWK[SASORI_WORK + ccond] = 0
					GWK[sasori_adv] = 0

			_wk = SCREEN_WORK + ( GWK[SASORI_WORK + cypos] // CSIZE ) * XSIZE + ( GWK[SASORI_WORK + cxpos] // CSIZE )
			if( 0x0b <= GWK[_wk] <= 0x0e ):
				#ノーマルキノコを毒キノコに変化させる
				GWK[_wk] += 4

		else:
			GWK[sasori_adv] = 0


def sasori_timer_set():
	_app_max = 2000 - GWK[stage_number] * 300
	if( _app_max < 500 ):
		GWK[sasori_timer] = pyxel.rndi( 200, 1000 )
	else:
		GWK[sasori_timer] = pyxel.rndi( 500, 2000 )

#-----------------------------------------------------------------
#移動先がキノコの横かどうかをチェックする
#つまり２回移動先がキノコが存在するマスかどうかをチェックする
#キノコがあった時上下移動するが、上下移動は２回実施され最初の１回移動時に左右移動反転を行う
#
#キ  ■□	（下がる前の段
#	↓
#キ ■□	（下がる前の段（移動先がキノコの横であることを判定し、次は下＆左移動
#	↓
#キ □		（下がる前の段
#　■　		（中間パターン（下向きキャラ）でキノコに衝突（ここで横方向の向きを反転
# 　　　	（次の段
#	↓
#キ　　		（下がる前の段
#　□
#　 ■→	（次の段へ・・・上下移動は２段階で移動する（下＆右移動
#
#return 2/1/0 = 毒キノコある/キノコある/ない
#-----------------------------------------------------------------
def kinoko_check( _wk ):

	if( GWK[_wk + ccond] & F_HMOVE ):
		#右移動時、見た目で2ドット減算
		#_xp = ( GWK[_wk + cxpos] + ( GWK[move_speed] * 2 ) + (CSIZE-2) ) // CSIZE
		_xp = pyxel.floor( ( GWK[_wk + cxpos] + ( GWK[move_speed] * 2 ) + (CSIZE-2) ) / CSIZE )
	else:
		#_xp = ( GWK[_wk + cxpos] - ( GWK[move_speed] * 2 ) ) // CSIZE
		_xp = pyxel.floor( ( GWK[_wk + cxpos] - ( GWK[move_speed] * 2 ) ) / CSIZE )

	#枠内チェック
	if( 1 <= _xp < (XSIZE - 1) ):
		#_yp = ( GWK[_wk + cypos] ) // CSIZE
		_yp = pyxel.floor( ( GWK[_wk + cypos] ) / CSIZE )
		_id = GWK[SCREEN_WORK + ( _yp * XSIZE + _xp )]
		if( 0x0b <= _id <= 0x0e ):
			return 1
		elif( 0x0f <= _id <= 0x12 ):
			return 2
		else:
			return 0

	return 0


#-----------------------------------------------------------------
#キノコ復活
#	ダメージ受けたキノコや毒キノコをノーマルキノコに変えていく
#	１フレーム１個変える、終わったら"1"を返す
#-----------------------------------------------------------------
def kinoko_revival():

	GWK[wait_counter] -= 1
	if( GWK[wait_counter] < 0 ):
		GWK[wait_counter]  = 5

		for _yp in range( YSIZE ):
			for _xp in range( XSIZE ):
				_wk = SCREEN_WORK + ( ( _yp * XSIZE ) + _xp )
				if( GWK[_wk] == 0 ):
					continue
				elif( GWK[_wk] != 0x0b ):
					GWK[_wk] = 0x0b
					return (0)

		#全チェック終了
		return (1)
	else:
		return (0)

#-----------------------------------------------------------------
#ムカデ初期化
#-----------------------------------------------------------------
def mukade_init():

	GWK[move_speed] = 2

	for _cnt in range( MUKADE_MAX ):
		_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
		if( _cnt == 0 ):
			#先頭
			GWK[_wk + cid] = 0x02
			GWK[_wk + ccond] = F_HEAD		#先頭セット
			GWK[_wk + cjoin] = -1			#接続先は無い（先頭）
			GWK[_wk + canum] = ANUM_MUKADE_LEFT
			GWK[_wk + cmukade] = 0		#MUKADE No.0
		else:
			GWK[_wk + cid] = 0x08
			GWK[_wk + ccond] = 0
			GWK[_wk + cjoin] = _cnt - 1		#接続先id
			GWK[_wk + canum] = ANUM_BODY_LEFT
			GWK[_wk + cmukade] = _cnt		#MUKADE No.

		GWK[_wk + cxpos] = SCREEN_WIDTH//2

		if( GWK[game_adv] == G_TITLE ):
			GWK[_wk + cypos] = TITLE_Y
		else:
			GWK[_wk + cypos] = CSIZE

	#保存ワークには初期値をセットしておく
	for _cnt in range( MUKADE_MAX ):
		for _cnt2 in range( SINGLE_SAVE_MAX ):
			_wk = SAVE_WORK + ( _cnt * SINGLE_SAVE_MAX * SAVE_PARTS ) + ( _cnt2 * SAVE_PARTS )
			GWK[_wk + 0] = 0
			GWK[_wk + 1] = SCREEN_WIDTH//2
			if( GWK[game_adv] == G_TITLE ):
				GWK[_wk + 2] = TITLE_Y
			else:
				GWK[_wk + 2] = CSIZE
			GWK[_wk + 3] = 0
	
#-----------------------------------------------------------------
#プレイヤーの弾に当たって分断、胴体が頭に変わる時に呼ばれる
#-----------------------------------------------------------------
def mukade_head_change( _wk ):
	GWK[_wk + ccond] |= F_HEAD		#先頭セット
	GWK[_wk + cjoin] = -1			#接続先は無い（先頭）

	#横移動方向反転
	if( GWK[_wk + ccond] & F_HMOVE ):
		GWK[_wk + ccond] &= ~F_HMOVE
	else:
		GWK[_wk + ccond] |= F_HMOVE

	#パターン番号再設定
	mukade_anum_set(_wk)

#-----------------------------------------------------------------
#ムカデ右端到達処理（右にキノコも同様）
#-----------------------------------------------------------------
def mukade_right_side( _wk ):
	#print("ムカデ右端到達処理")
	#左右移動方向反転は縦移動中に行う
	#[不要]GWK[_wk + ccond] &= ~F_HMOVE	#左移動セット
	GWK[_wk + ccond] |= F_VMOVE		#縦移動セット

	if( GWK[_wk + ccond] & F_DOKU ):
		GWK[_wk + cmcnt] = 3
	else:
		GWK[_wk + cmcnt] = 1

	#print("右移動 Y=",GWK[_wk + cypos])
	#下限？
	if( GWK[_wk + cypos] >= ( SCREEN_HEIGHT - CSIZE ) ):
		#print("右端で下限なので上方向移動セット")
		GWK[_wk + ccond] |= F_DIR 	#上移動セット
	#上移動かつ上移動上限？
	if( ( GWK[_wk + ccond] & F_DIR ) and ( GWK[_wk + cypos] <= ( SCREEN_HEIGHT - ( CSIZE * DOWN_AREA ) ) ) ):
		#print("右端で上移動かつ上移動上限なので下方向移動セット")
		GWK[_wk + ccond] &= ~F_DIR 	#下移動セット

	#アニメ番号制御
	mukade_anum_set(_wk)

#-----------------------------------------------------------------
#ムカデ左端到達処理（左にキノコも同様）
#-----------------------------------------------------------------
def mukade_left_side( _wk ):
	#print("ムカデ左端到達処理")
	#左右移動方向反転は縦移動中に行う
	#[不要]GWK[_wk + ccond] |= F_HMOVE		#右移動セット
	GWK[_wk + ccond] |= F_VMOVE		#縦移動セット

	if( GWK[_wk + ccond] & F_DOKU ):
		GWK[_wk + cmcnt] = 3
	else:
		GWK[_wk + cmcnt] = 1

	#print("左移動 Y=",GWK[_wk + cypos])
	#下限？
	if( GWK[_wk + cypos] >= ( SCREEN_HEIGHT - CSIZE ) ):
		#print("左端で下限なので上方向移動セット")
		GWK[_wk + ccond] |= F_DIR 	#上移動セット
	#上移動かつ上移動上限？
	if( ( GWK[_wk + ccond] & F_DIR ) and ( GWK[_wk + cypos] <= ( SCREEN_HEIGHT - ( CSIZE * DOWN_AREA ) ) ) ):
		#print("左端で上移動かつ上移動上限なので下方向移動セット")
		GWK[_wk + ccond] &= ~F_DIR 	#下移動セット

	#アニメ番号制御
	mukade_anum_set(_wk)

#-----------------------------------------------------------------
#通常移動動作
#　キ　　　■	登場
#　キ　　■□	スピード２で４回移動で胴体出現、接続先に追従（接続先のカウンタ＋４の座標にセット
#　キ　■□□	さらに次の胴体出現
#　キ■□□□	先頭キノコに衝突
#　キ□□□		先頭下に移動（下がる時も途中が存在する（いきなり８ドット移動では無くてスピード分
#　　■			なので胴体も追従で問題ない
#
#HIT時動作
#　　■□□□□□□□□
#　　　　　　↑			HIT
#
#　　■□□□キ■□□□	HITした箇所がキノコに変身、その手前が先頭に変化
#
#　■□□□　キ□□□	先端はそのまま進行
#　　　　　　　■		HITした後ろはキノコに衝突するので下に移動して逆方向に移動開始
#						後ろは先を追従してるので問題ない
#
#-----------------------------------------------------------------
#(済)まず先頭の動きを作る
#(済)次に胴体の動き（追従）を作る
#HITして切れた動作を作る

#-----------------------------------------------------------------
#ムカデアニメパターンセット
#	状態フラグ変化時に呼ぶ：F_VMOVE、F_HMOVE、F_DIR
#	F_VMOVE=1, F_DIR=1の時		上向き	canum = ANUM_MUKADE_UP(6)
#	F_VMOVE=1, F_DIR=0の時		下向き	canum = ANUM_MUKADE_DOWN(4)
#	F_VMOVE=0, F_HMOVE=1の時	右向き	canum = ANUM_MUKADE_RIGHT(2)
#	F_VMOVE=0, F_HMOVE=0の時	左向き	canum = ANUM_MUKADE_LEFT(0)
#-----------------------------------------------------------------
def mukade_anum_set( _wk ):
	if( GWK[_wk + ccond] & F_VMOVE ):
		if( GWK[_wk + ccond] & F_DIR ):
			GWK[_wk + canum] = ANUM_MUKADE_UP
		else:
			GWK[_wk + canum] = ANUM_MUKADE_DOWN
	else:
		if( GWK[_wk + ccond] & F_HMOVE ):
			GWK[_wk + canum] = ANUM_MUKADE_RIGHT
		else:
			GWK[_wk + canum] = ANUM_MUKADE_LEFT

#-----------------------------------------------------------------
def body_anum_set( _wk ):
	if( GWK[_wk + ccond] & F_VMOVE ):
		if( GWK[_wk + ccond] & F_DIR ):
			GWK[_wk + canum] = ANUM_BODY_UP
		else:
			GWK[_wk + canum] = ANUM_BODY_DOWN
	else:
		if( GWK[_wk + ccond] & F_HMOVE ):
			GWK[_wk + canum] = ANUM_BODY_RIGHT
		else:
			GWK[_wk + canum] = ANUM_BODY_LEFT

#-----------------------------------------------------------------
#ムカデ制御
#	上下移動方向、縦横移動フラグを見てGWK[move_speed]で移動する
#	横移動時、移動先がキノコ、または、画面端の時、上下移動（縦移動）に切り替わる
#	下移動時、画面一番下まで行ったとき、下移動から上移動に切り替わる
#	上移動時、下からDOWN_AREAを上限として上移動から下移動に切り替わる
#	上下移動はCSIZE分移動して横移動に切り替わる、移動方向は下移動する前に切り替えておく
#	毒キノコに当たった時は横移動に切り替わらず画面下まで移動する（左右パターンで一回分の移動を繰り返しながら
#	キノコに当たる時には中間パターンになっているので移動前にキノコチェックしているようだ
#	（一回分先にチェックしている
#
#	縦移動時、下移動時下向き、上移動時上向きパターンが存在する
#	縦移動時、左向きの場合、左→下→右というふうに中間パターンは１個で移動している
#
#	プレイヤーの弾に当たった時当たった部分はキノコに変わり、ムカデは分割される
#	分割された後ろ側はキノコに当たることになるのでキノコに当たった動作となる
#-----------------------------------------------------------------
def mukade_control():
	#ヒットチェック
	for _cnt in range( MUKADE_MAX ):
		_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
		if( GWK[_wk + ccond] & F_LIVE ):
			#プレイヤー本体、または、弾に当たった
			if( GWK[_wk + ccond] & F_HIT ):
				#当たったところはキノコに変わる
				_sw = SCREEN_WORK + ( ( GWK[_wk + cypos] // CSIZE ) * XSIZE + ( GWK[_wk + cxpos] // CSIZE ) )
				if( GWK[_sw] == 0 ):
					#何も無ければキノコをセット
					GWK[_sw] = 0x0b

				GWK[_wk + ccond] = 0				#キノコに変わって消滅する
				GWK[_wk + cypos] = SCREEN_HEIGHT	#画面外へ

				#当たったすぐ後ろが頭に変わる
				_wk2 = _wk + CWORK_SIZE
				if( GWK[_wk2 + ccond] & F_LIVE ):
					#横移動反転
					GWK[_wk2 + ccond] |= F_HEAD		#先頭セット
					GWK[_wk2 + cjoin] = -1			#接続先は無くなる

					#先頭に変わったところのフラグをチェック（方向フラグは継承してるはず）
					if( GWK[_wk2 + ccond] & F_HMOVE ):
						#右移動中は右端到達処理
						mukade_right_side( _wk2 )
					else:
						#左移動中は左端到達処理
						mukade_left_side( _wk2 )
				break	#ヒット処理は１フレーム１回

	#移動処理
	for _cnt in range( MUKADE_MAX ):
		_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
		if( GWK[_wk + ccond] & F_LIVE ):
			if( GWK[_wk + ccond] & F_HEAD ):
				mukade_head_move( _wk )
			else:
				mukade_body_move( _wk )


	#ムカデ全滅チェック
	_work = 0
	for _cnt in range( MUKADE_MAX ):
		_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
		if( GWK[_wk + ccond] & F_LIVE ):
			_work += 1

	if( _work == 0 ):
		GWK[wait_counter] = 30
		GWK[game_adv] = G_CLEAR
		GWK[game_subadv] = GS_INIT

#-----------------------------------------------------------------
#ムカデ頭移動制御
#	毒の縦移動が２回横移動＋１回縦移動のような感じになっている
#-----------------------------------------------------------------
def mukade_head_move( _wk ):
	#停止以外
	if( ( GWK[_wk + ccond] & F_STOP ) == 0 ):
		#縦移動？
		if( GWK[_wk + ccond] & F_VMOVE ):
			#縦移動
			if( GWK[_wk + ccond] & F_DIR ):
				#縦移動には横移動も同時に行う
				if( GWK[_wk + ccond] & F_HMOVE ):
					GWK[_wk + cxpos] += GWK[move_speed]
					#if( GWK[_wk + cmcnt] != 0 ):

					if( ( ( GWK[_wk + ccond] & F_DOKU ) and ( GWK[_wk + cmcnt] == 2 ) ) or
						( ( ( GWK[_wk + ccond] & F_DOKU ) == 0 ) and ( GWK[_wk + cmcnt] == 1 ) ) ):

						#中間パターンなら横移動方向反転
						GWK[_wk + ccond] &= ~F_HMOVE
				else:
					GWK[_wk + cxpos] -= GWK[move_speed]
					#if( GWK[_wk + cmcnt] != 0 ):

					if( ( ( GWK[_wk + ccond] & F_DOKU ) and ( GWK[_wk + cmcnt] == 2 ) ) or
						( ( ( GWK[_wk + ccond] & F_DOKU ) == 0 ) and ( GWK[_wk + cmcnt] == 1 ) ) ):

						#中間パターンなら横移動方向反転
						GWK[_wk + ccond] |= F_HMOVE

				#アニメ番号制御
				mukade_anum_set(_wk)

				#上移動（毒キノコの移動は下のみなのでここは判定を入れない）
				GWK[_wk + cypos] -= CSIZE//2	#GWK[move_speed]
				#上限チェック
				if( GWK[_wk + cypos] < ( SCREEN_HEIGHT - ( DOWN_AREA * CSIZE ) ) ):
					GWK[_wk + cypos] = ( SCREEN_HEIGHT - ( DOWN_AREA * CSIZE ) )
					GWK[_wk + ccond] &= ~F_DIR		#下移動セット
					GWK[_wk + ccond] &= ~F_VMOVE	#横移動セット

					#アニメ番号制御
					mukade_anum_set(_wk)

				#移動カウンタ減算（CSIZE分移動）
				GWK[_wk + cmcnt] -= 1
				if( GWK[_wk + cmcnt] < 0 ):
					GWK[_wk + cmcnt] = 0

					#縦移動終了
					GWK[_wk + ccond] &= ~F_VMOVE	#横移動セット

					#アニメ番号制御
					mukade_anum_set(_wk)

			else:
				#縦移動には横移動も同時に行う
				if( GWK[_wk + ccond] & F_HMOVE ):
					GWK[_wk + cxpos] += GWK[move_speed]
					if( GWK[_wk + cmcnt] != 0 ):
						#中間パターンなら横移動方向反転
						GWK[_wk + ccond] &= ~F_HMOVE
				else:
					GWK[_wk + cxpos] -= GWK[move_speed]
					if( GWK[_wk + cmcnt] != 0 ):
						#中間パターンなら横移動方向反転
						GWK[_wk + ccond] |= F_HMOVE

				#アニメ番号制御
				mukade_anum_set(_wk)

				#毒キノコの縦移動は横２回縦１回、通常キノコは横１回縦１回の動き
				if( ( ( GWK[_wk + ccond] & F_DOKU ) and ( ( GWK[_wk + cmcnt] == 2 ) or ( GWK[_wk + cmcnt] == 0 ) ) ) or
					( ( ( GWK[_wk + ccond] & F_DOKU ) == 0 ) and ( ( GWK[_wk + cmcnt] == 1 ) or ( GWK[_wk + cmcnt] == 0 ) ) ) ):
					#下移動
					GWK[_wk + cypos] += CSIZE//2	#GWK[move_speed]

					#下限チェック
					if( GWK[game_adv] == G_TITLE ):
						if( GWK[_wk + cypos] > ( TITLE_Y + (CSIZE * 3) ) ):
							GWK[_wk + cypos] = SCREEN_HEIGHT	#画面外へ
							GWK[_wk + ccond] |= F_STOP

					else:
						if( GWK[_wk + cypos] > ( SCREEN_HEIGHT - CSIZE - 1 ) ):		#"-1"は調整（毒キノコ判定移動で）
							GWK[_wk + cypos] = ( SCREEN_HEIGHT - CSIZE )
							GWK[_wk + ccond] |= F_DIR		#上移動セット
							GWK[_wk + ccond] &= ~F_VMOVE	#横移動セット
							GWK[_wk + ccond] &= ~F_DOKU		#毒キノコクリア
							GWK[_wk + cmcnt] = 0

							#アニメ番号制御
							mukade_anum_set(_wk)

				#移動カウンタ減算（CSIZE分移動）
				GWK[_wk + cmcnt] -= 1
				if( GWK[_wk + cmcnt] < 0 ):
					GWK[_wk + cmcnt] = 0

					#縦移動終了
					GWK[_wk + ccond] &= ~F_VMOVE	#横移動セット

					#アニメ番号制御
					mukade_anum_set(_wk)

					#毒キノコ移動中？
					if( GWK[_wk + ccond] & F_DOKU ):
						if( GWK[_wk + ccond] & F_HMOVE ):
							#右移動の時は右端到達処理
							mukade_right_side( _wk )
						else:
							#左移動の時は左端到達処理
							mukade_left_side( _wk )
					
					#アニメ番号制御
					mukade_anum_set(_wk)

		else:
			#横移動
			if( GWK[_wk + ccond] & F_HMOVE ):
				#右移動
				GWK[_wk + cxpos] += GWK[move_speed]

				#移動方向前方にキノコ有る？
				_res = kinoko_check( _wk )
				#キノコ見つけた
				if( _res == 1 ):
					#右端到達処理
					mukade_right_side( _wk )
				elif( _res == 2 ):
					#強制縦下移動になる・・・
					GWK[_wk + ccond] |= F_DOKU
					#右端到達処理
					mukade_right_side( _wk )
				else:
					#右端チェック
					if( ( GWK[_wk + cxpos] + GWK[move_speed] ) > ( SCREEN_WIDTH - CSIZE - CSIZE ) ):
						GWK[_wk + cxpos] = ( SCREEN_WIDTH - CSIZE - CSIZE ) - GWK[move_speed]
						#右端到達処理
						mukade_right_side( _wk )
			else:
				#左移動
				GWK[_wk + cxpos] -= GWK[move_speed]

				#移動方向前方にキノコ有る？
				_res = kinoko_check( _wk )
				#キノコ見つけた
				if( _res == 1 ):
					#左端到達処理
					mukade_left_side( _wk )
				elif( _res == 2 ):
					#強制縦下移動になる・・・
					GWK[_wk + ccond] |= F_DOKU
					#左端到達処理
					mukade_left_side( _wk )
				else:
					#左端チェック
					if( ( GWK[_wk + cxpos] - GWK[move_speed] ) < CSIZE ):
						GWK[_wk + cxpos] = CSIZE + GWK[move_speed]
						#左端到達処理
						mukade_left_side( _wk )

	#接続元は接続先の状態フラグを引き継ぐ
	_save_wk = SAVE_WORK + ( GWK[_wk + cmukade] * SINGLE_SAVE_MAX * SAVE_PARTS )
	GWK[_save_wk + ( GWK[_wk + csavecnt] * SAVE_PARTS ) + 0] = GWK[_wk + ccond] & (F_VMOVE+F_HMOVE+F_DIR+F_DOKU)
	GWK[_save_wk + ( GWK[_wk + csavecnt] * SAVE_PARTS ) + 1] = GWK[_wk + cxpos]
	GWK[_save_wk + ( GWK[_wk + csavecnt] * SAVE_PARTS ) + 2] = GWK[_wk + cypos]
	GWK[_save_wk + ( GWK[_wk + csavecnt] * SAVE_PARTS ) + 3] = 0		#（未使用）
	GWK[_wk + csavecnt] += 1
	if( SINGLE_SAVE_MAX <= GWK[_wk + csavecnt] ):
		GWK[_wk + csavecnt] = 0

#-----------------------------------------------------------------
#ムカデ胴体移動制御
#	GWK[move_speed]=2は変えられない・・・・かも
#-----------------------------------------------------------------
def mukade_body_move( _wk ):

	GWK[_wk + ccond] &= ~(F_VMOVE+F_HMOVE+F_DIR+F_DOKU)

	#接続先から情報取得
	#接続先ワークをセット
	_from_wk = MUKADE_WORK + ( GWK[_wk + cjoin] * CWORK_SIZE )

	#接続先の保存ワークをセット
	_save_from_wk = SAVE_WORK + ( GWK[_wk + cjoin] * SINGLE_SAVE_MAX * SAVE_PARTS )

	_addcnt = ( GWK[_from_wk + csavecnt] - 1 - 4 ) & 0x0f	#格納数は0x10なので0x0fでマスクする
	#_addcnt = ( GWK[_from_wk + csavecnt] - 1 - ( CSIZE//GWK[move_speed] ) ) & (SINGLE_SAVE_MAX-1)	#格納数は0x10なので0x0fでマスクする

	GWK[_wk + ccond] |= GWK[_save_from_wk + ( _addcnt * SAVE_PARTS ) + 0]
	GWK[_wk + cxpos]  = GWK[_save_from_wk + ( _addcnt * SAVE_PARTS ) + 1]
	GWK[_wk + cypos]  = GWK[_save_from_wk + ( _addcnt * SAVE_PARTS ) + 2]

	#自分の状態を保存
	_save_wk = SAVE_WORK + ( GWK[_wk + cmukade] * SINGLE_SAVE_MAX * SAVE_PARTS )
	GWK[_save_wk + ( GWK[_wk + csavecnt] * SAVE_PARTS ) + 0] = GWK[_wk + ccond] & (F_VMOVE+F_HMOVE+F_DIR+F_DOKU)
	GWK[_save_wk + ( GWK[_wk + csavecnt] * SAVE_PARTS ) + 1] = GWK[_wk + cxpos]
	GWK[_save_wk + ( GWK[_wk + csavecnt] * SAVE_PARTS ) + 2] = GWK[_wk + cypos]
	GWK[_save_wk + ( GWK[_wk + csavecnt] * SAVE_PARTS ) + 3] = 0		#（未使用）
	#保存カウンタ更新
	GWK[_wk + csavecnt] += 1
	if( SINGLE_SAVE_MAX <= GWK[_wk + csavecnt] ):
		GWK[_wk + csavecnt] = 0

	#アニメパターン更新
	body_anum_set( _wk )

#-----------------------------------------------------------------
#クモ制御
#	上下移動をベースとして上下移動の組み合わせが時々混じるような動き
#	ランダムっぽいけど、、、動きはまだ納得いかない
#-----------------------------------------------------------------
def kumo_control():

	#移動パターンをいくつか作ってどれかを選ぶ・・・
	movtbl = [0 for tbl in range(8)]
				#カウンタ、xspd,yspd
	movtbl[0] = [	20, -2,  2,
					18,  0, -2,
					12,  0,  2,
					18,  0, -2,
					24,  0,  2,
					20, -2, -2,
					20, -2,  2,
					20, -2, -2,
					20, -2,  2,
					20, -2, -2,
					20, -2,  2,
					0xff]
	movtbl[1] = [	20, -2,  2,
					18,  0, -2,
					12,  0,  2,
					18,  0, -2,
					24,  0,  2,
					20, -2, -2,
					20, -2,  2,
					20, -2, -2,
					20, -2,  2,
					18,  0, -2,
					12,  0,  2,
					18,  0, -2,
					24,  0,  2,
					20, -2, -2,
					20, -2,  2,
					0xff]
	movtbl[2] = [	20, -2,  2,
					20, -2, -2,
					20, -2,  2,
					20, -2, -2,
					20, -2,  2,
					18,  0, -2,
					12,  0,  2,
					18,  0, -2,
					24,  0,  2,
					20, -2, -2,
					20, -2,  2,
					0xff]
	movtbl[3] = [	20, -2,  2,
					18,  0, -2,
					18,  0,  2,
					20, -2, -2,
					20, -2,  2,
					20, -2, -2,
					20, -2,  2,
					18,  0, -2,
					18,  0,  2,
					20, -2, -2,
					20, -2,  2,
					0xff]
	movtbl[4] = [	20, -2,  2,
					20, -2, -2,
					20, -2,  2,
					18,  0, -2,
					12,  0,  2,
					18,  0, -2,
					24,  0,  2,
					20, -2, -2,
					20, -2,  2,
					20, -2, -2,
					20, -2,  2,
					0xff]
	movtbl[5] = [	20, -2,  2,
					18,  0, -2,
					18,  0,  2,
					20, -2, -2,
					20, -2,  2,
					18,  0, -2,
					12,  0,  2,
					18,  0, -2,
					24,  0,  2,
					20, -2, -2,
					20, -2,  2,
					18,  0, -2,
					18,  0,  2,
					20, -2, -2,
					20, -2,  2,
					0xff]
	movtbl[6] = [	13, -3,  3,
					13, -3, -3,
					13, -3,  3,
					13, -3, -3,
					13, -3,  3,
					13, -3, -3,
					13, -3,  3,
					0xff]
	movtbl[7] = [	13, -3,  3,
					13, -3, -3,
					13, -3,  3,
					18,  0, -2,
					12,  0,  2,
					18,  0, -2,
					24,  0,  2,
					13, -3, -3,
					13, -3,  3,
					13, -3, -3,
					13, -3,  3,
					0xff]

	for _cnt in range( KUMO_MAX ):
		_wk = KUMO_WORK + ( _cnt * CWORK_SIZE )
		if( GWK[_wk + cstep] == 0 ):
			#出現待ち
			GWK[_wk + cwait] -= 1
			if( GWK[_wk + cwait] < 0 ):
				#出現位置をセット
				if( pyxel.frame_count & 1 ):
					#右から左へ移動
					GWK[_wk + cxpos] = SCREEN_WIDTH
				else:
					#左から右へ移動
					GWK[_wk + cxpos] = -0x12
					GWK[_wk + ccond] |= F_HMOVE

				GWK[_wk + ccond] |= F_LIVE
				GWK[_wk + cypos] = SCREEN_HEIGHT - ( DOWN_AREA * CSIZE )
				GWK[_wk + cstep] = 1

		elif( GWK[_wk + cstep] == 1 ):
			_tbl = movtbl[GWK[_wk + cmpat]]
			if( GWK[_wk + ccond] & F_LIVE ):
				if( _tbl[ GWK[_wk + cmnum] * 3 + 0 ] == 0xff ):
					GWK[_wk + ccond] = 0
				else:
					if( GWK[_wk + ccond] & F_HMOVE ):
						#右移動
						GWK[_wk + cxspd] = _tbl[ GWK[_wk + cmnum] * 3 + 1 ] * (-1)
					else:
						#左移動
						GWK[_wk + cxspd] = _tbl[ GWK[_wk + cmnum] * 3 + 1 ]

					GWK[_wk + cyspd] = _tbl[ GWK[_wk + cmnum] * 3 + 2 ]
					GWK[_wk + cmcnt] += 1
					if( _tbl[ GWK[_wk + cmnum] * 3 + 0 ] < GWK[_wk + cmcnt] ):
						GWK[_wk + cmnum] += 1
						GWK[_wk + cmcnt] = 0
					else:
						GWK[_wk + cxpos] += GWK[_wk + cxspd]
						GWK[_wk + cypos] += GWK[_wk + cyspd]
						
						if( GWK[_wk + cxpos] < -0x12 ):
							GWK[_wk + ccond] = 0
							GWK[_wk + cwait] = kumo_wait_set()

#-----------------------------------------------------------------
#クモ登場待ち時間セット
#-----------------------------------------------------------------
def kumo_wait_set():
	_min = 200
	_max = 500
	if( GWK[stage_number] < 10 ):
		_min = _min - ( GWK[stage_number] * 10 )
		_max = _max - ( GWK[stage_number] * 20 )
	else:
		_min = 100
		_max = 300
	
	return ( pyxel.rndi( _min, _max ) )

#-----------------------------------------------------------------
#
#-----------------------------------------------------------------
def kumo_init():

	for _cnt in range( KUMO_MAX ):
		_wk = KUMO_WORK + ( _cnt * CWORK_SIZE )
		GWK[_wk + cid] = 0x13
		GWK[_wk + canum] = 0x0a
		GWK[_wk + cstep] = 0
		GWK[_wk + cmpat] = ( GWK[stage_number] & 7 )
		GWK[_wk + cmcnt] = 0
		GWK[_wk + cmnum] = 0
		GWK[_wk + ccond] = 0
		GWK[_wk + cwait] = kumo_wait_set()

		GWK[_wk + cxpos] = 0
		GWK[_wk + cypos] = 0
		GWK[_wk + cxspd] = 0
		GWK[_wk + cyspd] = 0
		GWK[_wk + cacnt] = 0
		GWK[_wk + caspd] = 0
		

#-----------------------------------------------------------------
#プレイヤー制御
#-----------------------------------------------------------------
def player_control():

	if( GWK[PLY_WORK + ccond] & F_LIVE ):
		#移動操作
		if( getInputRIGHT() ):
			GWK[PLY_WORK + cxpos] += GWK[PLY_WORK + cxspd]
			#右端チェック
			if( ( GWK[PLY_WORK + cxpos] + CSIZE ) > ( SCREEN_WIDTH - CSIZE ) ):
				GWK[PLY_WORK + cxpos] = ( SCREEN_WIDTH - CSIZE ) - CSIZE
			#移動した先にキノコがある？
			#今の画面位置を取得
			#[右上]
			_xp = ( GWK[PLY_WORK + cxpos] + (CSIZE-1) ) // CSIZE
			_yp = GWK[PLY_WORK + cypos] // CSIZE
			if( GWK[SCREEN_WORK + ( _yp * XSIZE + _xp )] != 0 ):
				#キノコがあるのでキノコの横（左）に移動
				GWK[PLY_WORK + cxpos] = ( _xp - 1 ) * CSIZE
			#[右下]
			_xp = ( GWK[PLY_WORK + cxpos] + (CSIZE-1) ) // CSIZE
			_yp = ( GWK[PLY_WORK + cypos] + (CSIZE-1) ) // CSIZE
			if( GWK[SCREEN_WORK + ( _yp * XSIZE + _xp )] != 0 ):
				#キノコがあるのでキノコの横（左）に移動
				GWK[PLY_WORK + cxpos] = ( _xp - 1 ) * CSIZE

		if( getInputLEFT() ):
			GWK[PLY_WORK + cxpos] -= GWK[PLY_WORK + cxspd]
			if( GWK[PLY_WORK + cxpos] < CSIZE ):
				GWK[PLY_WORK + cxpos] = CSIZE
			#移動した先にキノコがある？
			#今の画面位置を取得
			#[左上]
			_xp = GWK[PLY_WORK + cxpos] // CSIZE
			_yp = GWK[PLY_WORK + cypos] // CSIZE
			if( GWK[SCREEN_WORK + ( _yp * XSIZE + _xp )] != 0 ):
				#キノコがあるのでキノコの横（右）に移動
				GWK[PLY_WORK + cxpos] = ( _xp + 1 ) * CSIZE
			#[左下]
			_xp = GWK[PLY_WORK + cxpos] // CSIZE
			_yp = ( GWK[PLY_WORK + cypos] + (CSIZE-1) ) // CSIZE
			if( GWK[SCREEN_WORK + ( _yp * XSIZE + _xp )] != 0 ):
				#キノコがあるのでキノコの横（右）に移動
				GWK[PLY_WORK + cxpos] = ( _xp + 1 ) * CSIZE

		if( getInputDOWN() ):
			GWK[PLY_WORK + cypos] += GWK[PLY_WORK + cyspd]
			if( GWK[PLY_WORK + cypos] > ( SCREEN_HEIGHT - CSIZE ) ):
				GWK[PLY_WORK + cypos] = ( SCREEN_HEIGHT - CSIZE )
			#移動した先にキノコがある？
			#今の画面位置を取得
			#[左下]
			_xp = GWK[PLY_WORK + cxpos] // CSIZE
			_yp = ( GWK[PLY_WORK + cypos] + (CSIZE-1) ) // CSIZE
			if( GWK[SCREEN_WORK + ( _yp * XSIZE + _xp )] != 0 ):
				#キノコがあるのでキノコの横（上）に移動
				GWK[PLY_WORK + cypos] = ( _yp - 1 ) * CSIZE
			#[右下]
			_xp = ( GWK[PLY_WORK + cxpos] + (CSIZE-1) ) // CSIZE
			_yp = ( GWK[PLY_WORK + cypos] + (CSIZE-1) ) // CSIZE
			if( GWK[SCREEN_WORK + ( _yp * XSIZE + _xp )] != 0 ):
				#キノコがあるのでキノコの横（上）に移動
				GWK[PLY_WORK + cypos] = ( _yp - 1 ) * CSIZE

		if( getInputUP() ):
			GWK[PLY_WORK + cypos] -= GWK[PLY_WORK + cyspd]
			if( GWK[PLY_WORK + cypos] < ( SCREEN_HEIGHT - ( CSIZE * DOWN_AREA ) ) ):
				GWK[PLY_WORK + cypos] = ( SCREEN_HEIGHT - ( CSIZE * DOWN_AREA ) )
			#移動した先にキノコがある？
			#今の画面位置を取得
			#[左上]
			_xp = GWK[PLY_WORK + cxpos] // CSIZE
			_yp = GWK[PLY_WORK + cypos] // CSIZE
			if( GWK[SCREEN_WORK + ( _yp * XSIZE + _xp )] != 0 ):
				#キノコがあるのでキノコの横（下）に移動
				GWK[PLY_WORK + cypos] = ( _yp + 1 ) * CSIZE
			#[右上]
			_xp = ( GWK[PLY_WORK + cxpos] + (CSIZE-1) ) // CSIZE
			_yp = GWK[PLY_WORK + cypos] // CSIZE
			if( GWK[SCREEN_WORK + ( _yp * XSIZE + _xp )] != 0 ):
				#キノコがあるのでキノコの横（下）に移動
				GWK[PLY_WORK + cypos] = ( _yp + 1 ) * CSIZE
	
		#中心の座標
		_xp = GWK[PLY_WORK + cxpos] + (CSIZE/2)
		_yp = GWK[PLY_WORK + cypos] + (CSIZE/2)
	
		#プレイヤーとのヒットチェック（範囲判定）
		#プレイヤーとノミ
		for _cnt in range( NOMI_MAX ):
			_wk = NOMI_WORK + ( _cnt * CWORK_SIZE )
			if( GWK[_wk + ccond] & F_LIVE ):
				if( ( ( GWK[_wk + cxpos] - (CSIZE/2) ) <= _xp < ( GWK[_wk + cxpos]+10 + (CSIZE/2) ) ) and 
					( ( GWK[_wk + cypos] - (CSIZE/2) ) <= _yp < ( GWK[_wk + cypos]+8  + (CSIZE/2) ) ) ):
						#HIT!
						GWK[_wk + ccond] = 0
						GWK[PLY_WORK + ccond] |= F_HIT
						#ノミヒットスコアセット
						add_score(100)
						return
		
		##プレイヤーとサソリ（出現位置が違うので当たらない）
		#for _cnt in range( SASORI_MAX ):
		#	_wk = SASORI_WORK + ( _cnt * CWORK_SIZE )
		#	if( GWK[_wk + ccond] & F_LIVE ):
		#		if( ( ( GWK[_wk + cxpos] - (CSIZE/2) ) <= _xp < ( GWK[_wk + cxpos]+0x10 + (CSIZE/2) ) ) and 
		#			( ( GWK[_wk + cypos] - (CSIZE/2) ) <= _yp < ( GWK[_wk + cypos]+0x10 + (CSIZE/2) ) ) ):
		#				#HIT!
		#				GWK[_wk + ccond] = 0
		#				GWK[PLY_WORK + ccond] |= F_HIT
		#				#サソリヒットスコアセット
		#				return

		#プレイヤーとクモ
		for _cnt in range( KUMO_MAX ):
			_wk = KUMO_WORK + ( _cnt * CWORK_SIZE )
			if( GWK[_wk + ccond] & F_LIVE ):
				if( ( ( GWK[_wk + cxpos] - (CSIZE/2) ) <= _xp < ( GWK[_wk + cxpos]+0x12 + (CSIZE/2) ) ) and 
					( ( GWK[_wk + cypos] - (CSIZE/2) ) <= _yp < ( GWK[_wk + cypos]+8 + (CSIZE/2) ) ) ):
						#HIT!
						GWK[_wk + ccond] = 0
						GWK[PLY_WORK + ccond] |= F_HIT
						#クモヒットスコアセット
						_yp = GWK[_wk + cypos] // CSIZE
						if( _yp >= YSIZE - 2 ):
							add_score(900)
						elif( _yp >= YSIZE - 4 ):
							add_score(600)
						else:
							add_score(300)
						return

		#プレイヤーとムカデ
		for _cnt in range( MUKADE_MAX ):
			_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
			if( GWK[_wk + ccond] & F_LIVE ):
#				if( ( ( GWK[_wk + cxpos] - (CSIZE/2) ) <= _xp < ( GWK[_wk + cxpos]+7  + (CSIZE/2) ) ) and 
#					( ( GWK[_wk + cypos] - (CSIZE/2) ) <= _yp < ( GWK[_wk + cypos]+7  + (CSIZE/2) ) ) ):
				if( ( ( GWK[_wk + cxpos] - (CSIZE/2) ) <= _xp < ( GWK[_wk + cxpos]+6  + (CSIZE/2) ) ) and 
					( ( GWK[_wk + cypos] - (CSIZE/2) ) <= _yp < ( GWK[_wk + cypos]+6  + (CSIZE/2) ) ) ):
						#HIT!
						GWK[_wk + ccond] |= F_HIT		#ムカデヒット後の処理はムカデ側で実施
						GWK[PLY_WORK + ccond] |= F_HIT
						#ムカデヒットスコアセット
						add_score(100)
						return

	if( GWK[PLY_WORK + ccond] & F_LIVE ):
		if( GWK[PLY_WORK + ccond] & F_HIT ):

			#キノコ以外の敵を初期化
			other_enemy_clear()

			GWK[game_adv] = G_GAMEOVER
			GWK[game_subadv] = GS_INIT
			GWK[wait_counter] = 30

		else:
			#ショットON
			if( getInputA() ):
				if( ( GWK[PTAMA_WORK + ccond] & F_LIVE ) == 0 ):
					GWK[PTAMA_WORK + ccond] = F_LIVE
					GWK[PTAMA_WORK + cid] = 1
					GWK[PTAMA_WORK + cxpos] = GWK[PLY_WORK + cxpos] + 4
					GWK[PTAMA_WORK + cypos] = GWK[PLY_WORK + cypos]
					GWK[PTAMA_WORK + cxspd] = 0
					GWK[PTAMA_WORK + cyspd] = 12

#-----------------------------------------------------------------
#プレイヤー弾制御
#-----------------------------------------------------------------
def ptama_control():
	if( GWK[PTAMA_WORK + ccond] & F_LIVE ):

		#１ドット単位でヒットチェックを行う
		for _ptcnt in range( GWK[PTAMA_WORK + cyspd] ):
			GWK[PTAMA_WORK + cypos] = GWK[PTAMA_WORK + cypos] - 1
			#上限チェック
			if( GWK[PTAMA_WORK + cypos] < CSIZE ):
				GWK[PTAMA_WORK + ccond] = 0
				return

			#プレイヤーの弾の先端部分でヒットチェック実施
			_xp = GWK[PTAMA_WORK + cxpos]
			_yp = GWK[PTAMA_WORK + cypos]

			#プレイヤーの弾とのヒットチェック
			#プレイヤーの弾とノミ
			for _cnt in range( NOMI_MAX ):
				_wk = NOMI_WORK + ( _cnt * CWORK_SIZE )
				if( GWK[_wk + ccond] & F_LIVE ):
					if( ( GWK[_wk + cxpos] <= _xp < ( GWK[_wk + cxpos]+10 ) ) and 
						( GWK[_wk + cypos] <= _yp < ( GWK[_wk + cypos]+8  ) ) ):
							#HIT!
							GWK[_wk + ccond] = 0
							GWK[PTAMA_WORK + ccond] = 0
							#ノミヒットスコアセット
							add_score(100)
							return
			
			#プレイヤーの弾とサソリ
			for _cnt in range( SASORI_MAX ):
				_wk = SASORI_WORK + ( _cnt * CWORK_SIZE )
				if( GWK[_wk + ccond] & F_LIVE ):
					if( ( GWK[_wk + cxpos] <= _xp < ( GWK[_wk + cxpos]+0x10 ) ) and 
						( GWK[_wk + cypos] <= _yp < ( GWK[_wk + cypos]+0x10 ) ) ):
							#HIT!
							GWK[_wk + ccond] = 0
							GWK[PTAMA_WORK + ccond] = 0
							#サソリヒットスコアセット
							add_score(100)
							return

			#プレイヤーの弾とムカデ
			for _cnt in range( MUKADE_MAX ):
				_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
				if( GWK[_wk + ccond] & F_LIVE ):
					if( ( GWK[_wk + cxpos] <= _xp < ( GWK[_wk + cxpos]+8 ) ) and 
						( GWK[_wk + cypos] <= _yp < ( GWK[_wk + cypos]+8 ) ) ):
							#HIT!
							GWK[_wk + ccond] |= F_HIT		#ムカデヒット後の処理はムカデ側で実施
							GWK[PTAMA_WORK + ccond] = 0
							#ムカデヒットスコアセット
							add_score(100)
							return

			#プレイヤーの弾とキノコ
			for _ycnt in range( YSIZE ):
				for _xcnt in range( XSIZE ):
					_swk = SCREEN_WORK + ( _ycnt * XSIZE ) + _xcnt
					if( GWK[_swk] != 0 ):
						if( ( ( _xcnt * CSIZE ) <= _xp < ( _xcnt * CSIZE + 8 ) ) and 
							( ( _ycnt * CSIZE ) <= _yp < ( _ycnt * CSIZE + 8 ) ) ):
							
							if( ( GWK[_swk] == 0x0e ) or ( GWK[_swk] == 0x12 ) ):
								GWK[_swk] = 0		#消滅
							else:
								GWK[_swk] += 1
							
							GWK[PTAMA_WORK + ccond] = 0
							#キノコヒットスコアセット
							add_score(10)
							return

#-----------------------------------------------------------------
#タイトルセット
#-----------------------------------------------------------------
def title_set():
	GWK[game_adv] = G_TITLE
	GWK[game_subadv] = GS_INIT
	GWK[wait_counter] = 100		#タイトル用ムカデ登場待ち時間
	
#-----------------------------------------------------------------
#再スタート
#	ミス後のステージ開始時にはキノコ再作成しない
#-----------------------------------------------------------------
def restart_set():
	GWK[game_adv] = G_GAME
	GWK[game_subadv] = GS_RESTART
	GWK[wait_counter] = 30		#ムカデ登場待ち時間

	#サソリ出現タイマーセット
	sasori_timer_set()
	#ノミ初期設定
	nomi_stage_max_set()


#-----------------------------------------------------------------
#更新
#-----------------------------------------------------------------
def update():
	if( getInputB() ):
		if( ( ( pyxel.frame_count >> 2 ) & 0x01 ) == 0 ):
			return

	#タイトル
	if( GWK[game_adv] == G_TITLE ):
		if( GWK[game_subadv] == GS_INIT ):
			#ムカデ登場初期化
			mukade_init()
			GWK[game_subadv] = GS_WAIT
		
		elif( GWK[game_subadv] == GS_WAIT ):
			#登場待ち
			GWK[wait_counter] -= 1
			if( GWK[wait_counter] < 0 ):

				for _cnt in range( MUKADE_MAX ):
					_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
					GWK[_wk + ccond] |= F_LIVE
				GWK[game_subadv] = GS_MAIN

		elif( GWK[game_subadv] == GS_MAIN ):
			mukade_control()

			_work = 0
			for _cnt in range( MUKADE_MAX ):
				_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
				if( GWK[_wk + cypos] == SCREEN_HEIGHT ):
					_work += 1

			if( _work == MUKADE_MAX ):
				mukade_init()
				GWK[wait_counter] = 100
				GWK[game_subadv] = GS_WAIT
		else:
			pass


		#スタートチェック
		if( getInputA() ):
			start_init()
			GWK[game_adv] = G_GAME
			GWK[game_subadv] = GS_INIT
			GWK[wait_counter] = 30		#ムカデ登場待ち時間

			#サソリ出現タイマーセット
			sasori_timer_set()
			#ノミ初期設定
			nomi_stage_max_set()

			#プレイヤー初期化
			player_init()

	elif( GWK[game_adv] == G_GAME ):
		if( GWK[game_subadv] == GS_INIT ):
			kinoko_init()
			mukade_init()
			kumo_init()
			GWK[game_subadv] = GS_WAIT

		elif( GWK[game_subadv] == GS_WAIT ):
			#登場待ち
			GWK[wait_counter] -= 1
			if( GWK[wait_counter] < 0 ):

				for _cnt in range( MUKADE_MAX ):
					_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
					GWK[_wk + ccond] |= F_LIVE

				GWK[game_subadv] = GS_MAIN

		elif( GWK[game_subadv] == GS_MAIN ):
			kumo_control()
			nomi_control()
			sasori_control()
			mukade_control()
			player_control()
			ptama_control()
		elif( GWK[game_subadv] == GS_RESTART ):
			mukade_init()
			kumo_init()
			GWK[game_subadv] = GS_WAIT
		else:
			pass
			
	elif( GWK[game_adv] == G_GAMEOVER ):
		if( GWK[game_subadv] == GS_INIT ):
			#次作業までのウエイト
			GWK[wait_counter] -= 1
			if( GWK[wait_counter] < 0 ):

				#キノコ復活、復活終了したら次へ
				_res = kinoko_revival()
				if( _res != 0 ):

					GWK[rest_number] -= 1
					if( GWK[rest_number] < 0 ):
						GWK[game_subadv] = GS_MAIN
						GWK[wait_counter] = 200
					else:
						restart_set()
						#プレイヤー初期化
						player_init()

		elif( GWK[game_subadv] == GS_MAIN ):
			GWK[wait_counter] -= 1
			if( GWK[wait_counter] < 0 ):
				#ワークを初期化
				work_init()
				#タイトルに戻る
				title_set()

		elif( GWK[game_subadv] == GS_WAIT ):
			#キノコ復活、復活終了したら再スタート
			_res = kinoko_revival()
			if( _res != 0 ):
				restart_set()
				#プレイヤー初期化
				player_init()
		else:
			pass

	elif( GWK[game_adv] == G_CLEAR ):
		if( GWK[game_subadv] == GS_INIT ):
			#次作業までのウエイト
			GWK[wait_counter] -= 1
			if( GWK[wait_counter] < 0 ):
				GWK[wait_counter] = 5
				GWK[game_subadv] = GS_WAIT

		elif( GWK[game_subadv] == GS_MAIN ):
			GWK[wait_counter] -= 1
			if( GWK[wait_counter] < 0 ):
				#ワークを初期化
				work_init()
				#タイトルに戻る
				title_set()

		elif( GWK[game_subadv] == GS_WAIT ):
			#キノコ復活、復活終了したら再スタート
			_res = kinoko_revival()
			if( _res != 0 ):
				GWK[stage_number] += 1
				restart_set()
				#プレイヤーはそのまま継続
		else:
			pass

	else:
		pass

#-----------------------------------------------------------------
#描画
#-----------------------------------------------------------------
def draw():
	#画面クリア
	pyxel.cls(0)

	if( GWK[game_adv] == G_TITLE ):
		#タイトル下
		cput( TITLE_X, TITLE_Y, 0x1f )

		#この間をムカデが歩き回る
		#ムカデ
		for _cnt in range( MUKADE_MAX ):
			_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
			if( GWK[_wk + ccond] & F_LIVE ):
				anim_control( _wk, 0 )
				_id = atbl[GWK[_wk+canum]][GWK[_wk+cacnt]+ACNT_OFFSET]
				_h = 0
				_v = 0
				if( atbl[GWK[_wk+canum]][ACNT_HV] & 0x01 ):
					_h = 1
				if( atbl[GWK[_wk+canum]][ACNT_HV] & 0x02 ):
					_v = 1
				cput( GWK[_wk + cxpos], GWK[_wk + cypos], _id, _h, _v )

		#タイトル上
		cput( TITLE_X, TITLE_Y, 0x20 )
		#ムカデ出口のマスク
		pyxel.blt( TITLE_X + TITLE_XSIZE - 8, TITLE_Y + (CSIZE * 4), 0, 0, 0, 8, 8 )

		#ATARIロゴ
		cput( SCREEN_WIDTH//2 - 0x30, TITLE_Y + 0x21, 0x21 )
		pyxel.text( SCREEN_WIDTH//2 - (4*16//2) , TITLE_Y + 0x30, '= PYXEL  CLONE =', 7 )
		
		pyxel.text( SCREEN_WIDTH//2 - (4*28//2) , TITLE_Y + 0x60, 'Z-KEY OR A-BUTTON PUSH START', 7 )

		score_draw()

	elif( GWK[game_adv] == G_GAME ):
		#枠線
		pyxel.line( CSIZE, CSIZE-1, SCREEN_WIDTH - CSIZE, CSIZE-1, 7 )
		pyxel.line( CSIZE-1, CSIZE-1, CSIZE-1, SCREEN_HEIGHT, 7 )
		pyxel.line( SCREEN_WIDTH - CSIZE, CSIZE-1, SCREEN_WIDTH - CSIZE, SCREEN_HEIGHT, 7 )

		#プレイヤー
		if( GWK[PLY_WORK + ccond] & F_LIVE ):
			cput( GWK[PLY_WORK + cxpos], GWK[PLY_WORK + cypos], GWK[PLY_WORK + cid] )

		#プレイヤーの弾
		if( GWK[PTAMA_WORK + ccond] & F_LIVE ):
			cput( GWK[PTAMA_WORK + cxpos], GWK[PTAMA_WORK + cypos], GWK[PTAMA_WORK + cid] )

		#キノコ
		for _yp in range(1, YSIZE):
			for _xp in range(1, XSIZE-1):
				_id = GWK[SCREEN_WORK + (_yp * XSIZE + _xp)]
				if( _id != 0 ):
					cput( _xp * CSIZE, _yp * CSIZE, _id )

		#ムカデ
		for _cnt in range( MUKADE_MAX ):
			_wk = MUKADE_WORK + ( _cnt * CWORK_SIZE )
			if( GWK[_wk + ccond] & F_LIVE ):
				anim_control( _wk, 0 )
				_id = atbl[GWK[_wk+canum]][GWK[_wk+cacnt]+ACNT_OFFSET]
				_h = 0
				_v = 0
				if( atbl[GWK[_wk+canum]][ACNT_HV] & 0x01 ):
					_h = 1
				if( atbl[GWK[_wk+canum]][ACNT_HV] & 0x02 ):
					_v = 1
				cput( GWK[_wk + cxpos], GWK[_wk + cypos], _id, _h, _v )

		#ノミ
		for _cnt in range( GWK[nomi_stage_max] ):
			_wk = NOMI_WORK + ( _cnt * CWORK_SIZE )
			if( GWK[_wk + ccond] & F_LIVE ):
				anim_control( _wk, 0 )
				_id = atbl[GWK[_wk+canum]][GWK[_wk+cacnt]+ACNT_OFFSET]
				cput( GWK[_wk + cxpos], GWK[_wk + cypos], _id )

		#クモ
		for _cnt in range( KUMO_MAX ):
			_wk = KUMO_WORK + ( _cnt * CWORK_SIZE )
			if( GWK[_wk + ccond] & F_LIVE ):
				anim_control( _wk, 0 )
				_id = atbl[GWK[_wk+canum]][GWK[_wk+cacnt]+ACNT_OFFSET]
				cput( GWK[_wk + cxpos], GWK[_wk + cypos], _id )

		#サソリ
		_wk = SASORI_WORK
		if( GWK[_wk + ccond] & F_LIVE ):
			anim_control( _wk, 0 )
			_id = atbl[GWK[_wk+canum]][GWK[_wk+cacnt]+ACNT_OFFSET]
			_h = 0
			if( atbl[GWK[_wk+canum]][ACNT_HV] & 0x01 ):
				_h = 1
			cput( GWK[_wk + cxpos], GWK[_wk + cypos], _id, _h )

		score_draw()

	elif( GWK[game_adv] == G_GAMEOVER ):
		#枠線
		pyxel.line( CSIZE, CSIZE-1, SCREEN_WIDTH - CSIZE, CSIZE-1, 7 )
		pyxel.line( CSIZE-1, CSIZE-1, CSIZE-1, SCREEN_HEIGHT, 7 )
		pyxel.line( SCREEN_WIDTH - CSIZE, CSIZE-1, SCREEN_WIDTH - CSIZE, SCREEN_HEIGHT, 7 )


		#キノコ
		for _yp in range(1, YSIZE):
			for _xp in range(1, XSIZE-1):
				_id = GWK[SCREEN_WORK + (_yp * XSIZE + _xp)]
				if( _id != 0 ):
					cput( _xp * CSIZE, _yp * CSIZE, _id )
		
		score_draw()

		#ゲームオーバー表示
		if( GWK[game_subadv] == GS_MAIN ):
			pyxel.text( SCREEN_WIDTH//2 - (4*10//2), SCREEN_HEIGHT//2, 'GAME  OVER', 7)

	elif( GWK[game_adv] == G_CLEAR ):
		#枠線
		pyxel.line( CSIZE, CSIZE-1, SCREEN_WIDTH - CSIZE, CSIZE-1, 7 )
		pyxel.line( CSIZE-1, CSIZE-1, CSIZE-1, SCREEN_HEIGHT, 7 )
		pyxel.line( SCREEN_WIDTH - CSIZE, CSIZE-1, SCREEN_WIDTH - CSIZE, SCREEN_HEIGHT, 7 )

		#キノコ
		for _yp in range(1, YSIZE):
			for _xp in range(1, XSIZE-1):
				_id = GWK[SCREEN_WORK + (_yp * XSIZE + _xp)]
				if( _id != 0 ):
					cput( _xp * CSIZE, _yp * CSIZE, _id )
		
		score_draw()

		pyxel.text( SCREEN_WIDTH//2 - (4*12//2), SCREEN_HEIGHT//2, 'STAGE  CLEAR', 7)

#-----------------------------------------------------------------
#work clear
#-----------------------------------------------------------------
def work_clear():
	for _cnt in range( WORK_TOP, WORK_END ):
		GWK[_cnt] = 0

#-----------------------------------------------------------------
#ゲーム開始時のワークの初期値セット
#-----------------------------------------------------------------
def start_init():
	GWK[rest_number] = 2			#残機
	GWK[stage_number] = 0			#0～
	GWK[score] = 0					#スコア（最大６桁）

	#プレイヤー初期化
	player_init()

#-----------------------------------------------------------------
#ワークの初期化
#-----------------------------------------------------------------
def work_init():
	for _cnt in range( WORK_TOP+0x20, WORK_END ):
		GWK[_cnt] = 0

#-----------------------------------------------------------------
#プレイヤーの初期値セット
#-----------------------------------------------------------------
def player_init():
	GWK[PLY_WORK + ccond] = F_LIVE
	GWK[PLY_WORK + cid] = 0
	GWK[PLY_WORK + cxpos] = SCREEN_WIDTH//2
	GWK[PLY_WORK + cypos] = SCREEN_HEIGHT - CSIZE
	GWK[PLY_WORK + cxspd] = 3
	GWK[PLY_WORK + cyspd] = 2
	
	GWK[PTAMA_WORK + ccond] = 0
	GWK[PTAMA_WORK + cid] = 0
	GWK[PTAMA_WORK + cxpos] = 0
	GWK[PTAMA_WORK + cypos] = 0
	GWK[PTAMA_WORK + cxspd] = 0
	GWK[PTAMA_WORK + cyspd] = 0

#-----------------------------------------------------------------
#入力（キーボード＆ジョイパッド）
#-----------------------------------------------------------------
#上
def getInputUP():
	if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
		return 1
	else:
		return 0
#下
def getInputDOWN():
	if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
		return 1
	else:
		return 0
#左
def getInputLEFT():
	if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
		return 1
	else:
		return 0
#右
def getInputRIGHT():
	if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
		return 1
	else:
		return 0
#button-A（決定）
def getInputA():
	if pyxel.btnp(pyxel.KEY_Z, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A, hold=10, repeat=10):
		return 1
	else:
		return 0
#button-B（キャンセル）
def getInputB():
	#if pyxel.btnp(pyxel.KEY_X, hold=30, repeat=30) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B, hold=30, repeat=30):
	if pyxel.btn(pyxel.KEY_X) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_B):
		return 1
	else:
		return 0
#button-X
def getInputX():
	if pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X):
		return 1
	else:
		return 0
#button-Y
def getInputY():
	if pyxel.btnp(pyxel.KEY_Y, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_Y):
		return 1
	else:
		return 0

#上
def getTriggerUP():
	if pyxel.btnp(pyxel.KEY_UP, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP, hold=10, repeat=10):
		return 1
	else:
		return 0
#下
def getTriggerDOWN():
	if pyxel.btnp(pyxel.KEY_DOWN, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN, hold=10, repeat=10):
		return 1
	else:
		return 0
#左
def getTriggerLEFT():
	if pyxel.btnp(pyxel.KEY_LEFT, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, hold=10, repeat=10):
		return 1
	else:
		return 0
#右
def getTriggerRIGHT():
	if pyxel.btnp(pyxel.KEY_RIGHT, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, hold=10, repeat=10):
		return 1
	else:
		return 0

#===============================================================================
#INIT&RUN
#===============================================================================
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
#[use Web]ESCキーを無効化
#pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, quit_key=pyxel.KEY_NONE, title='centipede')

#リソース読み込み
pyxel.load("my_resource.pyxres")
#ワーククリア
work_clear()
#Goto タイトル
title_set()

#実行
pyxel.run(update, draw)
