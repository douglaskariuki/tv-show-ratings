from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

def get_show_info(url):
    seasons_page = urlopen(url)
    html = seasons_page.read()
    seasons_page.close()
    seasons_bs = bs(html, "html.parser")
    seasons_count = seasons_bs.find(id="bySeason").find_all("option")
    print(seasons_count)
    title = seasons_bs.find(
        "div", class_="subpage_title_block"
    ).find("h3").find("a")
    print(title.string)
    seasons = []
    for i in range(1, len(seasons_count) + 1):
        url = f'{url}?season={i}'
        seasons.append(url)

    print(seasons[0])
    return (seasons, title.string)


def get_season_ratings(season_url):
    season_number = season_url[-1:]
    season_page = urlopen(season_url)
    html = season_page.read()
    season_page.close()
    season_bs = bs(html, "html.parser")
    episodes = season_bs.find_all("div", class_="list_item")
    ratings = []
    for episode in episodes:
        rating = episode.find("span", class_="ipl-rating-star__rating")
        if rating:
            ratings.append(float(rating.string))

    print(ratings)
    return ratings


def main(show_id):
    show_url = f'https://www.imdb.com/title/{show_id}/episodes'
    seasons, title = get_show_info(show_url)
    ratings = {}
    for season in seasons:
        season_ratings = get_season_ratings(season)
        ratings[season[-1:]] = season_ratings
    return ratings, title