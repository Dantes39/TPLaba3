from Model.models import DanilModel, VadimModel, VladModel
from Model.ModelHZVlad import ModelHZVlad

class DataPresenter:
    """Presenter для координации View и Models."""
    def __init__(self, view):
        self.view = view
        self.models = {
            'Danil': DanilModel(),
            'Vadim': VadimModel(),
            'Vlad': ModelHZVlad()
        }
        self.current_file = None

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