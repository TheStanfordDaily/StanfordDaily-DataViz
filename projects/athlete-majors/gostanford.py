import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import xlsxwriter
from string import ascii_uppercase

msports = ['baseball', 'mens-basketball', 'football', 'mens-golf', 'mens-gymnastics', 'mens-rowing', 'mens-soccer',
           'mens-swimming-and-diving', 'mens-tennis', 'mens-volleyball', 'mens-water-polo', 'wrestling']

wsports = ['artswim', 'womens-basketball', 'womens-beach-volleyball', 'field-hockey', 'womens-golf', 'womens-gymnastics',
          'womens-lacrosse', 'womens-rowing', 'womens-lightweight-rowing', 'womens-soccer', 'softball', 'womens-squash',
          'womens-swimming-and-diving', 'womens-tennis', 'womens-volleyball', 'womens-water-polo']

usports = ['cross-country', 'fencing', 'sailing', 'track-and-field']
men = {}
women = {}
TOKEN_MAP = {"-": " ", "mens": "men\u2019s"}


class Athlete:
    def __init__(self, name, sport, major):
        self.name = name
        self.sport = sport
        self.major = major


class Sport:
    def __init__(self, name, coed=False):
        self.name = name
        self.coed = coed  # Will use this information to alternate between a few lines of logic in roster function.

    def url(self):
        return "https://gostanford.com/sports/" + self.name + "/roster"

    def roster(self):
        page = requests.get(self.url())
        soup = BeautifulSoup(page.content, 'html.parser')
        player_blocks = soup.find('ul', attrs={'class': 'sidearm-roster-players'}) # .find_all("li", attrs={"class": "sidearm-roster-player"})
        # for block in player_blocks.find_all("li", attrs={"class": "sidearm-roster-player"}):
        #     print(block)
        names = [x.find('h3').text.strip() for x in player_blocks.find_all('div', attrs={'class': 'sidearm-roster-player-name'})]
        majors = [x.text.strip() for x in player_blocks.find_all('span', attrs={'class': 'sidearm-roster-player-major'})]
        majors = [majors[i] for i in range(len(majors)) if i % 2 == 0]
        print(len(names), "\t", len(majors))
        players = {}
        if len(names) == len(majors):
            players = [Athlete(names[i], self.name, majors[i]) for i in range(len(names))]
        return players


def pruned(sport_name):
    out = sport_name
    for token, new_value in TOKEN_MAP.items():
        out = out.replace(token, new_value)
    return out


def capitalized(sport_name):
    return ' '.join(x.capitalize() if x != "and" else x for x in sport_name.split())


for sport in msports:
    cur = Sport(sport)
    print("--- {} ---".format(sport.upper()))
    cr = cur.roster()
    for athlete in cr:
        men[sport] = cr
        print("{} is majoring in {}.".format(athlete.name, athlete.major))

print(men)

for sport in wsports:
    cur = Sport(sport)
    print("--- {} ---".format(sport.upper()))
    cr = cur.roster()
    for athlete in cr:
        women[sport] = cr
        print("{} is majoring in {}.".format(athlete.name, athlete.major))

print(women)

workbook = xlsxwriter.Workbook('major-data.xlsx')
mworksheet = workbook.add_worksheet(name='Men')
wworksheet = workbook.add_worksheet(name='Women')
column = 0
for key, value in men.items():
    letter = ascii_uppercase[column]
    mworksheet.write(letter + '1', key)
    mworksheet.write_column(letter + '2', map(lambda a: a.major, value))
    column += 1

column = 0
for key, value in women.items():
    letter = ascii_uppercase[column]
    wworksheet.write(letter + '1', key)
    wworksheet.write_column(letter + '2', map(lambda a: a.major, value))
    column += 1

workbook.close()

mmajors = {sport: [x.major for x in roster] for sport, roster in men.items()}
mfreqs = {}

for sport in msports:
    try:
        for major in set(mmajors[sport]):
            if sport not in mfreqs:
                mfreqs[sport] = {}
            mfreqs[sport][major] = mmajors[sport].count(major)
            print("There are {} {} majors.".format(mmajors[sport].count(major), major))
    except KeyError:
        print("No major data available for {}.".format(sport))

print(mfreqs)

for sport, freqs in mfreqs.items():
    plt.pie(freqs.values(), labels=freqs.keys(), autopct="%1.1f%%")
    plt.title(capitalized(pruned(sport)))
    plt.show()
