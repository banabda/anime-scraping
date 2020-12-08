from bs4 import BeautifulSoup
import requests
import time
import datetime


def downLink(animeName, animeList):
    print('\nSearching the anime from the main page, please wait...')
    downloadlist = {}
    for anime in animeList:
        title = anime.find('a')
        if animeName.lower() in title.text.lower():
            link = []
            episode_url = title.get('href')
            print('\n\033[1m'+title.text+'\033[0m\n')
            print('Getting the anime download link, please wait...\n')
            episode = requests.get(episode_url).text
            soup_eps = BeautifulSoup(episode, 'lxml')

            episode_page = soup_eps.find('div', class_="epsc")
            undordered_list = episode_page.find_all('ul')

            for ind, ul in enumerate(undordered_list):
                if ind > 0:
                    link_list = ul.find('li')
                    download_link_list = link_list.find_all('a')

                    for dl in download_link_list:
                        linkdetail = {}
                        linkdetail[dl.text] = dl.get('href')
                        link.append(linkdetail)

            downloadlist[animeName] = link
            return downloadlist
    return 0


def todayList(today, animeList):
    animelist_ = []
    for anime in animeList:
        spanlist = anime.find_all('span')
        for index, span in enumerate(spanlist):
            if index == 1:
                published = span.text
                if today in published:
                    title = anime.find('a').text
                    animelist_.append(title)
    return animelist_


print('Welcome to anime scraping!')
animekompi = requests.get('http://animekompi.web.id/').text
soup = BeautifulSoup(animekompi, 'lxml')
animelist = soup.find_all('div', class_='dtl')
while True:
    inChoice = input('1. Today anime list; 2. Download link; 3. Close : ')
    cdf = datetime.datetime.today().strftime('%A')
    if inChoice == "1":
        animes = todayList(cdf, animelist)
        print("\t======\n"+"\n".join(animes)+"\n\t======")
    elif inChoice == "2":
        anime_name = input('Give an anime name: ')
        result = downLink(anime_name, animelist)
        if result == 0:
            print('\n\033[1m'+"Anime not found"+'\033[0m\n')
        else:
            for index, link in enumerate(result[anime_name]):
                for l in link:
                    server = l
                for x in link:
                    url = link[x]
                print(f"{server} : {url}")
                with open(f'C:/Users/Banabda/Documents/Python/Anime scraping/{cdf}_{anime_name}.txt', 'a') as f:
                    f.write(f'{index+1}. {server} : {url}\n')
    elif inChoice == "3":
        print("Thank you! See you later! :)")
        break
    else:
        print("Wrong input, try again!")
