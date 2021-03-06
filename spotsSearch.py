from os import path
import MeCab
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def spotSortByDocuments(chatDoc, spotsData) :
    """
    # spotSortByDocuments
    下記の用に作ってくれると嬉しい
    - param
        - chatDoc
            - type
                - str
            - doc
                - チャットで送られた文章
        - spotsData: List
            - type
                - List
            - doc
                - スポットのデータ
    - ret
        - sotedSpotsData
            - ソートしたスポットのデータ
    """
    
    cos_list = []

    chat_sep  = words_to_sep(chatDoc)
    chat_freq = words_to_freqdict(chat_sep)

    for spot in spotsData:
        spot_sep  = words_to_sep(spot["description"])
        spot_freq = words_to_freqdict(spot_sep)
        spot_cos  = calc_cos(chat_freq, spot_freq)
        cos_list.append( spot_cos )
    sorted_spotsData = sorted(spotsData, key=lambda item: cos_list[spotsData.index(item)], reverse=True)
    return sorted_spotsData

def words_to_sep(text): #分かち書き
    out_words = []
    tagger = MeCab.Tagger('-Ochasen')
    tagger.parse('')
    node = tagger.parseToNode(text)

    while node:
        word_type = node.feature.split(",")[0]
        if word_type in ["名詞"]:
            out_words.append(node.surface)
        node = node.next
    return out_words

def words_to_freqdict(words): #重さつけ的な
    freqdict = {}
    for word in words:
        if word in freqdict:
            freqdict[word] = freqdict[word] + 1
        else:
            freqdict[word] = 1
    return freqdict
	
def calc_cos(dictA, dictB): #cos類似度
    lengthA = 0.0
    for key,value in dictA.items():
        lengthA = lengthA + value*value
    lengthA = math.sqrt(lengthA)

    lengthB = 0.0
    for key,value in dictB.items():
        lengthB = lengthB + value*value
    lengthB = math.sqrt(lengthB)

    dotProduct = 0.0
    for keyA,valueA in dictA.items():
        for keyB,valueB in dictB.items():
            if keyA==keyB:
                dotProduct = dotProduct + valueA*valueB
    if lengthA*lengthB == 0:
        cos = 0
    else:
        cos = dotProduct / (lengthA*lengthB)
    return cos