import json
import random

def create_irregular_polyline(lon, lat, num_points=10, max_offset=1.15):
    points = []
    angle_step = 360 / num_points
    
    for i in range(num_points):
        angle = angle_step * i + random.uniform(-angle_step/3, angle_step/3)
        rad = angle * 3.14159 / 180
        radius = random.uniform(max_offset * 0.5, max_offset)
        offset_lon = lon + radius * random.uniform(0.5, 1.0) * random.choice([-1, 1]) * abs(random.uniform(0.7, 1.0)) * 0.7
        offset_lat = lat + radius * random.uniform(0.5, 1.0) * random.choice([-1, 1]) * abs(random.uniform(0.7, 1.0)) * 0.7
        points.append([round(offset_lon, 6), round(offset_lat, 6)])
    
    points.append(points[0])  # close polygon
    return points

italian_cities = [
    {"name": "Rome", "coordinates": (12.4964, 41.9028)},
    {"name": "Milan", "coordinates": (9.1900, 45.4642)},
    {"name": "Naples", "coordinates": (14.2681, 40.8518)},
    {"name": "Turin", "coordinates": (7.6869, 45.0703)},
    {"name": "Palermo", "coordinates": (13.3615, 38.1157)},
    {"name": "Genoa", "coordinates": (8.9463, 44.4056)},
    {"name": "Bologna", "coordinates": (11.3426, 44.4949)},
    {"name": "Florence", "coordinates": (11.2558, 43.7696)},
    {"name": "Venice", "coordinates": (12.3155, 45.4408)},
    {"name": "Verona", "coordinates": (10.9916, 45.4384)}
]

features = []

for city in italian_cities:
    lon, lat = city["coordinates"]
    polygon_coords = create_irregular_polyline(lon, lat)

    # Create a flows dictionary with keys as string sequential IDs and random scalar values
    flows = {str(i): random.randint(-100, 100) for i in range(1, 10)}  # 5 random flows
    
    feature = {
        "type": "Feature",
        "properties": {
            "name": city["name"],
            "flows": flows
        },
        "centroid": [lon, lat, 0],
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [[[polygon_coords]]]
        }
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

print(json.dumps(geojson, indent=2))


def ensure_multipolygon_validity(features):
    """
    Ensures each MultiPolygon in features:
    - Has correct nesting
    - Each linear ring is closed (first point == last point)
    """

    for feature in features:
        geom = feature.get('geometry', {})
        if geom.get('type') == 'MultiPolygon':
            new_coords = []
            for polygon in geom['coordinates']:
                new_polygon = []
                for ring in polygon:
                    # Ensure ring is a list of coordinates
                    if len(ring) == 0:
                        continue
                    # Close the ring if not closed
                    if ring[0] != ring[-1]:
                        ring = ring + [ring[0]]
                    new_polygon.append(ring)
                new_coords.append(new_polygon)
            # Replace with corrected coordinates
            feature['geometry']['coordinates'] = new_coords

    return features


def fix_geojson_for_deckgl(data):
    for feature in data.get('features', []):
        geom = feature.get('geometry', {})
        if geom.get('type') == 'MultiPolygon':
            fixed_coords = []
            for polygon in geom['coordinates']:
                fixed_polygon = []
                for ring in polygon:
                    if not ring:
                        continue  # skip empty rings
                    # Remove altitude if present (keep only first 2 coords)
                    ring_2d = [[pt[0], pt[1]] for pt in ring]

                    # Close ring if not closed
                    if ring_2d[0] != ring_2d[-1]:
                        ring_2d.append(ring_2d[0])
                    fixed_polygon.append(ring_2d)
                fixed_coords.append(fixed_polygon)
            feature['geometry']['coordinates'] = fixed_coords
    return data


geojson= fix_geojson_for_deckgl(geojson)

with open('italian_cities_flows.json', 'w') as f:
    json.dump(geojson, f, indent=2)
