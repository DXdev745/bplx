# BPLX File Format

## Description
BPLX (Betnix Project Language X) is a custom binary file format for 3D models with materials, skeletons, and animation data. This repository contains the reference implementation (encoder and decoder scripts) written in Python.

## File Format Specification
The BPLX format is designed to be compact and efficient. A detailed specification can be found in the `BPLX_Specification.md` file.

## Tools
* **`create_advanced_bplx.py`**: A Python script to encode a hard-coded animated cube model into the `animated_cube.bplx` binary file.
* **`read_bplx_binary.py`**: A Python script to decode and print the contents of a BPLX binary file.

## How to Use
1.  Ensure you have Python 3 and the `struct` module installed.
2.  Run the encoder to create the file:
    `python3 create_advanced_bplx.py`
3.  Run the decoder to read the file:
    `python3 read_bplx_binary.py`
