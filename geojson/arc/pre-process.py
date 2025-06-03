import json

# Sample irregular polygons roughly around city centers
# Coordinates are [lon, lat], rings closed (first==last)
italian_cities = [
    {
        "name": "Florence",
        "flows": {str(i): i * 10 for i in range(10)},
        "centroid": [11.2558, 43.7696, 0],
        "polygon": [
            [11.20, 43.80],
            [11.30, 43.80],
            [11.35, 43.75],
            [11.25, 43.70],
            [11.18, 43.73],
            [11.20, 43.80],
        ],
    },
    {
        "name": "Rome",
        "flows": {str(i): i * 15 for i in range(10)},
        "centroid": [12.4964, 41.9028, 0],
        "polygon": [
            [12.40, 41.95],
            [12.55, 41.95],
            [12.60, 41.85],
            [12.50, 41.80],
            [12.45, 41.85],
            [12.40, 41.95],
        ],
    },
    {
        "name": "Milan",
        "flows": {str(i): i * 12 for i in range(10)},
        "centroid": [9.1900, 45.4642, 0],
        "polygon": [
            [9.10, 45.50],
            [9.30, 45.50],
            [9.35, 45.40],
            [9.25, 45.35],
            [9.15, 45.40],
            [9.10, 45.50],
        ],
    },
    {
        "name": "Venice",
        "flows": {str(i): i * 8 for i in range(10)},
        "centroid": [12.3155, 45.4408, 0],
        "polygon": [
            [12.25, 45.50],
            [12.38, 45.50],
            [12.40, 45.43],
            [12.30, 45.40],
            [12.28, 45.43],
            [12.25, 45.50],
        ],
    },
    {
        "name": "Naples",
        "flows": {str(i): i * 14 for i in range(10)},
        "centroid": [14.2681, 40.8518, 0],
        "polygon": [
            [14.20, 40.90],
            [14.35, 40.90],
            [14.38, 40.85],
            [14.25, 40.80],
            [14.18, 40.83],
            [14.20, 40.90],
        ],
    },
    {
        "name": "Turin",
        "flows": {str(i): i * 11 for i in range(10)},
        "centroid": [7.6869, 45.0703, 0],
        "polygon": [
            [7.60, 45.12],
            [7.75, 45.12],
            [7.78, 45.05],
            [7.70, 45.00],
            [7.65, 45.03],
            [7.60, 45.12],
        ],
    },
    {
        "name": "Bologna",
        "flows": {str(i): i * 9 for i in range(10)},
        "centroid": [11.3426, 44.4949, 0],
        "polygon": [
            [11.28, 44.54],
            [11.40, 44.54],
            [11.42, 44.48],
            [11.35, 44.44],
            [11.30, 44.46],
            [11.28, 44.54],
        ],
    },
    {
        "name": "Genoa",
        "flows": {str(i): i * 13 for i in range(10)},
        "centroid": [8.9463, 44.4056, 0],
        "polygon": [
            [8.85, 44.45],
            [9.00, 44.45],
            [9.02, 44.40],
            [8.90, 44.38],
            [8.87, 44.40],
            [8.85, 44.45],
        ],
    },
    {
        "name": "Palermo",
        "flows": {str(i): i * 7 for i in range(10)},
        "centroid": [13.3615, 38.1157, 0],
        "polygon": [
            [13.30, 38.16],
            [13.42, 38.16],
            [13.45, 38.10],
            [13.35, 38.05],
            [13.31, 38.08],
            [13.30, 38.16],
        ],
    },
    {
        "name": "Verona",
        "flows": {str(i): i * 10 for i in range(10)},
        "centroid": [10.9916, 45.4384, 0],
        "polygon": [
            [10.90, 45.48],
            [11.05, 45.48],
            [11.08, 45.43],
            [11.00, 45.40],
            [10.95, 45.43],
            [10.90, 45.48],
        ],
    },
]

features = []
for city in italian_cities:
    coords = city["polygon"]
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    feature = {
        "type": "Feature",
        "properties": {
            "name": city["name"],
            "flows": city["flows"],
            "centroid": city["centroid"],
        },
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [[[coords]]],
        },
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features,
}

with open("italian_cities.json", "w") as f:
    json.dump(geojson, f, indent=2)

print("GeoJSON saved to italian_cities.geojson")
