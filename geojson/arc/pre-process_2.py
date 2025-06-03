"""
Created on Tue Jun  3 16:58:52 2025

@author: EMS GEA Computing
-Through Numbers the Earth
"""




"""
{
    "type": "Feature",
    "properties": {
      "name": "Italia",
      "flows": {
        "18": 999, "26": 999, "35": 999, "46": 999, "69": 999, "72": 999, "80": 999, "99": 999,
        "106": 999, "141": 999, "145": 999, "186": 999, "266": 999, "333": 999, "335": 999,
        "336": 999, "394": 999, "453": 999, "473": 999, "477": 999, "488": 999, "571": 999,
        "584": 999, "610": 999, "686": 999, "694": 999, "702": 999, "747": 999, "771": 999,
        "876": 999, "879": 999, "953": 999, "993": 999, "1007": 999, "1015": 999, "1017": 999,
        "1042": 999, "1043": 999, "1091": 999, "1104": 999, "1186": 999, "1227": 999, "1403": 999,
        "1410": 999, "1414": 999, "1418": 999, "1468": 999, "1473": 999, "1481": 999, "1482": 999,
        "1510": 999, "1540": 999, "1565": 999, "1567": 999, "1582": 999, "1585": 999, "1648": 999,
        "1714": 999, "1781": 999, "1791": 999, "1799": 999, "1800": 999, "1829": 999, "1885": 999,
        "1911": 999, "1961": 999, "1991": 999, "2062": 999, "2094": 999, "2095": 999, "2166": 999,
        "2279": 999, "2283": 999, "2357": 999, "2363": 999, "2374": 999, "2388": 999, "2406": 999,
        "2430": 999, "2452": 999, "2468": 999, "2475": 999, "2555": 999, "2583": 999, "2706": 999,
        "2786": 999, "2874": 999, "2902": 999, "2926": 999, "2976": 999, "2998": 999, "3017": 999,
        "3033": 999, "3110": 999, "3135": 999, "3141": 999
      },
      "centroid": [12.4964, 41.9028, 0]
    },
    "geometry": {
      "type": "MultiPolygon",
      "coordinates": [[[
          [12.0, 42.4],
	  [13.0, 42.4],
	  [13.0, 41.4],
	  [12.0, 41.4],
	  [12.0, 42.4]
      ]]]
    }
  }

"""

import geopandas as gpd
from shapely.geometry import mapping


fileIN ="./limits_IT_regions.geojson" 

df = gpd.read_file(fileIN)

    
def strip_z(coord):
    """Ensure coord is a list of [lon, lat], stripping Z if present."""
    if isinstance(coord, (list, tuple)) and len(coord) >= 2:
        return list(coord[:2])
    raise ValueError(f"Invalid coordinate: {coord}")

def close_ring(ring):
    cleaned = [strip_z(pt) for pt in ring]
    if cleaned[0] != cleaned[-1]:
        cleaned.append(cleaned[0])
    return cleaned

def to_pairs(ring):
    """Convert flat [x1, y1, x2, y2, ...] or 3D [[x, y, z], ...] to 2D [[x, y], ...]"""
    if isinstance(ring[0], (float, int)):
        ring = [[ring[i], ring[i + 1]] for i in range(0, len(ring) - 1, 2)]
    else:
        ring = [[pt[0], pt[1]] for pt in ring]
    return ring

def close_ring(ring):
    if ring[0] != ring[-1]:
        ring.append(ring[0])
    return ring

def simplify_ring(ring, step=10):
    ring = to_pairs(ring)
    ring = ring[::step]  # take every nth point
    return close_ring(ring)

def simplify_geometry_coords(coords, step=10):
    coords = json.loads(json.dumps(coords))  # convert any tuples to lists
    return [
        [simplify_ring(ring, step=step) for ring in polygon]
        for polygon in coords
    ]




import json

features = []

for item in df.reg_name:
    geometry = df[df['reg_name'] == item].geometry.values[0]
    centroid = geometry.centroid
    x = centroid.x
    y = centroid.y


    coords_raw = mapping(geometry)['coordinates']
    simplified_coords = simplify_geometry_coords(coords_raw, step=10350)


  
    
    feature = {
        "type": "Feature",
        "properties": {
            "name": item,
            "flows": {
              "18": 999, "26": 999, "35": 999, "46": 999, "69": 999, "72": 999, "80": 999, "99": 999,
              "106": 999, "141": 999, "145": 999, "186": 999, "266": 999, "333": 999, "335": 999,
              "336": 999, "394": 999, "453": 999, "473": 999, "477": 999, "488": 999, "571": 999,
              "584": 999, "610": 999, "686": 999, "694": 999, "702": 999, "747": 999, "771": 999,
              "876": 999, "879": 999, "953": 999, "993": 999, "1007": 999, "1015": 999, "1017": 999,
              "1042": 999, "1043": 999, "1091": 999, "1104": 999, "1186": 999, "1227": 999, "1403": 999,
              "1410": 999, "1414": 999, "1418": 999, "1468": 999, "1473": 999, "1481": 999, "1482": 999,
              "1510": 999, "1540": 999, "1565": 999, "1567": 999, "1582": 999, "1585": 999, "1648": 999,
              "1714": 999, "1781": 999, "1791": 999, "1799": 999, "1800": 999, "1829": 999, "1885": 999,
              "1911": 999, "1961": 999, "1991": 999, "2062": 999, "2094": 999, "2095": 999, "2166": 999,
              "2279": 999, "2283": 999, "2357": 999, "2363": 999, "2374": 999, "2388": 999, "2406": 999,
              "2430": 999, "2452": 999, "2468": 999, "2475": 999, "2555": 999, "2583": 999, "2706": 999,
              "2786": 999, "2874": 999, "2902": 999, "2926": 999, "2976": 999, "2998": 999, "3017": 999,
              "3033": 999, "3110": 999, "3135": 999, "3141": 999
            },  # Or replace with actual keys
            "centroid": [x, y, 0]
        },
        "geometry": {
                "type": "MultiPolygon",
                "coordinates": simplified_coords
            } 
    }

    features.append(feature)
    


# Wrap in a FeatureCollection
geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Save to file
output_path = "italian_regions_with_flows.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(geojson, f, indent=2)