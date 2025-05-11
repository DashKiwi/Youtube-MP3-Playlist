from models.player_model import PlayerModel

class PlayerController:
    def __init__(self, application_path):
        self.player_model = PlayerModel(application_path)

    def toggle_pause(self):
        self.player_model.toggle_pause()

    def skip_song(self):
        self.player_model.stop_audio()

    def toggle_shuffling(self):
        settings = self.player_model.load_settings()
        settings["shuffling"] = not settings.get("shuffling", False)
        self.player_model.save_settings(settings)

    def get_shuffling(self):
        settings = self.player_model.load_settings()
        return settings.get("shuffling", False)
