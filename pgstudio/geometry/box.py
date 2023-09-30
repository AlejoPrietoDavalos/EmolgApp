from __future__ import annotations
__all__ = ["BBox"]

from . import shp
from .point import Point
from .polygon import Polygon

import numpy as np

from typing import TypeVar, Type, List
from .typings import BoxList, CoordX, CoordY, Width, Height, CoordsXY

def xywh_to_box(x: CoordX, y: CoordY, w: Width, h: Height) -> BoxList:
    return [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]

def wh_to_box_list(w: Width, h: Height) -> BoxList:
    """ Caja centrada en el origen de dimensiones `w` y `h`."""
    return [(0,0), (w,0), (w,h), (0,h)]


T_BBox = TypeVar("T_BBox", bound="BBox")

class BBox:     # Esto quizás se podría pasar a pydantic, ver.
    """
    FIXME: Bastante entrelazada la lógica, hay q optimizar.

    La caja se crea a partir de un polígono estático, trasladado con `pt_ref`.

    - pt_ref = (x1,y1)
    - x2=x1+w ^ y2=y1+h
    - xy_tl=(x1,y1) +--------+ xy_tr=(x2,y1)
    - xy_bl=(x1,y2) +--------+ xy_br=(x2,y2)
    """
    def __init__(self, pt_geom: Point, w: Width, h: Height):
        assert isinstance(pt_geom, Point)
        self.pt_ref = pt_geom
        self.box = Polygon(shp.Polygon(wh_to_box_list(w=w, h=h)))
        self.w = w
        self.h = h
    
    @property
    def coords(self) -> CoordsXY:
        return self.box.coords + self.pt_ref.coords

    @property
    def xywh(self) -> BoxList:
        return [self.pt_ref.x, self.pt_ref.y, self.w, self.h]

    @classmethod
    def from_box(cls: Type[T_BBox], box: BoxList) -> T_BBox:
        """ FIXME: Muy sucio."""
        pt_ref = Point(shp.Point(box[0], box[1]))
        return cls(pt_ref, box[2], box[3])

    # TODO: Agregar repr y str.