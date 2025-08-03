import struct

def read_binary_bplx(filename):
    """
    Reads a binary BPLX file and returns its header and data.
    """
    try:
        with open(filename, 'rb') as f:
            # Step 1: Read the header (24 bytes)
            # 'rb' means "read binary"
            
            magic_number = f.read(4).decode('ascii')
            if magic_number != 'BPLX':
                print(f"Error: Invalid file format. Magic number is '{magic_number}', expected 'BPLX'.")
                return None
            
            # Unpack the counts from the next 16 bytes
            header_data = struct.unpack('IIIII', f.read(20))
            version, vertex_count, face_count, material_count, padding = header_data

            print("--- BPLX Header ---")
            print(f"Magic Number: {magic_number}")
            print(f"Version: {version}.0")
            print(f"Vertex Count: {vertex_count}")
            print(f"Face Count: {face_count}")
            print(f"Material Count: {material_count}")
            
            # Step 2: Read the vertex data
            print("\n--- Reading Vertex Data ---")
            # Unpack all vertex positions (3 floats per vertex)
            position_count = vertex_count * 3
            positions = struct.unpack(f'{position_count}f', f.read(position_count * 4))

            # Unpack all vertex normals (3 floats per vertex)
            normal_count = vertex_count * 3
            normals = struct.unpack(f'{normal_count}f', f.read(normal_count * 4))

            # Unpack all vertex UVs (2 floats per vertex)
            uv_count = vertex_count * 2
            uvs = struct.unpack(f'{uv_count}f', f.read(uv_count * 4))
            
            print(f"  Successfully read {len(positions) // 3} vertex positions.")
            print(f"  Successfully read {len(normals) // 3} vertex normals.")
            print(f"  Successfully read {len(uvs) // 2} vertex UVs.")
            
            # Step 3: Read the face data
            print("\n--- Reading Face Data ---")
            # Unpack all face indices (3 unsigned integers per face)
            face_index_count = face_count * 3
            faces = struct.unpack(f'{face_index_count}I', f.read(face_index_count * 4))
            
            print(f"  Successfully read {len(faces) // 3} faces.")
            
            # A simple sanity check on the data
            print("\n--- Sanity Check ---")
            print(f"First Vertex Position: ({positions[0]}, {positions[1]}, {positions[2]})")
            print(f"First Face (indices): ({faces[0]}, {faces[1]}, {faces[2]})")
            
            print("\nBinary BPLX file read successfully!")

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the decoder to read our binary file
read_binary_bplx("cube.bplx_bin")

