"""Top package for chaoslocust."""
from typing import List
from logzero import logger

from chaoslib.discovery.discover import discover_actions, discover_probes, \
    initialize_discovery_result
from chaoslib.types import Discovery, DiscoveredActivities

name = "chaoslocust"
__author__ = """Gabor Gerencser"""
__email__ = 'gabor.gerencser@vodafone.com'
__version__ = '0.0.1'
__all__ = ["discover", "__version__"]


def discover(discover_system: bool = True) -> Discovery:
    logger.info("Discovering capabilities from chaostoolkit-locust")

    discovery = initialize_discovery_result(
        "chaoslocust", __version__, "locust")
    discovery["activities"].extend(load_exported_activities())
    return discovery

def load_exported_activities() -> List[DiscoveredActivities]:
    """
    Extract metadata from actions and probes exposed by this extension.
    """
    activities = []
    activities.extend(discover_actions("chaoslocust.actions"))
    activities.extend(discover_probes("chaoslocust.probes"))
    return activities
