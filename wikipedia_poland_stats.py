
import pandas as pd

URL = "https://en.wikipedia.org/wiki/Statistics_of_the_COVID-19_pandemic_in_Poland"


# def parse_covid_19_timeline_table(url):
    # rs = requests.get(url=URL)
    # html_text = rs.text
    # soup = BeautifulSoup(html_text, "html.parser")
    # table = soup.find('table', {'class': "wikitable sortable mw-collapsible floatright"})
    # rows = table.find_all('tr')
    # l = []
    # for tr in rows:
    #     td = tr.find_all('td')
    #     row = [tr.text for tr in td]
    #     l.append(row)
    # pd.DataFrame(l, columns=["A", "B", ...])

def covid_19_timeline(url):
    dfs = pd.read_html(URL)
    covid_19_timeline_df = dfs[2]
    return covid_19_timeline_df


covid_19_timeline(URL)
