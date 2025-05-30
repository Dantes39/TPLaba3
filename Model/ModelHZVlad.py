import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class ModelHZVlad:
    def process_file(self, filepath: str, n_years_str: str):
        # 1) Парсим N лет
        try:
            n_years = int(n_years_str)
        except ValueError:
            n_years = 0

        # 2) Читаем и формируем DataFrame
        df = pd.read_csv(filepath)  # или ваш кастомный парсинг, см. прошлый вариант
        df['Year'] = df['Year'].astype(int)
        df['InflationPercent'] = df['InflationPercent'].astype(float)

        # 3) Подготавливаем табличку
        headers = list(df.columns)
        table_data = [headers] + df.values.tolist()

        # 4) Создаём Figure с двумя subplots
        fig, (ax_hist, ax_fore) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        fig.suptitle('Инфляция и прогноз в России')

        # Верхний график — исторические данные
        ax_hist.plot(df['Year'], df['InflationPercent'],
                     marker='o', label='Историческая инфляция')
        ax_hist.set_ylabel('Инфляция, %')
        ax_hist.legend()
        ax_hist.grid(True)

        # Нижний — прогноз
        window = 3
        df['MA'] = df['InflationPercent'].rolling(window).mean()
        last_year = df['Year'].iat[-1]

        # Собираем прогнозные точки
        ma_vals = df['MA'].dropna().tolist()
        years_fore = [last_year + i for i in range(1, n_years + 1)]
        forecasts = [ma_vals[-1]] * n_years if ma_vals else []

        if n_years > 0:
            ax_fore.plot(years_fore, forecasts,
                         linestyle='--', marker='o', label=f'Прогноз на {n_years} лет')
            ax_fore.fill_between(years_fore, forecasts, alpha=0.2)
        else:
            ax_fore.text(0.5, 0.5, 'N=0 → прогноз не строится',
                         ha='center', va='center', transform=ax_fore.transAxes)

        ax_fore.set_xlabel('Год')
        ax_fore.set_ylabel('Прогноз, %')
        ax_fore.legend()
        ax_fore.grid(True)

        fig.tight_layout(rect=[0, 0, 1, 0.96])

        # 5) Считаем стоимость товара через N лет
        base_price = 100
        cum_factor = np.prod([1 + f/100 for f in forecasts]) if forecasts else 1
        future_price = base_price * cum_factor
        summary = (
            f"Прогноз инфляции на {n_years} лет методом скользящей средней (окно={window}).\n"
            f"Стоимость товара из 100 у.е. через {n_years} лет ≈ {future_price:.2f} у.е."
        )

        return table_data, fig, summary
