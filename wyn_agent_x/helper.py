import json
import os
from typing import Dict, Any

# Load metadata.json
def load_metadata() -> Dict[str, Any]:
    path = os.path.join(os.path.dirname(__file__), "metadata.json")
    with open(path, "r") as f:
        return json.load(f)

# Decorator to register functions
FUNCTION_REGISTRY = {}

def register_function(name):
    def decorator(func):
        FUNCTION_REGISTRY[name] = func
        return func
    return decorator

# Match intent
def detect_intent(text: str, metadata: Dict[str, Any]) -> str:
    for intent, details in metadata.items():
        for trigger in details['trigger_word']:
            if trigger.lower() in text.lower():
                return intent
    return None

# Fill missing parameters
def fill_parameters(sample_payload: Dict[str, str], user_input: Dict[str, str]) -> Dict[str, str]:
    filled_payload = {}
    for key in sample_payload.keys():
        if key in user_input:
            filled_payload[key] = user_input[key]
        else:
            filled_payload[key] = None  # Needs to be asked later
    return filled_payload
