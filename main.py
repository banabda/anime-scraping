from bs4 import BeautifulSoup
import requests
import time
import datetime


def requestUrl(ext):
    animekompi = requests.get(f'http://animekompi.web.id/{ext}').text
    soup = BeautifulSoup(animekompi, 'lxml')
    return soup


def downLink(animeName, count):
    print(f'Search in page = {count}')
    soup = requestUrl(f'page/{count}/')

    animelist = soup.find_all('div', class_='dtl')
    downloadlist = {}
    animeName_ = animeName.split()

    for anime in animelist:
        match = True
        matches = []
        title = anime.find('a')

        for name in animeName_:
            if name.isdigit():
                name = ' '+name+' '
            if name.lower() in title.text.lower():
                matches.append(True)
            else:
                matches.append(False)

        for item in matches:
            match = match and item

        if match:
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
            return downloadlist, title.text
    return 0, 0


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


def firstChoice(cdf):
    soup = requestUrl('')
    animelist = soup.find_all('div', class_='dtl')
    animes = todayList(cdf, animelist)
    print("\t======\n"+"\n".join(animes)+"\n\t======")


def secondChoice():
    global count
    anime_name = input('Give an anime name: ')
    print('\n\033[1m'+"Searching the anime..."+'\033[0m\n')
    soup = requestUrl('')
    pagerawtext = soup.find('span', class_="pages").text
    pagetext = pagerawtext.split()
    page = int(pagetext[-1].replace(",", ""))

    start = time.time()

    count = 1

    while count <= page:
        result, title = downLink(anime_name, count)
        if result != 0:
            break
        count += 1

    end = time.time()

    if result == 0:
        print('\n\033[1m'+"Anime not found"+'\033[0m\n')
    else:
        for index, link in enumerate(result[anime_name]):
            for l in link:
                server = l
            for x in link:
                url = link[x]
            with open(f'C:/Users/Banabda/Documents/Python/Anime scraping/Result/{title}.txt', 'a') as f:
                f.write(f'{index+1}. {server} : {url}\n')
        print('\033[1m'+f"Link for \"{title}\" Saved!"+'\033[0m\n')
    print('Time taken in seconds -', end - start)


# Run
print('Welcome to anime scraping!')
while True:
    inChoice = input('1. Today anime list; 2. Download link; 3. Close : ')
    cdf = datetime.datetime.today().strftime('%A')
    if inChoice == "1":
        firstChoice(cdf)
    elif inChoice == "2":
        secondChoice()
    elif inChoice == "3":
        print("Thank you! See you later! :)")
        break
    else:
        print("Wrong input, try again!")
