from Model import InflationModel


class InflationPresenter:
    def __init__(self, view):
        self.view = view
        self.model = InflationModel()
        self.view.calc_btn.bind(on_press=self.calculate)

    def calculate(self, instance):
        try:
            file_path = self.view.file_input.text
            current_price = float(self.view.price_input.text)
            years = int(self.view.years_input.text)

            self.model.load_data(file_path)
            future_price = self.model.calculate_future_price(current_price, years)

            self.view.show_result(future_price, years)
        except Exception as e:
            self.view.result_label.text = f"Ошибка: {str(e)}"