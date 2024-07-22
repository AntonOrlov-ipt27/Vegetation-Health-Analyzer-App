from spyre import server
import pandas as pd

class SetData(server.App):
    title = "NOAA Data Visualization"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'NOAA Data',
            "options": [{"label": "VCI", "value": "VCI"},
                        {"label": "TCI", "value": "TCI"},
                        {"label": "VHI", "value": "VHI"}],
            "key": 'ticker',
        },
        {
            "type": 'dropdown',
            "label": 'Area',
            "options": [{"label": "Cherkasy", "value": "Cherkasy"},
                        {"label": "Chernihiv", "value": "Chernihiv"},
                        {"label": "Chernivtsi", "value": "Chernivtsi"},
                        {"label": "Crimea", "value": "Crimea"},
                        {"label": "Dnipropetrovs'k", "value": "Dnipropetrovs'k"},
                        {"label": "Donets'k", "value": "Donets'k"},
                        {"label": "Ivano-Frankivs'k", "value": "Ivano-Frankivs'k"},
                        {"label": "Kharkiv", "value": "Kharkiv"},
                        {"label": "Kherson", "value": "Kherson"},
                        {"label": "Khmel'nyts'kyy", "value": "Khmel'nyts'kyy"},
                        {"label": "Kiev", "value": "Kiev"},
                        {"label": "Kiev City", "value": "Kiev City"},
                        {"label": "Kirovohrad", "value": "Kirovohrad"},
                        {"label": "Luhans'k", "value": "Luhans'k"},
                        {"label": "L'viv", "value": "L'viv"},
                        {"label": "Mykolayiv", "value": "Mykolayiv"},
                        {"label": "Odessa", "value": "Odessa"},
                        {"label": "Poltava", "value": "Poltava"},
                        {"label": "Rivne", "value": "Rivne"},
                        {"label": "Sevastopol'", "value": "Sevastopol'"},
                        {"label": "Sumy", "value": "Sumy"},
                        {"label": "Ternopil'", "value": "Ternopil'"},
                        {"label": "Transcarpathia", "value": "Transcarpathia"},
                        {"label": "Vinnytsya", "value": "Vinnytsya"},
                        {"label": "Volyn", "value": "Volyn"},
                        {"label": "Zaporizhzhya", "value": "Zaporizhzhya"},
                        {"label": "Zhytomyr", "value": "Zhytomyr"}],
            "key": 'area',
        },
        {
            "type": 'text',
            "label": 'Year',
            "key": 'year',
            "value": '',
        },
        {
            "type": 'text',
            "label": 'Week Range',
            "key": 'weekRange',
            "value": '',
        }
    ]

    controls = [{"type": "button",
                 "label": "Build",
                 "id": "update_data"}]

    tabs = ["Table", "Plot"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def getData(self, params):
        data = pd.read_csv("df.csv")
        return data

    def getTable(self, params):
        df = self.getData(params)
        area = params['area']
        year = int(params['year'])
        weekRange = [int(x) for x in str(params['weekRange']).split('-')]

        searched_df = df[(df['Area'] == area) & (df['Year'] == year) & (df['Week'] >= weekRange[0]) & (df['Week'] <= weekRange[1])]
        searched_df = searched_df[['Year', 'Week', params['ticker'], 'Area']]
        return searched_df

    def getPlot(self, params):
        df = self.getData(params)
        area = params['area']
        year = int(params['year'])
        weekRange = [int(x) for x in str(params['weekRange']).split('-')]
        ticker = params['ticker']

        searched_data = df[(df['Area'] == area) & (df['Year'] == year) & (df['Week'] >= weekRange[0]) & (df['Week'] <= weekRange[1])]
        plt_obj = searched_data.plot(x='Week', y=ticker, figsize=(20, 10), grid=True)
        plt_obj.set_title(f"Graph for {area} in {year} for the specified year and range of weeks")
        plt_obj.set_ylabel("Value")
        plt_obj.set_xlabel("Week")
        plot = plt_obj.get_figure()
        return plot


if __name__ == '__main__':
    app = SetData()
    app.launch()