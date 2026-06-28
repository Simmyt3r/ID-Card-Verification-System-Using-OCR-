"""OCR and camera helpers for extracting text from ID card images."""

from __future__ import annotations

import importlib.util
import re
import time
from pathlib import Path

MATRIC_PATTERN = re.compile(r"[A-Z]{2,4}/\d{2}[A-Z]/\d{3,5}", re.IGNORECASE)


def is_module_available(module_name: str) -> bool:
    """Return whether an optional dependency can be imported."""

    return importlib.util.find_spec(module_name) is not None


def extract_matric_number(text: str) -> str | None:
    """Find the first matriculation number-like value in OCR text."""

    normalized = text.upper().replace(" ", "")
    match = MATRIC_PATTERN.search(normalized)
    return match.group(0).upper() if match else None


def read_text_from_image(image_path: Path | str) -> str:
    """Read text from an image using OpenCV preprocessing and Tesseract OCR.

    The optional dependencies are loaded only when this feature is used so the
    rest of the desktop application can still run in PyCharm without them.
    """

    if not is_module_available("cv2") or not is_module_available("pytesseract"):
        raise RuntimeError(
            "Image OCR requires opencv-python and pytesseract. Install the Python "
            "packages and the Tesseract desktop application, or paste card text manually."
        )

    import cv2
    import pytesseract

    path = Path(image_path)
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Could not open image: {path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.bilateralFilter(gray, 11, 17, 17)
    thresholded = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return pytesseract.image_to_string(thresholded)


def capture_image_from_webcam(
    output_path: Path | str,
    *,
    warmup_seconds: float = 2.0,
    minimum_warmup_frames: int = 10,
) -> Path:
    """Capture a stable frame from the default webcam and save it to disk.

    Webcams commonly return a dark or blurry first frame while autofocus,
    auto-exposure, and white balance settle.  Waiting briefly and discarding
    warm-up frames makes the capture feel intentional instead of snapping the
    instant the button is pressed.
    """

    if not is_module_available("cv2"):
        raise RuntimeError("Webcam capture requires opencv-python. Install it with pip.")

    import cv2

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("Could not open the default webcam.")

    try:
        deadline = time.monotonic() + warmup_seconds
        frame = None
        frames_read = 0

        while frames_read < minimum_warmup_frames or time.monotonic() < deadline:
            ok, candidate = camera.read()
            if not ok:
                raise RuntimeError("Could not read an image from the webcam.")
            frame = candidate
            frames_read += 1

        if frame is None:
            raise RuntimeError("Could not read an image from the webcam.")

        cv2.imwrite(str(output), frame)
    finally:
        camera.release()

    return output
