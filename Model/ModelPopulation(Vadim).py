import pandas as pd

class PopulationModel:
    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        df = pd.read_excel(file_path)
        df = df.rename(columns=lambda x: x.strip())
        if 'Год' not in df.columns or 'Население' not in df.columns:
            raise ValueError("В файле должны быть столбцы 'Год' и 'Население'")
        self.data = df[['Год', 'Население']]
        return self.data

    def calculate_forecast(self, n, forecast_years):
        if self.data is None:
            raise ValueError("Данные не загружены")

        df = self.data.copy()
        df.sort_values('Год', inplace=True)
        df['Прирост (%)'] = df['Население'].pct_change() * 100
        max_increase = df['Прирост (%)'].max()
        max_decrease = df['Прирост (%)'].min()

        forecast = []
        years = df['Год'].tolist()
        values = df['Население'].tolist()

        for _ in range(forecast_years):
            if len(values) < n:
                break
            avg = sum(values[-n:]) / n
            forecast.append(avg)
            values.append(avg)
            years.append(years[-1] + 1)

        return df, years[-forecast_years:], forecast, max_increase, max_decrease
