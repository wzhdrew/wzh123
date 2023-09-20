import nltk
from nltk.corpus import gutenberg
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt

# 下载停止词和标记数据
nltk.download('stopwords')
nltk.download('punkt')

# 读取白鲸记文本
whale_text = gutenberg.raw('Moby Dick.txt')

# 将文本标记化（分成单词）
tokens = word_tokenize(whale_text)

# 过滤停止词
stop_words = set(stopwords.words('english'))
filtered_tokens = [word.lower() for word in tokens if word.isalnum() and word.lower() not in stop_words]

# 词性标记
pos_tags = nltk.pos_tag(filtered_tokens)

# 统计词性
pos_freq = FreqDist(tag for (word, tag) in pos_tags)

# 获取前5个最常见的词性
top_pos = pos_freq.most_common(5)

# 词根化
stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(word) for word in filtered_tokens]

# 绘制频率分布
plt.figure(figsize=(10, 6))
pos_freq.plot(20, title='Frequency Distribution of POS Tags')
plt.show()

# 输出结果
print("Top 5 POS Tags and Their Frequencies:")
for tag, freq in top_pos:
    print(f"{tag}: {freq}")

print("\nSample of Stemmed Tokens:")
print(stemmed_tokens[:20])
