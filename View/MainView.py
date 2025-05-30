from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import sys
import os
import numpy as np
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture
from kivy.config import Config
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from plyer import filechooser
from kivy.uix.boxlayout import BoxLayout



# Добавляем корень проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Настройка окна
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'multisamples', '0')


class TableRow(FocusBehavior, BoxLayout):
    """Класс для отображения строки таблицы."""
    index = None
    selected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(TableRow, self).__init__(**kwargs)
        self.orientation = 'horizontal'

    def refresh_view_attrs(self, rv, index, data):
        """Обновление данных строки."""
        self.index = index
        self.clear_widgets()
        for value in data['row']:
            self.add_widget(Label(text=str(value)))
        return super().refresh_view_attrs(rv, index, data)


class MatplotlibWidget(Widget):
    """Виджет для отображения графиков Matplotlib."""

    def __init__(self, **kwargs):
        super(MatplotlibWidget, self).__init__(**kwargs)
        self.figure = Figure(figsize=(4, 3))
        self.canvas_agg = FigureCanvasAgg(self.figure)
        self.texture = None
        self.size = (400, 300)  # Начальный размер
        self.bind(pos=self._update_texture, size=self._update_texture)
        self._update_texture()

    def _update_texture(self, *args):
        """Обновление текстуры для отображения графика."""
        try:
            # Рендерим фигуру
            self.canvas_agg.draw()
            # Получаем буфер RGBA
            buf = self.canvas_agg.buffer_rgba()
            # Преобразуем в одномерный массив
            buf = np.frombuffer(buf, dtype=np.uint8).ravel()
            # Создаем текстуру
            w, h = self.canvas_agg.get_width_height()
            self.texture = Texture.create(size=(w, h), colorfmt='rgba')
            self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
            # Обновляем графику
            self.canvas.clear()
            with self.canvas:
                Rectangle(texture=self.texture, pos=self.pos, size=self.size)
        except Exception as e:
            print(f"Error updating texture: {e}")

    def update_plot(self, figure):
        """Обновление графика."""
        print("Updating plot in MatplotlibWidget")
        self.figure = figure
        self.canvas_agg = FigureCanvasAgg(self.figure)
        self._update_texture()


class DataView(BoxLayout):
    """Основной класс представления (View) для интерфейса."""

    def __init__(self, presenter, **kwargs):
        super(DataView, self).__init__(**kwargs)
        self.presenter = presenter
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        print("Initializing DataView...")
        self._build_ui()

    def _build_ui(self):
        """Создание пользовательского интерфейса."""
        print("Building UI...")
        # Верхняя часть: загрузка файла и текстовое поле
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)

        # Кнопка для открытия нативного диалогового окна
        file_button = Button(text='Load CSV/XLSX', size_hint=(0.5, 1))
        file_button.bind(on_press=self._open_file_chooser)
        top_layout.add_widget(file_button)
        print("Added file button")

        # Текстовое поле для ввода чисел
        self.number_input = TextInput(hint_text='Enter numbers', multiline=False, size_hint=(0.5, 1))
        self.number_input.bind(text=self._on_number_input)
        top_layout.add_widget(self.number_input)
        print("Added number input")

        self.add_widget(top_layout)
        print("Added top layout")

        # Средняя часть: таблица и график
        middle_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6))

        # Окно для таблицы
        self.table_view = RecycleView(size_hint=(0.5, 1))
        self.table_view.layout = RecycleBoxLayout(default_size=(None, 30),
                                                  default_size_hint=(1, None),
                                                  size_hint=(1, None),
                                                  height=400,
                                                  orientation='vertical')
        self.table_view.data = []
        middle_layout.add_widget(self.table_view)
        print("Added table view")

        # Окно для графика
        self.plot_container = BoxLayout(size_hint=(0.5, 1))
        middle_layout.add_widget(self.plot_container)
        print("Added plot widget")

        self.add_widget(middle_layout)
        print("Added middle layout")

        # Текстовое поле для вывода
        self.output_text = TextInput(readonly=True, hint_text='Output text', size_hint=(1, 0.2))
        self.add_widget(self.output_text)
        print("Added output text")

        # Нижняя часть: кнопки
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        for name in ['Danil', 'Vadim', 'Vlad']:
            btn = Button(text=name)
            btn.bind(on_press=lambda instance, n=name: self.presenter.on_button_press(n))
            button_layout.add_widget(btn)
            print(f"Added button: {name}")
        self.add_widget(button_layout)
        print("Added button layout")
        print("UI build complete")

    def _open_file_chooser(self, instance):
        """Открытие нативного диалогового окна для выбора файла."""
        print("Opening native file chooser...")
        filechooser.open_file(
            filters=['*.csv', '*.xlsx'],
            on_selection=self._on_file_selected
        )

    def _on_file_selected(self, selection):
        """Обработка выбора файла."""
        print("File selected")
        if selection:
            file_path = selection[0]
            self.presenter.on_file_selected(file_path)
        print(f"Selected: {selection}")

    def _on_number_input(self, instance, value):
        """Обработка ввода текста."""
        print(f"Number input changed: {value}")
        self.presenter.on_number_input(value)

    def update_table(self, data):
        """Обновление данных таблицы."""
        print(f"Updating table with data: {data}")
        self.table_view.data = [{'row': row} for row in data]

    def update_plot(self, figure):
        """Обновление графика."""
        print("Updating plot (via FigureCanvasKivyAgg)")
        # Убираем старый график
        self.plot_container.clear_widgets()
        # Вставляем новый
        canvas = FigureCanvasKivyAgg(figure)
        self.plot_container.add_widget(canvas)

    def update_output_text(self, text):
        """Обработка ввода текста."""
        print(f"Updating output text: {text}")
        self.output_text.text = text


class MainApp(App):
    """Основной класс приложения Kivy."""

    def build(self):
        print("Building MainApp...")
        from Presenter.MainPresenter import DataPresenter
        view = DataView(presenter=None)  # Временная инициализация
        presenter = DataPresenter(view)
        view.presenter = presenter  # Установка презентера после создания
        print("MainApp build complete")
        return view


if __name__ == '__main__':
    print("Starting Kivy app...")
    MainApp().run()
    print("App closed.")