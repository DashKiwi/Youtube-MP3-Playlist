class MainController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self.view.display_welcome_message()
        while True:
            user_input = self.view.get_user_input()
            if user_input.lower() == 'exit':
                self.view.display_exit_message()
                break
            self.process_input(user_input)

    def process_input(self, user_input):
        # Example processing logic
        if user_input == 'get_data':
            data = self.model.get_data()
            self.view.display_data(data)
        else:
            self.view.display_error("Invalid command.")