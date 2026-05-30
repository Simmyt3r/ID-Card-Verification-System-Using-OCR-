"""Text-to-speech helper with graceful fallback."""

from __future__ import annotations

import importlib.util


def speak(text: str) -> bool:
    """Speak text aloud when pyttsx3 is installed.

    Returns True when speech was attempted and False when the optional package is
    unavailable. The GUI always displays the same text, so speech is an
    enhancement rather than a hard requirement.
    """

    if importlib.util.find_spec("pyttsx3") is None:
        return False

    import pyttsx3

    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    return True
