import hashlib

def _seed_from_id(student_id: str) -> int:
    """Stable 32-bit seed from arbitrary student ID/email."""
    return int(hashlib.sha1(student_id.encode()).hexdigest(), 16) & 0xFFFFFFFF

def generate_config(student_id: str) -> dict:
    """
    Return a deterministic but unique environment config for `student_id`.
    Keys:
        - start_position (tuple[x, y])
        - wind_scale (float)
        - wind_update_interval (int)
    """
    seed = _seed_from_id(student_id)

    # Wind scale in [0.8, 1.8]
    wind_scale = 0.8 + (seed % 101) / 100.0              # 0.8 … 1.81

    # Wind update interval in {5,10,15,20}
    interval_options = (5, 10, 15, 20)
    wind_update_interval = interval_options[(seed >> 8) % 4]

    # Start X in {0.0, 0.5, 1.0}
    start_options = (0.0, 0.5, 1.0)
    start_x = start_options[(seed >> 16) % 3]

    return {
        "start_position": (start_x, 0.0),
        "wind_scale": wind_scale,
        "wind_update_interval": wind_update_interval,
    }
