import os
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_test_assets_dir():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    assets_dir = os.path.join(script_dir, "..", "..", "tests")
    return os.path.abspath(assets_dir)


def get_asset_path(asset: str) -> str:
    return os.path.abspath(os.path.join(get_test_assets_dir(), asset))
