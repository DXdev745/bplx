import struct

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
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif parts[0] == 'vn':
                normals.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif parts[0] == 'vt':
                uvs.append([float(parts[1]), float(parts[2])])
            elif parts[0] == 'f':
                face = []
                for part in parts[1:]:
                    # OBJ uses v/vt/vn. We only need the vertex index (v)
                    # We also need to subtract 1 to convert from 1-based to 0-based
                    face.append(int(part.split('/')[0]) - 1)
                faces.append(face)

    return {
        "vertices": vertices,
        "normals": normals,
        "uvs": uvs,
        "faces": faces
    }

def create_bplx_from_obj(obj_data, output_filename):
    """
    Takes parsed OBJ data and writes it to a new BPLX file.
    """
    # --- SKELETON & ANIMATION DATA (for now, we'll keep it hardcoded for a cube) ---
    skeleton_data = {
        "bones": [
            {"name": "RootBone", "parent_index": -1, "rest_pos": [0.0, 0.0, 0.0], "rest_rot": [0.0, 0.0, 0.0, 1.0], "rest_scale": [1.0, 1.0, 1.0]},
            {"name": "ChildBone", "parent_index": 0, "rest_pos": [0.0, 2.0, 0.0], "rest_rot": [0.0, 0.0, 0.0, 1.0], "rest_scale": [1.0, 1.0, 1.0]}
        ]
    }
    animation_data = {
        "clips": [
            {"name": "SimpleMovement", "length": 2.0, "keyframes": [
                {"time": 0.0, "bone_index": 1, "pos": [0.0, 2.0, 0.0], "rot": [0.0, 0.0, 0.0, 1.0], "scale": [1.0, 1.0, 1.0]},
                {"time": 1.0, "bone_index": 1, "pos": [2.0, 2.0, 0.0], "rot": [0.0, 0.0, 0.0, 1.0], "scale": [1.0, 1.0, 1.0]},
                {"time": 2.0, "bone_index": 1, "pos": [0.0, 2.0, 0.0], "rot": [0.0, 0.0, 0.0, 1.0], "scale": [1.0, 1.0, 1.0]}
            ]}
        ]
    }

    # --- MATERIAL DATA (simple hardcoded material) ---
    materials = [
        {"name": "DefaultMaterial", "diffuse_color": [0.8, 0.8, 0.8], "specular_color": [1.0, 1.0, 1.0], "shininess": 100.0, "emissive_color": [0.0, 0.0, 0.0], "transparency": 1.0, "is_textured": False, "texture_path": None}
    ]

    # Extract data for packing
    vertex_positions = [val for v in obj_data["vertices"] for val in v]
    vertex_normals = [val for n in obj_data["normals"] for val in n]
    vertex_uvs = [val for uv in obj_data["uvs"] for val in uv]
    face_indices = [val for f in obj_data["faces"] for val in f]

    # Calculate counts
    vertex_count = len(obj_data["vertices"])
    face_count = len(obj_data["faces"])
    material_count = len(materials)
    bone_count = len(skeleton_data["bones"])
    clip_count = len(animation_data["clips"])

    with open(output_filename, 'wb') as f:
        # Step 1: Write the existing header
        f.write(b'BPLX')
        f.write(struct.pack('IIIII', 1, vertex_count, face_count, material_count, 0))

        # Step 2: Write vertex and face data
        f.write(struct.pack(f'{len(vertex_positions)}f', *vertex_positions))
        f.write(struct.pack(f'{len(vertex_normals)}f', *vertex_normals))
        f.write(struct.pack(f'{len(vertex_uvs)}f', *vertex_uvs))
        f.write(struct.pack(f'{len(face_indices)}I', *face_indices))

        # Step 3: Write SKELETON DATA
        f.write(struct.pack('I', bone_count))
        for bone in skeleton_data["bones"]:
            name_bytes = bone["name"].encode('utf-8')
            f.write(struct.pack('I', len(name_bytes)))
            f.write(name_bytes)
            f.write(struct.pack('i', bone["parent_index"]))
            f.write(struct.pack('3f', *bone["rest_pos"]))
            f.write(struct.pack('4f', *bone["rest_rot"]))
            f.write(struct.pack('3f', *bone["rest_scale"]))

        # Step 4: Write ANIMATION DATA
        f.write(struct.pack('I', clip_count))
        for clip in animation_data["clips"]:
            name_bytes = clip["name"].encode('utf-8')
            f.write(struct.pack('I', len(name_bytes)))
            f.write(name_bytes)
            f.write(struct.pack('f', clip["length"]))
            f.write(struct.pack('I', len(clip["keyframes"])))
            for keyframe in clip["keyframes"]:
                f.write(struct.pack('f', keyframe["time"]))
                f.write(struct.pack('I', keyframe["bone_index"]))
                f.write(struct.pack('3f', *keyframe["pos"]))
                f.write(struct.pack('4f', *keyframe["rot"]))
                f.write(struct.pack('3f', *keyframe["scale"]))

    print(f"\nSuccessfully converted '{input_filename}' to '{output_filename}'!")


# --- MAIN EXECUTION ---
# Define the input and output filenames
input_filename = "cube.obj"
output_filename = "converted_cube.bplx"

# Step A: Parse the OBJ file
obj_data = parse_obj(input_filename)

# Step B: Write the data to a BPLX file
create_bplx_from_obj(obj_data, output_filename)
