from janome.tokenizer import Tokenizer
t = Tokenizer()
tokens = t.tokenize("AIに脅かされないために、AIを作る側の人間になる")
for token in tokens:
        if token.part_of_speech.split(',')[0] == '名詞':
                if token.part_of_speech.split(',')[1] == '一般':
                        if token.base_form == '*':
                                print(token.surface)
                        else:
                                print(token.base_form)

        
        elif token.part_of_speech.split(',')[0] == '動詞':
                if token.part_of_speech.split(',')[1] == '自立':
                        if token.base_form == '*':
                                print(token.surface)
                        else:
                                print(token.base_form)

        elif token.part_of_speech.split(',')[0] == '助詞' or token.part_of_speech.split(',')[0] == '助動詞':
                if token.base_form == '*':
                        print(token.surface)
                else:
                        print(token.base_form)
