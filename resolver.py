import pandas as pd
import sys 
import json
import re

item_fname ="data/movie_final.csv"

columns = ['id', 'title', 'genres', 'imdb_id', 'tmdb_id', 'imdb_url', 'rating_count', 'rating_avg', 'image_url']


#랜덤으로 count개의 아이템을 반환
def random_items(count):
    movies_df=pd.read_csv(item_fname)[1:]
    movies_df=movies_df.fillna("")
    result_items=movies_df.sample(n=count).to_dict("records")
    return result_items

#최신영화를 count개 반환
def latest_items(count):
    movies_df = pd.read_csv(item_fname)[1:]
    movies_df = movies_df.fillna("")

    # 타이틀에서 연도를 추출하는 함수
    def extract_year(title):
        match = re.search(r'\((\d{4})\)', title)  # 타이틀에서 괄호 안의 4자리 숫자를 찾음
        if match:
            return int(match.group(1))  # 연도가 추출되면 정수로 변환하여 반환
        return None  # 연도가 없으면 None 반환

    # 타이틀에서 연도를 추출하여 'release_year' 열 생성
    movies_df['release_year'] = movies_df['title'].apply(extract_year)

    # 연도가 없는 영화는 제외하고, 최신 연도 순으로 정렬
    sorted_movies_df = movies_df.dropna(subset=['release_year']).sort_values(by='release_year', ascending=False)

    # 상위 count개의 영화 반환
    result_items = sorted_movies_df.head(count).to_dict("records")
    return result_items

#ganre 키워드를 포함하는 영화 count개 반환
def genres_items(genre, count):
    movies_df = pd.read_csv(item_fname, names=columns)
    movies_df = movies_df.fillna("")
    genre_df = movies_df[movies_df["genres"].str.contains(genre, case=False, na=False)]
    #case = False : 대소문자 구분 안함

    result_items = genre_df.head(count).to_dict("records")
    return result_items

if __name__ == "__main__":
    try:
        command =sys.argv[1]

        if command == "random":
            count =int(sys.argv[2])
            print(json.dumps(random_items(count)))

        elif command == "latest":
            count =int(sys.argv[2])
            print(json.dumps(latest_items(count)))   

        elif command == "genres":
            genre=sys.argv[2]
            count =int(sys.argv[3])
            print(json.dumps(genres_items(genre, count)))   

        else:
            print("Error: Invalid command error")
            sys.exit(1)


       
      


    except ValueError:
        print("Error : Invalid arguments")
        sys.exit(1)