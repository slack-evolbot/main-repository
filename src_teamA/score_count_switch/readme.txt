���Y�p�C�W���p�́A�X�C�b�`�����񐔃J�E���g�p�v���O�����B
�ꎞ�I���p�̂��ߎ菇�͈ȉ��ȈՎ菇���Ƃ��ċL���B

�O�D�T�v
	�X�C�b�`A,B,C,D���ꂼ�ꉟ���ꂽ�񐔂��J�E���g�����Y�p�C��DB��ɕێ�����B
	�񐔂̓f�B�X�v���C��ɕ\������B
	�X�C�b�`E�͑��X�C�b�`���͎�����щ񐔃��Z�b�g���ɗ��p����B

�P�D���Y�p�C-�X�C�b�`�ڑ�
	�e�X�C�b�`�ɑ΂��āA�u���b�h�{�[�h����Ĉȉ���ڑ��B
	�E3.3V
	�E�Ή�GPIO�iA�FGPIO4, B�FGPIO17, C�FGPIO27, D�FGPIO22, E�FGPIO26�j

�Q�D���Y�p�C-�f�B�X�v���C�ڑ�
	�ȉ��̒ʂ�ɐڑ��B
	�EVCC�F5V
	�ESDA�FGPIO2
	�ESCL�FGPIO3
	�EGND�FGND
	��5V�Ȃ̂ŗv����

�R�D�e�[�u���쐬
	�ȉ�2�̃e�[�u���ƃf�[�^���쐬����B
	score�F�e�`�[���̌���̃X�R�A�i�����񐔁j��ێ�����e�[�u���B
	score_history�F�e�`�[���̃X�R�A�����Z���ꂽ�^�C�~���O��ێ�����e�[�u���B

	��SQL��
		create table raspberry.score(group_id varchar(10) NOT NULL PRIMARY KEY, group_name varchar(10), score int)
		create table raspberry.score_history(group_id varchar(10), update_time datetime)
		insert into raspberry.score(group_id, group_name, score) values('A','A', 0);
		insert into raspberry.score(group_id, group_name, score) values('B','B', 0);
		insert into raspberry.score(group_id, group_name, score) values('C','C', 0);
		insert into raspberry.score(group_id, group_name, score) values('D','D', 0);
		���`�[�����͒P����A,B,C,D�Ƃ��Ă��邪�A����group_name�ɉ����ăf�B�X�v���C��ɕ\�������`�[�������ς��B

�S�D�v���O����
	�Egit clone �� score_count_switch �f�B���N�g�����N���[���B
	�Emain.py �����s�B

�T�D���p���@
	���N������
		�E�N����A�����ꂩ�̃X�C�b�`������
			�e�`�[���̌��݂̉񐔂�\�����A���͑҂���ԂƂȂ�B
	���񐔉��Z��
		�E�X�C�b�`E������
			�X�C�b�`�i�`�[���j�I����ԂƂȂ�B
		�E�X�C�b�`A�`D�̂����ꂩ������
			���������X�C�b�`�̉񐔂�1���������B
	���񐔃��Z�b�g��
		�E�X�C�b�`E��2�񉟉�
			���Z�b�g�m�F��ԂƂȂ�B
		�E�X�C�b�`A������
			�񐔂��I�[��0�Ƀ��Z�b�g�����B
			�����̃X�C�b�`����������ƃ��Z�b�g���L�����Z������B
