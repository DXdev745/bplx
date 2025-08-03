import struct

# --- MODEL DATA ---
# We'll keep the cube mesh and material data from before
cube_data = {
    "materials": [
        {"name": "ShinyRed", "diffuse_color": [1.0, 0.0, 0.0], "specular_color": [1.0, 1.0, 1.0], "shininess": 200.0, "emissive_color": [0.0, 0.0, 0.0], "transparency": 1.0, "is_textured": False, "texture_path": None}
    ],
    "meshes": [
        {"name": "Cube_Mesh", "material_index": 0, "vertices": [
            {"position": [-1.0, -1.0, 1.0], "normal": [-0.57735, -0.57735, 0.57735], "uv": [0.0, 0.0]},
            {"position": [1.0, -1.0, 1.0], "normal": [0.57735, -0.57735, 0.57735], "uv": [1.0, 0.0]},
            {"position": [-1.0, 1.0, 1.0], "normal": [-0.57735, 0.57735, 0.57735], "uv": [0.0, 1.0]},
            {"position": [1.0, 1.0, 1.0], "normal": [0.57735, 0.57735, 0.57735], "uv": [1.0, 1.0]},
            {"position": [-1.0, -1.0, -1.0], "normal": [-0.57735, -0.57735, -0.57735], "uv": [1.0, 0.0]},
            {"position": [1.0, -1.0, -1.0], "normal": [0.57735, -0.57735, -0.57735], "uv": [0.0, 0.0]},
            {"position": [-1.0, 1.0, -1.0], "normal": [-0.57735, 0.57735, -0.57735], "uv": [1.0, 1.0]},
            {"position": [1.0, 1.0, -1.0], "normal": [0.57735, 0.57735, -0.57735], "uv": [0.0, 1.0]}
        ], "faces": [[0, 2, 3], [0, 3, 1], [4, 5, 7], [4, 7, 6], [4, 6, 2], [4, 2, 0], [1, 3, 7], [1, 7, 5], [2, 6, 7], [2, 7, 3], [4, 0, 1], [4, 1, 5]]}
    ]
}

# --- SKELETON DATA ---
# A simple two-bone skeleton: one root and one child
skeleton_data = {
    "bones": [
        {"name": "RootBone", "parent_index": -1, "rest_pos": [0.0, 0.0, 0.0], "rest_rot": [0.0, 0.0, 0.0, 1.0], "rest_scale": [1.0, 1.0, 1.0]},
        {"name": "ChildBone", "parent_index": 0, "rest_pos": [0.0, 2.0, 0.0], "rest_rot": [0.0, 0.0, 0.0, 1.0], "rest_scale": [1.0, 1.0, 1.0]}
    ]
}

# --- ANIMATION DATA ---
# A single animation clip that moves the child bone over time
animation_data = {
    "clips": [
        {"name": "SimpleMovement", "length": 2.0, "keyframes": [
            {"time": 0.0, "bone_index": 1, "pos": [0.0, 2.0, 0.0], "rot": [0.0, 0.0, 0.0, 1.0], "scale": [1.0, 1.0, 1.0]},
            {"time": 1.0, "bone_index": 1, "pos": [2.0, 2.0, 0.0], "rot": [0.0, 0.0, 0.0, 1.0], "scale": [1.0, 1.0, 1.0]},
            {"time": 2.0, "bone_index": 1, "pos": [0.0, 2.0, 0.0], "rot": [0.0, 0.0, 0.0, 1.0], "scale": [1.0, 1.0, 1.0]}
        ]}
    ]
}

def create_advanced_bplx(filename):
    mesh = cube_data["meshes"][0]
    materials = cube_data["materials"]
    
    # Extract data for packing
    vertex_positions = [val for v in mesh["vertices"] for val in v["position"]]
    vertex_normals = [val for v in mesh["vertices"] for val in v["normal"]]
    vertex_uvs = [val for v in mesh["vertices"] for val in v["uv"]]
    face_indices = [val for f in mesh["faces"] for val in f]
    
    # Calculate counts
    vertex_count = len(mesh["vertices"])
    face_count = len(mesh["faces"])
    material_count = len(materials)
    bone_count = len(skeleton_data["bones"])
    clip_count = len(animation_data["clips"])

    with open(filename, 'wb') as f:
        # Step 1: Write the existing header
        f.write(b'BPLX')
        f.write(struct.pack('IIIII', 1, vertex_count, face_count, material_count, 0)) # Version, counts, padding
        
        # Step 2: Write vertex and face data
        f.write(struct.pack(f'{len(vertex_positions)}f', *vertex_positions))
        f.write(struct.pack(f'{len(vertex_normals)}f', *vertex_normals))
        f.write(struct.pack(f'{len(vertex_uvs)}f', *vertex_uvs))
        f.write(struct.pack(f'{len(face_indices)}I', *face_indices))

        # --- NEW SECTION: WRITE SKELETON DATA ---
        f.write(struct.pack('I', bone_count))
        for bone in skeleton_data["bones"]:
            name_bytes = bone["name"].encode('utf-8')
            f.write(struct.pack('I', len(name_bytes))) # Name length
            f.write(name_bytes)                        # Name
            f.write(struct.pack('i', bone["parent_index"])) # Parent index (signed int)
            f.write(struct.pack('3f', *bone["rest_pos"])) # Rest position
            f.write(struct.pack('4f', *bone["rest_rot"])) # Rest rotation (quaternion)
            f.write(struct.pack('3f', *bone["rest_scale"])) # Rest scale

        # --- NEW SECTION: WRITE ANIMATION DATA ---
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

    print(f"Advanced BPLX file '{filename}' created with skeleton and animation successfully!")

# Run the encoder to create the advanced binary file
create_advanced_bplx("animated_cube.bplx")
