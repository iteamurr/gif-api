from pathlib import Path


def get_components():
    return Path(__file__).parent.joinpath("components.yaml").resolve()
