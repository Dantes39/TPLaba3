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

        # Поля ввода
        self.file_input = TextInput(hint_text='Файл данных (inflation_data.csv)')
        self.price_input = TextInput(hint_text='Текущая цена товара')
        self.years_input = TextInput(hint_text='Прогноз на лет')

        # Кнопки
        self.calc_btn = Button(text='Рассчитать')
        self.back_btn = Button(text='Назад')

        # Результат
        self.result_label = Label(text="")

        # Добавление элементов
        self.add_widget(Label(text="Анализ инфляции"))
        self.add_widget(self.file_input)
        self.add_widget(self.price_input)
        self.add_widget(self.years_input)
        self.add_widget(self.calc_btn)
        self.add_widget(self.back_btn)
        self.add_widget(self.result_label)

    def show_result(self, price, years):
        self.result_label.text = f"Через {years} лет: {price:.2f} руб."