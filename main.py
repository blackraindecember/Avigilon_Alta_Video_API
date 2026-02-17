from config_loader import load_config
from dashboard import AltaCountingDashboard
from gui import build_gui

if __name__ == "__main__":

    config = load_config()

    dashboard = AltaCountingDashboard(config)

    build_gui(dashboard)
