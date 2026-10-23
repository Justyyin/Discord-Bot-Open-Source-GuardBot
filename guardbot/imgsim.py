"""Image similarity with a difference hash: the same picture re-saved, resized or slightly changed gets a hash that differs in only a few bits."""

import io

from PIL import Image

MAX_PIXELS = 40_000_000
NEAR = 6


def dhash(data: bytes) -> str:
    """A 64 bit hash of the picture as 16 hex digits. Raises ValueError for files that are not usable images."""
    try:
        with Image.open(io.BytesIO(data)) as im:
            if im.width * im.height > MAX_PIXELS:
                raise ValueError("image too large")
            im.draft("L", (64, 64))
            small = im.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
    except (OSError, Image.DecompressionBombError, Image.DecompressionBombWarning) as exc:
        raise ValueError("not an image") from exc
    px = small.tobytes()
    bits = 0
    for row in range(8):
        for col in range(8):
            bits = (bits << 1) | (px[row * 9 + col] > px[row * 9 + col + 1])
    return f"{bits:016x}"


def distance(a: str, b: str) -> int:
    """Number of different bits between two hashes."""
    return bin(int(a, 16) ^ int(b, 16)).count("1")


def similar(h: str, known: list[str], near: int = NEAR) -> bool:
    """True if a hash is close to one of the known hashes. Flat pictures (nearly all bits equal) never match, they say nothing."""
    if bin(int(h, 16)).count("1") in range(0, 6) or bin(int(h, 16)).count("1") in range(59, 65):
        return False
    return any(distance(h, k) <= near for k in known)
