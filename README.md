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
 - Kaggle https://www.kaggle.com/datasets/marshalll3302/favorite-music-genres-by-country
 - Kaggle https://www.kaggle.com/datasets/conorvaneden/best-songs-on-spotify-for-every-year-2000-2023
 - Github https://github.com/albertyw/avenews/blob/master/old/data/average-latitude-longitude-countries.csv
 - Project Presentation (Google Slides): https://docs.google.com/presentation/d/1TTsX6pZhqfhEHLp71BxxL5VOM0qGY6hbfFOpJ0FSu1Q/edit#slide=id.g2552d193502_2_95

## Languages
 - Python
 - JavaScript
 - JQuery
 - HTML/Jinja
 - CSS

## Python environment requirements:
 - Pandas
 - Flask
 - SQLite
 - render_template
   
## Database testing done in:  
 - pgAdmin 4
 - ERD:
   ![image](https://github.com/TinTesla/Project-3/assets/126313924/459cbdca-ab1a-494e-a131-564a3f42dde1)


## Java Script Libraries Used
- Bootstrap dashboard template(codepen.io)  
- Chart.js(bar, line, doughnut,radar)
- Slick Carousel
- js-tree
- Leaflet.js
- regression-js(for linear regression plots)
- D3
- Plotly
- Plotly_express

## Data Flow of the Project

- Imported csv files from Kaggle resources

- Cleaned csv files (deleted repeats, changed them to the same style)

- Created SQL database using pgAdmin4

- Used SQLite for easy portability with Flask API and dashboard

- Used Bootstrap dashboard template to incorporate an interactive home page



## Analyses

1. Song characteristics vs Popularity
   - On the interactive dashboard clicking on each Year(buttons) takes to series of scatter plots of each song characteristics vs popularity/rating. Here is a snapshot of 2023:
     ![image](https://github.com/TinTesla/Project-3/assets/126313924/7b6f31d4-1ef3-4734-8c87-fdcd3cd93c4e)
     
   - Heatmap was used to determine correlation coefficient between each characteristics and popularity:

     ![image](https://github.com/TinTesla/Project-3/assets/126313924/8ec5760e-8439-4d6f-af05-0abe4e462b28)

   - We did not observe a strong correlation between each characteristics and song popularity/rating, however heatmap data gave us an idea that Liveness, Danceability, Accousticness, Speechiness          and Duration of a song has somewhat positive correlation with popularity of a song, as compared to Bpm , Energy and Valence. Considering data limitations, we believe
     there could be additional factors determining popularity/rating of a song.    
  

2. Spotify song characteristics over time

   #### A:
   - These plots show the mean score for each song characteristic every year (1985-2023). Overlayed is the mean score for       that characteristic over the whole 43 year span. Song characteristics include: Bpm, Energy, Danceability,  dB,Liveness, Valence, Duration (in seconds), Acousticness, Speechiness, & Spotify Rating.    
      In my opinion, the most eye-catching trend is between 1995 and 2000. If you look at the years 1996-1999, you can see a period of sharp decline in the following plots:⋅⋅
  
  BPM,
  Energy
  
  While you can see a distinct rise during that same time period in the following plots:
  
  Speechiness
  
  Acousticness
  
  Our hypothesis is that during the late 1990's the public had a phase where slow, speechy, and acoustic-y songs were highly appreciated and quite popular
  
  ![image](https://github.com/TinTesla/Project-3/assets/126313924/8764e842-64e6-4ad1-b55d-5befd95478cd)

  ![image](https://github.com/TinTesla/Project-3/assets/126313924/5c711817-fc15-41fa-9c06-2de7c8fb48d9)

  

   #### B:
   - The second trend we observed was how the duration of popular songs has slowly decreased over time. From 1999-2002 the average length of song in the top 100 was over 240s (4 minutes), following this is a stable period where song length remains between 220-240s (3.5-4 min). However, after 2016, things begin to change; by 2019 the mean song length is 200s and by 2023 it drops down to 192s which equates to 3min, 9s per song.
At the peak, songs were averaging 250s and by 2023 they have dropped to ~190s. This is close to a full minute shorter. Our hypothesis is that as everyday technology consumption has grown exponentially since 2000, along with the shortening of attention-spans and increase in screen time, musicians have been encouraged to produce shorter and shorter tracks. There is a lot of competition for attention these days and it could be considered risky to create longer tracks as it is more time for a listener to skip or move on to the next thing.
After running a linear regression, the difference in values is statistically significant (p-value < 0.001). Duration decreases, on average, by ~2s per year.
  - 
 
3. Artists and their Songs over Time

By counting the number of times an artist’s name appears on the charts over the years, we found the top 40 popular artists and put them in a list.
In the dataset, there are some song titles that are duplicated, but they have different values in the other columns (such as Spotify ratings). These are the songs that have stayed on the charts for more than one year; we put them into a list.
Another question that interested us is who has the most songs that have stayed on the charts for more than one year. With the list of songs that stayed on the charts for more than one year, we were able to pull all the artist names for those songs, and count the frequency an artist’s name appears.

![Project 3 Top 40](https://github.com/TinTesla/Project-3/assets/126445425/a4dc600e-1a67-4c4c-9612-63de99015a3e)

![Project 3 Top 15 Artists with Multiple Songs that Stayed on the Charts for More than One Year](https://github.com/TinTesla/Project-3/assets/126445425/27e96e7c-d5c1-4cff-bb65-4561e067837d)

### Dashboard interactiveness: 
  - run web.py(flask API)  either in vscode or pycharm in a python environment that has flask,pandas, render_template modules.

    
### references:

- chart.js
  - bar chart: 
    - https://www.chartjs.org/docs/latest/getting-started/
    - https://www.chartjs.org/docs/latest/charts/bar.html
    - CDN : <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  - radar chart: 
    - https://www.chartjs.org/docs/latest/charts/radar.html
  - doughnut:
    - https://www.chartjs.org/docs/latest/charts/doughnut.html#doughnut
   
- Stamen toner leaflet.js plugin for maps:
  - https://stackoverflow.com/questions/48874337/how-to-use-leaflet-js-plugin-with-stamen-maps
  - https://leafletjs.com/examples/quick-start/
 
- flag icons
  - https://flagpedia.net/download/api
 
- bootstrap dashboard example
  - https://codepen.io/NolWag/pen/LzdOmb
  - https://getbootstrap.com/docs/4.0/components/buttons/

- css tutorial: 
  - https://www.w3schools.com/css/
 
- jquery tutorial:
  - https://www.w3schools.com/jquery/default.asp
 
- slick carousel:
  - https://alvarotrigo.com/blog/jquery-carousel/
  - https://github.com/kenwheeler/slick
 
- js-tree, jquery plugin: 
  - https://www.jstree.com/
  - <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jstree/3.2.1/themes/default/style.min.css" />
  
- regression-js
  - https://tom-alexander.github.io/regression-js/
  - how to use- https://github.com/Tom-Alexander/regression-js
  - CDN: https://cdnjs.com/libraries/regression

- random color generator:
  - https://stackoverflow.com/questions/20553036/random-color-in-jquery
 
- for icons: 
 - https://icons8.com/

- https://www.w3schools.com/html/   
  
