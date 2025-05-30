from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class InflationView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 20

        # Заголовок
        self.add_widget(Label(text="Анализ инфляции", size_hint_y=0.1))

        # Поля ввода
        input_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)
        self.file_input = TextInput(hint_text='Файл данных (inflation_data.csv)', size_hint_y=0.3)
        self.price_input = TextInput(hint_text='Текущая стоимость товара', size_hint_y=0.3)
        self.years_input = TextInput(hint_text='Лет для прогноза', size_hint_y=0.3)
        input_layout.add_widget(self.file_input)
        input_layout.add_widget(self.price_input)
        input_layout.add_widget(self.years_input)
        self.add_widget(input_layout)

        # Кнопки
        btn_layout = BoxLayout(size_hint_y=0.2)
        self.calculate_btn = Button(text='Рассчитать')
        self.back_btn = Button(text='Назад')
        btn_layout.add_widget(self.calculate_btn)
        btn_layout.add_widget(self.back_btn)
        self.add_widget(btn_layout)

        # Результаты
        self.result_label = Label(text="", size_hint_y=0.2)
        self.add_widget(self.result_label)

    def show_result(self, price, years):
        self.result_label.text = f"Прогнозируемая стоимость через {years} лет: {price:.2f} руб."