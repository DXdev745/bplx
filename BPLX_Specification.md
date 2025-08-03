# BPLX File Format Specification

## Overview
The BPLX file is a binary format designed for 3D models. All multi-byte values are stored in little-endian byte order.

## File Structure
The file is composed of several continuous data chunks:

1.  Header
2.  Materials
3.  Vertices
4.  Faces
5.  Skeletons
6.  Animations

### 1. Header (24 bytes)
* **Magic Number:** `4 bytes` (ASCII string `"BPLX"`)
* **Version:** `4 bytes` (unsigned integer, `1` for version 1.0)
* **Vertex Count:** `4 bytes` (unsigned integer)
* **Face Count:** `4 bytes` (unsigned integer)
* **Material Count:** `4 bytes` (unsigned integer)
* **Padding:** `4 bytes` (unsigned integer, reserved for future use)

### 2. Materials (variable size)
* **Count:** `4 bytes` (unsigned integer)
* **For each material:**
    * **Name Length:** `4 bytes` (unsigned integer)
    * **Name:** `variable bytes` (UTF-8 encoded string)
    * **Diffuse Color:** `12 bytes` (3 floats)
    * **Specular Color:** `12 bytes` (3 floats)
    * **Shininess:** `4 bytes` (float)
    * **Emissive Color:** `12 bytes` (3 floats)
    * **Transparency:** `4 bytes` (float)
    * **Is Textured:** `1 byte` (boolean, `0` or `1`)
    * **Texture Path Length:** `4 bytes` (unsigned integer)
    * **Texture Path:** `variable bytes` (UTF-8 encoded string)

### 3. Vertices (variable size)
* **Position Data:** `(Vertex Count * 3 * 4)` bytes (continuous stream of floats)
* **Normal Data:** `(Vertex Count * 3 * 4)` bytes (continuous stream of floats)
* **UV Data:** `(Vertex Count * 2 * 4)` bytes (continuous stream of floats)

### 4. Faces (variable size)
* **Face Indices:** `(Face Count * 3 * 4)` bytes (continuous stream of unsigned integers)

### 5. Skeletons (variable size)
* **Bone Count:** `4 bytes` (unsigned integer)
* **For each bone:**
    * **Name Length:** `4 bytes` (unsigned integer)
    * **Name:** `variable bytes` (UTF-8 encoded string)
    * **Parent Index:** `4 bytes` (signed integer, `-1` for root)
    * **Rest Position:** `12 bytes` (3 floats)
    * **Rest Rotation:** `16 bytes` (4 floats, quaternion)
    * **Rest Scale:** `12 bytes` (3 floats)

### 6. Animations (variable size)
* **Clip Count:** `4 bytes` (unsigned integer)
* **For each clip:**
    * **Name Length:** `4 bytes` (unsigned integer)
    * **Name:** `variable bytes` (UTF-8 encoded string)
    * **Animation Length:** `4 bytes` (float)
    * **Keyframe Count:** `4 bytes` (unsigned integer)
    * **For each keyframe:**
        * **Time:** `4 bytes` (float)
        * **Bone Index:** `4 bytes` (unsigned integer)
        * **Position:** `12 bytes` (3 floats)
        * **Rotation:** `16 bytes` (4 floats)
        * **Scale:** `12 bytes` (3 floats)

