from typing import Optional, Iterable

import networkx as nx
from duckietown_world import TileMap

from dt_maps import Map
from dt_maps.exceptions import EntityNotFound
from dt_maps.graph.tiles import get_tile_graph
from dt_maps.types import Tile, TileCoordinates, MapLayer
from dt_maps.utils.tiles import get_tile


def get_tile_map_graph(m: Map, tile_map_key: str) -> nx.DiGraph:
    # get tilemap
    tile_map: Optional[TileMap] = m.layers.tile_maps[tile_map_key]
    if tile_map is None:
        raise EntityNotFound("tile_maps", tile_map=tile_map_key)
    # create empty graph
    G = nx.DiGraph()
    # populate graph
    for i, j in get_tile_map_tiles(m, tile_map_key):
        tile: Optional[Tile] = get_tile(m, i, j)
        if tile is None:
            raise EntityNotFound("tiles", i=i, j=j)
        # get tile graph
        get_tile_graph()


        # g = get_tile_graph(tile, )


def get_tile_map_tiles(m: Map, tile_map: str) -> Iterable[TileCoordinates]:
    for tile_key, tile in m.layers.tiles.items():
        if tile_key.startswith(tile_map):
            yield tile["i"], tile["j"]
