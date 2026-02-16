import json
import datetime

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

