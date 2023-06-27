import pandas as pd
import json
import sqlite3

app_config_file = "config/config.json"
app_config = {}
app_data_path = None
genre_by_country_file = None
spotify_data_file = None
countries_file = None
db_filename = None

with open(app_config_file,"r") as configobj:
    app_config = json.load(configobj)
    app_data_path = app_config.get("appdataDirectory")
    genre_by_country_file = app_config.get("Genres_by_country_filename")
    spotify_data_file = app_config.get("Spotify_data_filename")
    countries_file = app_config.get("Countries_lat_lng")
    db_path = app_config.get("db_path")
    db_filename = app_config.get("db_filename")
    db_filename = "{0}/{1}".format(db_path,db_filename)

conn = sqlite3.connect(db_filename)

def importCountries():
    filepath = "{0}/{1}".format(app_data_path, countries_file)
    df = pd.read_csv(filepath, sep=",")
    df["ID"] = df["Country"]
    df["ID"] = df["ID"].apply(lambda x: x.lower().replace(" ", "_"))
    df["Country"] = df["ID"]
    countries_df = df[["CountryCode","Country","Latitude","Longitude"]]
    countries_df.to_sql(name="countries",con=conn,if_exists="replace",index=False)



def generateID(text):
    return str(abs(hash(text)))

def importSpotifyData():
    filepath = "{0}/{1}".format(app_data_path, spotify_data_file)
    raw_spotify_data_df = pd.read_csv(filepath, sep=";")
    raw_spotify_data_df["Artist_ID"] = raw_spotify_data_df["Artist"].apply(generateID)
    artist_df = raw_spotify_data_df[["Artist_ID","Artist"]].drop_duplicates()
    artist_df.to_sql(name="artists", con=conn, if_exists="replace", index=False)
    raw_spotify_data_df.to_sql(name="spotify_data",con=conn,if_exists="replace",index=False)

def importCountriesbyGenreData():
    filepath = "{0}/{1}".format(app_data_path, genre_by_country_file)
    genre_countries_df = pd.read_csv(filepath, sep=",")
    genre_countries_df.to_sql(name="country_genres_data",con=conn,if_exists="replace",index=False)



importCountries()
importSpotifyData()
importCountriesbyGenreData()

