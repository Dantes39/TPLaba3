from Model.models import DanilModel, VadimModel, VladModel
from models import InflationModel
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

class DataPresenter:
    """Presenter для координации View и Models."""
    def __init__(self, view):
        self.view = view
        self.models = {
            'Danil': DanilModel(),
            'Vadim': VadimModel(),
            'Vlad': VladModel()
        }
        self.current_file = None

    def open_inflation(self):
        """Открытие экрана анализа инфляции"""
        print("Opening inflation screen")

        # Очищаем текущий экран
        self.view.clear_widgets()

        # Создаем экран инфляции
        from MainView import InflationView
        inflation_view = InflationView()

        # Создаем презентер для инфляции
        self.inflation_presenter = InflationPresenter(inflation_view)

        # Добавляем экран
        self.view.add_widget(inflation_view)

    def on_file_selected(self, file_path):
        """Обработка выбора файла."""
        print(f"Presenter: File selected: {file_path}")
        self.current_file = file_path
        self.view.update_output_text(f"File loaded: {file_path}")

    def on_number_input(self, value):
        """Обработка ввода чисел."""
        print(f"Presenter: Number input: {value}")
        self.view.update_output_text(f"Number entered: {value}")

    def on_button_press(self, name):
        """Обработка нажатия кнопки."""
        print(f"Presenter: Button pressed: {name}")

        if name == 'Danil':
            # Логика для Данила
            print("Opening Danil's screen")

        elif name == 'Vadim':
            # Логика для Вадима
            print("Opening Vadim's screen")

        elif name == 'Vlad':
            # Логика для Владислава (ваш вариант инфляции)
            self.open_inflation()

        if self.current_file:
            model = self.models.get(name)
            if model:
                table_data, figure, summary = model.process_file(self.current_file, self.view.number_input.text)
                self.view.update_table(table_data)
                if figure:
                    self.view.update_plot(figure)
                self.view.update_output_text(summary)
            else:
                self.view.update_output_text(f"Error: No model for {name}")
        else:
            self.view.update_output_text("Error: No file selected")


class InflationPresenter:
    def __init__(self, view):
        self.view = view
        self.model = InflationModel()

        # Привязка событий
        self.view.calculate_btn.bind(on_press=self.calculate)
        self.view.back_btn.bind(on_press=self.go_back)

    def calculate(self, instance):
        try:
            # Очистка предыдущих результатов
            self.view.clear_plot()

            # Получение данных
            file_path = self.view.file_input.text
            current_price = float(self.view.price_input.text)
            years = int(self.view.years_input.text)

            # Загрузка данных
            data = self.model.load_data(file_path)

            # Расчет будущей стоимости
            future_price = self.model.calculate_future_price(current_price, years)
            self.view.show_result(future_price, years)

            # Прогнозирование и построение графика (опционально)
            # forecast = self.model.predict_inflation(future_years=years)
            # self.plot_inflation(forecast)

        except Exception as e:
            self.view.result_label.text = f"Ошибка: {str(e)}"

    def plot_inflation(self, data):
        """Построение графика инфляции (опционально)"""
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data['Year'], data['Inflation'], 'bo-', label='Факт')
        ax.set_title('Инфляция в России')
        ax.set_xlabel('Год')
        ax.set_ylabel('%')
        ax.legend()
        ax.grid(True)
        self.view.add_plot(FigureCanvasKivyAgg(fig))

    def go_back(self, instance):
        """Возврат в главное меню"""
        app = App.get_running_app()
        app.root.clear_widgets()

        # Импортируем главный экран
        from MainView import MainView
        from MainPresenter import Presenter

        main_view = MainView()
        presenter = Presenter(main_view)
        app.root.add_widget(main_view)