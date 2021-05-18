from pandas import read_csv, to_datetime
import plotly.graph_objects as go


def main():
    print('reading data')
    data_csv = read_csv('https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/csv/data.csv')
    data_csv.loc[:, 'dateRep'] = data_csv['dateRep'].apply(to_datetime)

    print('converting data')
    traces = []
    for country in ('ITA', 'NLD', 'PRT', 'IRL', 'BEL', 'FRA', 'DEU'):
        df = data_csv.loc[data_csv['countryterritoryCode'] == country]
        df = df[::-1]
        df = df[1:]

        df['x'] = df['cases'] / df['popData2020'] * 100e3

        y = df['x'].rolling(14, center=False).sum()
        traces.append(
            go.Scatter(
                x=df['dateRep'][13:],
                y=y[13:],
                name=country,
            )
        )

    print('preparing figure')
    fig = go.Figure(
        data=traces,
        layout=go.Layout(
            showlegend=True,
            xaxis=dict(
                range=(0, None),
            ),
            shapes=[
                dict(
                    type="line",
                    x0=0,
                    x1=1,
                    y0=150,
                    y1=150,
                    xref='paper',
                    line=dict(
                        color="Black",
                        width=4,
                        dash="dot",
                    ))
            ],
        ))

    print('writing file')
    fig.write_html('report/index.html', include_plotlyjs='cdn', auto_open=False)


if __name__ == '__main__':
    main()
