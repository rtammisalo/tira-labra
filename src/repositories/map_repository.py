import os


class MapRepository:
    """ A utility class for loading maps.
    """

    def __init__(self):
        self._dir = "maps"
        self._map_files = set(["AR0011SR.map", "AR0516SR.map", "AR0711SR.map",
                               "AR0012SR.map", "AR0203SR.map", "AR0700SR.map",
                               "AR0400SR.map", "AR0511SR.map", "huge.map",
                               "dijkstra_wins.map"])

    def read_map(self, map_file):
        """ Reads the map indicated by map_file. Returns a tuple of
        (map description, definition of the map as a string).
        """
        with open(map_file, "r", encoding="utf-8") as file:
            file.readline()
            height = int(file.readline().split()[1])
            width = int(file.readline().split()[1])
            map_decorator = file.readline()
            if not "map" in map_decorator:
                raise Exception("Error: Unknown map format.")

            map_string = "\n".join(file.readlines())
            map_description = f"Map file: {map_file}, {width}x{height} = {width * height} cells."

        return map_description, map_string


    def iter_maps(self):
        """ Loads all known maps. Yields a map (description, map_string) tuple per map
        to the caller.
        """
        for map_file in self._map_files:
            filename = os.path.join(self._dir, map_file)
            map_desc, map_string = self.read_map(filename)
            yield map_desc, map_string
