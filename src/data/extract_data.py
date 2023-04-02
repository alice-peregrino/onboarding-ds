import pymongo
from pymongo import MongoClient
from imdb import Cinemagoer
from tqdm import tqdm
import logging
logging.basicConfig(level=logging.INFO)

def check_key(key):
    return movie[key] if key in movie.infoset2keys['main'] else "NOT_AVAILABLE"

def extract_from_object(lst):
    try:
        return [name["name"] for name in lst if lst != "NOT_AVAILABLE"]
    except KeyError:
        return "NOT_AVAILABLE"

client = MongoClient('105.210.54.125', 27017)

imdb = client['imdb-db']
best_250_movies = imdb.best_250_movies

ia = Cinemagoer()
top = ia.get_top250_movies()
movie_ids = [movie.movieID for movie in top]

for i in tqdm(movie_ids):
    movie = ia.get_movie(i)
    obj = {
        "localized_title": check_key("localized title"),
        "cast": extract_from_object(check_key("cast")),
        "genres": check_key("genres"),
        "runtimes": check_key("runtimes"),
        "countries": check_key("countries"),
        "country_codes": check_key("country codes"),
        "language_codes": check_key("language codes"),
        "color_info": check_key("color info"),
        "aspect_ratio": check_key("aspect ratio"),
        "sound_mix": check_key("sound mix"),
        "box_office": check_key("box office"),
        "certificates": check_key("certificates"),
        "original_air_date": check_key("original_air_date"),
        "rating": check_key("rating"),
        "votes": check_key("votes"),
        "cover_url": check_key("cover url"),
        "imdbID": check_key("imdbID"),
        "videos": check_key("videos"),
        "plot_outline": check_key("plot outline"),
        "languages": check_key("languages"),
        "title": check_key("title"),
        "year": check_key("year"),
        "kind": check_key("kind"),
        "original_title": check_key("original title"),
        "director": extract_from_object(check_key("director")),
        "writer": extract_from_object(check_key("writer")),
        "producer": extract_from_object(check_key("producer")),
        "composer": extract_from_object(check_key("composer")),
        "cinematographer": extract_from_object(check_key("cinematographer")),
        "editor": extract_from_object(check_key("editor")),
        "editorial_department": extract_from_object(check_key("editorial department")),
        "casting_director": extract_from_object(check_key("casting director")),
        "production_design": extract_from_object(check_key("production design")),
        "art_direction": extract_from_object(check_key("art direction")),
        "set_decoration": extract_from_object(check_key("set decoration")),
        "costume_designer": extract_from_object(check_key("costume designer")),
        "make_up": extract_from_object(check_key("make up")),
        "production_manager": extract_from_object(check_key("production manager")),
        "assistant_director": extract_from_object(check_key("assistant director")),
        "art_department": extract_from_object(check_key("art department")),
        "sound_crew": extract_from_object(check_key("sound crew")),
        "special_effects": extract_from_object(check_key("special effects")),
        "visual_effects": extract_from_object(check_key("visual effects")),
        "stunt_performer": extract_from_object(check_key("stunt performer")),
        "camera_and_electrical_department": extract_from_object(check_key("camera and electrical department")),
        "casting_department": extract_from_object(check_key("casting department")),
        "costume_department": extract_from_object(check_key("costume department")),
        "location_management": extract_from_object(check_key("location management")),
        "music_department": extract_from_object(check_key("music department")),
        "script_department": extract_from_object(check_key("script_department")),
        "transportation_department": extract_from_object(check_key("transportation department")),
        "miscellaneous_crew": extract_from_object(check_key("miscellaneous crew")),
        "thanks": extract_from_object(check_key("thanks")),
        "akas": check_key("akas"),
        "top_250_rank": check_key("top_250_rank"),
        "production_companies": extract_from_object(check_key("production companies")),
        "distributors": extract_from_object(check_key("distributors")),
        "special_effects_companies": extract_from_object(check_key("special effects companies")),
        "other_companies": extract_from_object(check_key("other companies"))
    }

    best_250_movies.insert_one(obj)
    logging.info(f"Successfully inserted movie id {i}!")

