from collections import Counter
from datetime import date
from helpers import to_date
from corrections import CORRECTION_POLAND_05_10, CORRECTION_POLAND_06_10


def monthly(data: list, country: str) -> list:
    selector = lambda x: x['countriesAndTerritories']==country
    selected_data = list(filter(selector, data))
    sorted_selected_data = sorted(selected_data, key = lambda x: (int(x['month']), int(x['day'])))

    agg_data = dict()
    z_stats = {'cases': 0, 'deaths': 0}
    for v in sorted_selected_data:
        ym = v['month'] + '/' + v['year']
        cases = v['cases']
        deaths = v['deaths']
        curr = agg_data.get(ym, z_stats)
        summary = Counter(curr) + Counter({'cases': cases, 'deaths': deaths})
        agg_data[ym] = summary

    return [{'dateRep': k, 'cases': v['cases'], 'deaths': v['deaths']} for k, v in agg_data.items()]


def daily(data: list, country: str,) -> list:
    selector = lambda x: (x['countriesAndTerritories']==country)
    selected_data = list(filter(selector, data))
    sorted_selected_data = sorted(selected_data, key = lambda x: (
            int(x['year']), int(x['month']), int(x['day'])
        )
    )

    def correct_fun(x):
        if country!='Poland':
            return x
        if x['dateRep'] == '05/10/2020':
            return CORRECTION_POLAND_05_10
        elif x['dateRep'] == '06/10/2020':
            return CORRECTION_POLAND_06_10
        return x                

    return list(map(correct_fun, sorted_selected_data))

