import uuid
from typing import Callable, Dict

import networkx as nx

from dt_maps.constants import YELLOW_TAPE, CENTER_OF_LANE_NORMALIZED
from dt_maps.types import Tile


def _populate_tile_straight(g: nx.DiGraph, tile_size: float):
    # get tapes and points of interest
    half_yellow = YELLOW_TAPE.width / 2.0
    distance_to_lane_center = half_yellow + CENTER_OF_LANE_NORMALIZED * tile_size
    # left lane (direction: north to south)
    left_top_id = str(uuid.uuid4())
    left_top = {
        "position": [-distance_to_lane_center, tile_size, 0],
        "lane": "left"
    }
    left_bottom_id = str(uuid.uuid4())
    left_bottom = {
        "position": [-distance_to_lane_center, -tile_size, 0],
        "lane": "left"
    }
    # right lane (direction: south to north)
    right_bottom_id = str(uuid.uuid4())
    right_bottom = {
        "position": [distance_to_lane_center, -tile_size, 0],
        "lane": "right"
    }
    right_top_id = str(uuid.uuid4())
    right_top = {
        "position": [distance_to_lane_center, tile_size, 0],
        "lane": "right"
    }
    # add nodes
    g.add_node(left_top_id, **left_top)
    g.add_node(left_bottom_id, **left_bottom)
    g.add_node(right_bottom_id, **right_bottom)
    g.add_node(right_top_id, **right_top)
    # add edges
    g.add_edge(left_top_id, left_bottom_id)
    g.add_edge(right_bottom_id, right_top_id)


tile_type_to_populate_fcn: Dict[str, Callable[[nx.DiGraph, float], None]] = {
    "straight": _populate_tile_straight,
}


def get_tile_graph(tile: Tile, tile_size: float) -> nx.DiGraph:
    # get tile
    tile_type: str = tile["type"]
    # create empty graph
    G = nx.DiGraph()
    # get function to populate the graph
    populate = tile_type_to_populate_fcn.get(tile_type, None)
    if populate is None:
        raise NotImplementedError("Function 'get_tile_graph' is not implemented for tile "
                                  f"of type {tile_type}")
    # populate graph
    populate(G, tile_size)
    # ---
    return G
