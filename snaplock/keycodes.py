
from typing import Dict

# Key code mappings
KEY_CODES: Dict[str, int] = {
    'enter': 13,
    'tab': 9,
    'space': 32,
    'backspace': 8,
    'escape': 27,
    'up': 38,
    'down': 40,
    'left': 37,
    'right': 39,
    'delete': 46,
    'home': 36,
    'end': 35,
    'page_up': 33,
    'page_down': 34,
    'insert': 45,
    'f1': 112,
    'f2': 113,
    'f3': 114,
    'f4': 115,
    'f5': 116,
    'f6': 117,
    'f7': 118,
    'f8': 119,
    'f9': 120,
    'f10': 121,
    'f11': 122,
    'f12': 123,
}

def get_key_code(key_name: str) -> int:
    """Get the key code for a given key name."""
    return KEY_CODES.get(key_name.lower(), 0)

def is_control_key(key_code: int) -> bool:
    """Check if the key code represents a control key."""
    return key_code in KEY_CODES.values()
