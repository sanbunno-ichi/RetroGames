#------------------------------------------
# title: Gemx
# author: sanbunnoichi
# desc: Amiga's Puzzle Gem'X clone
# site: https://github.com/sanbunno-ichi/retrogame/gemx
# license: MIT
# version: 1.0
#
#更新履歴
#2024.11.29 作成開始
#------------------------------------------
#ソースは非公開を予定
#------------------------------------------
#非公開更新履歴

#arcade game	通常ゲーム
#training		練習：mine選択して全ステージプレイ


#2024.12.11 ゲーム一連の流れ完了
#2024.12.11 3mine map組み込み
#2024.12.11 mine map作成
#2024.12.11 タイトル作成
#2024.12.11 バグ修正
#(済)UNDOできない（UNDOワーク保存は選択後ではなく選択時変更前を保存に修正）
#(済)SKIPSTAGE動かない（処理が入っていない）
#(済)SKIPSTAGEにカーソル合わせてもフォントの色が変わらない（GWK[cursol_y]がGWK[cursol_x]になってた）
#(済)Y=0のGEMが変更できない（getFieldPos()の戻り値が0になることがあるので枠外の時は-1を返すよう修正）
#2024.12.10 ゲーム内処理組み込み
#2024.12.09 ゲーム基本部分の描画セット
#2024.12.08 ゲームやネットからステージ情報取得
#2024.11.29 作成開始
#------------------------------------------
#解き方ガイド：https://gamefaqs.gamespot.com/amiga/656104-gemx/faqs
#------------------------------------------
import pyxel
import mine
import time	


#-----------------------------------------------------------------
SCREEN_WIDTH		=	320		#ゲーム画面横サイズ
SCREEN_HEIGHT		=	240		#ゲーム画面縦サイズ

#-----------------------------------------------------------------
#[workass]変数
WORK_TOP			=	0
WORK_END			=	0x800
_ass = WORK_TOP
GWK = [WORK_TOP for _ass in range(WORK_END)]	#変数管理(RAM領域)

game_adv			=	WORK_TOP+0x00		#game_control number

G_TITLE				=	0
G_DEMOPLAY			=	1
G_GAME				=	2
G_MAP				=	3
G_SETTING			=	4
G_EDITOR			=	5
G_END				=	6

game_subadv			=	WORK_TOP+0x01		#game_control sub-number

GS_INIT				=	0
GS_MAIN				=	1
GS_BREAK			=	2
GS_FALL				=	3
GS_CLEAR			=	4
GS_SKIP				=	5
GS_NEXT				=	6
GS_OVER				=	7

mine_number			=	WORK_TOP+0x02		#A～Z
stage_number		=	WORK_TOP+0x03		#0,1～16
move_number			=	WORK_TOP+0x04
skip_number			=	WORK_TOP+0x05
next_number			=	WORK_TOP+0x06
rest_time			=	WORK_TOP+0x07

cursol_x			=	WORK_TOP+0x08
cursol_y			=	WORK_TOP+0x09
field_x				=	WORK_TOP+0x0a
field_y				=	WORK_TOP+0x0b
score				=	WORK_TOP+0x0c		#スコア（最大６桁）
highscore			=	WORK_TOP+0x0d
multi_color_switch	=	WORK_TOP+0x0e		#0/1 : マルチカラースイッチ
move_counter		=	WORK_TOP+0x0f

yelanim_count		=	WORK_TOP+0x10		#黄こわれアニメ用カウンタ
heartanim_count		=	WORK_TOP+0x11		#スコアハートアニメカウンタ
fall_counter		=	WORK_TOP+0x12		#GEM落下アニメで使用
fall_number			=	WORK_TOP+0x13		#GEM落下アニメで使用
wait_counter		=	WORK_TOP+0x14		#汎用カウンタ
start_time			=	WORK_TOP+0x15		#開始時間
past_time			=	WORK_TOP+0x16		#経過時間
skip_btn_sw			=	WORK_TOP+0x17
undo_number			=	WORK_TOP+0x18
remaining_time		=	WORK_TOP+0x19
select_mine1		=	WORK_TOP+0x1a
select_mine2		=	WORK_TOP+0x1b

SCORE_MAX			=	999999
SCORE_KETA			=	6

GEM_SIZE			=	0x10

FIELD_X_MAX			=	8
FIELD_Y_MAX			=	10

FIELD_LEFT_BASEX	=	0x10
FIELD_LEFT_BASEY	=	0x50

FIELD_RIGHT_BASEX	=	0xB0
FIELD_RIGHT_BASEY	=	FIELD_LEFT_BASEY

SKIP_BTN_BASEX		=	0xC0
SKIP_BTN_BASEY		=	0x18
SKIP_BTN_WIDTH		=	0x28
SKIP_BTN_HEIGHT		=	0x10

STAGE_WORK			=	WORK_TOP+0x20	#0x10
STAGE_MIN			=	1
STAGE_MAX			=	16

FIELD_LEFT_WORK		=	WORK_TOP+0x30	#+0x50(FIELD_X_MAX * FIELD_Y_MAX)
FIELD_RIGHT_WORK	=	WORK_TOP+0x80	#+0x50(FIELD_X_MAX * FIELD_Y_MAX)

SAVE_WORK			=	WORK_TOP+0xd0	#+0x50(FIELD_X_MAX * FIELD_Y_MAX)
FALL_WORK			=	WORK_TOP+0x120	#+0x50*5	FALL MOVE後のFIELD_WORK保存用

cid					=	0
cnum				=	1
mcnt				=	2
xpos				=	3
ypos				=	4
CWORK_SIZE			=	5


SCORE_BASEX			=	0x20
SCORE_BASEY			=	0x21
STAGE_BASEX			=	0x20
STAGE_BASEY			=	0x30

MOVE_REMAIN_BASEX	=	0x80
MOVE_REMAIN_BASEY	=	0x08+1
SKIP_REMAIN_BASEX	=	0x80
SKIP_REMAIN_BASEY	=	0x18+1
NEXT_REMAIN_BASEX	=	0x80
NEXT_REMAIN_BASEY	=	0x28+1
TIME_BASEX			=	0x80
TIME_BASEY			=	0x38+1

SAMPLE_GEMX			=	0x98
SAMPLE_GEMY			=	0x60-2

GEM_NOT				=	0
GEM_MIN				=	1
GEM_MAX				=	5
GEM_ERASE			=	6		#消えアニメ用

FIELD_UNDO_MAX		=	16
FIELD_UNDO_WORK		=	WORK_TOP+0x300			#UNDO用：FIELD_X_MAX * FIELD_Y_MAX * 最大保管数


#-----------------------------------------------------------------
#ワーク初期化
#-----------------------------------------------------------------
def work_clear():
	for _cnt in range(WORK_TOP,WORK_END):
		GWK[_cnt] = 0


#-----------------------------------------------------------------
#MINE MAPテーブル
#-----------------------------------------------------------------
#	1	2	3	4	5	6	7
#						P		1
#					K		V	2
#				G		Q		3
#			D		L		W	4
#		B		H		R		5
#	A		E		M		X	6
#		C		I		S		7
#			F		N		Y	8
#				J		T		10
#					O		Z	11
#						U		12

map_mine_table = [
	SCREEN_WIDTH * 1//8,	SCREEN_HEIGHT * (12+6)//28,		0x41,	0,	#A

	SCREEN_WIDTH * 2//8,	SCREEN_HEIGHT * (12+5)//28,		0x42,	0,	#B
	SCREEN_WIDTH * 2//8,	SCREEN_HEIGHT * (12+7)//28,		0x43,	0,	#C

	SCREEN_WIDTH * 3//8,	SCREEN_HEIGHT * (12+4)//28,		0x44,	0,	#D
	SCREEN_WIDTH * 3//8,	SCREEN_HEIGHT * (12+6)//28,		0x45,	0,	#E
	SCREEN_WIDTH * 3//8,	SCREEN_HEIGHT * (12+8)//28,		0x46,	0,	#F

	SCREEN_WIDTH * 4//8,	SCREEN_HEIGHT * (12+3)//28,		0x47,	0,	#G
	SCREEN_WIDTH * 4//8,	SCREEN_HEIGHT * (12+5)//28,		0x48,	0,	#H
	SCREEN_WIDTH * 4//8,	SCREEN_HEIGHT * (12+7)//28,		0x49,	0,	#I
	SCREEN_WIDTH * 4//8,	SCREEN_HEIGHT * (12+9)//28,		0x4a,	0,	#J

	SCREEN_WIDTH * 5//8,	SCREEN_HEIGHT * (12+2)//28,		0x4b,	0,	#K
	SCREEN_WIDTH * 5//8,	SCREEN_HEIGHT * (12+4)//28,		0x4c,	0,	#L
	SCREEN_WIDTH * 5//8,	SCREEN_HEIGHT * (12+6)//28,		0x4d,	0,	#M
	SCREEN_WIDTH * 5//8,	SCREEN_HEIGHT * (12+8)//28,		0x4e,	0,	#N
	SCREEN_WIDTH * 5//8,	SCREEN_HEIGHT * (12+10)//28,	0x4f,	0,	#O

	SCREEN_WIDTH * 6//8,	SCREEN_HEIGHT * (12+1)//28,		0x50,	0,	#P
	SCREEN_WIDTH * 6//8,	SCREEN_HEIGHT * (12+3)//28,		0x51,	0,	#Q
	SCREEN_WIDTH * 6//8,	SCREEN_HEIGHT * (12+5)//28,		0x52,	0,	#R
	SCREEN_WIDTH * 6//8,	SCREEN_HEIGHT * (12+7)//28,		0x53,	0,	#S
	SCREEN_WIDTH * 6//8,	SCREEN_HEIGHT * (12+9)//28,		0x54,	0,	#T
	SCREEN_WIDTH * 6//8,	SCREEN_HEIGHT * (12+11)//28,	0x55,	0,	#U

	SCREEN_WIDTH * 7//8,	SCREEN_HEIGHT * (12+2)//28,		0x56,	0,	#V
	SCREEN_WIDTH * 7//8,	SCREEN_HEIGHT * (12+4)//28,		0x57,	0,	#W
	SCREEN_WIDTH * 7//8,	SCREEN_HEIGHT * (12+6)//28,		0x58,	0,	#X
	SCREEN_WIDTH * 7//8,	SCREEN_HEIGHT * (12+8)//28,		0x59,	0,	#Y
	SCREEN_WIDTH * 7//8,	SCREEN_HEIGHT * (12+10)//28,	0x5a,	0,	#Z
	]


#-----------------------------------------------------------------
#選択可能なmine
#-----------------------------------------------------------------
select_mine_table = [
	1,2,		#A[ 0]→B[1]C[2]
	3,4,		#B[ 1]→D[3]E[4]
	4,5,		#C[ 2]→E[4]F[5]
	6,7,		#D[ 3]→G[6]H[7]
	7,8,		#E[ 4]→H[7]I[8]
	8,9,		#F[ 5]→I[8]J[9]
	10,11,		#G[ 6]→K[10]L[11]
	11,12,		#H[ 7]→L[11]M[12]
	12,13,		#I[ 8]→M[12]N[13]
	13,14,		#J[ 9]→N[13]O[14]
	15,16,		#K[10]→P[15]Q[16]
	16,17,		#L[11]→Q[16]R[17]
	17,18,		#M[12]→R[17]S[18]
	18,19,		#N[13]→S[18]T[19]
	19,20,		#O[14]→T[19]U[20]
	21,-1,		#P[15]→V[21]
	21,22,		#Q[16]→V[21]W[22]
	22,23,		#R[17]→W[22]X[23]
	23,24,		#S[18]→X[23]Y[24]
	24,25,		#T[19]→Y[24]Z[25]
	25,-1,		#U[20]→Z[25]
	]

#-----------------------------------------------------------------
#キャラクタテーブル
#-----------------------------------------------------------------
SCORE_CID = 0x0c
DEF_BASE = 0x00
MULTI_BASE = 0x05
FONT_START = 0x20

IDMAX = 0x120
ctbl = [
	# u,    v,    us,   vs
	[ 0x40, 0x00, 0x10, 0x10 ],		#0x00 DEF gem1(赤)
	[ 0x40, 0x10, 0x10, 0x10 ],		#0x01 DEF gem2(緑)
	[ 0x40, 0x20, 0x10, 0x10 ],		#0x02 DEF gem3(青)
	[ 0x40, 0x30, 0x10, 0x10 ],		#0x03 DEF gem4(紫)
	[ 0x40, 0x40, 0x10, 0x10 ],		#0x04 DEF gem5(黄)

	[ 0xff, 0xff, 0x10, 0x10 ],		#0x05 MULTI gem1(赤)
	[ 0xff, 0xff, 0x10, 0x10 ],		#0x06 MULTI gem2(緑)
	[ 0xff, 0xff, 0x10, 0x10 ],		#0x07 MULTI gem3(青)
	[ 0xff, 0xff, 0x10, 0x10 ],		#0x08 MULTI gem4(紫)
	[ 0xff, 0xff, 0x10, 0x10 ],		#0x09 MULTI gem5(黄)

	[ 0xff, 0xff, 0x10, 0x10 ],		#0x0a MULTI 黄GEMこわれダミー
	[ 0xff, 0xff, 0x10, 0x10 ],		#0x0b 

	[ 0x40, 0x80, 0x08, 0x10 ],		#0x0c SCORE_0
	[ 0x48, 0x80, 0x08, 0x10 ],		#0x0d SCORE_1
	[ 0x50, 0x80, 0x08, 0x10 ],		#0x0e SCORE_2
	[ 0x58, 0x80, 0x08, 0x10 ],		#0x0f SCORE_3
	[ 0x60, 0x80, 0x08, 0x10 ],		#0x10 SCORE_4
	[ 0x68, 0x80, 0x08, 0x10 ],		#0x11 SCORE_5
	[ 0x70, 0x80, 0x08, 0x10 ],		#0x12 SCORE_6
	[ 0x78, 0x80, 0x08, 0x10 ],		#0x13 SCORE_7
	[ 0x80, 0x80, 0x08, 0x10 ],		#0x14 SCORE_8
	[ 0x88, 0x80, 0x08, 0x10 ],		#0x15 SCORE_9
	[ 0x90, 0x80, 0x08, 0x10 ],		#0x16 SCORE_KORON

	[ 0x10, 0x00, 0x08, 0x08 ],		#0x17 カーソル
	[ 0x40, 0x70, 0x10, 0x10 ],		#0x18 paramアイコン１
	[ 0x50, 0x70, 0x10, 0x10 ],		#0x19 paramアイコン２
	[ 0x60, 0x70, 0x10, 0x10 ],		#0x1a paramアイコン３
	[ 0x70, 0x70, 0x10, 0x10 ],		#0x1b paramアイコン４
	[ 0x60, 0x60, 0x10, 0x10 ],		#0x1c stageアイコン
	[ 0x50, 0x60, 0x08, 0x10 ],		#0x1d 1P
	[ 0x70, 0x50, 0x10, 0x10 ],		#0x1e SCOREハート2(small
	[ 0x60, 0x50, 0x10, 0x10 ],		#0x1f SCOREハート1

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x20 フォント用予約
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x21 フォント用予約
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x22 フォント用予約
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x23 フォント用予約
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x24 フォント用予約
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x25 フォント用予約
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x26 フォント用予約

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x27 （空き）
	[ 0x30, 0x40, 0x08, 0x08 ],		#0x28 '('
	[ 0x38, 0x40, 0x08, 0x08 ],		#0x29 ')'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x2a （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x2b （空き）
	[ 0x10, 0x40, 0x08, 0x08 ],		#0x2c ','（カンマ）
	[ 0x20, 0x40, 0x08, 0x08 ],		#0x2d '-'（ハイフン）
	[ 0x18, 0x40, 0x08, 0x08 ],		#0x2e '.'（ピリオド）
	[ 0x28, 0x40, 0x08, 0x08 ],		#0x2f '/'（スラッシュ）

	[ 0x00, 0x38, 0x08, 0x08 ],		#0x30 '0'
	[ 0x08, 0x38, 0x08, 0x08 ],		#0x31 '1'
	[ 0x10, 0x38, 0x08, 0x08 ],		#0x32 '2'
	[ 0x18, 0x38, 0x08, 0x08 ],		#0x33 '3'
	[ 0x20, 0x38, 0x08, 0x08 ],		#0x34 '4'
	[ 0x28, 0x38, 0x08, 0x08 ],		#0x35 '5'
	[ 0x30, 0x38, 0x08, 0x08 ],		#0x36 '6'
	[ 0x38, 0x38, 0x08, 0x08 ],		#0x37 '7'
	[ 0x00, 0x40, 0x08, 0x08 ],		#0x38 '8'
	[ 0x08, 0x40, 0x08, 0x08 ],		#0x39 '9'

	[ 0x20, 0x60, 0x08, 0x08 ],		#0x3a ':'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x3b （空き）
	[ 0x10, 0x60, 0x08, 0x08 ],		#0x3c '<'→'RD'	
	[ 0x18, 0x60, 0x08, 0x08 ],		#0x3d '>'→'ED'	
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x3e （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x3f （空き）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x40 （空き）
	[ 0x00, 0x48, 0x08, 0x08 ],		#0x41 'A'
	[ 0x08, 0x48, 0x08, 0x08 ],		#0x42 'B'
	[ 0x10, 0x48, 0x08, 0x08 ],		#0x43 'C'
	[ 0x18, 0x48, 0x08, 0x08 ],		#0x44 'D'
	[ 0x20, 0x48, 0x08, 0x08 ],		#0x45 'E'
	[ 0x28, 0x48, 0x08, 0x08 ],		#0x46 'G'
	[ 0x30, 0x48, 0x08, 0x08 ],		#0x47 'G'
	[ 0x38, 0x48, 0x08, 0x08 ],		#0x48 'H'
	[ 0x00, 0x50, 0x08, 0x08 ],		#0x49 'I'
	[ 0x08, 0x50, 0x08, 0x08 ],		#0x4a 'J'
	[ 0x10, 0x50, 0x08, 0x08 ],		#0x4b 'K'
	[ 0x18, 0x50, 0x08, 0x08 ],		#0x4c 'L'
	[ 0x20, 0x50, 0x08, 0x08 ],		#0x4d 'M'
	[ 0x28, 0x50, 0x08, 0x08 ],		#0x4e 'N'
	[ 0x30, 0x50, 0x08, 0x08 ],		#0x4f 'O'

	[ 0x38, 0x50, 0x08, 0x08 ],		#0x50 'P'
	[ 0x00, 0x58, 0x08, 0x08 ],		#0x51 'Q'
	[ 0x08, 0x58, 0x08, 0x08 ],		#0x52 'R'
	[ 0x10, 0x58, 0x08, 0x08 ],		#0x53 'S'
	[ 0x18, 0x58, 0x08, 0x08 ],		#0x54 'T'
	[ 0x20, 0x58, 0x08, 0x08 ],		#0x55 'U'
	[ 0x28, 0x58, 0x08, 0x08 ],		#0x56 'V'
	[ 0x30, 0x58, 0x08, 0x08 ],		#0x57 'W'
	[ 0x38, 0x58, 0x08, 0x08 ],		#0x58 'X'
	[ 0x00, 0x60, 0x08, 0x08 ],		#0x59 'Y'
	[ 0x08, 0x60, 0x08, 0x08 ],		#0x5a 'Z'

	[ 0x70, 0x00, 0x10, 0x10 ],		#0x5b 黄壊れアニメ１
	[ 0x70, 0x10, 0x10, 0x10 ],		#0x5c 黄壊れアニメ２
	[ 0x70, 0x20, 0x10, 0x10 ],		#0x5d 黄壊れアニメ３
	[ 0x70, 0x30, 0x10, 0x10 ],		#0x5e 黄壊れアニメ４
	[ 0x70, 0x40, 0x10, 0x10 ],		#0x5f 黄壊れアニメ５

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x60 ' '（スペース）	黄文字
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x61 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x62 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x63 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x64 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x65 （黄文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x66 （黄文字予約）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x67 （空き）
	[ 0x30, 0x70, 0x08, 0x08 ],		#0x68 '('
	[ 0x38, 0x70, 0x08, 0x08 ],		#0x69 ')'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x6a （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x6b （空き）
	[ 0x10, 0x70, 0x08, 0x08 ],		#0x6c ','（カンマ）
	[ 0x20, 0x70, 0x08, 0x08 ],		#0x6d '-'（ハイフン）
	[ 0x18, 0x70, 0x08, 0x08 ],		#0x6e '.'（ピリオド）
	[ 0x28, 0x70, 0x08, 0x08 ],		#0x6f '/'（スラッシュ）

	[ 0x00, 0x68, 0x08, 0x08 ],		#0x70 '0'
	[ 0x08, 0x68, 0x08, 0x08 ],		#0x71 '1'
	[ 0x10, 0x68, 0x08, 0x08 ],		#0x72 '2'
	[ 0x18, 0x68, 0x08, 0x08 ],		#0x73 '3'
	[ 0x20, 0x68, 0x08, 0x08 ],		#0x74 '4'
	[ 0x28, 0x68, 0x08, 0x08 ],		#0x75 '5'
	[ 0x30, 0x68, 0x08, 0x08 ],		#0x76 '6'
	[ 0x38, 0x68, 0x08, 0x08 ],		#0x77 '7'
	[ 0x00, 0x70, 0x08, 0x08 ],		#0x78 '8'
	[ 0x08, 0x70, 0x08, 0x08 ],		#0x79 '9'

	[ 0x20, 0x90, 0x08, 0x08 ],		#0x7a ':'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x7b （空き）
	[ 0x10, 0x90, 0x08, 0x08 ],		#0x7c '<'→'RD'	
	[ 0x18, 0x90, 0x08, 0x08 ],		#0x7d '>'→'ED'	
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x7e （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x7f （空き）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x80 （空き）
	[ 0x00, 0x78, 0x08, 0x08 ],		#0x81 'A'
	[ 0x08, 0x78, 0x08, 0x08 ],		#0x82 'B'
	[ 0x10, 0x78, 0x08, 0x08 ],		#0x83 'C'
	[ 0x18, 0x78, 0x08, 0x08 ],		#0x84 'D'
	[ 0x20, 0x78, 0x08, 0x08 ],		#0x85 'E'
	[ 0x28, 0x78, 0x08, 0x08 ],		#0x86 'G'
	[ 0x30, 0x78, 0x08, 0x08 ],		#0x87 'G'
	[ 0x38, 0x78, 0x08, 0x08 ],		#0x88 'H'
	[ 0x00, 0x80, 0x08, 0x08 ],		#0x89 'I'
	[ 0x08, 0x80, 0x08, 0x08 ],		#0x8a 'J'
	[ 0x10, 0x80, 0x08, 0x08 ],		#0x8b 'K'
	[ 0x18, 0x80, 0x08, 0x08 ],		#0x8c 'L'
	[ 0x20, 0x80, 0x08, 0x08 ],		#0x8d 'M'
	[ 0x28, 0x80, 0x08, 0x08 ],		#0x8e 'N'
	[ 0x30, 0x80, 0x08, 0x08 ],		#0x8f 'O'

	[ 0x38, 0x80, 0x08, 0x08 ],		#0x90 'P'
	[ 0x00, 0x88, 0x08, 0x08 ],		#0x91 'Q'
	[ 0x08, 0x88, 0x08, 0x08 ],		#0x92 'R'
	[ 0x10, 0x88, 0x08, 0x08 ],		#0x93 'S'
	[ 0x18, 0x88, 0x08, 0x08 ],		#0x94 'T'
	[ 0x20, 0x88, 0x08, 0x08 ],		#0x95 'U'
	[ 0x28, 0x88, 0x08, 0x08 ],		#0x96 'V'
	[ 0x30, 0x88, 0x08, 0x08 ],		#0x97 'W'
	[ 0x38, 0x88, 0x08, 0x08 ],		#0x98 'X'
	[ 0x00, 0x90, 0x08, 0x08 ],		#0x99 'Y'
	[ 0x08, 0x90, 0x08, 0x08 ],		#0x9a 'Z'

	[ 0x00, 0x30, 0x10, 0x08 ],		#0x9b 矢印左白
	[ 0x10, 0x30, 0x10, 0x08 ],		#0x9c 矢印右白
	[ 0x20, 0x30, 0x10, 0x08 ],		#0x9d 矢印左黄
	[ 0x30, 0x30, 0x10, 0x08 ],		#0x9e 矢印右黄

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x9f (空き)

	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa0 ' '（スペース）	赤文字
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa1 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa2 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa3 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa4 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa5 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa6 （赤文字予約）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0xa7 （空き）
	[ 0x30, 0xa0, 0x08, 0x08 ],		#0xa8 '('
	[ 0x38, 0xa0, 0x08, 0x08 ],		#0xa9 ')'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xaa （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xab （空き）
	[ 0x10, 0xa0, 0x08, 0x08 ],		#0xac ','（カンマ）
	[ 0x20, 0xa0, 0x08, 0x08 ],		#0xad '-'（ハイフン）
	[ 0x18, 0xa0, 0x08, 0x08 ],		#0xae '.'（ピリオド）
	[ 0x28, 0xa0, 0x08, 0x08 ],		#0xaf '/'（スラッシュ）

	[ 0x00, 0x98, 0x08, 0x08 ],		#0xb0 '0'
	[ 0x08, 0x98, 0x08, 0x08 ],		#0xb1 '1'
	[ 0x10, 0x98, 0x08, 0x08 ],		#0xb2 '2'
	[ 0x18, 0x98, 0x08, 0x08 ],		#0xb3 '3'
	[ 0x20, 0x98, 0x08, 0x08 ],		#0xb4 '4'
	[ 0x28, 0x98, 0x08, 0x08 ],		#0xb5 '5'
	[ 0x30, 0x98, 0x08, 0x08 ],		#0xb6 '6'
	[ 0x38, 0x98, 0x08, 0x08 ],		#0xb7 '7'
	[ 0x00, 0xa0, 0x08, 0x08 ],		#0xb8 '8'
	[ 0x08, 0xa0, 0x08, 0x08 ],		#0xb9 '9'

	[ 0x20, 0xc0, 0x08, 0x08 ],		#0xba ':'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xbb （空き）
	[ 0x10, 0xc0, 0x08, 0x08 ],		#0xbc '<'→'RD'	
	[ 0x18, 0xc0, 0x08, 0x08 ],		#0xbd '>'→'ED'	
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xbe （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xbf （空き）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0xc0 （空き）
	[ 0x00, 0xa8, 0x08, 0x08 ],		#0xc1 'A'
	[ 0x08, 0xa8, 0x08, 0x08 ],		#0xc2 'B'
	[ 0x10, 0xa8, 0x08, 0x08 ],		#0xc3 'C'
	[ 0x18, 0xa8, 0x08, 0x08 ],		#0xc4 'D'
	[ 0x20, 0xa8, 0x08, 0x08 ],		#0xc5 'E'
	[ 0x28, 0xa8, 0x08, 0x08 ],		#0xc6 'G'
	[ 0x30, 0xa8, 0x08, 0x08 ],		#0xc7 'G'
	[ 0x38, 0xa8, 0x08, 0x08 ],		#0xc8 'H'
	[ 0x00, 0xb0, 0x08, 0x08 ],		#0xc9 'I'
	[ 0x08, 0xb0, 0x08, 0x08 ],		#0xca 'J'
	[ 0x10, 0xb0, 0x08, 0x08 ],		#0xcb 'K'
	[ 0x18, 0xb0, 0x08, 0x08 ],		#0xcc 'L'
	[ 0x20, 0xb0, 0x08, 0x08 ],		#0xcd 'M'
	[ 0x28, 0xb0, 0x08, 0x08 ],		#0xce 'N'
	[ 0x30, 0xb0, 0x08, 0x08 ],		#0xcf 'O'

	[ 0x38, 0xb0, 0x08, 0x08 ],		#0xd0 'P'
	[ 0x00, 0xb8, 0x08, 0x08 ],		#0xd1 'Q'
	[ 0x08, 0xb8, 0x08, 0x08 ],		#0xd2 'R'
	[ 0x10, 0xb8, 0x08, 0x08 ],		#0xd3 'S'
	[ 0x18, 0xb8, 0x08, 0x08 ],		#0xd4 'T'
	[ 0x20, 0xb8, 0x08, 0x08 ],		#0xd5 'U'
	[ 0x28, 0xb8, 0x08, 0x08 ],		#0xd6 'V'
	[ 0x30, 0xb8, 0x08, 0x08 ],		#0xd7 'W'
	[ 0x38, 0xb8, 0x08, 0x08 ],		#0xd8 'X'
	[ 0x00, 0xc0, 0x08, 0x08 ],		#0xd9 'Y'
	[ 0x08, 0xc0, 0x08, 0x08 ],		#0xda 'Z'

	[ 0x40, 0x50, 0x10, 0x10 ],		#0xdb STAR
	[ 0x40, 0x60, 0x10, 0x10 ],		#0xdc HEART
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xdd （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xde （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xdf （空き）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0xe0 ' '（スペース）	灰文字
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xe1 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xe2 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xe3 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xe4 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xe5 （赤文字予約）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xe6 （赤文字予約）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0xe7 （空き）
	[ 0x30, 0xd0, 0x08, 0x08 ],		#0xe8 '('
	[ 0x38, 0xd0, 0x08, 0x08 ],		#0xe9 ')'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xea （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xeb （空き）
	[ 0x10, 0xd0, 0x08, 0x08 ],		#0xec ','（カンマ）
	[ 0x20, 0xd0, 0x08, 0x08 ],		#0xed '-'（ハイフン）
	[ 0x18, 0xd0, 0x08, 0x08 ],		#0xee '.'（ピリオド）
	[ 0x28, 0xd0, 0x08, 0x08 ],		#0xef '/'（スラッシュ）

	[ 0x00, 0xc8, 0x08, 0x08 ],		#0xf0 '0'
	[ 0x08, 0xc8, 0x08, 0x08 ],		#0xf1 '1'
	[ 0x10, 0xc8, 0x08, 0x08 ],		#0xf2 '2'
	[ 0x18, 0xc8, 0x08, 0x08 ],		#0xf3 '3'
	[ 0x20, 0xc8, 0x08, 0x08 ],		#0xf4 '4'
	[ 0x28, 0xc8, 0x08, 0x08 ],		#0xf5 '5'
	[ 0x30, 0xc8, 0x08, 0x08 ],		#0xf6 '6'
	[ 0x38, 0xc8, 0x08, 0x08 ],		#0xf7 '7'
	[ 0x00, 0xd0, 0x08, 0x08 ],		#0xf8 '8'
	[ 0x08, 0xd0, 0x08, 0x08 ],		#0xf9 '9'

	[ 0x20, 0xf0, 0x08, 0x08 ],		#0xfa ':'
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xfb （空き）
	[ 0x10, 0xf0, 0x08, 0x08 ],		#0xfc '<'→'RD'	
	[ 0x18, 0xf0, 0x08, 0x08 ],		#0xfd '>'→'ED'	
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xfe （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0xff （空き）

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x100 （空き）
	[ 0x00, 0xd8, 0x08, 0x08 ],		#0x101 'A'
	[ 0x08, 0xd8, 0x08, 0x08 ],		#0x102 'B'
	[ 0x10, 0xd8, 0x08, 0x08 ],		#0x103 'C'
	[ 0x18, 0xd8, 0x08, 0x08 ],		#0x104 'D'
	[ 0x20, 0xd8, 0x08, 0x08 ],		#0x105 'E'
	[ 0x28, 0xd8, 0x08, 0x08 ],		#0x106 'G'
	[ 0x30, 0xd8, 0x08, 0x08 ],		#0x107 'G'
	[ 0x38, 0xd8, 0x08, 0x08 ],		#0x108 'H'
	[ 0x00, 0xe0, 0x08, 0x08 ],		#0x109 'I'
	[ 0x08, 0xe0, 0x08, 0x08 ],		#0x10a 'J'
	[ 0x10, 0xe0, 0x08, 0x08 ],		#0x10b 'K'
	[ 0x18, 0xe0, 0x08, 0x08 ],		#0x10c 'L'
	[ 0x20, 0xe0, 0x08, 0x08 ],		#0x10d 'M'
	[ 0x28, 0xe0, 0x08, 0x08 ],		#0x10e 'N'
	[ 0x30, 0xe0, 0x08, 0x08 ],		#0x10f 'O'

	[ 0x38, 0xe0, 0x08, 0x08 ],		#0x110 'P'
	[ 0x00, 0xe8, 0x08, 0x08 ],		#0x111 'Q'
	[ 0x08, 0xe8, 0x08, 0x08 ],		#0x112 'R'
	[ 0x10, 0xe8, 0x08, 0x08 ],		#0x113 'S'
	[ 0x18, 0xe8, 0x08, 0x08 ],		#0x114 'T'
	[ 0x20, 0xe8, 0x08, 0x08 ],		#0x115 'U'
	[ 0x28, 0xe8, 0x08, 0x08 ],		#0x116 'V'
	[ 0x30, 0xe8, 0x08, 0x08 ],		#0x117 'W'
	[ 0x38, 0xe8, 0x08, 0x08 ],		#0x118 'X'
	[ 0x00, 0xf0, 0x08, 0x08 ],		#0x119 'Y'
	[ 0x08, 0xf0, 0x08, 0x08 ],		#0x11a 'Z'

	[ 0x00, 0x00, 0x00, 0x00 ],		#0x11b （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x11c （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x11d （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x11e （空き）
	[ 0x00, 0x00, 0x00, 0x00 ],		#0x11f （空き）
	]

#entry_table = [0 for dot in range(0x2b)]
entry_table = [
	#0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
	'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
	'Q','R','S','T','U','V','W','X','Y','Z','.','-','/',' ','0','1',
	'2','3','4','5','6','7','8','9','>','<',' ']

#---------------------------------------------------------------------------------------------------
#指定された位置に8x8フォントを描画します
#	dn = ord(string)で取得したコード
#---------------------------------------------------------------------------------------------------
def font_put( _xp, _yp, _dn ):
	if( _dn == 0x00 ):		#スペース
		return

	_id = _dn
	pyxel.blt( _xp, _yp, 0, ctbl[_id][0], ctbl[_id][1], ctbl[_id][2], ctbl[_id][3], 0 )

#---------------------------------------------------------------------------------------------------
#フォントテキストセット
#---------------------------------------------------------------------------------------------------
def set_font_text( _xp, _yp, _string, _col=0 ):
	_code = 0x00
	_codelist = list(_string)
	for i in range( len(_string) ):
		_code = ord( _codelist[i] )
		if( _col == 1 ):
			_code = _code + 0x40
		elif( _col == 2 ):
			_code = _code + 0x80
		elif( _col == 3 ):
			_code = _code + 0xc0
		font_put( _xp + (i*8), _yp, _code )

#-----------------------------------------------------------------
m_gem_tbl = [0 for tbl in range(11)]
#MULTI TAMA
#	0 1 2 3 4 5 6 7   8 9 a b c d e f
#0	□□□□□■■■　■■■□□□□□
#1	□□□■■■■■　■■■■■□□□
#2	□□■■■■■■　■■■■■■□□
#3	□■■■■■■■　■■■■■■■□
#4	□■■■■■■■　■■■■■■■□
#5	■■■■■■■■　■■■■■■■■
#6	■■■■■■■■　■■■■■■■■
#7	■■■■■■■■　■■■■■■■■

#8	■■■■■■■■　■■■■■■■■
#9	■■■■■■■■　■■■■■■■■
#a	■■■■■■■■　■■■■■■■■
#b	■■■■■■■■　■■■■■■■□
#c	□■■■■■■■　■■■■■■■□
#d	□□■■■■■■　■■■■■■□□
#e	□□□■■■■■　■■■■■□□□
#f	□□□□□■■■　■■■□□□□□

#16x16
m_gem_tbl[0] = [
#	0 1 2 3 4 5 6 7 8 9 a b c d e f
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,	#0
	0,0,7,5,5,3,3,3,3,3,3,3,5,7,0,0,	#1
	0,7,5,3,4,5,5,5,5,5,4,4,5,4,7,0,	#2
	7,5,3,1,3,4,5,5,4,4,4,5,4,3,5,7,	#3
	7,5,5,3,1,1,1,3,3,3,3,4,3,5,5,7,	#4
	7,3,5,5,1,3,4,5,5,5,5,3,5,5,5,7,	#5
	7,3,5,5,1,4,5,5,5,5,4,3,5,5,5,7,	#6
	7,3,5,5,3,5,5,5,5,3,3,1,5,5,5,7,	#7
	7,3,5,5,3,5,5,5,3,1,1,1,5,5,5,7,	#8
	7,3,3,5,3,5,5,3,1,1,1,1,5,5,5,7,	#9
	7,3,3,5,3,5,4,4,4,4,3,1,3,5,5,7,	#a
	7,3,5,3,3,3,3,3,3,3,3,3,3,4,5,7,	#b
	7,5,5,5,3,5,5,5,5,5,5,3,1,3,5,7,	#c
	0,7,5,5,4,4,4,4,4,4,4,4,3,1,7,0,	#d
	0,0,7,5,5,5,1,1,1,1,5,5,5,7,0,0,	#e
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,	#f
	0xff]

m_gem_tbl[1] = [
#	0 1 2 3 4 5 6 7 8 9 a b c d e f
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,	#0
	0,0,7,3,3,1,5,5,5,5,5,3,3,7,0,0,	#1
	0,7,3,3,1,1,1,5,5,5,5,5,5,3,7,0,	#2
	7,5,3,1,1,1,1,3,3,3,5,5,5,5,3,7,	#3
	7,5,5,1,1,1,3,3,3,2,2,3,5,5,2,7,	#4
	7,2,5,3,1,3,3,5,2,2,2,2,5,3,2,7,	#5
	7,2,5,3,3,3,5,3,2,2,2,2,5,2,2,7,	#6
	7,2,5,3,3,5,3,3,3,2,2,3,5,2,2,7,	#7
	7,2,5,3,5,5,5,3,3,2,3,2,5,2,2,7,	#8
	7,2,2,5,5,5,5,5,5,5,2,1,5,3,2,7,	#9
	7,2,2,2,5,5,5,5,5,2,2,1,5,5,3,7,	#a
	7,5,2,3,3,3,3,5,2,2,1,3,5,4,5,7,	#b
	7,5,5,3,3,2,2,2,1,1,3,5,6,4,3,7,	#c
	0,7,5,5,5,5,5,5,5,5,5,6,2,3,7,0,	#d
	0,0,7,3,3,3,3,3,3,3,4,4,3,7,0,0,	#e
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,	#f
	0xff]

m_gem_tbl[2] = [
#	0 1 2 3 4 5 6 7 8 9 a b c d e f
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,	#0
	0,0,7,4,1,1,1,1,1,2,2,2,2,7,0,0,	#1
	0,7,4,4,2,1,1,1,1,1,2,4,1,2,7,0,	#2
	7,4,4,2,2,4,4,4,4,4,4,4,1,1,5,7,	#3
	7,4,1,4,4,4,7,4,1,1,1,4,5,1,5,7,	#4
	7,2,1,5,4,5,5,5,4,1,1,4,5,5,5,7,	#5
	7,2,1,5,4,4,5,5,5,1,1,4,5,5,5,7,	#6
	7,2,1,5,4,4,4,5,5,5,1,4,5,5,5,7,	#7
	7,4,1,5,1,4,4,4,5,4,4,4,5,5,2,7,	#8
	7,4,4,5,1,1,4,4,4,4,4,4,5,5,2,7,	#9
	7,4,4,5,1,1,4,4,4,4,4,4,5,2,2,7,	#a
	7,4,4,5,1,1,1,4,4,4,4,4,1,4,4,7,	#b
	7,2,2,2,4,1,1,1,1,4,4,1,4,4,4,7,	#c
	0,7,2,2,2,5,5,5,5,5,5,2,2,4,7,0,	#d
	0,0,7,2,4,4,4,2,2,2,2,4,4,7,0,0,	#e
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,	#f
	0xff]

m_gem_tbl[3] = [
#	0 1 2 3 4 5 6 7 8 9 a b c d e f
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,
	0,0,7,5,2,2,2,2,4,4,4,4,5,7,0,0,
	0,7,1,1,1,1,1,2,2,2,2,2,1,5,7,0,
	7,1,2,2,1,1,1,1,1,1,1,1,1,1,5,7,
	7,4,2,1,1,1,1,1,1,1,1,1,1,1,2,7,
	7,4,1,5,2,2,2,2,2,2,2,2,1,2,2,7,
	7,4,2,5,5,5,5,5,5,5,5,5,2,2,4,7,
	7,4,2,5,5,5,5,4,4,2,2,2,2,2,4,7,
	7,4,2,5,4,4,4,2,1,1,1,1,2,4,4,7,
	7,4,2,4,4,4,1,1,1,1,1,1,4,4,4,7,
	7,4,5,4,4,2,2,2,2,1,1,1,4,4,1,7,
	7,4,5,4,4,2,2,2,2,1,1,4,5,5,1,7,
	7,4,5,5,4,1,1,1,1,1,1,4,5,5,5,7,
	0,7,5,5,5,2,2,2,2,2,5,5,5,5,7,0,
	0,0,7,4,4,4,4,4,4,4,4,4,4,7,0,0,
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,
	0xff]

m_gem_tbl[4] = [
#	0 1 2 3 4 5 6 7 8 9 a b c d e f
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,
	0,0,7,5,3,3,5,5,5,1,5,5,5,7,0,0,
	0,7,5,3,3,5,5,5,4,1,3,5,5,5,7,0,
	7,5,3,3,5,5,5,1,1,1,2,5,5,2,4,7,
	7,2,2,5,5,5,1,1,1,2,2,4,2,2,2,7,
	7,1,1,4,5,5,1,1,2,2,2,2,5,5,5,7,
	7,1,1,2,4,1,5,5,2,2,2,2,5,5,5,7,
	7,1,1,1,2,5,5,5,2,5,2,2,5,5,5,7,
	7,1,1,2,4,5,5,5,5,2,2,2,5,4,4,7,
	7,1,1,4,4,3,5,5,2,2,2,1,4,4,4,7,
	7,1,1,4,3,3,3,5,2,2,1,1,4,2,4,7,
	7,2,1,3,3,3,3,5,2,1,1,5,2,2,4,7,
	7,3,2,2,2,2,3,3,1,1,5,4,2,1,4,7,
	0,7,3,3,2,2,3,5,5,5,4,2,1,1,7,0,
	0,0,7,3,3,3,3,4,4,2,2,1,1,7,0,0,
	0,0,0,7,7,7,7,7,7,7,7,7,7,0,0,0,
	0xff]

#-----------------------------------------------------------------
#効果音セット
#-----------------------------------------------------------------
def se_set(_number):
	#タイトル時効果音は出力しない
	if( ( GWK[game_adv] != G_TITLE ) and ( GWK[game_adv] != G_DEMOPLAY ) ):
		pyxel.play( 3,_number )

#-----------------------------------------------------------------
#ドットパターン描画（玉は16dotx16dot）
#-----------------------------------------------------------------
def dot_pattern( _dx, _dy, _tp, _adr ):

	for _yp in range(16):
		for _xp in range(16):
			if( _adr[_yp * 16 + _xp] != 0 ):
				pyxel.pset( _dx + _xp, _dy + _yp, _tp * 0x10 + _adr[_yp * 16 + _xp] )

#-----------------------------------------------------------------
#ドットパターン描画（8dotx8dot）
#-----------------------------------------------------------------
def dot8_pattern( _dx, _dy, _adr ):

	for _yp in range(8):
		for _xp in range(8):
			if( _adr[_yp * 8 + _xp] != 0 ):
				pyxel.pset( _dx + _xp, _dy + _yp, _yp+2 )

#-----------------------------------------------------------------
#キャラクタセット
#	X座標, Y座標, id番号
#-----------------------------------------------------------------
def cput( _xp, _yp, _id ):
	if( _id >= IDMAX ):
		#print("[cput]IDMAX OVER ERROR", _id)
		return
	#ドットパターンタイプ？
	if( ctbl[_id][0] == 0xff ):
		#マルチカラー
		#ブロック
		if( _id == (MULTI_BASE + 0) ):
			dot_pattern( _xp, _yp, 2, m_gem_tbl[0] )
		elif( _id == (MULTI_BASE + 1) ):
			dot_pattern( _xp, _yp, 3, m_gem_tbl[1] )
		elif( _id == (MULTI_BASE + 2) ):
			dot_pattern( _xp, _yp, 1, m_gem_tbl[2] )
		elif( _id == (MULTI_BASE + 3) ):
			dot_pattern( _xp, _yp, 6, m_gem_tbl[3] )
		elif( _id == (MULTI_BASE + 4) ):
			dot_pattern( _xp, _yp, 4, m_gem_tbl[4] )

		elif( _id == (MULTI_BASE + 5) ):
			#黄こわれアニメ用
			_id = GWK[yelanim_count] + 0x5b
			pyxel.blt( _xp, _yp, 0, ctbl[_id][0], ctbl[_id][1], ctbl[_id][2], ctbl[_id][3], 0 )

	else:
		if( _id < IDMAX ):
			pyxel.blt( _xp, _yp, 0, ctbl[_id][0], ctbl[_id][1], ctbl[_id][2], ctbl[_id][3], 0 )


#-----------------------------------------------------------------
#タイトルセット
#-----------------------------------------------------------------
def title_set():
	GWK[game_adv] = G_TITLE
	GWK[game_subadv] = GS_INIT

#-----------------------------------------------------------------
#mine初期パラメータセット
#	GWK[mine_number]
#
#	ゲーム開始時、または、mine選択後に呼ばれるmine共通パラメータをセット
#-----------------------------------------------------------------
def mine_param_set():
	mine_adr = mine.mine_table[GWK[mine_number]]
	GWK[skip_number] = mine_adr[0][0]
	GWK[next_number] = mine_adr[0][1]
	GWK[remaining_time] = 0

	#ステージ選択用初期化
	for _cnt in range(STAGE_MAX):
		GWK[STAGE_WORK + _cnt] = 0

#-----------------------------------------------------------------
#ステージフィールドセット
#	GWK[mine_number]
#	GWK[stage_number]
#-----------------------------------------------------------------
def stage_set():

	GWK[move_counter] = 0
	GWK[undo_number] = 0

	mine_adr = mine.mine_table[GWK[mine_number]]
	#ステージパラメータセット
	GWK[rest_time] = mine_adr[GWK[stage_number]][0]
	GWK[move_number] = mine_adr[GWK[stage_number]][1]

	#rint("stage_number=",GWK[stage_number])
	#ステージフィールドセット
	_cnt = 2
	for _yp in range(FIELD_Y_MAX):
		for _xp in range(FIELD_X_MAX):
			_wk = FIELD_LEFT_WORK + ( _yp * FIELD_X_MAX + _xp )
			GWK[_wk] = mine_adr[GWK[stage_number]][_cnt]
			_cnt+=1

	for _yp in range(FIELD_Y_MAX):
		for _xp in range(FIELD_X_MAX):
			_wk = FIELD_RIGHT_WORK + ( _yp * FIELD_X_MAX + _xp )
			#print("_cnt=",_cnt)
			GWK[_wk] = mine_adr[GWK[stage_number]][_cnt]
			_cnt+=1

	#UNDOワーククリア
	for _undocnt in range(FIELD_X_MAX * FIELD_Y_MAX*FIELD_UNDO_MAX):
		GWK[FIELD_UNDO_WORK+_undocnt] = 0

	#UNDOワークに初期画面をセット
	for _yp in range(FIELD_Y_MAX):
		for _xp in range(FIELD_X_MAX):
			_wk_to = FIELD_UNDO_WORK + ( _yp * FIELD_X_MAX + _xp )
			_wk_from = FIELD_LEFT_WORK + ( _yp * FIELD_X_MAX + _xp )
			GWK[_wk_to] = GWK[_wk_from]


#-----------------------------------------------------------------
#カーソル移動
#-----------------------------------------------------------------
def cursol_move():

	#キーボード＆ジョイパッド
	if( getInputUP() ):
		GWK[cursol_y] -= 2
		if( GWK[cursol_y] < 0 ):
			GWK[cursol_y] = 0

	if( getInputDOWN() ):
		GWK[cursol_y] += 2
		if( GWK[cursol_y] > ( SCREEN_HEIGHT - 8 ) ):
			GWK[cursol_y] = SCREEN_HEIGHT - 8

	if( getInputLEFT() ):
		GWK[cursol_x] -= 2
		if( GWK[cursol_x] < 0 ):
			GWK[cursol_x] = 0

	if( getInputRIGHT() ):
		GWK[cursol_x] += 2
		if( GWK[cursol_x] > ( SCREEN_WIDTH - 8 ) ):
			GWK[cursol_x] = SCREEN_WIDTH - 8


	#アナログスティック
	_axis_x = getAxisLeftX()
	if( _axis_x < 0 ):
		_axis_x = ( (-1) * _axis_x ) >> 13		#/2000
		GWK[cursol_x] -= _axis_x
		if( GWK[cursol_x] < 0 ):
			GWK[cursol_x] = 0

	else:
		_axis_x = _axis_x >> 13
		GWK[cursol_x] += _axis_x
		if( GWK[cursol_x] > ( SCREEN_WIDTH - 8 ) ):
			GWK[cursol_x] = SCREEN_WIDTH - 8

	_axis_y = getAxisLeftY()
	if( _axis_y < 0 ):
		_axis_y = ( (-1) * _axis_y ) >> 13
		GWK[cursol_y] -= _axis_y
		if( GWK[cursol_y] < 0 ):
			GWK[cursol_y] = 0

	else:
		_axis_y = _axis_y >> 13
		GWK[cursol_y] += _axis_y
		if( GWK[cursol_y] > ( SCREEN_HEIGHT - 8 ) ):
			GWK[cursol_y] = SCREEN_HEIGHT - 8

#-----------------------------------------------------------------
#カーソル位置からフィールド位置を算出
#cursol_x,y -> field_x,y
#戻り値-1：枠外, フィールドオフセットを返す
#-----------------------------------------------------------------
def getFieldPos():

	if( ( GWK[cursol_x] >= FIELD_LEFT_BASEX ) and
		( GWK[cursol_x] < ( FIELD_LEFT_BASEX + ( FIELD_X_MAX * GEM_SIZE ) ) ) and
		( GWK[cursol_y] >= FIELD_LEFT_BASEY ) and
		( GWK[cursol_y] < ( FIELD_LEFT_BASEY + ( FIELD_Y_MAX * GEM_SIZE ) ) ) ):

		GWK[field_x] = ( GWK[cursol_x] - FIELD_LEFT_BASEX ) // GEM_SIZE
		GWK[field_y] = ( GWK[cursol_y] - FIELD_LEFT_BASEY ) // GEM_SIZE

		return ( GWK[field_y] * FIELD_X_MAX + GWK[field_x] )

	return -1

#-----------------------------------------------------------------
#スコア加算
#-----------------------------------------------------------------
def add_score(point):
	GWK[score] += point

#-----------------------------------------------------------------
#指定位置のGEMチェック
#戻り値	:-1 : 枠外
#		: 0 : 無し
#		: 1～5 : GEM(GEM_MIN～GEM_MAX)
#-----------------------------------------------------------------
#-----------------------------------------------------------------
#GEM決定→変化
#-----------------------------------------------------------------
def gem_change():

	_erase_f = 0		#消滅フラグ（GEM変化後"1"の時はスライドアニメが起きる）
	_check_ofs = getFieldPos()
	if( _check_ofs >= 0 ):
		_check_gem = GWK[FIELD_LEFT_WORK + _check_ofs]
		if( _check_gem == GEM_NOT ):
			#処理無し
			return

		#スコア加算★[TODO]暫定
		add_score(105)

		#中心セット
		_check_gem += 2
		if( _check_gem > GEM_MAX ):
			_check_gem = GEM_ERASE		#消滅
			_erase_f = 1				#消滅フラグセット
		GWK[FIELD_LEFT_WORK + _check_ofs] = _check_gem

		#上チェック
		if( GWK[field_y] >= 1 ):
			_check_ofs = ( GWK[field_y] - 1 ) * FIELD_X_MAX + GWK[field_x]
			_check_gem = GWK[FIELD_LEFT_WORK + _check_ofs]
			if( _check_gem != 0 ):
				_check_gem += 1
				if( _check_gem > GEM_MAX ):
					_check_gem = GEM_ERASE		#消滅
					_erase_f = 1				#消滅フラグセット
				GWK[FIELD_LEFT_WORK + _check_ofs] = _check_gem

		#下チェック
		if( GWK[field_y] < ( FIELD_Y_MAX-1 ) ):
			_check_ofs = ( GWK[field_y] + 1 ) * FIELD_X_MAX + GWK[field_x]
			_check_gem = GWK[FIELD_LEFT_WORK + _check_ofs]
			if( _check_gem != 0 ):
				_check_gem += 1
				if( _check_gem > GEM_MAX ):
					_check_gem = GEM_ERASE		#消滅
					_erase_f = 1				#消滅フラグセット
				GWK[FIELD_LEFT_WORK + _check_ofs] = _check_gem

		#左チェック
		if( GWK[field_x] >= 1 ):
			_check_ofs = GWK[field_y] * FIELD_X_MAX + ( GWK[field_x] - 1 )
			_check_gem = GWK[FIELD_LEFT_WORK + _check_ofs]
			if( _check_gem != 0 ):
				_check_gem += 1
				if( _check_gem > GEM_MAX ):
					_check_gem = GEM_ERASE		#消滅
					_erase_f = 1				#消滅フラグセット
				GWK[FIELD_LEFT_WORK + _check_ofs] = _check_gem

		#右チェック
		if( GWK[field_x] < ( FIELD_X_MAX-1 ) ):
			_check_ofs = GWK[field_y] * FIELD_X_MAX + ( GWK[field_x] + 1 )
			_check_gem = GWK[FIELD_LEFT_WORK + _check_ofs]
			if( _check_gem != 0 ):
				_check_gem += 1
				if( _check_gem > GEM_MAX ):
					_check_gem = GEM_ERASE		#消滅
					_erase_f = 1				#消滅フラグセット
				GWK[FIELD_LEFT_WORK + _check_ofs] = _check_gem

		#スライドアニメ実行
		if( _erase_f != 0 ):
			GWK[yelanim_count] = 0
			#GEM_ERASEを消えアニメ実行＆消える箇所の上のGEMを落とす

			#移動後のGEMフィールドをSAVE_WORKに保存、落下終了状態にしておく（落下終了後にFIELD_LEFT_WORKに転送する）
			#現状のfield workを保存ワークに転送
			for _cnt in range(FIELD_X_MAX * FIELD_Y_MAX):
				GWK[SAVE_WORK + _cnt] = GWK[FIELD_LEFT_WORK + _cnt]
			#保存ワークをスライド後のfieldに直しておく
			#下からチェック
			for _xp in range(FIELD_X_MAX):
				_cnt = 0
				_flag = 0
				for _yp in range(FIELD_Y_MAX-1, 0, -1):
					_wk = SAVE_WORK + ( _yp * FIELD_X_MAX + _xp )
					if( GWK[_wk] == GEM_ERASE ):
						_cnt += 1
						_flag = 1
						GWK[_wk] = GEM_NOT
						continue
					elif( GWK[_wk] == GEM_NOT ):
						if( _flag == 0 ):
							break
						else:
							_cnt += 1
					else:
						if( _flag == 1 ):
							#移動先と入れ替え
							_newyp = _yp + _cnt
							_wk2 = SAVE_WORK + ( _newyp * FIELD_X_MAX + _xp )
							if( GWK[_wk2] == GEM_NOT ):
								GWK[_wk2] = GWK[_wk]
								GWK[_wk] = GEM_NOT
							else:
								print("★ERROR：移動先はGEMがあるので移動できない")

			#スライドすべきGEMを抽出
			#下から検索、GEM_ERASE箇所の上をスライドさせる
			#移動ワークに転送FALL_WORK
			#移動総数はfall_counter
			#移動すべきGEMに番号つけて（下から順）番号順にシフト移動を実施
			GWK[fall_counter] = 0		
			for _xp in range(FIELD_X_MAX):
				_cnt = 0
				_flag = 0
				for _yp in range(FIELD_Y_MAX-1, 0, -1):
					_wk = FIELD_LEFT_WORK + ( _yp * FIELD_X_MAX + _xp )
					if( GWK[_wk] == GEM_ERASE ):
						_cnt += 1
						_flag = 1
						continue
					elif( GWK[_wk] == GEM_NOT ):
						if( _flag == 0 ):
							break
						else:
							_cnt += 1
					else:
						if( _flag == 1 ):
							_fallwk = FALL_WORK + ( GWK[fall_counter] * CWORK_SIZE )
							GWK[_fallwk + cid] = GWK[_wk]
							GWK[_fallwk + cnum] = GWK[fall_counter]
							GWK[_fallwk + mcnt] = _cnt * 8		#移動カウンタ（スピード２で１個あたり１６ドット移動するから８かける）
							GWK[_fallwk + xpos] = _xp * GEM_SIZE + FIELD_LEFT_BASEX
							GWK[_fallwk + ypos] = _yp * GEM_SIZE + FIELD_LEFT_BASEY
							GWK[_wk] = GEM_NOT		#field上は一旦無しにする
							GWK[fall_counter] += 1

			#print("GWK[fall_counter]=",GWK[fall_counter])
			GWK[fall_number] = 0
			
			#こわれアニメ実行
			GWK[game_subadv] = GS_BREAK

#-----------------------------------------------------------------
#UNDOワークに保存
#-----------------------------------------------------------------
def undo_save():

	if( GWK[undo_number] >= ( FIELD_UNDO_MAX - 1 ) ):
		print("★ERROR：これ以上UNDO保存できません")
		return

	_wk = FIELD_UNDO_WORK + ( FIELD_X_MAX * FIELD_Y_MAX * GWK[undo_number] )
	for _cnt in range(FIELD_X_MAX * FIELD_Y_MAX):
		GWK[_wk + _cnt] = GWK[FIELD_LEFT_WORK + _cnt]

	GWK[undo_number] += 1
	#移動数デクリメント
	GWK[move_number] -= 1
	if( GWK[move_number] <= 0 ):

		#移動数オーバーでスキップ数減算
		GWK[skip_number] -= 1
		if( GWK[skip_number] <= 0 ):
			#スキップ数オーバー
			GWK[game_subadv] = GS_OVER
			GWK[wait_counter] = 0
		else:
			GWK[game_subadv] = GS_SKIP
			GWK[wait_counter] = 0

		##移動数オーバー
		#GWK[game_subadv] = GS_OVER
		#GWK[wait_counter] = 0

#-----------------------------------------------------------------
#UNDO実行
#	ゲーム開始時は、GWK[undo_number]= 0
#	GEM選択後、選択前のGWK[undo_number]で保存して選択後の画面になる
#-----------------------------------------------------------------
def undo_exe():
	if( GWK[undo_number] <= 0 ):
		print("★ERROR：これ以上UNDO実行できません")
		return

	#保存してる番号はひとつ前なので減算する
	GWK[undo_number] -= 1

	#UNDOワークから転送
	_wk = FIELD_UNDO_WORK + ( FIELD_X_MAX * FIELD_Y_MAX * GWK[undo_number] )
	for _cnt in range(FIELD_X_MAX * FIELD_Y_MAX):
		GWK[FIELD_LEFT_WORK + _cnt] = GWK[_wk + _cnt]

	#移動数デクリメント
	GWK[move_number] -= 1
	if( GWK[move_number] <= 0 ):

		#移動数オーバーでスキップ数減算
		GWK[skip_number] -= 1
		if( GWK[skip_number] <= 0 ):
			#スキップ数オーバー
			GWK[game_subadv] = GS_OVER
			GWK[wait_counter] = 0
		else:
			GWK[game_subadv] = GS_SKIP
			GWK[wait_counter] = 0

		##移動数オーバー
		#GWK[game_subadv] = GS_OVER
		#GWK[wait_counter] = 0

#-----------------------------------------------------------------
#更新
#-----------------------------------------------------------------
def update():

	#カーソル移動
	cursol_move()

	if( GWK[game_adv] == G_TITLE ):
		if( GWK[game_subadv] == GS_INIT ):

			GWK[game_subadv] = GS_MAIN
		elif( GWK[game_subadv] == GS_MAIN ):
			if( getInputA() ):
			
				GWK[multi_color_switch] = 1
				GWK[mine_number] = 0

				#mineパラメータ初期化
				mine_param_set()

				#ステージ選択
				stage_select()
				
				GWK[game_adv] = G_GAME
				
				#GWK[remaining_time] = 150	#[debug]
				#GWK[game_adv] = G_MAP		#[debug]
				
				GWK[game_subadv] = GS_INIT
				
	elif( GWK[game_adv] == G_GAME ):
		if( GWK[game_subadv] == GS_INIT ):
			#ステージセット
			stage_set()
			#カーソル位置初期化
			GWK[cursol_x] = SCREEN_WIDTH//2
			GWK[cursol_y] = SCREEN_HEIGHT//2

			GWK[start_time] = time.perf_counter()

			GWK[game_subadv] = GS_MAIN
		elif( GWK[game_subadv] == GS_MAIN ):
		
			_now_time = time.perf_counter()
			GWK[past_time] = _now_time - GWK[start_time]
			_rest_time = GWK[rest_time] - GWK[past_time]
			if( _rest_time <= 0 ):
				#タイムオーバー
				GWK[game_subadv] = GS_OVER
				GWK[wait_counter] = 0

			#SKIP BTNチェック
			GWK[skip_btn_sw] = 0
			if( ( SKIP_BTN_BASEX <= GWK[cursol_x] < ( SKIP_BTN_BASEX + SKIP_BTN_WIDTH ) ) and
				( SKIP_BTN_BASEY <= GWK[cursol_y] < ( SKIP_BTN_BASEY + SKIP_BTN_HEIGHT ) ) ):
				GWK[skip_btn_sw] = 1

			#GEM選択
			if( getInputA() ):
				if( GWK[skip_btn_sw] != 0 ):
					GWK[skip_number] -= 1
					if( GWK[skip_number] <= 0 ):
						#スキップ数オーバー
						GWK[game_subadv] = GS_OVER
						GWK[wait_counter] = 0
					else:
						GWK[game_subadv] = GS_SKIP
						GWK[wait_counter] = 0
				
				else:
					#選択前の状態をUNDOワークに保存
					undo_save()
					
					#移動数オーバーでゲーム中じゃなくなったら終了
					if( GWK[game_subadv] != GS_MAIN ):
						return

					#GEM変化
					gem_change()

					#ゲーム中ならステージクリアチェック（こわれアニメになる場合がある）
					if( GWK[game_subadv] == GS_MAIN ):
						_res = stage_clear_check()
						if( _res != 0 ):
							GWK[game_subadv] = GS_CLEAR
							GWK[wait_counter] = 0

			elif( getInputB() ):
				#UNDO実行
				undo_exe()

		elif( GWK[game_subadv] == GS_BREAK ):
			#黄こわれアニメ実行
			if( ( pyxel.frame_count & 3 ) == 3 ):
				GWK[yelanim_count] += 1
				if( GWK[yelanim_count] > 5 ):
					#アニメ終了
					for _yp in range(FIELD_Y_MAX):
						for _xp in range(FIELD_X_MAX):
							_wk = FIELD_LEFT_WORK + ( _yp * FIELD_X_MAX + _xp )
							if( GWK[_wk] == GEM_ERASE ):
								GWK[_wk] = GEM_NOT

					#こわれアニメの後にGEM移動が入る
					GWK[game_subadv] = GS_FALL

		elif( GWK[game_subadv] == GS_FALL ):
			_cnt2 = 0
			for _cnt in range(GWK[fall_counter]):
				_fallwk = FALL_WORK + ( _cnt * CWORK_SIZE )
				if( GWK[_fallwk + cnum] == 99 ):	#アニメ中
					GWK[_fallwk + mcnt] -= 1
					if( GWK[_fallwk + mcnt] < 0 ):
						GWK[_fallwk + cnum] = 98	#アニメ終了
					else:
						GWK[_fallwk + ypos] += 2

				#落とすアニメ実行チェック（この間は操作選択不可、移動はできる）
				elif( GWK[_fallwk + cnum] == GWK[fall_number] ):
					GWK[_fallwk + cnum] = 99

				elif( GWK[_fallwk + cnum] == 98 ):	#アニメ終了済み
					_cnt2 += 1

			#４フレームに１個アニメ開始させる
			if( GWK[fall_number] < GWK[fall_counter] ):
				if( ( pyxel.frame_count & 0x03 ) == 0x03 ):
					GWK[fall_number] += 1

			if( _cnt2 >= GWK[fall_counter] ):
				#落とすアニメ終了
				for _cnt in range(FIELD_X_MAX * FIELD_Y_MAX):
					GWK[FIELD_LEFT_WORK + _cnt] = GWK[SAVE_WORK + _cnt]
					GWK[SAVE_WORK + _cnt] = 0

				for _cnt in range(GWK[fall_counter] * CWORK_SIZE):
					GWK[FALL_WORK + _cnt] = 0
				GWK[fall_counter] = 0

				#移動終了ならステージクリアチェック
				_res = stage_clear_check()
				if( _res == 0 ):
					GWK[game_subadv] = GS_MAIN
				else:
					GWK[game_subadv] = GS_CLEAR
					GWK[wait_counter] = 0

		elif( GWK[game_subadv] == GS_CLEAR ):
			#ステージクリアメッセージ表示
			GWK[wait_counter] += 1
			if( GWK[wait_counter] > 100 ):
				#残り時間を加算
				GWK[remaining_time] += GWK[rest_time]
			
				GWK[game_subadv] = GS_NEXT
		
		elif( GWK[game_subadv] == GS_SKIP ):
			#ステージクリアメッセージ表示
			GWK[wait_counter] += 1
			if( GWK[wait_counter] > 100 ):
				#ステージ選択
				stage_select()
				GWK[game_subadv] = G_GAME
				GWK[game_subadv] = GS_INIT
		
		elif( GWK[game_subadv] == GS_NEXT ):
			#次のステージ or mine選択 or エンディングへ
			_res = next_stage_set()
			if( _res == 0 ):
				#次のステージへ
				GWK[game_adv] = G_GAME
				GWK[game_subadv] = GS_INIT
			elif( _res == 1 ):
				#mine選択へ
				GWK[game_adv] = G_MAP
				GWK[game_subadv] = GS_INIT
			elif( _res == 2 ):
				#エンディングへ
				GWK[game_adv] = G_END
				GWK[game_subadv] = GS_INIT

		elif( GWK[game_subadv] == GS_OVER ):
			#ゲームオーバーメッセージ表示
			GWK[wait_counter] += 1
			if( GWK[wait_counter] > 200 ):
				title_set()

	elif( GWK[game_adv] == G_MAP ):
		
		

		#MINE SELECT & REMAINING TIME加算
		if( GWK[game_subadv] == GS_INIT ):
		
			#選択可能値をセット
			if( GWK[mine_number] <= 20 ):
				GWK[select_mine1] = select_mine_table[GWK[mine_number] * 2 + 0]
				GWK[select_mine2] = select_mine_table[GWK[mine_number] * 2 + 1]
			else:
				print("★ERROR：mine選択不可です GWK[mine_number]=",GWK[mine_number])
		
			#カーソル位置初期化
			GWK[cursol_x] = SCREEN_WIDTH//2
			GWK[cursol_y] = SCREEN_HEIGHT//2

			GWK[game_subadv] = GS_MAIN
		
		elif( GWK[game_subadv] == GS_MAIN ):

			if( ( pyxel.frame_count & 3 ) == 3 ):
				if( GWK[remaining_time] > 0 ):
					GWK[remaining_time] -= 1
					add_score(20)
			
			if( getInputA() ):
				#選択可能なmineを選択したかどうかのチェック
				_res = select_mine_check()
				if( _res != 0 ):
					#有効なmineだった時はセットする
					GWK[mine_number] = _res

					#残り時間の得点加算が終わってないならここで加算する
					if( GWK[remaining_time] > 0 ):
						add_score( GWK[remaining_time] * 20 )

					#mineパラメータ初期化
					mine_param_set()

					#ステージ選択
					stage_select()
					
					GWK[game_adv] = G_GAME
					GWK[game_subadv] = GS_INIT


#-----------------------------------------------------------------
#選択可能なmineを選択したかどうかのチェック
#	カーソル位置が正しい選択場所かどうかをチェック
#	選択可能な値は、GWK[select_mine1]、GWK[select_mine2]に格納されている
#	選択可能なmine番号を返す、選択不可な場合は0を返す
#-----------------------------------------------------------------
def select_mine_check():
	_xp1 = map_mine_table[GWK[select_mine1]*4+0]
	_yp1 = map_mine_table[GWK[select_mine1]*4+1]
	if( ( _xp1 <= GWK[cursol_x] < (_xp1+8) ) and  _yp1 <= GWK[cursol_y] < (_yp1+8) ):
		return GWK[select_mine1]

	_xp2 = map_mine_table[GWK[select_mine2]*4+0]
	_yp2 = map_mine_table[GWK[select_mine2]*4+1]
	if( ( _xp2 <= GWK[cursol_x] < (_xp2+8) ) and  _yp2 <= GWK[cursol_y] < (_yp2+8) ):
		return GWK[select_mine2]

	return 0

#-----------------------------------------------------------------
#次のステージ(0) or mine選択(1) or エンディングへ(2)
#  0:A,  1:B,  2:C,  3:D,  4:E,  5:F,  6:G,  7:H
#  8:I,  9:J, 10:K, 11:L, 12:M, 13:N, 14:O, 15:P
# 16:Q, 17:R, 18:S, 19:T, 20:U, 21:V, 22:W, 23:X
# 24:Y, 25:Z
#-----------------------------------------------------------------
def next_stage_set():

	GWK[next_number] -= 1
	if( GWK[next_number] <= 0 ):
		return 1

	if( GWK[mine_number] >= 21 ):
		#GOTO エンディング
		return 2
	
	#ステージ選択
	stage_select()
	return 0

#-----------------------------------------------------------------
#ステージ選択
#	GWK[stage_number]をセット
#-----------------------------------------------------------------
def stage_select():
	_stage = pyxel.rndi(STAGE_MIN,STAGE_MAX)
	for _cnt in range(STAGE_MAX):
		_stage = _stage + _cnt
		if( _stage > STAGE_MAX ):
			_stage = STAGE_MIN
		if( GWK[STAGE_WORK + (_stage-1)] == 0 ):
			GWK[STAGE_WORK + (_stage-1)] = 1
			GWK[stage_number] = _stage
			return

	#STAGE_WORK全部埋まったらしい
	for _cnt in range(STAGE_MAX):
		GWK[STAGE_WORK + _cnt] = 0

	_stage = pyxel.rndi(STAGE_MIN,STAGE_MAX)
	GWK[STAGE_WORK + (_stage-1)] = 1
	GWK[stage_number] = _stage

#-----------------------------------------------------------------
#ステージクリアチェック
#戻り値：0/1=まだ/次へ
#-----------------------------------------------------------------
def stage_clear_check():
	for _cnt in range(FIELD_X_MAX * FIELD_Y_MAX):
		if( GWK[FIELD_RIGHT_WORK + _cnt] != GWK[FIELD_LEFT_WORK + _cnt] ):
			return 0

	#すべて同じなのでクリア
	return 1

#-----------------------------------------------------------------
#スコア＆ステージ出力
#-----------------------------------------------------------------
def score_out():

	#スコアアイコン
	cput( SCORE_BASEX, SCORE_BASEY, 0x1d )
	cput( SCORE_BASEX+4, SCORE_BASEY+3, 0x1f )

	#６桁数値のスコアセット
	_flg = 0
	_num = GWK[score]//100000
	if( _num != 0 ):
		cput( SCORE_BASEX+0x10, SCORE_BASEY, _num+SCORE_CID )
		_flg = 1
	_num = ( GWK[score]//10000 )%10
	if( ( _num != 0 ) or ( ( _num == 0 ) and ( _flg != 0 ) ) ):
		cput( SCORE_BASEX+0x18, SCORE_BASEY, _num+SCORE_CID )
		_flg = 1
	_num = ( GWK[score]//1000 )%10
	if( ( _num != 0 ) or ( ( _num == 0 ) and ( _flg != 0 ) ) ):
		cput( SCORE_BASEX+0x20, SCORE_BASEY, _num+SCORE_CID )
		_flg = 1
	_num = ( GWK[score]//100 )%10
	if( ( _num != 0 ) or ( ( _num == 0 ) and ( _flg != 0 ) ) ):
		cput( SCORE_BASEX+0x28, SCORE_BASEY, _num+SCORE_CID )
		_flg = 1
	_num = ( GWK[score]//10 )%10
	if( ( _num != 0 ) or ( ( _num == 0 ) and ( _flg != 0 ) ) ):
		cput( SCORE_BASEX+0x30, SCORE_BASEY, _num+SCORE_CID )

	_num = GWK[score]%10
	cput( SCORE_BASEX+0x38, SCORE_BASEY, _num+SCORE_CID )

	#ステージアイコン
	cput( STAGE_BASEX, STAGE_BASEY, 0x1c )
	#ステージ
	cput( STAGE_BASEX+0x20, STAGE_BASEY+6, GWK[mine_number] + 0xc1 )
	_num = GWK[stage_number]//10
	cput( STAGE_BASEX+0x30, STAGE_BASEY+6, _num + 0xb0 )
	_num = GWK[stage_number]%10
	cput( STAGE_BASEX+0x38, STAGE_BASEY+6, _num + 0xb0 )

#-----------------------------------------------------------------
#パラメータ出力
#-----------------------------------------------------------------
def param_out():
	#move paramアイコン
	cput( MOVE_REMAIN_BASEX, MOVE_REMAIN_BASEY, 0x18 )
	_num = GWK[move_number]//10
	cput( MOVE_REMAIN_BASEX+0x18, MOVE_REMAIN_BASEY, _num+SCORE_CID )
	_num = GWK[move_number]%10
	cput( MOVE_REMAIN_BASEX+0x20, MOVE_REMAIN_BASEY, _num+SCORE_CID )

	#skip paramアイコン
	cput( SKIP_REMAIN_BASEX, SKIP_REMAIN_BASEY, 0x19 )
	_num = GWK[skip_number]//10
	cput( SKIP_REMAIN_BASEX+0x18, SKIP_REMAIN_BASEY, _num+SCORE_CID )
	_num = GWK[skip_number]%10
	cput( SKIP_REMAIN_BASEX+0x20, SKIP_REMAIN_BASEY, _num+SCORE_CID )

	#next paramアイコン
	cput( NEXT_REMAIN_BASEX, NEXT_REMAIN_BASEY, 0x1a )
	_num = GWK[next_number]//10
	cput( NEXT_REMAIN_BASEX+0x18, NEXT_REMAIN_BASEY, _num+SCORE_CID )
	_num = GWK[next_number]%10
	cput( NEXT_REMAIN_BASEX+0x20, NEXT_REMAIN_BASEY, _num+SCORE_CID )

	#time paramアイコン
	cput( TIME_BASEX, TIME_BASEY, 0x1b )

	_rest_time = pyxel.floor(GWK[rest_time] - GWK[past_time])
	#表示がおかしくならないように補正しておく
	if( _rest_time < 0 ):
		_rest_time = 0
	#分
	_minnum = _rest_time // 60
	_min = _minnum // 10
	cput( TIME_BASEX+0x10, TIME_BASEY, _min+SCORE_CID )
	_min = _minnum % 10
	cput( TIME_BASEX+0x18, TIME_BASEY, _min+SCORE_CID )
	#コロン
	cput( TIME_BASEX+0x20, TIME_BASEY, 0x16 )
	#秒
	_secnum = _rest_time % 60
	_sec = _secnum // 10
	cput( TIME_BASEX+0x28, TIME_BASEY, _sec+SCORE_CID )
	_sec = _secnum % 10
	cput( TIME_BASEX+0x30, TIME_BASEY, _sec+SCORE_CID )

	#print(_rest_time, _minnum, _secnum )
	
	_col = 0
	if( GWK[skip_btn_sw] != 0 ):
		_col =1
	set_font_text( SKIP_BTN_BASEX+4, SKIP_BTN_BASEY, 'SKIP', _col )
	set_font_text( SKIP_BTN_BASEX, SKIP_BTN_BASEY+8, 'STAGE', _col )
	
#-----------------------------------------------------------------
#SAMPLE GEM
#-----------------------------------------------------------------
def sample_gem_out():
	for _cnt in range(5):
		if( GWK[multi_color_switch] != 0 ):
			cput( SAMPLE_GEMX, SAMPLE_GEMY + (0x20*_cnt), MULTI_BASE+_cnt )
		else:
			cput( SAMPLE_GEMX, SAMPLE_GEMY + (0x20*_cnt), DEF_BASE+_cnt )

#-----------------------------------------------------------------
#描画
#-----------------------------------------------------------------
def draw():
	pyxel.cls(0)
	if( GWK[game_adv] == G_TITLE ):
		pyxel.blt( SCREEN_WIDTH//2-0x40, SCREEN_HEIGHT//2-0x40, 1, 0,0,0x80,0x40, 0 )
		set_font_text( SCREEN_WIDTH//2 - (8*12//2), SCREEN_HEIGHT//2-0x10, 'PYXEL  CLONE', 0 )
		set_font_text( (SCREEN_WIDTH//2) - (8*24//2), SCREEN_HEIGHT//2+0x28, 'Z-KEY OR A-BUTTON  START', 0 )
		set_font_text( (SCREEN_WIDTH//2) - (8*18//2), SCREEN_HEIGHT//2+0x40, 'VERSION 2024.12.11', 0 )
	elif( GWK[game_adv] == G_GAME ):
		#背景描画
		pyxel.bltm(0, 0, 0, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
		#gemセット
		for _yp in range(FIELD_Y_MAX):
			for _xp in range(FIELD_X_MAX):
				_wk = FIELD_LEFT_WORK + ( _yp * FIELD_X_MAX + _xp )
				if( GWK[_wk] != 0 ):
					if( GWK[multi_color_switch] != 0 ):
						_cid = GWK[_wk] + MULTI_BASE - 1
					else:
						_cid = GWK[_wk] + DEF_BASE - 1
					cput( ( _xp * GEM_SIZE ) + FIELD_LEFT_BASEX, ( _yp * GEM_SIZE ) + FIELD_LEFT_BASEY, _cid )
				_wk = FIELD_RIGHT_WORK + ( _yp * FIELD_X_MAX + _xp )
				if( GWK[_wk] != 0 ):
					if( GWK[multi_color_switch] != 0 ):
						_cid = GWK[_wk] + MULTI_BASE - 1
					else:
						_cid = GWK[_wk] + DEF_BASE - 1
					cput( ( _xp * GEM_SIZE ) + FIELD_RIGHT_BASEX, ( _yp * GEM_SIZE ) + FIELD_RIGHT_BASEY, _cid )

		if( ( GWK[game_subadv] == GS_FALL ) or ( GWK[game_subadv] == GS_BREAK ) ):
			#移動アニメ
			for _cnt in range(GWK[fall_counter]):
				_fallwk = FALL_WORK + ( _cnt * CWORK_SIZE )
				if( GWK[multi_color_switch] != 0 ):
					_cid = GWK[_wk] + MULTI_BASE - 1
				else:
					_cid = GWK[_wk] + DEF_BASE - 1
				cput( GWK[_fallwk + xpos], GWK[_fallwk + ypos], _cid )


		#スコア＆ステージ出力
		score_out()
		#パラメータ出力
		param_out()
		#サンプルGEM出力
		sample_gem_out()
		#カーソル出力
		cput( GWK[cursol_x], GWK[cursol_y], 0x17 )

		#フォント出力
		if( GWK[game_subadv] == GS_CLEAR ):
			set_font_text( SCREEN_WIDTH//2 - (8*12//2), SCREEN_HEIGHT//2, 'STAGE  CLEAR', 0 )
		elif( GWK[game_subadv] == GS_SKIP ):
			set_font_text( SCREEN_WIDTH//2 - (8*10//2), SCREEN_HEIGHT//2, 'STAGE SKIP', 0 )
		elif( GWK[game_subadv] == GS_OVER ):
			set_font_text( SCREEN_WIDTH//2 - (8*10//2), SCREEN_HEIGHT//2, 'GAME  OVER', 0 )


	elif( GWK[game_adv] == G_MAP ):
		set_font_text( SCREEN_WIDTH//2 - (8*28//2), SCREEN_HEIGHT//8, 'RESULTS AND CHOOSE NEXT MINE', 0 )
		set_font_text( SCREEN_WIDTH//16, SCREEN_HEIGHT//8 + 0x20, 'PLAYER ONE', 0 )
		set_font_text( SCREEN_WIDTH//16, SCREEN_HEIGHT//8 + 0x28, 'SCORE', 0 )
		set_font_text( SCREEN_WIDTH//16+0x30, SCREEN_HEIGHT//8 + 0x28, str(GWK[score]), 1 )

		set_font_text( SCREEN_WIDTH//16, SCREEN_HEIGHT//8 + 0x38, 'REMAINING', 0 )
		set_font_text( SCREEN_WIDTH//16, SCREEN_HEIGHT//8 + 0x40, 'TIME', 0 )

		_remaining_time = GWK[remaining_time]
		if( _remaining_time < 0 ):
			_remaining_time = 0
		_minnum = _remaining_time // 60
		_secnum = _remaining_time % 60
		set_font_text( SCREEN_WIDTH//16+0x30, SCREEN_HEIGHT//8 + 0x40, 
			str(_minnum//10)+str(_minnum%10)+":"+str(_secnum//10)+str(_secnum%10), 1 )

		#アルファベット接続ライン
		for _base in range(21):
			_sel1 = select_mine_table[_base * 2 + 0]
			_sel2 = select_mine_table[_base * 2 + 1]
			
			pyxel.line(	map_mine_table[_base*4+0]+4, map_mine_table[_base*4+1]+4,
						map_mine_table[_sel1*4+0]+4, map_mine_table[_sel1*4+1]+4, 4 )
			if( _sel2 > 0 ):
				pyxel.line(	map_mine_table[_base*4+0]+4, map_mine_table[_base*4+1]+4,
						map_mine_table[_sel2*4+0]+4, map_mine_table[_sel2*4+1]+4, 4 )
		
		#アルファベット表示
		for _cnt in range(26):
			_xp = map_mine_table[_cnt*4+0]
			_yp = map_mine_table[_cnt*4+1]
			_cid = map_mine_table[_cnt*4+2]

			if( GWK[mine_number] == _cnt ):
				#現在位置
				 _cid = _cid + 0x80
			elif( _cnt == GWK[select_mine1] ):
				#選択可能
				_xp1 = map_mine_table[GWK[select_mine1]*4+0]
				_yp1 = map_mine_table[GWK[select_mine1]*4+1]
				if( ( _xp1 <= GWK[cursol_x] < (_xp1+8) ) and  _yp1 <= GWK[cursol_y] < (_yp1+8) ):
					_cid = _cid + 0x40
			elif( _cnt == GWK[select_mine2] ):
				#選択可能
				_xp2 = map_mine_table[GWK[select_mine2]*4+0]
				_yp2 = map_mine_table[GWK[select_mine2]*4+1]
				if( ( _xp2 <= GWK[cursol_x] < (_xp2+8) ) and  _yp2 <= GWK[cursol_y] < (_yp2+8) ):
					_cid = _cid + 0x40
			else:
				#選択不可能
				_cid = _cid + 0xc0

			cput( _xp, _yp, _cid )

		#カーソル出力
		cput( GWK[cursol_x], GWK[cursol_y], 0x17 )

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
	if pyxel.btnp(pyxel.KEY_X, hold=10, repeat=10) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B, hold=10, repeat=10):
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

#アナログスティック（値：0x8000～0xffff,0～7fff）
def getAxisLeftX():
	return pyxel.btnv( pyxel.GAMEPAD1_AXIS_LEFTX )
	
def getAxisLeftY():
	return pyxel.btnv( pyxel.GAMEPAD1_AXIS_LEFTY )

def getAxisRightX():
	return pyxel.btnv( pyxel.GAMEPAD1_AXIS_RIGHTX )

def getAxisRightY():
	return pyxel.btnv( pyxel.GAMEPAD1_AXIS_RIGHTY )

#-----------------------------------------------------------------
#INIT&RUN
#-----------------------------------------------------------------
pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=60)
#[use Web]ESCキーを無効化
#pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=60, quit_key=pyxel.KEY_NONE, title='pyxelgem')

#リソース読み込み（マルチカラー有り）
pyxel.load("gemx.pyxres")
#ワーククリア
work_clear()
#Goto タイトル
title_set()

#実行
pyxel.run(update, draw)
