def parse_obj(filename):
    """
    Parses a simple OBJ file and returns a dictionary of data.
    """
    vertices = []
    normals = []
    uvs = []
    faces = []

    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == 'v':
                # Parse vertex positions
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif parts[0] == 'vn':
                # Parse vertex normals
                normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif parts[0] == 'vt':
                # Parse texture coordinates (UVs)
                uvs.append([float(parts[1]), float(parts[2])])
            elif parts[0] == 'f':
                # Parse faces
                face = []
                for part in parts[1:]:
                    # Each part is like 'v/vt/vn', so we split by '/'
                    # We only care about the vertex index (the first number) for now
                    face.append(int(part.split('/')[0]))
                faces.append(face)

    print(f"Parsed OBJ file: {filename}")
    print(f"Found {len(vertices)} vertices, {len(normals)} normals, {len(uvs)} uvs.")
    print(f"Found {len(faces)} faces.")
    print("\n--- First Vertex ---")
    print(vertices[0])
    print("\n--- First Face (indices) ---")
    print(faces[0])

    # We can return the data to use later
    return {
        "vertices": vertices,
        "normals": normals,
        "uvs": uvs,
        "faces": faces
    }


# Run the parser with our test file
parse_obj("cube.obj")
