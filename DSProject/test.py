import jieba
from wordcloud import WordCloud, ImageColorGenerator
from matplotlib import pyplot as plt
import pandas as pd


def create_wordcloud(df):
    # 分词
    text = ''
    for line in df['name']:
        text += ' '.join(jieba.cut(line, cut_all=False))
        text += ' '
    backgroud_Image = plt.imread('rocket.jpg')

    wc = WordCloud(
        background_color='white',
        mask=backgroud_Image,
        font_path='font_demo.ttf',
        max_words=1000,
        max_font_size=150,
        min_font_size=15,
        prefer_horizontal=1,
        random_state=50,
    )
    wc.generate_from_text(text)
    img_colors = ImageColorGenerator(backgroud_Image)
    wc.recolor(color_func=img_colors)
    # 看看词频高的有哪些
    process_word = WordCloud.process_text(wc, text)
    sort = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    print(sort[:50])
    plt.imshow(wc)
    plt.axis('off')
    wc.to_file("中国校名词云.jpg")


df = pd.read_csv("college_data.csv")

# 去除大学
df_name = df['name'].str.replace('大学', '')
dict_name = {'name': df_name.values, 'numbers': df_name.index}
df_name = pd.DataFrame(dict_name)

# 去除学院
df_name = df_name['name'].str.replace('学院', '')
dict_name = {'name': df_name.values, 'numbers': df_name.index}
df_name = pd.DataFrame(dict_name)

# 去除专科学校
df_name = df_name['name'].str.replace('专科学校', '')
dict_name = {'name': df_name.values, 'numbers': df_name.index}
df_name = pd.DataFrame(dict_name)

df = pd.read_csv("college_data.csv")
df_new = df.drop_duplicates(subset=['name'])
df_site = df_new[df_new['site'] != '——']
df_site = df_site[df_site['site'] != '------']
site_counts = df_site['site'].value_counts()
dict_site = {'name': site_counts.index, 'counts': site_counts.values}
for city in site_counts.index:
    df_name = df_name['name'].str.replace(city, '')
    dict_name = {'name': df_name.values, 'numbers': df_name.index}
    df_name = pd.DataFrame(dict_name)


# 生成校名词云图
create_wordcloud(df_name)