import plotly.express as px
import requests
from pandas import read_xml, DataFrame, concat, to_numeric

url = 'http://udim.koeri.boun.edu.tr/zeqmap/xmlt/{month}.xml'

years = list(range(2003, 2023))
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

df = DataFrame()

for year in years:
    for month in months:
        print(f'{year}{month}')
        t = requests.get(url.format(month=f'{year}{month}')).text

        df_partial = read_xml(t)
        df_partial = df_partial[df_partial['mag'] != '-.-']
        df_partial['mag'] = to_numeric(df_partial['mag'])

        # df_partial = df_partial[df_partial['mag'] >= 5.5]

        df = concat([df, df_partial])

for month in ['01', '02']:
    print(f'2023{month}')
    t = requests.get(url.format(month=f'2023{month}')).text

    df_partial = read_xml(t)
    # df_partial = df_partial[df_partial['mag'] >= 5.5]

    df = concat([df, df_partial])

df.to_csv('data.csv')

fig = px.density_mapbox(df, lat='lat', lon='lng', z='mag', radius=2,
                        center=dict(lat=39, lon=35), zoom=5,
                        mapbox_style="stamen-terrain")

open('graph.html', 'w').write(fig.to_html())
