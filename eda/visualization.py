import matplotlib.pyplot as plt
from wordcloud import WordCloud


def make_wordcloud(corpus, collocations=True, stopwords=None):
    wrd = WordCloud(
        background_color="white",
        width=700,
        height=500,
        margin=0,
        collocations=collocations,
        max_words=15,
        colormap="winter",
        stopwords=stopwords,
    )
    wordcloud = wrd.generate(corpus)
    plt.figure(figsize=(14, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
