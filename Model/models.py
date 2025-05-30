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

    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)
        return self.data

    def calculate_future_price(self, current_price, years):
        avg_inflation = self.data['Inflation'].mean()
        return current_price * (1 + avg_inflation / 100) ** years


class InflationModel:
    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)
        return self.data

    def calculate_future_price(self, current_price, years):
        avg_inflation = self.data['Inflation'].mean()
        return current_price * (1 + avg_inflation / 100) ** years




