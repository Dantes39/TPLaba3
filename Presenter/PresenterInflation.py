import pandas as pd
from kivy.app import App
from Model import InflationModel


class InflationPresenter:
    def __init__(self, view):
        self.view = view
        self.model = InflationModel()

        # Привязка событий
        self.view.calculate_btn.bind(on_press=self.calculate)
        self.view.back_btn.bind(on_press=self.go_back)

    def calculate(self, instance):
        try:
            # Получение данных
            file_path = self.view.file_input.text
            current_price = float(self.view.price_input.text)
            years = int(self.view.years_input.text)

            # Загрузка данных
            self.model.load_data(file_path)

            # Расчет будущей стоимости
            future_price = self.model.calculate_future_price(current_price, years)
            self.view.show_result(future_price, years)

        except Exception as e:
            self.view.result_label.text = f"Ошибка: {str(e)}"

    def go_back(self, instance):
        # Возврат в главное меню
        app = App.get_running_app()
        app.root.clear_widgets()

        # Импортируем здесь, чтобы избежать циклических зависимостей
        from ViewMainView import MainView
        from Presenter import Presenter

        main_view = MainView()
        presenter = Presenter(main_view)
        app.root.add_widget(main_view)