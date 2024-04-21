import overpass


def get_maramures_communes():
    # Interogare Overpass pentru a obține toate comunele din județul Maramureș
    api = overpass.API()
    query = """
    area["name"="Maramureș"]->.searchArea;
    (
      node["place"="village"](area.searchArea);
      way["place"="village"](area.searchArea);
      relation["place"="village"](area.searchArea);
    );
    out;
    """
    response = api.get(query)

    # Extragerea numelor localităților, longitudinii și latitudinii
    communes_info = []
    for feature in response["features"]:
        commune_name = feature["properties"]["name"]
        lon, lat = feature["geometry"]["coordinates"]
        communes_info.append({"name": commune_name, "lon": lon, "lat": lat})

    return communes_info


# Obținem lista de comune din Maramureș și sortăm după numărul de locuitori
maramures_communes_data = get_maramures_communes()
