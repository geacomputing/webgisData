"""
GeoJsonLayer
===========

Property values in Vancouver, Canada, adapted from the deck.gl example pages.
"""


import math

import pandas as pd
import pydeck as pdk
import geopandas as gpd
import xarray as xr
import numpy as np

# Load NetCDF
netcdfPath = r'Production_Total_maksed_Italy.nc'
band = 'Band30'
ds = xr.open_dataset(netcdfPath)[band]

# Grid spacing
dx = ds.lon.diff(dim='lon').mean().values
dy = ds.lat.diff(dim='lat').mean().values

assert np.abs(dx - dy) < 0.01, f"dx and dy differ too much: dx={dx}, dy={dy}"

# Extract lat, lon, and values
lat = ds['lat'].values
lon = ds['lon'].values
data = ds.values

# Flatten grid
lon_grid, lat_grid = np.meshgrid(lon, lat)
flat_lon = lon_grid.flatten()
flat_lat = lat_grid.flatten()
flat_val = data.flatten()

# Remove NaNs
mask = ~np.isnan(flat_val)
flat_lon = flat_lon[mask]
flat_lat = flat_lat[mask]
flat_val = flat_val[mask]



def make_polygon(lon, lat, dx, dy, shrink=.5):
    hdx, hdy = dx / 2, dy / 2
    hdx, hdy = shrink*hdx, shrink*hdy
    return [[
        [lon - hdx, lat - hdy],
        [lon + hdx, lat - hdy],
        [lon + hdx, lat + hdy],
        [lon - hdx, lat + hdy],
        [lon - hdx, lat - hdy],
    ]]

# Create DataFrame
df = pd.DataFrame({
    "lon": flat_lon,
    "lat": flat_lat,
    "value": flat_val
})

# Add geometry
df["coordinates"] = df.apply(lambda row: make_polygon(row["lon"], row["lat"], dx, dy), axis=1)
df["WaterStress"] = np.random.choice(["apple", "banana", "cherry", "date", "elderberry"])
df["Depletion"] = np.random.choice(["apple", "banana", "cherry", "date", "elderberry"])
df["Draught"] = np.random.choice(["apple", "banana", "cherry", "date", "elderberry"])
df["Decline"] = df.apply(lambda row: np.random.choice(["apple", "banana", "cherry", "date", "elderberry"]))
# Add elevation: scaled from raw value
df["elevation"] = df["value"].apply(lambda v: math.sqrt(v) * 5 if v > 0 else 0)
df["Production"] = (df["value"] /1000000).apply(lambda x: f"{x:.2f}")
# Add fill color from color scale (based on normalized value)
min_val = df["value"].min()
max_val = df["value"].max()
df["norm"] = (df["value"] - min_val) / (max_val - min_val + 1e-8)  # avoid div0


#df["fill_color"] = json["features"].apply(lambda row: color_scale(row["properties"]["growth"]))
# Optional: drop intermediate norm column
#df.drop(columns="norm", inplace=True)


# Load in the JSON data
DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
json = pd.read_json(DATA_URL)
#df = pd.DataFrame()

# Custom color scale



# Define the color scale function
def color_scale(val):
    COLOR_RANGE = [
        [255, 255, 255],  # white
        [230, 245, 255],
        [198, 219, 239],
        [158, 202, 225],
        [107, 174, 214],
        [66, 146, 198],
        [33, 113, 181],
        [8, 81, 156],
        [8, 48, 107],
        [3, 19, 43]       # dark blue
    ]
    BREAKS = [0, 5, 10, 20, 25, 30, 25, 40, 45, 50]
    for i, b in enumerate(BREAKS):
        if val < b:
            return COLOR_RANGE[i]
    return COLOR_RANGE[-1]  # fallback to last color





df["fill_color"] = (df["value"] /1000000).apply(lambda v: color_scale(v))



#df["fill_color"] = json["features"].apply(lambda row: color_scale(['norm']))
# Add sunlight shadow to the polygons
sunlight = {
    "@@type": "_SunLight",
    "timestamp": 1564696800000,  # Date.UTC(2019, 7, 1, 22),
    "color": [255, 255, 255],
    "intensity": .95,
    "_shadow": True,
}

ambient_light = {"@@type": "AmbientLight", "color": [255, 255, 255], "intensity": 1.0}

lighting_effect = {
    "@@type": "LightingEffect",
    "shadowColor": [0, 0, 0, 0.5],
    "ambientLight": ambient_light,
    "directionalLights": [sunlight],
}

view_state = pdk.ViewState(
    **{"latitude": 39.254, "longitude": 12.93, "zoom": 6, "maxZoom": 16, "pitch": 45, "bearing": 0}
)

LAND_COVER = [[
    [6.627, 36.619],   # Bottom-left (SW)
    [6.627, 47.095],   # Top-left (NW)
    [18.784, 47.095],  # Top-right (NE)
    [18.784, 36.619],  # Bottom-right (SE)
    [6.627, 36.619]    # Close polygon
]]
polygon_layer = pdk.Layer(
    "PolygonLayer",
    LAND_COVER,
    stroked=False,
    # processes the data as a flat longitude-latitude pair
    get_polygon="-",
    get_fill_color=[0, 0, 0, 20],
)

polygon_layer = pdk.Layer(
    "PolygonLayer",
    df,
    id="geojson",
    opacity=0.8,
    stroked=False,
    get_polygon="coordinates",
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="elevation",
    get_fill_color="fill_color",
    get_line_color=[255, 255, 255],
    auto_highlight=True,
    pickable=True,
)




tooltip = {
    "html": "<b>Total Production:</b> {Production} milions of mc<br />" +
             " _ <br /> " + 
            " <br /> Aqueduct 4.0 Indicators:<br />" + 
            "<b>Water Stress:</b> {WaterStress}<br />" +
            "<b>Water Depletion:</b> {Depletion}<br />" +
            "<b>Table Decline:</b> {Draught}<br />" +
            "<b>Drought Risk:</b> {Decline}<br />"
}








geojson_url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"


geo = gpd.read_file("limits_IT_regions.geojson")
# Load GeoJSON file from disk
# with open("your_file.geojson", "r", encoding="utf-8") as f:
#     geojson_data = json.load(f)

# Create GeoJsonLayer
geojson_layer = pdk.Layer(
    "GeoJsonLayer",
    geojson_url,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    get_fill_color=[50, 50, 50, 10],  # semi-transparent red
    get_line_color=[0, 0, 0],
    line_width_min_pixels=1
)


r = pdk.Deck(
    layers=[polygon_layer, geojson_layer],
    initial_view_state=view_state,
    #effects=[lighting_effect],
    map_style=pdk.map_styles.LIGHT,
    tooltip=tooltip,
)









if False:
    html = r.to_html(as_string=True)
    # Define the slider HTML and JavaScript
    slider_html = """
    <div style="position:absolute; top:10px; left:10px; z-index:10; background:white; padding:8px;">
      Opacity:
      <input type="range" id="opacity-slider" min="0" max="1" step="0.01" value="0.8">
    </div>
    """
    
    slider_js = """
<script>
  const slider = document.getElementById('opacity-slider');

  // Patch deck.gl instance setup
  const oldDeckGL = deck.DeckGL;
  deck.DeckGL = function (props) {
    const instance = new oldDeckGL(props);
    window.deckgl = instance; // 👈 make it global
    return instance;
  };

  slider.addEventListener('input', () => {
    const opacity = parseFloat(slider.value);
    console.log("Slider changed:", opacity);

    if (!window.deckgl) {
      console.error("deckgl is still undefined!");
      return;
    }

    const layers = window.deckgl.props.layers.map(layer => {
      console.log("Updating layer:", layer.constructor.name);
      return new deck[layer.constructor.name]({
        ...layer.props,
        opacity: opacity
      });
    });

    window.deckgl.setProps({ layers });
  });
</script>

    """
    
    # Inject slider HTML just after <body>
    html = html.replace("<body>", f"<body>{slider_html}", 1)
    
    # Inject JS just before </body>
    html = html.replace("</body>", f"{slider_js}</body>", 1)
    
    
    
    
    with open("deck_opacity_slider.html", "w", encoding="utf-8") as f:
        f.write(html)


html = r.to_html(as_string=True)


# Replace the title tag
custom_title = "JustWATER - Dr. Francesca Greco"
html = html.replace("<title>pydeck</title>", f"<title>{custom_title}</title>")

# Save to file
with open("custom_map.html", "w", encoding="utf-8") as f:
    f.write(html)
