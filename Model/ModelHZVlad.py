import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class ModelHZVlad:
    def process_file(self, filepath: str, n_years_str: str):
        # Парсим N лет из текстового поля
        try:
            n_years = int(n_years_str)
        except ValueError:
            n_years = 0

        # 1) читаем данные (ожидается CSV или Excel)
        df = pd.read_csv(filepath)  # или pd.read_excel, если нужно
        # в df: столбцы ['Year', 'InflationPercent']

        # 2) готовим табличку для отображения
        headers = list(df.columns)
        table_data = [headers] + df.values.tolist()

        # 3) строим график исторической инфляции
        fig, ax = plt.subplots()
        ax.plot(df['Year'], df['InflationPercent'], marker='o', label='Историческая')
        ax.set_xlabel('Год')
        ax.set_ylabel('Инфляция, %')
        ax.set_title('Инфляция в России за последние 15 лет')

        # 4) прогноз методом скользящей средней
        window = 3  # например, среднее за 3 года
        df['MA'] = df['InflationPercent'].rolling(window).mean()
        last_year = df['Year'].iloc[-1]
        forecasts = []
        years_fore = []
        ma_values = list(df['MA'].dropna())

        for i in range(1, n_years + 1):
            # используем последнее значение MA
            forecast = ma_values[-1]
            ma_values.append(forecast)
            years_fore.append(last_year + i)
            forecasts.append(forecast)

        # отображаем прогноз
        if n_years > 0:
            ax.plot(years_fore, forecasts, linestyle='--', label=f'Прогноз ({n_years} лет)')
            ax.fill_between(years_fore, forecasts, alpha=0.2)

        ax.legend()
        fig.tight_layout()

        # 5) рассчитываем стоимость товара через N лет
        # например, базовая цена = 100 у.е.
        base_price = 100
        cum_factor = np.prod([(1 + f/100) for f in forecasts])
        future_price = base_price * cum_factor
        summary = (
            f"Прогноз инфляции на {n_years} лет сделан методом скользящей средней (окно={window}).\n"
            f"Стоимость товара (из базовых 100 у.е.) через {n_years} лет ≈ {future_price:.2f} у.е."
        )

        return table_data, fig, summary
