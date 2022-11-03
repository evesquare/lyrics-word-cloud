import os
import re
from os import path

import MeCab
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud


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
        text += extract_words(line)


# Generate a word cloud image
fpath = "assets/fonts/Noto_Sans_JP/NotoSansJP-Medium.otf"
wordcloud = WordCloud(
            font_path=fpath,
            # background_color="whitesmoke",
            # colormap="viridis",
            width=1000, 
            height=540
        ).generate(text)

# image = wordcloud.to_image()
# image.show()

wordcloud.to_file("arabic_example.png")
