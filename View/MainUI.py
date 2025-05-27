from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.config import Config

# Настройка окна
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'multisamples', '0')  # Отключаем мультисэмплинг


class StubPresenter:
    """Заглушка для Presenter."""

    def on_file_selected(self, file_path):
        print(f"Selected file: {file_path}")

    def on_number_input(self, value):
        print(f"Number input: {value}")

    def on_button_press(self, name):
        print(f"Button pressed: {name}")


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
        top_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))

        # Кнопка для открытия диалогового окна загрузки файла
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

        # Средняя часть: таблица и график (временные заглушки)
        middle_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.6))

        # Окно для таблицы
        self.table_view = Label(text="Table Placeholder", size_hint=(0.5, 1))
        middle_layout.add_widget(self.table_view)
        print("Added table placeholder")

        # Окно для графика
        self.plot_widget = Label(text="Plot Placeholder", size_hint=(0.5, 1))
        middle_layout.add_widget(self.plot_widget)
        print("Added plot placeholder")

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
        """Открытие диалогового окна для выбора файла."""
        print("Opening file chooser...")
        content = BoxLayout(orientation='vertical')
        self.file_chooser = FileChooserListView(filters=['*.csv', '*.xlsx'])
        content.add_widget(self.file_chooser)
        select_button = Button(text='Select', size_hint=(1, 0.1))
        content.add_widget(select_button)

        popup = Popup(title='Select CSV/XLSX file', content=content, size_hint=(0.9, 0.9))
        select_button.bind(on_press=lambda x: self._on_file_selected(popup))
        popup.open()
        print("File chooser opened")

    def _on_file_selected(self, popup):
        """Обработка выбора файла."""
        print("File selected")
        if self.file_chooser.selection:
            file_path = self.file_chooser.selection[0]
            self.presenter.on_file_selected(file_path)
        popup.dismiss()

    def _on_number_input(self, instance, value):
        """Обработка ввода текста."""
        print(f"Number input changed: {value}")
        self.presenter.on_number_input(value)

    def update_table(self, data):
        """Обновление данных таблицы."""
        print(f"Updating table with data: {data}")
        self.table_view.text = str(data)

    def update_plot(self, figure):
        """Обновление графика."""
        print("Updating plot (placeholder)")
        self.plot_widget.text = "Plot updated (placeholder)"

    def update_output_text(self, text):
        """Обновление текстового поля вывода."""
        print(f"Updating output text: {text}")
        self.output_text.text = text


class MainApp(App):
    """Основной класс приложения Kivy."""

    def build(self):
        print("Building MainApp...")
        presenter = StubPresenter()
        view = DataView(presenter=presenter)
        print("MainApp build complete")
        return view


if __name__ == '__main__':
    print("Starting Kivy app...")
    MainApp().run()
    print("App closed.")