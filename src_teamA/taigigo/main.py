# coding: utf-8
#下記ページを参考に1ファイルにまとめたもの。
#https://qiita.com/youwht/items/f21325ff62603e8664e6
#※ほぼコピペだが上記ページには一部間違いあり修正している

from gensim.models.word2vec import Word2Vec
import gensim
import MeCab
import random
import pandas as pd

#作成済みのモデルをロード
def load_model():
    modelW_path = './word2vec.gensim.model'
    return Word2Vec.load(modelW_path)

model = load_model()

#対義語リストを作成
def create_taigigo_df():
    #対義語一覧のCSV
    df = pd.read_csv('./Taigigolist.csv')
    # dfと全く同じものを作成。コレに逆にしたデータを追加する。
    df2 = pd.DataFrame(index=[], columns = df.columns)

    for index, rows in df.iterrows():
        series = pd.Series([rows[1], rows[0]], index = df2.columns )
        df2 = df2.append(series, ignore_index = True)

    return df2.reset_index(drop=True)

df_alltaigigo = create_taigigo_df()

# 対義語データ内で、辞書データにあるもののみを抜粋＆再構築
def create_filterd_taigigo_list(input_word):
    # 空のデータフレームを生成する。
    df_alltaigigo_filterd = pd.DataFrame(index=[], columns = ["org","taigigo","sim_inp_org","sim_inp_tai","sim_org_tai"])
    for index, rows in df_alltaigigo.iterrows():
        #データフレームごとの列のクラスは、pd.Seriesを用いる
        try:
            #それぞれの単語の間の類似度を表示する
            sim_INP_ORG = model.similarity(input_word, rows[0]) #input_wordと対義語一覧の1つめの類似度
            sim_INP_TAI = model.similarity(input_word, rows[1]) #input_wordと対義語一覧の2つめの類似度
            sim_ORG_TAI = model.similarity(rows[0], rows[1]) #対義語一覧の1つめと2つめの類似度
        except:
            #キーエラーが発生する場合は採用しない。
            #Word2Vecの辞書に無い用語が出てくるとエラーになるために、このエラー処理は重要。
            continue

        #エラーが無い場合は処理を継続して以下を実施        
        series = pd.Series([rows[0], rows[1], sim_INP_ORG, sim_INP_TAI, sim_ORG_TAI], index = df_alltaigigo_filterd.columns )

        df_alltaigigo_filterd = df_alltaigigo_filterd.append(series, ignore_index = True)
    return df_alltaigigo_filterd

#対義語リストのソート
df_alltaigigo_filterd = create_filterd_taigigo_list("コアラ")
df_alltaigigo_filterd = df_alltaigigo_filterd.sort_values(by='sim_inp_org', ascending=False)

#対象語句の品詞を取得
def check_hinsi(taisyou_word):
    mecab = MeCab.Tagger("-Ochasen")
    WordHinsi = []
    #前処理：トリムなど。例「\t」はトリムしておく。全角スペース化
    trline = taisyou_word.replace(u'\t', u'　')

    #Mecabでの解析を実施
    parsed_line = mecab.parse(trline)

    #分析結果を、１行（単語）ごとに分割する。改行コードで分割する。
    wordsinfo_list = parsed_line.split('\n')
    #状況を見る場合はコメント解除
    #print(taisyou_word+"は"+str(len(wordsinfo_list))+"単語に分かれました")

    #単語ごとに、解析処理に入れていく。
    for wordsinfo in wordsinfo_list:
        #print("wordsinfo= " + wordsinfo)
        # 各単語の情報をタブで分割する。
        # たき火,タキビ,たき火,名詞-一般 などのような１行が、list形式になる。
        info_list = wordsinfo.split('\t')
        #print(info_list)

        #空白などの場合、三番目の要素が無い場合もあるため、
        #最初にそのリストの長さをチェック
        #以下のように無意味に３分割されるため、品詞情報が存在しないものは無視する。
        #['コアラ', 'コアラ', 'コアラ', '名詞-一般', '', '']
        #['EOS']
        #['']
        if(len(info_list)>2):
            WordHinsi.append((info_list[0], info_list[3]))

    return WordHinsi
    
#特定の単語の中から似ているものを選び、順番に並べる
def most_niteiru(input_word, entries_list):
    similarities = [model.similarity(input_word, entry) for entry in entries_list]
    results = [[similarity, entry] for (entry, similarity) in zip(entries_list, similarities)]
    return sorted(results, reverse=True)

#対象語句の対義語リストを取得する
def get_natural_taigigo_NEO(input_word, input_hinsi):
    FinalKouhoList = []
    for index, rows in df_alltaigigo_filterd.iterrows():
        # input_word +  rows['taigigo'] - rows['org']　のWord2Vecの演算を実施する。
        # つまり、「入力語」 + 「入力語に似ている言葉の対義語」 - 「入力語に似ている言葉」
        #★トップいくつまで取得するかは重要なチューニングパラメータ
        enzan_kekka_list = model.most_similar(positive = [input_word, rows['taigigo']], negative=[rows['org']], topn=15)
        KouhoList = []

        #似ている語句の上位から順番にfor文に入れていく。
        for enzan_kekka in enzan_kekka_list:
            #複数語判定＆品詞判定の関数に入れる
            enzan_kekka_hinsi_list = check_hinsi(enzan_kekka[0])
            # 以下のような結果が返ってくる
            # [('多摩', '名詞-固有名詞-地域-一般'), ('動物', '名詞-一般'), ('公園', '名詞-一般')]

            #品詞リストを作成時に、複数に分かれた場合、そもそも一語ではないのでNG⇒長さが１の時だけ処理を継続
            #多摩動物公園は長さが３なので無視されるというワケ
            if( len(enzan_kekka_hinsi_list) == 1 ):
                #品詞チェックは、冒頭の２文字まで一致していればOKとする
                #（名詞～～のあとはあまり気にしない）
                # 厳密にチェックする場合 ⇒ if(input_hinsi == enzan_kekka_hinsi_list[0][1]):
                if(input_hinsi[:2] == enzan_kekka_hinsi_list[0][1][:2]):
                    #品詞も一致したため、候補に登録する。
                    KouhoList.append(enzan_kekka_hinsi_list[0][0])

        #候補リストが作られていて、２個以上あれば、その上位２個を取得する。（リストが作られない場合もあるよ。）
        #一個しかない場合、もともとイマイチなリストであったため、取得は避ける。
        if( len(KouhoList)>1 ):
            #途中経過（上位で取得したキーワード）を見る場合コメントを外す。
            #print(KouhoList)

            #おおもとの候補リストへ追加。
            FinalKouhoList.append( KouhoList[0] )
            FinalKouhoList.append( KouhoList[1] )

        #一定量のおおもとの候補がたまったら、全部検索する必要はないため、全文ループを修了する。
        #★いくつの候補まで取得するかは重要なチューニングパラメータ
        if(len(FinalKouhoList) > 10):
            break

    #もし、何も入っていない場合は、もとのキーワードを入れておく(変換しないので。)
    if(len(FinalKouhoList)<1):
        FinalKouhoList.append( input_word )

    #同じ言葉が何度も入る場合もあるため、作成したリストから、重複を除去する。
    #print(FinalKouhoList)
    FinalKouhoList_unique = list(set(FinalKouhoList))

    #候補リストの中から、最もINPUTに似たワードから並ぶように並び替えを行う。
    #上位N件を抽出する。(あまり下位を取得しても意味がないため、ある程度絞る)
    nita_word_list = most_niteiru(input_word, FinalKouhoList_unique)[:5]
    return nita_word_list

#対義語の文章を取得する
def get_Taigigo_bun(inputtext):
    mecab = MeCab.Tagger("-Ochasen")
    #語彙が多すぎる辞書を使うと、対義語にしたいワードが
    #一語と認識されてしまう場合が増えてしまうので、あえて辞書は使わない
    #mecab = MeCab.Tagger(r"-Ochasen -d .\mecab-ipadic-neologd")

    resulttext = ""

    #前処理：トリムなど。例「\t」はトリムして全角スペース化
    trline = inputtext.replace(u'\t', u'　')

    #####メイン処理：
    #Mecabでの解析を実施
    parsed_line = mecab.parse(trline)

    #途中経過を見てみる場合は以下のprintで。
    #parse結果は、改行区切りで全単語の品詞情報が格納されている。
    #分析結果を、１行（単語）ごとに分割する。改行コードで分割する。
    wordsinfo_list = parsed_line.split('\n')

    #単語ごとに、解析処理に入れていく。
    for wordsinfo in wordsinfo_list:
        #print("wordsinfo= " + wordsinfo)

        # 各単語の情報をタブで分割する。
        # たき火,タキビ,たき火,名詞-一般 などのような１行をlist形式にして要素を取り出せるように。
        info_list = wordsinfo.split('\t')

        #空白などの場合、三番目の要素が無い場合もあるため、
        #最初に、出来たリストの長さをチェック
        if(len(info_list)>2):
            #一部の品詞や、一部の例外単語は、変換処理を実施しない。
            if( info_list[3].startswith('助詞') or 
                info_list[3].startswith('副詞-助詞類接続') or
                info_list[3].startswith('名詞-特殊-助動詞語幹') or
                info_list[3].startswith('フィラー') or
                info_list[3].startswith('動詞-接尾') or
                info_list[3].startswith('記号') or
                info_list[3].startswith('接頭詞') or
                info_list[3].startswith('助動詞') or
                info_list[0]==u'の'
                ):
                    #上記パターンは、何もしない
                    resulttext+=info_list[0]
            else :
                #動詞の場合、原型に対して対義語を取るか、元々の入力に対して対義語を取るか２通りある。
                #どうせ対義語化するときに変換はずれるため、多少のずれは無視して原型を対象とする。
                #（動詞以外は、原型も元々の入力も変わらないはずなので影響しない）
                #元々の入力を使う場合
                word = info_list[0]
                #原型を使う場合
                #word = info_list[2]

                #品詞を保存する
                word_hinsi = info_list[3]

                try:
                    #キーワードが辞書に入っているか確認する。
                    #中のベクトルそのものを出す。（なければエラーに）
                    out = model[word]

                    #以下で、別途作成の、単語⇒対義語のリスト、返す関数を呼び出す
                    taigigo_kouho_list = get_natural_taigigo_NEO(word, word_hinsi)
                    
                    #乱数でそのなかから一語を選ぶ
                    taigigo = random.choice(taigigo_kouho_list)[1]
                    resulttext += taigigo

                except KeyError:
                    # モデル内にキーワードが無い場合
                    #　全体をエラーにさせないため、とりあえず元の言葉を入れておく   
                    resulttext += word
    return resulttext

#上記の関数は、ランダムで一つを返すため、任意の回数繰り返したり、
#デバッグ用に表示する関数をつけておく。
def get_Taigigo_bun_kurikaesi(input_bun, kurikaesi):
    print(input_bun)
    print("== 結果 ==")
    for i in range(kurikaesi):
        print(get_Taigigo_bun(input_bun))

if __name__ == "__main__":
    while True:
        text = input("何を対義語にしますか>")
        #引数に入れた文章の対義語文章を5つ作成する
        get_Taigigo_bun_kurikaesi(text,3)
