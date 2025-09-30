import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Set style for plots
plt.rcParams['figure.figsize'] = (10,6)
sns.set(style="whitegrid")

# Load the dataset (make sure the CSV is in the same folder)
df = pd.read_csv("netflix1_cleaned.csv", parse_dates=['date_added'])

print("Shape of dataset:", df.shape)
print(df.head())

# 1. Movies vs TV Shows
df['type'].value_counts().plot(kind='bar')
plt.title("Movies vs TV Shows")
plt.ylabel("Count")
plt.show()
#content added by the year
df['year_added'] = df['date_added'].dt.year
df['year_added'].value_counts().sort_index().plot()
plt.title("Content added by year")
plt.xlabel("Year")
plt.ylabel("Number of titles added")
plt.show()
#TOP GENES
df['genres_list'] = df['listed_in'].str.split(', ')
genres = df.explode('genres_list')['genres_list'].value_counts().head(10)
genres.plot(kind='barh')
plt.title("Top genres")
plt.gca().invert_yaxis()
plt.show()
#WORK CLOUD
text = " ".join(df['title'].dropna().tolist())
wc = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()
# Top Countries with most titles
df['countries_list'] = df['country'].str.split(', ')
countries = df.explode('countries_list')['countries_list'].value_counts().head(10)
countries.plot(kind='barh')
plt.title("Top producing countries")
plt.gca().invert_yaxis()
plt.show()
# Ratings Distribution
df['rating'].value_counts().plot(kind='bar')
plt.title("Content by Rating")
plt.xticks(rotation=45)
plt.show()
# Top Directors
top_dirs = df['director'].value_counts().head(10)
top_dirs.plot(kind='barh')
plt.title("Top directors with most titles")
plt.gca().invert_yaxis()
plt.show()
# Movie Duration Distribution
movies = df[df['type'] == "Movie"]
movies['duration_num'] = movies['duration'].str.extract('(\\d+)').astype(float)
movies['duration_num'].dropna().plot(kind='hist', bins=25)
plt.title("Movie duration distribution (minutes)")
plt.xlabel("Minutes")
plt.show()
# Word Cloud of Titles
text = " ".join(df['title'].dropna().tolist())
wc = WordCloud(width=800, height=400, background_color='white').generate(text)
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.show()


