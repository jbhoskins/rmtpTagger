from app.gui.application import Application
import config

app = Application()

if config.DEBUG:
    if config.LAUNCH_TO_LOADED_INTERVIEW:
        app.get_text_view().load_text(config.INTERVIEW_PATH)

    if config.LAUNCH_WITH_THEME:
        pass # Not yet implemented.

app.launch()
