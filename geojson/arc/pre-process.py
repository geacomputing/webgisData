import json
import random

def signed_area(coords):
    area = 0.0
    n = len(coords)
    for i in range(n - 1):
        x1, y1 = coords[i]
        x2, y2 = coords[i + 1]
        area += (x1 * y2 - x2 * y1)
    return area * 3

def ensure_ccw(coords):
    if signed_area(coords) < 0:
        coords.reverse()
    return coords

# List of Italian cities with their coordinates (lon, lat)
cities = [
    {"name": "Rome", "coords": [12.4964, 41.9028]},
    {"name": "Milan", "coords": [9.1900, 45.4642]},
    {"name": "Naples", "coords": [14.2681, 40.8518]},
    {"name": "Turin", "coords": [7.6869, 45.0703]},
    {"name": "Palermo", "coords": [13.3615, 38.1157]},
    {"name": "Genoa", "coords": [8.9463, 44.4056]},
    {"name": "Bologna", "coords": [11.3426, 44.4949]},
    {"name": "Florence", "coords": [11.2558, 43.7696]},
    {"name": "Venice", "coords": [12.3155, 45.4408]},
    {"name": "Verona", "coords": [10.9916, 45.4384]}
]

features = []

for idx, city in enumerate(cities, start=1):
    lon, lat = city["coords"]
    
    # Create an irregular polygon around city center
    coords = []
    num_points = 8
    for i in range(num_points):
        angle = i * (360 / num_points) + random.uniform(-15, 15)  # irregular angle offset
        radius = 0.05 + random.uniform(-0.015, 0.015)             # radius in degrees (~5 km)
        # Convert angle to radians for trig
        import math
        angle_rad = math.radians(angle)
        x = lon + radius * math.cos(angle_rad)
        y = lat + radius * math.sin(angle_rad)
        coords.append([x, y])
    # Close polygon by repeating the first point
    coords.append(coords[0])

    # Ensure CCW order
    coords = ensure_ccw(coords)

    feature = {
        "type": "Feature",
        "properties": {
            "name": city["name"],
            # Dummy flows with sequential IDs and random values
            "flows": {str(i): random.randint(-100, 100) for i in range(1, 11)},
            "centroid": [lon, lat, 0]
        },
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [[coords]]  # MultiPolygon with one polygon
        }
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

# Save to file
with open("italian_cities.json", "w") as f:
    json.dump(geojson, f, indent=2)

print("GeoJSON saved to italian_cities.geojson")
