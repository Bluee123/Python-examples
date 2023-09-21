import nltk
from nltk.corpus import gutenberg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt

# 下载必要的NLTK资源
nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# 加载《白鲸记》
moby_dick = gutenberg.raw('melville-moby_dick.txt')

# 分词
tokens = word_tokenize(moby_dick.lower())  # 转为小写

# 停用词过滤
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]

# 词性标注
pos_tags = pos_tag(filtered_tokens)

# 函数以获取WordNet词性标签
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
    else:
        return nltk.corpus.wordnet.NOUN

# 词形归一化
lemmatizer = WordNetLemmatizer()
top_lemmas = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in pos_tags[:20]]

# 绘制词性频率分布的柱状图
freq_dist = FreqDist(tag for word, tag in pos_tags)
tags, counts = zip(*freq_dist.items())

plt.figure(figsize=(10, 5))
plt.bar(tags, counts)
plt.title('词性频率分布')
plt.xlabel('词性')
plt.ylabel('频率')
plt.show()

# 显示结果
print(f"前5个词性: {FreqDist(tag for word, tag in pos_tags).most_common(5)}")
print(f"前20个词的词形: {top_lemmas}")
