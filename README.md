# Project 3
 Group Project 3 - Music Analyis + Dashboard

# Music Analysis + Dashboard

## Description
For this project, we analyzed a dataset of the top 100 songs every year (2000 – 2023) and built an interactive dashboard with our analysis. We looked into:
1.    Song characteristics and their popularity,
2.    Songs that stayed on the charts for more than one year,
3.    Artists who made onto the charts most over the years, and
4.    Artists who have most songs that stayed on the charts for more than one year.
On our interactive dashboard, we visualized our analysis by graphs.

## Team Members
Bijoyeta Kayal, Crimson Amaro, Emma Ng, Ryan Kincheloe, Stelios Kosmidis, and Tristan Marcum

## Data Sources
-         Kaggle https://www.kaggle.com/datasets/marshalll3302/favorite-music-genres-by-country
-         Kaggle https://www.kaggle.com/datasets/conorvaneden/best-songs-on-spotify-for-every-year-2000-2023
-         Github https://github.com/albertyw/avenews/blob/master/old/data/average-latitude-longitude-countries.csv
-         Project Presentation (Google Slides): https://docs.google.com/presentation/d/1TTsX6pZhqfhEHLp71BxxL5VOM0qGY6hbfFOpJ0FSu1Q/edit#slide=id.g2552d193502_2_95

## Languages
- Python
- JavaScript
- HTML
- CSS

## Software Used
- Flask
- Jupyter notebook
- SQLite
- pgAdmin 4

## Java Script Libraries Used
- Chart.js
- Slick Carousel
- Jquery
- D3
- Plotly

## Data Flow of the Project

- Imported csv files from Kaggle resources

- Cleaned csv files (deleted repeats, changed them to the same style)

- Created SQL database using pgAdmin4

- Used SQLite to create a database that was able to interact with Flask

- Used Bootstrap to incorporate an interactive home page

-


## Analyses

1.

2. Spotify song characteristics over time

- A.
These plots show the mean score for each song characteristic every year (1985-2023). Overlayed is the mean score for that characteristic over the whole 43 year span. Song characteristics include: Bpm, Energy, Danceability, dB, Liveness, Valence, Duration (in seconds), Acousticness, Speechiness, & Spotify Rating.
In my opinion, the most eye-catching trend is between 1995 and 2000. If you look at the years 1996-1999, you can see a period of sharp decline in the following plots:⋅⋅

BPM,
Energy

While you can see a distinct rise during that same time period in the following plots:

Speechiness

Acousticness

Our hypothesis is that during the late 1990's the public had a phase where slow, speechy, and acoustic-y songs were highly appreciated and quite popular
- B.
The second trend we observed was how the duration of popular songs has slowly decreased over time. From 1999-2002 the average length of song in the top 100 was over 240s (4 minutes), following this is a stable period where song length remains between 220-240s (3.5-4 min). However, after 2016, things begin to change; by 2019 the mean song length is 200s and by 2023 it drops down to 192s which equates to 3min, 9s per song.
At the peak, songs were averaging 250s and by 2023 they have dropped to ~190s. This is close to a full minute shorter. Our hypothesis is that as everyday technology consumption has grown exponentially since 2000, along with the shortening of attention-spans and increase in screen time, musicians have been encouraged to produce shorter and shorter tracks. There is a lot of competition for attention these days and it could be considered risky to create longer tracks as it is more time for a listener to skip or move on to the next thing.
After running a linear regression, the difference in values is statistically significant (p-value < 0.001). Duration decreases, on average, by ~2s per year.

3. Artists and their Songs over Time

By counting the number of times an artist’s name appears on the charts over the years, we found the top 40 popular artists and put them in a list.
In the dataset, there are some song titles that are duplicated, but they have different values in the other columns (such as Spotify ratings). These are the songs that have stayed on the charts for more than one year; we put them into a list.
Another question that interested us is who has the most songs that have stayed on the charts for more than one year. With the list of songs that stayed on the charts for more than one year, we were able to pull all the artist names for those songs, and count the frequency an artist’s name appears.

![Project 3 Top 40](https://github.com/TinTesla/Project-3/assets/126445425/a4dc600e-1a67-4c4c-9612-63de99015a3e)

![Project 3 Top 15 Artists with Multiple Songs that Stayed on the Charts for More than One Year](https://github.com/TinTesla/Project-3/assets/126445425/27e96e7c-d5c1-4cff-bb65-4561e067837d)
