import os
import re
from os import path

import MeCab
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud

mecab = MeCab.Tagger()
mecab.parse('')

stop_words = ['そう', 'ない', 'いる', 'する', 'まま', 'よう',
              'てる', 'なる', 'こと', 'もう', 'いい', 'ある',
              'ゆく', 'れる', 'なっ', 'ちゃっ', 'ちょっ',
              'ちょっ', 'やっ', 'あっ', 'ちゃう', 'その', 'あの',
              'この', 'どの', 'それ', 'あれ', 'これ', 'どれ',
              'から', 'なら', 'だけ', 'じゃあ', 'られ', 'たら', 'のに',
              'って', 'られ', 'ずっ', 'じゃ', 'ちゃ', 'くれ', 'なんて', 'だろ',
              'でしょ', 'せる', 'なれ', 'どう', 'たい', 'けど', 'でも', 'って',
              'まで', 'なく', 'もの', 'ここ', 'どこ', 'そこ', 'さえ', 'なく',
              'たり', 'なり', 'だっ', 'まで', 'ため', 'ながら', 'より', 'られる', 'です']

def text_to_words(text):
    
    words_song = []
    #分解した単語ごとにループする。
    node = mecab.parseToNode(text)
    while node:
        word_type = node.feature.split(",")[0]
        #名詞、形容詞、副詞、動詞の場合のみ追加
        if word_type in ["名詞", "形容詞", "副詞", "動詞"]:
            words_song.append(node.surface.upper())            
        node = node.next
        
    #曲毎の単語の重複を削除して'空白区切のテキストを返す。
    words = ' '.join(set(words_song))
    return words


def extract_words(text,exclusion=[]):
    """
    形態素解析により一般名詞と固有名詞のリストを作成
    ---------------
    Parameters:
        text : str         テキスト
        exclusion : [str]  除外したいワードのリスト
    """
    token = Tokenizer().tokenize(text)
    words = []

    for line in token:
        tkn = re.split('\t|,', str(line))
        # 名詞のみ対象
        if tkn[0] not in exclusion and tkn[1] in ['名詞'] and tkn[2] in ['一般', '固有名詞'] :
            words.append(tkn[0])

    return ' '.join(words)

# get data directory (using getcwd() is needed to support running example in generated IPython notebook)
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# Read the whole text.
t = Tokenizer()
text = ""
with open(path.join(d, 'constitution.txt'), encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        text += text_to_words(line)


# Generate a word cloud image
fpath = "assets/fonts/Noto_Serif_JP/NotoSerifJP-Medium.otf"
wordcloud = WordCloud(
            font_path=fpath,
            # background_color="whitesmoke",
            # colormap="viridis",
            width=1920, 
            height=1080,
            collocations=False,
            stopwords=set(stop_words),
        ).generate(text)

# image = wordcloud.to_image()
# image.show()

wordcloud.to_file("arabic_example.png")
