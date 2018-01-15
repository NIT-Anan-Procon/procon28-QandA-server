# -*- coding: utf-8 -*-

import collections
from shapely.geometry import Polygon, Point
from rtree import index

Area = collections.namedtuple('Area', ['area_id', 'polygon'])


class ReverseGeocoder():
    def __init__(self):
        self.idx = index.Index()

    def insert_from_iterator(self, itr):
        for i, (area_id, polygon) in enumerate(itr):
            obj = Area(area_id=area_id, polygon=polygon)
            self.idx.insert(i, polygon.bounds, obj)

    def contains(self, lat, lon):
        result = []
        point = Point(lat, lon)
        for hit in self.idx.intersection(point.bounds, objects=True):
            if hit.object.polygon.contains(point):
                result.append(hit.object)
        if len(result) > 1:
            result.sort(key=lambda x: (x.polygon.area, x.area_id))
        return [r.area_id for r in result]

    def address(self, latlng):
        lat, lng = list(map(float, latlng.split("/")))
        return self.contains(lat, lng)

    def __repr__(self):
        return '<ReverseGeocoder contains {} polygons>'.format(self.idx.count(self.idx.bounds))