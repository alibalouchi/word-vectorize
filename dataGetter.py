import urllib.request
import csv
import json


def array_crawler(array):
        res = []
        for item in array:
            res.append(item["name"])
        return (";".join(res))

def data_getter(endId, csv_file, url, api_key):
    movieId = 270
    csv_file = csv.writer(open(csv_file, mode="w"))
    csv_file.writerow([
        "adult",
        "backdrop_path",
        "belongs_to_collection",
        "budget",
        "genres",
        "homepage",
        "id",
        "imdb_id",
        "original_language",
        "original_title",
        "overview",
        "popularity",
        "poster_path",
        "production_companies",
        "production_countries",
        "release_date",
        "revenue",
        "runtime",
        "spoken_languages",
        "status",
        "tagline",
        "title",
        "video",
        "vote_average",
        "vote_count"
    ])
    while movieId < endId:
        try:
            link = url + str(movieId) + api_key
            data = urllib.request.urlopen(link)
            json_data = json.loads(data.read())
            # print(json_data)
            csv_file.writerow([ 
                json_data["adult"],
                json_data["backdrop_path"],
                json_data["belongs_to_collection"],
                json_data["budget"],
                array_crawler(json_data["genres"]),
                json_data["homepage"],
                json_data["id"],
                json_data["imdb_id"],
                json_data["original_language"],
                json_data["original_title"],
                json_data["overview"],
                json_data["popularity"],
                json_data["poster_path"],
                array_crawler(json_data["production_companies"]),
                array_crawler(json_data["production_countries"]),
                json_data["release_date"],
                json_data["revenue"],
                json_data["runtime"],
                array_crawler(json_data["spoken_languages"]),
                json_data["status"],
                json_data["tagline"],
                json_data["title"],
                json_data["video"],
                json_data["vote_average"],
                json_data["vote_count"]
            ])
            print(movieId, "Success")
            movieId = movieId + 1
            pass
        except:
            print(movieId, "Faild")
            movieId = movieId + 1
            pass

data_getter(275, csv_file='./newDB.csv', url="https://api.themoviedb.org/3/movie/", api_key="?api_key=f8973ce743250a31fd041bc2327a772d")
