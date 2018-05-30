ラズパイ展示用の、スイッチ押下回数カウント用プログラム。
一時的利用のため手順は以下簡易手順書として記す。

０．概要
	スイッチA,B,C,Dそれぞれ押された回数をカウントしラズパイのDB上に保持する。
	回数はディスプレイ上に表示する。
	スイッチEは他スイッチ入力時および回数リセット時に利用する。

１．ラズパイ-スイッチ接続
	各スイッチに対して、ブレッドボードを介して以下を接続。
	・3.3V
	・対応GPIO（A：GPIO4, B：GPIO17, C：GPIO27, D：GPIO22, E：GPIO26）

２．ラズパイ-ディスプレイ接続
	以下の通りに接続。
	・VCC：5V
	・SDA：GPIO2
	・SCL：GPIO3
	・GND：GND
	※5Vなので要注意

３．テーブル作成
	以下2つのテーブルとデータを作成する。
	score：各チームの現状のスコア（押下回数）を保持するテーブル。
	score_history：各チームのスコアが加算されたタイミングを保持するテーブル。

	＜SQL＞
		create table raspberry.score(group_id varchar(10) NOT NULL PRIMARY KEY, group_name varchar(10), score int)
		create table raspberry.score_history(group_id varchar(10), update_time datetime)
		insert into raspberry.score(group_id, group_name, score) values('A','A', 0);
		insert into raspberry.score(group_id, group_name, score) values('B','B', 0);
		insert into raspberry.score(group_id, group_name, score) values('C','C', 0);
		insert into raspberry.score(group_id, group_name, score) values('D','D', 0);
		※チーム名は単純にA,B,C,Dとしているが、このgroup_nameに応じてディスプレイ上に表示されるチーム名が変わる。

４．プログラム
	・git clone で score_count_switch ディレクトリをクローン。
	・main.py を実行。

５．利用方法
	＜起動時＞
		・起動後、いずれかのスイッチを押下
			各チームの現在の回数を表示し、入力待ち状態となる。
	＜回数加算＞
		・スイッチEを押下
			スイッチ（チーム）選択状態となる。
		・スイッチA～Dのいずれかを押下
			押下したスイッチの回数が1増加される。
	＜回数リセット＞
		・スイッチEを2回押下
			リセット確認状態となる。
		・スイッチAを押下
			回数がオール0にリセットされる。
			※他のスイッチを押下するとリセットをキャンセルする。
