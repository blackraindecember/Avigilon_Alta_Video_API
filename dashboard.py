import pandas as pd
from io import StringIO
import traceback

from avigilon_alta_lib import (
    dologin,
    get_countingAreas,
    get_countingAreas_csv
)

from utils import (
    convert_to_iso,
    build_step,
    map_counting_area_name_id
)


class AltaCountingDashboard:

    # -------------------------------------------------
    # INIT
    # -------------------------------------------------
    def __init__(self, config):

        self.base_url = config["base_url"]
        self.username = config["username"]
        self.password = config["password"]
        self.code = config.get("code", "")
        self.timezone = config.get("timezone", "Asia/Ho_Chi_Minh")

        self.va_cookie = None
        self.area_map = {}

    # -------------------------------------------------
    # CONNECTION
    # -------------------------------------------------
    def is_connected(self):
        return self.va_cookie is not None

    def connect(self):
        try:
            print("[INFO] Connecting to Alta...")

            self.va_cookie = dologin(
                self.base_url,
                self.username,
                self.password,
                self.code
            )

            if not self.va_cookie:
                raise Exception("Login failed")

            print("[INFO] Login successful")

        except Exception:
            print("[ERROR] Connection failed")
            traceback.print_exc()
            raise

    # -------------------------------------------------
    # LOAD COUNTING AREAS
    # -------------------------------------------------
    def reload_areas(self):

        if not self.is_connected():
            raise Exception("Not connected")

        try:
            print("[INFO] Loading counting areas...")

            response = get_countingAreas(self.base_url, self.va_cookie)

            if not response:
                raise Exception("Session expired or API error")

            self.area_map = map_counting_area_name_id(response)

            print(f"[INFO] Loaded {len(self.area_map)} counting areas")

            return self.area_map

        except Exception:
            print("[ERROR] Failed to load counting areas")
            traceback.print_exc()
            raise

    # -------------------------------------------------
    # LOAD DATAFRAME (PHÙ HỢP CSV CỦA BẠN)
    # -------------------------------------------------
    def get_dataframe(self, area_id, start, end,
                      hours=0, minutes=0, seconds=0):

        try:
            print("[INFO] Preparing time range...")

            start_iso = convert_to_iso(start, self.timezone)
            end_iso = convert_to_iso(end, self.timezone)

            print(f"[DEBUG] Start ISO: {start_iso}")
            print(f"[DEBUG] End ISO:   {end_iso}")

            step = build_step(hours=hours, minutes=minutes, seconds=seconds)

            print(f"[DEBUG] Step (ms): {step}")

            print("[INFO] Requesting CSV data...")

            csv_text = get_countingAreas_csv(
                self.base_url,
                self.va_cookie,
                area_id,
                start_iso,
                end_iso,
                step
            )

            df = pd.read_csv(StringIO(csv_text))

            print(f"[DEBUG] Columns received: {df.columns.tolist()}")

            # ---------------------------------------------------------
            # CHUẨN HÓA CỘT THEO CSV DEPLOYMENT CỦA BẠN
            # ---------------------------------------------------------

            rename_map = {}

            # Time column
            if "Start time" in df.columns:
                rename_map["Start time"] = "time"
            elif "timestamp" in df.columns:
                rename_map["timestamp"] = "time"

            # People counts
            if "People: total in crossings" in df.columns:
                rename_map["People: total in crossings"] = "in"

            if "People: total out crossings" in df.columns:
                rename_map["People: total out crossings"] = "out"

            # Vehicle counts (optional)
            if "Vehicles: total in crossings" in df.columns:
                rename_map["Vehicles: total in crossings"] = "vehicle_in"

            if "Vehicles: total out crossings" in df.columns:
                rename_map["Vehicles: total out crossings"] = "vehicle_out"

            df.rename(columns=rename_map, inplace=True)

            print(f"[DEBUG] Columns after rename: {df.columns.tolist()}")

            if "time" not in df.columns:
                raise Exception("No usable time column found in CSV")

            print("[INFO] DataFrame ready")

            return df

        except Exception:
            print("[ERROR] Failed to get dataframe")
            traceback.print_exc()
            raise
