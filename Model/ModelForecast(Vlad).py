import pandas as pd


class InflationModel:
    def __init__(self):
        self.data = None

    def load_data(self, file_path):
        self.data = pd.read_csv(file_path)
        return self.data

    def predict(self, years=5):
        # Простое прогнозирование (реализуйте позже)
        return self.data

    def calculate_future_price(self, current_price, years):
        avg_inflation = self.data['Inflation'].mean()
        return current_price * (1 + avg_inflation / 100) ** years