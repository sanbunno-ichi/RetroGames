#mine_table

mine_A = [0 for tbl in range(17)]
#skip数, 次のmineに進むためのクリア数残り
mine_A[0] = [8,4]
#制限時間(sec), 移動回数
#FIELD_X_MAX * FIELD_Y_MAX * 2(left,right)
mine_A[1] = [
		90,5,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,1,0,0,0,
		0,0,0,1,2,1,0,0,
		0,0,2,2,2,2,2,0,
		0,0,1,1,2,1,1,0,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,1,0,0,0,
		0,0,0,1,3,1,0,0,
		0,0,2,3,4,3,2,0,
		0,0,1,1,3,1,1,0,
	]
mine_A[2] = [
		90,3,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,5,5,5,5,5,5,0,
		0,5,4,3,3,4,5,0,
		0,5,3,3,3,3,5,0,
		0,5,3,3,3,3,5,0,
		0,5,4,3,3,4,5,0,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,5,5,5,5,5,5,0,
		0,5,4,3,4,4,5,0,
		0,5,3,4,5,4,5,0,
		0,5,3,3,4,3,5,0,
		0,5,4,3,3,4,5,0,
	]
mine_A[3] = [
		120, 5,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,2,3,3,3,2,0,
		0,0,3,2,3,2,3,0,
		0,0,3,3,2,3,3,0,
		0,0,3,2,3,2,3,0,
		0,0,2,3,3,3,2,0,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,2,3,3,3,2,0,
		0,0,3,3,3,3,3,0,
		0,0,4,5,4,5,4,0,
		0,0,3,3,3,3,3,0,
		0,0,2,3,3,3,2,0,
	]

mine_A[4] = [
		40,2,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,2,0,0,0,
		0,0,0,0,4,0,0,0,
		0,0,0,0,5,0,0,0,
		0,0,0,0,5,0,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,4,0,0,0,
		0,0,0,0,5,0,0,0,
		0,0,0,0,5,0,0,0,
		0,0,0,0,5,0,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
	]

mine_A[5] = [
		60,6,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		3,3,3,0,0,3,3,3,
		2,2,2,0,0,2,2,2,
		3,3,3,0,0,3,3,3,
		3,3,3,0,0,3,3,3,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		3,3,3,0,0,3,4,3,
		2,3,2,0,0,3,4,3,
		4,5,4,0,0,3,4,3,
		3,4,3,0,0,3,3,3,
	]

mine_A[6] = [
		120,8,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,1,3,0,0,0,
		3,0,0,3,3,0,0,1,
		3,3,0,3,3,0,3,3,
		1,3,0,3,1,0,3,3,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,2,3,0,0,0,
		3,0,0,5,4,0,0,2,
		4,3,0,4,4,0,4,5,
		3,4,0,4,3,0,3,4,
	]

mine_A[7] = [
		110,6,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,1,1,1,1,0,0,
		0,0,4,4,4,4,0,0,
		0,0,2,2,2,2,0,0,
		0,0,2,2,2,2,0,0,
		0,0,4,4,3,3,0,0,
		0,0,3,3,4,4,0,0,
		0,0,2,2,2,2,0,0,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,2,3,2,1,0,0,
		0,0,4,5,4,4,0,0,
		0,0,2,2,2,2,0,0,
		0,0,2,2,3,2,0,0,
		0,0,4,5,5,4,0,0,
		0,0,3,3,5,4,0,0,
		0,0,2,2,2,2,0,0,
	]

mine_A[8] = [
		90,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		2,2,0,0,0,0,2,2,
		3,3,0,0,0,0,3,3,
		2,2,0,0,0,0,1,1,
		1,1,0,0,0,0,2,2,
		4,4,0,0,0,0,4,4,
		2,2,0,0,0,0,2,2,
		5,5,0,0,0,0,5,5,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		2,2,0,0,0,0,2,2,
		4,3,0,0,0,0,3,4,
		4,3,0,0,0,0,2,3,
		2,1,0,0,0,0,2,3,
		4,4,0,0,0,0,4,4,
		2,2,0,0,0,0,2,2,
		5,5,0,0,0,0,5,5,
	]

mine_A[9] = [
		110,8,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,1,2,1,1,1,1,0,
		0,2,1,2,1,1,1,0,
		0,1,2,1,1,2,1,0,
		0,1,1,1,2,1,2,0,
		0,1,1,1,1,2,1,0,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,3,4,1,1,1,1,0,
		0,4,3,3,1,1,1,0,
		0,1,3,1,1,3,1,0,
		0,1,1,1,3,3,4,0,
		0,1,1,1,1,4,3,0,
	]

mine_A[10] = [
		80,6,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		3,3,3,3,3,3,3,3,
		1,1,1,3,3,2,2,2,
		1,1,1,3,3,2,2,2,
		3,3,3,3,3,3,3,3,
		3,4,4,4,4,4,4,3,
		3,4,5,5,5,5,4,3,
		3,4,5,5,5,5,4,3,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		5,4,3,3,3,3,4,5,
		2,1,1,3,3,2,2,3,
		1,1,1,3,3,2,2,2,
		3,3,3,3,3,3,3,3,
		3,4,4,4,4,4,4,3,
		4,4,5,5,5,5,4,4,
		5,5,5,5,5,5,5,5,
	]

mine_A[11] = [
		90,6,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		3,3,3,0,0,2,2,2,
		3,3,3,0,0,2,2,2,
		3,3,3,0,0,2,2,2,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		5,4,3,0,0,2,3,4,
		4,3,4,0,0,3,2,3,
		3,4,5,0,0,4,3,2,
	]

mine_A[12] = [
		60,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,5,5,5,5,0,0,
		0,0,4,4,4,4,0,0,
		0,0,3,3,3,3,0,0,
		0,0,2,2,2,2,0,0,
		0,0,1,1,1,1,0,0,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,5,5,5,5,0,0,
		0,0,4,4,4,4,0,0,
		0,0,3,3,3,3,0,0,
		0,0,3,2,2,3,0,0,
		0,0,3,2,2,3,0,0,
	]

mine_A[13] = [
		130,12,
		3,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,0,
		3,3,3,3,3,3,3,3,
		
		5,0,0,0,0,0,0,0,
		5,0,0,0,0,0,0,0,
		5,0,0,0,0,0,0,0,
		5,0,0,0,0,0,0,0,
		5,0,0,0,0,0,0,0,
		5,0,0,0,0,0,0,0,
		5,0,0,0,0,0,0,0,
		5,0,0,0,0,0,0,0,
		5,0,0,0,0,0,0,0,
		5,5,5,5,5,5,5,5,
	]

mine_A[14] = [
		130,8,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		2,3,3,3,3,3,3,3,
		2,2,3,3,3,3,3,1,
		2,2,2,3,3,3,1,1,
		2,2,2,2,3,1,1,1,
		2,2,2,2,1,1,1,1,
		2,2,2,1,1,1,1,1,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		4,4,3,3,3,3,4,5,
		3,2,3,3,3,3,3,2,
		2,2,2,3,4,3,1,1,
		2,2,2,3,5,2,1,1,
		3,2,2,2,2,1,1,2,
		4,3,2,1,1,1,2,3,
	]

mine_A[15] = [
		50,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		4,3,4,0,0,3,2,3,
		3,2,3,0,0,2,1,2,
		4,3,4,0,0,3,2,3,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		4,4,4,0,0,3,3,3,
		4,4,4,0,0,3,3,3,
		4,4,4,0,0,3,3,3,
	]

mine_A[16] = [
		120,5,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		1,1,1,3,3,3,3,3,
		3,3,3,3,3,1,1,1,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		1,1,2,5,5,3,3,3,
		3,3,3,5,5,2,1,1,
	]


mine_B = [0 for tbl in range(17)]
mine_B[0] = [6,4]
mine_B[1] = [
		100,8,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		1,1,1,1,1,1,1,1,
		1,2,2,2,2,2,2,1,
		1,2,2,2,2,2,2,1,
		1,2,2,2,2,2,2,1,
		1,1,1,1,1,1,1,1,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		1,2,1,1,1,1,2,1,
		2,4,3,2,2,3,4,2,
		1,4,2,2,2,2,4,1,
		2,4,3,2,2,3,4,2,
		1,2,1,1,1,1,2,1,
	]
	
mine_B[2] = [
		160,6,
		2,2,2,2,3,3,3,1,
		2,2,2,3,3,3,1,1,
		2,2,3,3,3,1,1,1,
		2,3,3,3,1,1,1,2,
		3,3,3,1,1,1,2,2,
		3,3,1,1,1,2,2,2,
		3,1,1,1,2,2,2,3,
		1,1,1,3,3,3,2,2,
		1,1,2,2,2,3,3,3,
		1,2,2,2,3,3,3,3,
		
		4,3,2,2,3,3,3,2,
		3,2,2,3,3,3,2,3,
		2,2,3,3,3,1,1,2,
		2,3,3,3,1,1,1,2,
		3,3,3,1,1,1,2,2,
		3,3,1,1,1,2,2,2,
		3,1,1,1,2,2,2,3,
		2,1,1,2,2,2,3,3,
		3,2,2,2,2,3,3,4,
		2,2,2,2,3,3,4,5,
	]
	
mine_B[3] = [
		80,5,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,4,4,4,4,4,4,
		0,0,4,1,1,1,1,1,
		0,0,4,1,4,5,5,4,
		0,0,4,1,5,5,5,5,
		0,0,4,1,4,5,5,5,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,4,4,4,4,4,5,
		0,0,4,2,1,1,2,3,
		0,0,5,3,5,5,5,5,
		0,0,4,3,5,5,5,5,
		0,0,5,3,5,5,5,5,
	]
	
mine_B[4] = [
		180,14,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		3,3,3,3,3,3,3,3,
		3,3,3,3,3,3,3,3,
		3,3,3,3,3,3,3,3,
		3,3,3,3,3,3,3,3,
		3,3,3,3,3,3,3,3,
		3,3,3,3,3,3,3,3,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		5,5,3,3,3,3,5,5,
		5,5,5,3,3,5,5,5,
		3,5,5,4,4,5,5,3,
		3,4,4,3,3,4,4,3,
		5,5,4,3,3,4,5,5,
		5,5,3,3,3,3,5,5,
	]
	
mine_B[5] = [
		180,14,
		1,1,0,0,0,0,2,2,
		1,1,0,0,0,0,2,2,
		1,1,0,0,0,0,2,2,
		1,1,0,0,0,0,2,2,
		1,1,0,0,0,0,2,2,
		1,1,4,4,4,4,2,2,
		1,1,3,4,4,4,2,2,
		1,1,3,3,4,4,2,2,
		1,1,3,3,3,4,2,2,
		1,1,3,3,3,3,2,2,
		
		3,2,0,0,0,0,3,4,
		2,2,0,0,0,0,3,3,
		2,3,0,0,0,0,4,3,
		2,2,0,0,0,0,3,3,
		3,2,0,0,0,0,3,4,
		2,1,4,4,4,4,2,3,
		1,1,3,4,4,4,2,2,
		1,1,3,3,4,4,2,2,
		1,2,3,3,3,4,3,2,
		2,3,4,3,3,4,4,3,
	]
	
mine_B[6] = [
		70,10,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		2,2,2,2,2,2,2,2,
		1,1,1,1,1,1,1,1,
		2,2,2,2,2,2,2,2,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		3,3,2,3,3,2,3,3,
		4,4,3,4,4,3,4,4,
		3,3,2,3,3,2,3,3,
	]
	
mine_B[7] = [
		90,10,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,1,
		0,0,0,0,0,0,1,2,
		0,0,0,0,0,1,2,1,
		0,0,0,0,1,2,1,2,
		0,0,0,1,2,1,2,1,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,1,
		0,0,0,0,0,0,1,3,
		0,0,0,0,0,1,4,3,
		0,0,0,0,1,4,3,4,
		0,0,0,1,3,3,4,1,
	]
	
mine_B[8] = [
		120,12,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,4,4,4,3,4,4,4,
		0,4,4,3,1,3,4,4,
		0,4,3,1,2,1,3,4,
		0,3,1,2,2,2,1,3,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,4,4,4,4,4,4,4,
		0,4,4,4,3,4,4,4,
		0,4,4,1,4,1,4,4,
		0,4,3,4,4,4,3,4,
	]
	
mine_B[9] = [
		160,16,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		3,2,3,4,4,2,1,2,
		2,2,2,4,4,1,1,1,
		3,2,3,4,4,2,1,2,
		3,2,3,4,4,2,1,2,
		2,2,2,4,4,1,1,1,
		3,2,3,4,4,2,1,2,

		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		5,4,4,4,4,4,4,5,
		5,4,3,4,4,2,3,4,
		4,4,3,4,4,2,3,3,
		3,3,3,4,4,2,2,2,
		3,3,3,4,4,2,2,2,
		4,4,3,4,4,2,3,3,
		5,4,3,4,4,2,3,4,
	]
	
mine_B[10] = [
		200,16,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,2,2,2,2,2,2,0,
		0,2,2,3,3,2,2,0,
		0,2,3,3,3,3,2,0,
		0,2,3,3,3,3,2,0,
		0,2,2,3,3,2,2,0,
		0,2,2,2,2,2,2,0,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,4,4,2,2,4,4,0,
		0,4,4,4,4,4,4,4,
		0,2,4,3,3,4,2,0,
		0,2,4,3,3,4,2,0,
		0,4,4,4,4,4,4,0,
		0,4,4,3,3,4,4,0,
	]
	
mine_B[11] = [
		150,12,
		0,0,0,0,0,0,0,0,
		0,0,0,1,1,0,0,0,
		0,0,1,1,1,1,0,0,
		0,1,1,1,1,1,1,0,
		4,2,2,2,2,2,2,4,
		4,4,2,2,2,2,4,4,
		4,4,4,2,2,4,4,4,
		4,4,4,2,2,4,4,4,
		4,4,2,2,2,2,4,4,
		4,2,2,2,2,2,2,4,
		
		0,0,0,0,0,0,0,0,
		0,0,0,4,4,0,0,0,
		0,0,1,2,2,1,0,0,
		0,3,2,1,1,2,3,0,
		4,3,3,2,2,3,3,4,
		4,5,4,3,3,4,5,4,
		4,4,5,2,2,5,4,4,
		4,4,4,2,2,4,4,4,
		4,5,2,2,2,2,5,4,
		5,4,3,2,2,3,4,5,
	]
	
mine_B[12] = [
		130,10,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		1,3,3,1,1,2,2,1,
		3,1,1,3,2,1,1,2,
		3,1,1,3,2,1,1,2,
		1,3,3,1,1,2,2,1,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		1,3,5,3,2,2,4,3,
		3,3,3,5,2,3,3,4,
		5,3,3,3,4,3,3,2,
		3,5,3,2,3,4,2,1,
	]
	
mine_B[13] = [
		210,12,
		2,2,2,2,1,1,1,1,
		2,2,2,2,1,1,1,1,
		2,2,2,2,1,1,1,1,
		1,1,1,1,2,2,2,2,
		1,1,1,1,2,2,2,2,
		1,1,1,1,2,2,2,2,
		2,2,4,4,3,3,1,1,
		2,2,4,4,3,3,1,1,
		4,4,2,2,1,1,3,3,
		4,4,2,2,1,1,3,3,
		
		4,3,2,2,1,1,1,1,
		3,2,2,2,2,1,1,1,
		2,2,2,4,3,2,1,1,
		1,1,2,3,4,3,3,3,
		1,1,1,2,2,2,2,3,
		2,1,1,1,2,2,3,4,
		4,3,4,4,3,3,2,2,
		3,2,4,4,3,5,3,2,
		4,4,2,3,2,3,5,3,
		4,4,3,4,2,2,3,3,
	]
	
mine_B[14] = [
		180,10,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		4,3,4,3,4,3,4,3,
		2,2,1,2,1,2,1,2,
		2,1,2,1,2,1,2,2,
		3,4,3,4,3,4,3,4,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
		4,4,4,4,4,4,4,4,
	]
	
mine_B[15] = [
		170,12,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,3,3,3,0,0,
		0,0,0,4,4,4,0,0,
		0,0,0,3,3,3,0,0,
		0,0,0,3,2,3,0,0,
		0,0,0,4,4,4,0,0,
		0,0,0,4,3,4,0,0,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
		0,0,0,5,5,5,0,0,
	]
	
mine_B[16] = [
		150,10,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		1,1,1,1,1,1,1,1,
		1,3,2,3,2,3,2,1,
		1,3,2,3,2,3,2,1,
		1,3,2,3,2,3,2,1,
		1,3,2,3,2,3,2,1,
		1,1,1,1,1,1,1,1,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		1,2,1,1,1,1,2,1,
		2,5,3,3,3,4,4,2,
		1,4,2,4,5,4,3,1,
		1,4,2,4,5,4,3,1,
		2,5,3,3,3,4,4,2,
		1,2,1,1,1,1,2,1,
	]
	

mine_C = [0 for tbl in range(17)]
mine_C[0] = [8,6]
mine_C[1] = [
		30,2,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,1,1,0,0,0,
		0,0,1,1,1,1,0,0,
		0,0,1,1,1,1,0,0,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,2,4,0,0,0,
		0,0,2,3,2,1,0,0,
		0,0,1,2,1,1,0,0,
	]
	
mine_C[2] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,3,3,0,0,0,
		0,0,0,1,1,0,0,0,
		0,0,2,1,1,2,0,0,
		0,2,2,1,1,2,2,0,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,3,3,0,0,0,
		0,0,0,1,1,0,0,0,
		0,0,2,1,1,2,0,0,
		0,4,3,1,1,3,4,0,
	]
	
mine_C[3] = [
		30,2,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,1,0,0,0,1,0,
		0,0,5,1,0,1,5,0,
		0,0,5,1,1,1,5,0,
		0,1,5,5,1,5,5,1,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,1,0,0,0,1,0,
		0,0,5,1,0,1,5,0,
		0,0,5,2,3,2,5,0,
		0,1,5,5,2,5,5,1,
	]
	
mine_C[4] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		2,0,0,0,0,0,0,2,
		2,0,0,0,0,0,0,2,
		2,2,0,0,0,0,2,2,
		2,2,1,0,0,1,2,2,
		2,2,1,3,3,1,2,2,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		2,0,0,0,0,0,0,2,
		3,0,0,0,0,0,0,3,
		4,3,0,0,0,0,3,4,
		3,2,1,0,0,1,2,3,
		2,2,1,3,3,1,2,2,
	]
	
mine_C[5] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,2,
		1,3,0,0,0,0,0,1,
		1,1,0,0,0,0,0,1,
		3,1,0,0,0,0,2,3,
		3,2,3,0,0,2,2,3,
		3,2,3,0,1,1,2,3,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		3,0,0,0,0,0,0,2,
		1,3,0,0,0,0,0,1,
		1,1,0,0,0,0,0,2,
		3,2,0,0,0,0,3,5,
		4,4,4,0,0,2,2,4,
		3,3,3,0,1,1,2,3,
	]
	
mine_C[6] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,2,2,0,2,2,0,
		0,0,3,3,2,3,3,0,
		0,0,1,1,3,1,1,0,
		0,0,4,4,1,4,4,0,
		0,0,5,5,4,5,5,0,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,3,2,0,3,2,0,
		0,0,5,4,3,5,4,0,
		0,0,2,1,3,2,5,0,
		0,0,4,4,1,4,4,0,
		0,0,5,5,4,5,5,0,
	]
	
mine_C[7] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,5,0,0,0,0,
		0,0,0,1,0,1,0,0,
		0,0,0,1,0,1,0,0,
		0,0,0,1,0,1,5,0,
		0,0,0,1,5,1,5,0,
		0,0,3,1,3,1,3,5,
		0,1,3,2,3,2,3,5,
		1,1,3,2,3,2,3,5,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,5,0,0,0,0,
		0,0,0,1,0,1,0,0,
		0,0,0,1,0,1,0,0,
		0,0,0,1,0,1,5,0,
		0,0,0,1,5,2,5,0,
		0,0,4,1,4,3,4,5,
		0,2,5,3,3,3,3,5,
		1,1,4,2,3,2,3,5,
	]
	
mine_C[8] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,5,5,0,0,
		0,5,1,1,1,5,0,0,
		0,5,1,1,1,5,5,0,
		5,5,1,2,1,5,5,0,
		5,5,2,2,2,5,5,5,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,5,5,0,0,
		0,5,2,3,2,5,0,0,
		0,5,1,2,1,5,5,0,
		5,5,1,3,1,5,5,0,
		5,5,3,4,3,5,5,5,
	]
	
mine_C[9] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,4,0,0,0,0,0,0,
		0,2,0,0,0,2,0,0,
		2,1,2,0,3,2,3,0,
		5,2,5,4,5,3,5,4,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,4,0,0,0,0,0,0,
		0,3,0,0,0,3,0,0,
		3,3,3,0,4,4,4,0,
		5,3,5,4,5,4,5,4,
	]
	
mine_C[10] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,1,1,1,1,0,0,
		0,0,1,3,3,1,0,0,
		0,0,1,3,3,3,0,0,
		0,0,1,1,1,1,0,0,
		0,0,2,2,2,1,0,0,
		0,0,1,2,2,1,0,0,
		0,0,1,1,1,1,0,0,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,1,2,1,1,0,0,
		0,0,2,5,4,1,0,0,
		0,0,1,4,3,3,0,0,
		0,0,1,1,1,1,0,0,
		0,0,2,2,2,1,0,0,
		0,0,1,2,3,1,0,0,
		0,0,1,2,3,2,0,0,
	]
	
mine_C[11] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,1,0,0,0,0,0,
		0,0,1,0,0,0,0,0,
		0,0,5,0,0,5,0,0,
		0,1,4,0,0,4,0,0,
		0,1,3,1,0,3,0,0,
		5,1,1,1,0,2,0,0,
		5,3,3,4,1,3,4,0,
		5,5,2,1,1,2,5,4,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,1,0,0,0,0,0,
		0,0,1,0,0,0,0,0,
		0,0,5,0,0,5,0,0,
		0,1,4,0,0,4,0,0,
		0,1,3,1,0,3,0,0,
		5,1,2,1,0,2,0,0,
		5,4,5,5,1,3,4,0,
		5,5,3,1,1,2,5,4,
	]
	
mine_C[12] = [
		40,4,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,5,0,0,0,
		0,0,0,0,1,0,0,0,
		0,0,0,0,1,5,0,0,
		0,0,0,0,1,1,0,0,
		0,0,5,1,3,1,0,0,
		0,5,2,2,3,2,1,0,
		5,4,3,4,3,4,3,1,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,5,0,0,0,
		0,0,0,0,1,0,0,0,
		0,0,0,0,2,5,0,0,
		0,0,0,0,3,2,0,0,
		0,0,5,1,4,2,0,0,
		0,5,2,2,4,4,2,0,
		5,4,3,4,3,5,3,1,
	]
	
mine_C[13] = [
		30,2,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,3,0,0,
		0,1,0,0,3,2,1,0,
		4,2,4,0,5,2,5,0,
		3,4,3,0,4,5,4,0,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,4,0,0,
		0,1,0,0,4,4,2,0,
		4,2,4,0,5,3,5,0,
		3,4,3,0,4,5,4,0,
	]
	
mine_C[14] = [
		30,3,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,1,0,
		0,0,0,0,0,0,1,0,
		0,0,2,0,0,0,2,0,
		0,1,3,0,5,0,2,3,
		3,2,4,5,3,1,2,4,
		1,4,1,5,1,4,1,5,
		2,1,2,1,2,1,2,1,
		2,2,2,2,2,2,2,2,

		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,1,0,
		0,0,0,0,0,0,1,0,
		0,0,2,0,0,0,2,0,
		0,0,3,0,5,0,2,3,
		3,1,4,5,3,1,2,4,
		2,3,2,5,1,4,1,5,
		2,2,2,1,2,1,2,1,
		2,2,2,2,2,2,2,2,
	]
	
mine_C[15] = [
		30,2,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,2,0,0,0,0,
		0,0,1,4,1,0,0,0,
		0,2,1,5,1,0,2,0,
		0,1,2,5,1,0,2,1,
		5,2,4,4,4,2,1,1,
		2,4,5,5,5,4,2,1,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,0,0,0,
		0,0,0,2,0,0,0,0,
		0,0,1,4,1,0,0,0,
		0,3,1,5,1,0,2,0,
		0,3,3,5,1,0,2,1,
		5,3,4,4,4,2,1,1,
		2,4,5,5,5,4,2,1,
	]
	
mine_C[16] = [
		30,3,
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,5,0,0,
		0,0,0,0,0,5,0,0,
		0,0,0,0,0,5,5,0,
		0,0,0,0,0,5,5,0,
		0,0,3,0,0,3,5,0,
		0,5,2,3,3,2,5,0,
		0,3,4,2,2,4,3,0,
		4,2,4,2,2,4,2,0,
		5,1,4,1,1,4,1,5,
		
		0,0,0,0,0,0,0,0,
		0,0,0,0,0,5,0,0,
		0,0,0,0,0,5,0,0,
		0,0,0,0,0,5,5,0,
		0,0,0,0,0,5,5,0,
		0,0,3,0,0,3,5,0,
		0,5,2,3,3,2,5,0,
		0,3,4,2,3,4,3,0,
		4,2,4,3,4,5,2,0,
		5,1,4,1,2,4,1,5,
	]
	

mine_D = [0 for tbl in range(17)]
mine_D[0] = [
	]
	
mine_D[1] = [
	]
	
mine_D[2] = [
	]
	
mine_D[3] = [
	]
	
mine_D[4] = [
	]
	
mine_D[5] = [
	]
	
mine_D[6] = [
	]
	
mine_D[7] = [
	]
	
mine_D[8] = [
	]
	
mine_D[9] = [
	]
	
mine_D[10] = [
	]
	
mine_D[11] = [
	]
	
mine_D[12] = [
	]
	
mine_D[13] = [
	]
	
mine_D[14] = [
	]
	
mine_D[15] = [
	]
	
mine_D[16] = [
	]
	

mine_E = [0 for tbl in range(17)]
mine_E[0] = [
	]
	
mine_E[1] = [
	]
	
mine_E[2] = [
	]
	
mine_E[3] = [
	]
	
mine_E[4] = [
	]
	
mine_E[5] = [
	]
	
mine_E[6] = [
	]
	
mine_E[7] = [
	]
	
mine_E[8] = [
	]
	
mine_E[9] = [
	]
	
mine_E[10] = [
	]
	
mine_E[11] = [
	]
	
mine_E[12] = [
	]
	
mine_E[13] = [
	]
	
mine_E[14] = [
	]
	
mine_E[15] = [
	]
	
mine_E[16] = [
	]
	

mine_F = [0 for tbl in range(17)]
mine_F[0] = [
	]
	
mine_F[1] = [
	]
	
mine_F[2] = [
	]
	
mine_F[3] = [
	]
	
mine_F[4] = [
	]
	
mine_F[5] = [
	]
	
mine_F[6] = [
	]
	
mine_F[7] = [
	]
	
mine_F[8] = [
	]
	
mine_F[9] = [
	]
	
mine_F[10] = [
	]
	
mine_F[11] = [
	]
	
mine_F[12] = [
	]
	
mine_F[13] = [
	]
	
mine_F[14] = [
	]
	
mine_F[15] = [
	]
	
mine_F[16] = [
	]
	

mine_G = [0 for tbl in range(17)]
mine_G[0] = [
	]
	
mine_G[1] = [
	]
	
mine_G[2] = [
	]
	
mine_G[3] = [
	]
	
mine_G[4] = [
	]
	
mine_G[5] = [
	]
	
mine_G[6] = [
	]
	
mine_G[7] = [
	]
	
mine_G[8] = [
	]
	
mine_G[9] = [
	]
	
mine_G[10] = [
	]
	
mine_G[11] = [
	]
	
mine_G[12] = [
	]
	
mine_G[13] = [
	]
	
mine_G[14] = [
	]
	
mine_G[15] = [
	]
	
mine_G[16] = [
	]
	

mine_H = [0 for tbl in range(17)]
mine_H[0] = [
	]
	
mine_H[1] = [
	]
	
mine_H[2] = [
	]
	
mine_H[3] = [
	]
	
mine_H[4] = [
	]
	
mine_H[5] = [
	]
	
mine_H[6] = [
	]
	
mine_H[7] = [
	]
	
mine_H[8] = [
	]
	
mine_H[9] = [
	]
	
mine_H[10] = [
	]
	
mine_H[11] = [
	]
	
mine_H[12] = [
	]
	
mine_H[13] = [
	]
	
mine_H[14] = [
	]
	
mine_H[15] = [
	]
	
mine_H[16] = [
	]
	

mine_I = [0 for tbl in range(17)]
mine_I[0] = [
	]
	
mine_I[1] = [
	]
	
mine_I[2] = [
	]
	
mine_I[3] = [
	]
	
mine_I[4] = [
	]
	
mine_I[5] = [
	]
	
mine_I[6] = [
	]
	
mine_I[7] = [
	]
	
mine_I[8] = [
	]
	
mine_I[9] = [
	]
	
mine_I[10] = [
	]
	
mine_I[11] = [
	]
	
mine_I[12] = [
	]
	
mine_I[13] = [
	]
	
mine_I[14] = [
	]
	
mine_I[15] = [
	]
	
mine_I[16] = [
	]
	

mine_J = [0 for tbl in range(17)]
mine_J[0] = [
	]
	
mine_J[1] = [
	]
	
mine_J[2] = [
	]
	
mine_J[3] = [
	]
	
mine_J[4] = [
	]
	
mine_J[5] = [
	]
	
mine_J[6] = [
	]
	
mine_J[7] = [
	]
	
mine_J[8] = [
	]
	
mine_J[9] = [
	]
	
mine_J[10] = [
	]
	
mine_J[11] = [
	]
	
mine_J[12] = [
	]
	
mine_J[13] = [
	]
	
mine_J[14] = [
	]
	
mine_J[15] = [
	]
	
mine_J[16] = [
	]
	

mine_K = [0 for tbl in range(17)]
mine_K[0] = [
	]
	
mine_K[1] = [
	]
	
mine_K[2] = [
	]
	
mine_K[3] = [
	]
	
mine_K[4] = [
	]
	
mine_K[5] = [
	]
	
mine_K[6] = [
	]
	
mine_K[7] = [
	]
	
mine_K[8] = [
	]
	
mine_K[9] = [
	]
	
mine_K[10] = [
	]
	
mine_K[11] = [
	]
	
mine_K[12] = [
	]
	
mine_K[13] = [
	]
	
mine_K[14] = [
	]
	
mine_K[15] = [
	]
	
mine_K[16] = [
	]
	

mine_L = [0 for tbl in range(17)]
mine_L[0] = [
	]
	
mine_L[1] = [
	]
	
mine_L[2] = [
	]
	
mine_L[3] = [
	]
	
mine_L[4] = [
	]
	
mine_L[5] = [
	]
	
mine_L[6] = [
	]
	
mine_L[7] = [
	]
	
mine_L[8] = [
	]
	
mine_L[9] = [
	]
	
mine_L[10] = [
	]
	
mine_L[11] = [
	]
	
mine_L[12] = [
	]
	
mine_L[13] = [
	]
	
mine_L[14] = [
	]
	
mine_L[15] = [
	]
	
mine_L[16] = [
	]
	

mine_M = [0 for tbl in range(17)]
mine_M[0] = [
	]
	
mine_M[1] = [
	]
	
mine_M[2] = [
	]
	
mine_M[3] = [
	]
	
mine_M[4] = [
	]
	
mine_M[5] = [
	]
	
mine_M[6] = [
	]
	
mine_M[7] = [
	]
	
mine_M[8] = [
	]
	
mine_M[9] = [
	]
	
mine_M[10] = [
	]
	
mine_M[11] = [
	]
	
mine_M[12] = [
	]
	
mine_M[13] = [
	]
	
mine_M[14] = [
	]
	
mine_M[15] = [
	]
	
mine_M[16] = [
	]
	

mine_N = [0 for tbl in range(17)]
mine_N[0] = [
	]
	
mine_N[1] = [
	]
	
mine_N[2] = [
	]
	
mine_N[3] = [
	]
	
mine_N[4] = [
	]
	
mine_N[5] = [
	]
	
mine_N[6] = [
	]
	
mine_N[7] = [
	]
	
mine_N[8] = [
	]
	
mine_N[9] = [
	]
	
mine_N[10] = [
	]
	
mine_N[11] = [
	]
	
mine_N[12] = [
	]
	
mine_N[13] = [
	]
	
mine_N[14] = [
	]
	
mine_N[15] = [
	]
	
mine_N[16] = [
	]
	

mine_O = [0 for tbl in range(17)]
mine_O[0] = [
	]
	
mine_O[1] = [
	]
	
mine_O[2] = [
	]
	
mine_O[3] = [
	]
	
mine_O[4] = [
	]
	
mine_O[5] = [
	]
	
mine_O[6] = [
	]
	
mine_O[7] = [
	]
	
mine_O[8] = [
	]
	
mine_O[9] = [
	]
	
mine_O[10] = [
	]
	
mine_O[11] = [
	]
	
mine_O[12] = [
	]
	
mine_O[13] = [
	]
	
mine_O[14] = [
	]
	
mine_O[15] = [
	]
	
mine_O[16] = [
	]
	

mine_P = [0 for tbl in range(17)]
mine_P[0] = [
	]
	
mine_P[1] = [
	]
	
mine_P[2] = [
	]
	
mine_P[3] = [
	]
	
mine_P[4] = [
	]
	
mine_P[5] = [
	]
	
mine_P[6] = [
	]
	
mine_P[7] = [
	]
	
mine_P[8] = [
	]
	
mine_P[9] = [
	]
	
mine_P[10] = [
	]
	
mine_P[11] = [
	]
	
mine_P[12] = [
	]
	
mine_P[13] = [
	]
	
mine_P[14] = [
	]
	
mine_P[15] = [
	]
	
mine_P[16] = [
	]
	

mine_Q = [0 for tbl in range(17)]
mine_Q[0] = [
	]
	
mine_Q[1] = [
	]
	
mine_Q[2] = [
	]
	
mine_Q[3] = [
	]
	
mine_Q[4] = [
	]
	
mine_Q[5] = [
	]
	
mine_Q[6] = [
	]
	
mine_Q[7] = [
	]
	
mine_Q[8] = [
	]
	
mine_Q[9] = [
	]
	
mine_Q[10] = [
	]
	
mine_Q[11] = [
	]
	
mine_Q[12] = [
	]
	
mine_Q[13] = [
	]
	
mine_Q[14] = [
	]
	
mine_Q[15] = [
	]
	
mine_Q[16] = [
	]
	

mine_R = [0 for tbl in range(17)]
mine_R[0] = [
	]
	
mine_R[1] = [
	]
	
mine_R[2] = [
	]
	
mine_R[3] = [
	]
	
mine_R[4] = [
	]
	
mine_R[5] = [
	]
	
mine_R[6] = [
	]
	
mine_R[7] = [
	]
	
mine_R[8] = [
	]
	
mine_R[9] = [
	]
	
mine_R[10] = [
	]
	
mine_R[11] = [
	]
	
mine_R[12] = [
	]
	
mine_R[13] = [
	]
	
mine_R[14] = [
	]
	
mine_R[15] = [
	]
	
mine_R[16] = [
	]
	

mine_S = [0 for tbl in range(17)]
mine_S[0] = [
	]
	
mine_S[1] = [
	]
	
mine_S[2] = [
	]
	
mine_S[3] = [
	]
	
mine_S[4] = [
	]
	
mine_S[5] = [
	]
	
mine_S[6] = [
	]
	
mine_S[7] = [
	]
	
mine_S[8] = [
	]
	
mine_S[9] = [
	]
	
mine_S[10] = [
	]
	
mine_S[11] = [
	]
	
mine_S[12] = [
	]
	
mine_S[13] = [
	]
	
mine_S[14] = [
	]
	
mine_S[15] = [
	]
	
mine_S[16] = [
	]
	

mine_T = [0 for tbl in range(17)]
mine_T[0] = [
	]
	
mine_T[1] = [
	]
	
mine_T[2] = [
	]
	
mine_T[3] = [
	]
	
mine_T[4] = [
	]
	
mine_T[5] = [
	]
	
mine_T[6] = [
	]
	
mine_T[7] = [
	]
	
mine_T[8] = [
	]
	
mine_T[9] = [
	]
	
mine_T[10] = [
	]
	
mine_T[11] = [
	]
	
mine_T[12] = [
	]
	
mine_T[13] = [
	]
	
mine_T[14] = [
	]
	
mine_T[15] = [
	]
	
mine_T[16] = [
	]
	

mine_U = [0 for tbl in range(17)]
mine_U[0] = [
	]
	
mine_U[1] = [
	]
	
mine_U[2] = [
	]
	
mine_U[3] = [
	]
	
mine_U[4] = [
	]
	
mine_U[5] = [
	]
	
mine_U[6] = [
	]
	
mine_U[7] = [
	]
	
mine_U[8] = [
	]
	
mine_U[9] = [
	]
	
mine_U[10] = [
	]
	
mine_U[11] = [
	]
	
mine_U[12] = [
	]
	
mine_U[13] = [
	]
	
mine_U[14] = [
	]
	
mine_U[15] = [
	]
	
mine_U[16] = [
	]
	

mine_V = [0 for tbl in range(17)]
mine_V[0] = [
	]
	
mine_V[1] = [
	]
	
mine_V[2] = [
	]
	
mine_V[3] = [
	]
	
mine_V[4] = [
	]
	
mine_V[5] = [
	]
	
mine_V[6] = [
	]
	
mine_V[7] = [
	]
	
mine_V[8] = [
	]
	
mine_V[9] = [
	]
	
mine_V[10] = [
	]
	
mine_V[11] = [
	]
	
mine_V[12] = [
	]
	
mine_V[13] = [
	]
	
mine_V[14] = [
	]
	
mine_V[15] = [
	]
	
mine_V[16] = [
	]
	

mine_W = [0 for tbl in range(17)]
mine_W[0] = [
	]
	
mine_W[1] = [
	]
	
mine_W[2] = [
	]
	
mine_W[3] = [
	]
	
mine_W[4] = [
	]
	
mine_W[5] = [
	]
	
mine_W[6] = [
	]
	
mine_W[7] = [
	]
	
mine_W[8] = [
	]
	
mine_W[9] = [
	]
	
mine_W[10] = [
	]
	
mine_W[11] = [
	]
	
mine_W[12] = [
	]
	
mine_W[13] = [
	]
	
mine_W[14] = [
	]
	
mine_W[15] = [
	]
	
mine_W[16] = [
	]
	

mine_X = [0 for tbl in range(17)]
mine_X[0] = [
	]
	
mine_X[1] = [
	]
	
mine_X[2] = [
	]
	
mine_X[3] = [
	]
	
mine_X[4] = [
	]
	
mine_X[5] = [
	]
	
mine_X[6] = [
	]
	
mine_X[7] = [
	]
	
mine_X[8] = [
	]
	
mine_X[9] = [
	]
	
mine_X[10] = [
	]
	
mine_X[11] = [
	]
	
mine_X[12] = [
	]
	
mine_X[13] = [
	]
	
mine_X[14] = [
	]
	
mine_X[15] = [
	]
	
mine_X[16] = [
	]
	

mine_Y = [0 for tbl in range(17)]
mine_Y[0] = [
	]
	
mine_Y[1] = [
	]
	
mine_Y[2] = [
	]
	
mine_Y[3] = [
	]
	
mine_Y[4] = [
	]
	
mine_Y[5] = [
	]
	
mine_Y[6] = [
	]
	
mine_Y[7] = [
	]
	
mine_Y[8] = [
	]
	
mine_Y[9] = [
	]
	
mine_Y[10] = [
	]
	
mine_Y[11] = [
	]
	
mine_Y[12] = [
	]
	
mine_Y[13] = [
	]
	
mine_Y[14] = [
	]
	
mine_Y[15] = [
	]
	
mine_Y[16] = [
	]
	

mine_Z = [0 for tbl in range(17)]
mine_Z[0] = [
	]
	
mine_Z[1] = [
	]
	
mine_Z[2] = [
	]
	
mine_Z[3] = [
	]
	
mine_Z[4] = [
	]
	
mine_Z[5] = [
	]
	
mine_Z[6] = [
	]
	
mine_Z[7] = [
	]
	
mine_Z[8] = [
	]
	
mine_Z[9] = [
	]
	
mine_Z[10] = [
	]
	
mine_Z[11] = [
	]
	
mine_Z[12] = [
	]
	
mine_Z[13] = [
	]
	
mine_Z[14] = [
	]
	
mine_Z[15] = [
	]
	
mine_Z[16] = [
	]
	

	
mine_table = [
	mine_A,mine_B,mine_C,mine_D,mine_E,mine_F,mine_G,mine_H,
	mine_I,mine_J,mine_K,mine_L,mine_M,mine_N,mine_O,mine_P,
	mine_Q,mine_R,mine_S,mine_T,mine_U,mine_V,mine_W,mine_X,
	mine_Y,mine_Z ]

