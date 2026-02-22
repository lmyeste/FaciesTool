# FaciesTool

FaciesTool is a lightweight Python-based tool for interactive
sedimentary facies mapping on Digital Outcrop Models generated in
Agisoft Metashape.

The tool operates entirely within the Metashape environment and enables
direct visual interpretation of facies on three-dimensional
photogrammetric models without exporting data to external software.

------------------------------------------------------------------------

## Features

-   Interactive assignment of sedimentary facies directly on Digital
    Outcrop Models
-   Definition of custom facies with user-defined RGB color codes
-   Direct vertex coloring for immediate visual feedback
-   Operation entirely within Agisoft Metashape (no model export
    required)
-   Preservation of original model geometry and textures
-   Saving and loading of facies configurations using JSON files
-   Lightweight graphical user interface built with PySide2
-   Extensible Python-based architecture

------------------------------------------------------------------------

## Requirements

-   Agisoft Metashape Professional (version 1.8 or higher)
-   Python 3.x (internal Metashape Python environment)
-   PySide2 (included with Metashape)

No external Python dependencies are required.

------------------------------------------------------------------------

## Installation

FaciesTool does not require installation.

1.  Download `FaciesTool.py`
2.  Open Agisoft Metashape Professional
3.  Load a project containing a fully processed 3D model
4.  Run the script via:


    Tools > Run Script...

------------------------------------------------------------------------

## Usage

### Facies Definition

-   Define sedimentary facies by entering a name and selecting an RGB
    color.
-   Optionally save or load facies definitions using a JSON file.
-   Proceed to the facies assignment window.

### Facies Assignment

-   Select faces directly on the 3D model using native Metashape
    selection tools.
-   Choose the desired facies from the dropdown menu.
-   Apply the facies to the selection.
-   Selected vertices are colored automatically.

All operations are performed in memory and do not modify the original
model unless explicitly saved.

------------------------------------------------------------------------

## Data Management

-   Facies definitions and vertex assignments can be exported to JSON
    files.
-   Saved configurations can be reloaded in future sessions.
-   The original Digital Outcrop Model remains unaltered during
    interpretation.

------------------------------------------------------------------------

## Limitations

-   Facies assignment is manual.
-   Automated classification methods are not included.
-   No built-in statistical analysis tools are provided.

------------------------------------------------------------------------

## Citation

If you use FaciesTool in academic work, please cite:

Yeste, L. M., Sánchez-Guerra, J.A., Gil-Ortiz, M., Rua-Alkain, E.,
Viseras, C., Cabello, P. (2026).\
FaciesTool: A Python Tool for Interactive Facies Mapping of Digital
Outcrop Models in Agisoft Metashape (Version 1.0.0).\
Zenodo. https://doi.org/10.5281/zenodo.18588405

------------------------------------------------------------------------

## License

FaciesTool is released under the MIT License.
