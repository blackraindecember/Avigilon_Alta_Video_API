import json
import datetime
from datetime import datetime
from zoneinfo import ZoneInfo

def beautify_json(json_text: str, indent: int = 4) -> str:
    try:
        parsed = json.loads(json_text)
        return json.dumps(parsed, indent=indent, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"


import json
from typing import Union


def beautify_json_v1(data: Union[str, dict, list], indent: int = 4) -> str:
    """
    Beautify JSON.

    - Nếu truyền vào JSON string -> parse rồi format
    - Nếu truyền vào dict/list -> format trực tiếp
    """

    try:
        # Nếu là string -> parse
        if isinstance(data, str):
            parsed = json.loads(data)
        else:
            parsed = data

        return json.dumps(parsed, indent=indent, ensure_ascii=False)

    except (json.JSONDecodeError, TypeError) as e:
        return f"Invalid JSON: {e}"


def map_counting_area_name_id(response_text: str) -> dict:
    data = json.loads(response_text)

    temp = {}

    for area in data:
        name = area.get("name")
        area_id = area.get("id")

        if not name or not area_id:
            continue

        if name in temp:
            if isinstance(temp[name], list):
                temp[name].append(area_id)
            else:
                temp[name] = [temp[name], area_id]
        else:
            temp[name] = area_id

    return temp

def convert_to_iso(user_time: str, input_timezone: str = "UTC", output_as_utc: bool = True) -> str:
    """
    Convert time from:
        YY-MM-DD/HH-MM-SS

    Parameters:
        user_time (str): Time string
        input_timezone (str): Timezone of input (e.g., "UTC", "Asia/Ho_Chi_Minh")
        output_as_utc (bool):
            True  -> convert to UTC and return Z format
            False -> keep original timezone offset

    Returns:
        ISO formatted string
    """

    try:
        # Parse time string
        dt = datetime.strptime(user_time, "%y-%m-%d/%H-%M-%S")

        # Attach timezone
        dt = dt.replace(tzinfo=ZoneInfo(input_timezone))

        if output_as_utc:
            dt = dt.astimezone(ZoneInfo("UTC"))
            return dt.isoformat().replace("+00:00", "Z")
        else:
            return dt.isoformat()

    except Exception as e:
        return f"Invalid input: {e}"

def build_step(hours: int = 0, minutes: int = 0, seconds: int = 0) -> int:
    """
    Convert hours/minutes/seconds to milliseconds (step value for counting CSV API)

    Max allowed: 24 hours (86400000 ms)
    """

    total_ms = (
        hours * 3600 * 1000 +
        minutes * 60 * 1000 +
        seconds * 1000
    )

    max_ms = 24 * 3600 * 1000  # 86400000

    if total_ms <= 0:
        raise ValueError("Step must be greater than 0")

    if total_ms > max_ms:
        raise ValueError("Step cannot exceed 24 hours (86400000 ms)")

    return total_ms


