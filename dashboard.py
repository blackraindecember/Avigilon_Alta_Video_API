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

    def __init__(self, config):

        self.base_url = config["base_url"]
        self.username = config["username"]
        self.password = config["password"]
        self.code = config.get("code", "")

        self.va_cookie = None
        self.area_map = {}

    # =====================================================
    # CONNECT
    # =====================================================
    def connect(self):

        self.va_cookie = dologin(
            self.base_url,
            self.username,
            self.password,
            self.code
        )

        if not self.va_cookie:
            raise Exception("Login failed")

        print("[INFO] Connected successfully")

    # =====================================================
    # LOAD COUNTING AREAS
    # =====================================================
    def reload_areas(self):

        if not self.va_cookie:
            raise Exception("Not connected")

        response = get_countingAreas(self.base_url, self.va_cookie)

        if not response:
            raise Exception("Failed to load counting areas")

        self.area_map = map_counting_area_name_id(response)

        print(f"[INFO] Loaded {len(self.area_map)} areas")

        return self.area_map

    # =====================================================
    # LOAD DATAFRAME
    # =====================================================
    def get_dataframe(self, area_id, start, end,
                      hours=0, minutes=0, seconds=0):

        try:
            start_iso = convert_to_iso(start)
            end_iso = convert_to_iso(end)

            step = build_step(hours, minutes, seconds)

            csv_text = get_countingAreas_csv(
                self.base_url,
                self.va_cookie,
                area_id,
                start_iso,
                end_iso,
                step
            )

            df = pd.read_csv(StringIO(csv_text))

            print("[DEBUG] Original columns:", df.columns.tolist())

            rename_map = {}

            # ==============================
            # TIME
            # ==============================
            if "Start time" in df.columns:
                rename_map["Start time"] = "time"

            # ==============================
            # SMART RENAME PEOPLE
            # ==============================
            for col in df.columns:

                col_lower = col.lower()

                # Crossing IN
                if "people" in col_lower and "in crossings" in col_lower:
                    rename_map[col] = "in"

                # Crossing OUT
                elif "people" in col_lower and "out crossings" in col_lower:
                    rename_map[col] = "out"

                # Occupancy MAX
                elif "people" in col_lower and "max" in col_lower:
                    rename_map[col] = "occupancy_max"

                # Occupancy MIN
                elif "people" in col_lower and "min" in col_lower:
                    rename_map[col] = "occupancy_min"

                # Vehicle IN
                elif "vehicles" in col_lower and "in crossings" in col_lower:
                    rename_map[col] = "vehicle_in"

                # Vehicle OUT
                elif "vehicles" in col_lower and "out crossings" in col_lower:
                    rename_map[col] = "vehicle_out"

                # Vehicle MAX
                elif "vehicles" in col_lower and "max" in col_lower:
                    rename_map[col] = "vehicle_occupancy_max"

                # Vehicle MIN
                elif "vehicles" in col_lower and "min" in col_lower:
                    rename_map[col] = "vehicle_occupancy_min"

            df.rename(columns=rename_map, inplace=True)

            print("[DEBUG] Columns after rename:", df.columns.tolist())

            if "time" not in df.columns:
                raise Exception("No time column found in CSV")

            return df

        except Exception:
            print("[ERROR] Failed to build DataFrame")
            traceback.print_exc()
            raise
