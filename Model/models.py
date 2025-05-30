import pandas as pd
from matplotlib.figure import Figure

class DanilModel:
    """Модель для обработки данных по нажатию кнопки Danil."""
    def process_file(self, file_path, number_input):
        try:
            # Чтение файла
            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
            # Фильтрация по числовому вводу, если указано
            if number_input:
                try:
                    threshold = float(number_input)
                    df = df[df.iloc[:, 0] > threshold]
                except ValueError:
                    pass
            # Данные для таблицы
            table_data = df.values.tolist()
            # Сумма первого столбца
            summary = f"Sum of first column: {df.iloc[:, 0].sum()}"
            # Гистограмма первого столбца
            fig = Figure()
            ax = fig.add_subplot(111)
            ax.hist(df.iloc[:, 0], bins=10, color='blue')
            ax.set_title("Histogram (Danil)")
            ax.set_xlabel("Value")
            ax.set_ylabel("Frequency")
            return table_data, fig, summary
        except Exception as e:
            return [], None, f"Error: {str(e)}"

class VadimModel:
    """Модель для обработки данных по нажатию кнопки Vadim."""
    def process_file(self, file_path, number_input):
        try:
            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
            if number_input:
                try:
                    threshold = float(number_input)
                    df = df[df.iloc[:, 0] > threshold]
                except ValueError:
                    pass
            table_data = df.values.tolist()
            summary = f"Mean of first column: {df.iloc[:, 0].mean()}"
            fig = Figure()
            ax = fig.add_subplot(111)
            ax.plot(df.iloc[:, 0], color='green')
            ax.set_title("Line Plot (Vadim)")
            ax.set_xlabel("Index")
            ax.set_ylabel("Value")
            return table_data, fig, summary
        except Exception as e:
            return [], None, f"Error: {str(e)}"

class VladModel:
    """Модель для обработки данных по нажатию кнопки Vlad."""
    def process_file(self, file_path, number_input):
        try:
            df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
            if number_input:
                try:
                    threshold = float(number_input)
                    df = df[df.iloc[:, 0] > threshold]
                except ValueError:
                    pass
            table_data = df.values.tolist()
            summary = f"Max of first column: {df.iloc[:, 0].max()}"
            fig = Figure()
            ax = fig.add_subplot(111)
            ax.scatter(range(len(df)), df.iloc[:, 0], color='red')
            ax.set_title("Scatter Plot (Vlad)")
            ax.set_xlabel("Index")
            ax.set_ylabel("Value")
            return table_data, fig, summary
        except Exception as e:
            return [], None, f"Error: {str(e)}"


class InflationModel:
    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        """Загрузка данных из CSV-файла"""
        self.data = pd.read_csv(file_path)
        return self.data

    def calculate_future_price(self, current_price, years):
        """Расчет будущей стоимости товара"""
        if self.data is None or self.data.empty:
            raise ValueError("Данные не загружены")

        avg_inflation = self.data['Inflation'].mean()
        return current_price * (1 + avg_inflation / 100) ** years

    def predict_inflation(self, window_size=3, future_years=5):
        """Прогнозирование методом скользящей средней (опционально)"""
        if self.data is None:
            raise ValueError("Данные не загружены")

        # Расчет скользящей средней
        self.data['MA'] = self.data['Inflation'].rolling(window=window_size).mean().shift(1)

        # Экстраполяция
        last_value = self.data['MA'].dropna().iloc[-1]
        future_data = pd.DataFrame({
            'Year': range(self.data['Year'].max() + 1, self.data['Year'].max() + future_years + 1),
            'Inflation': [last_value] * future_years,
            'MA': [last_value] * future_years
        })

        return pd.concat([self.data, future_data], ignore_index=True)