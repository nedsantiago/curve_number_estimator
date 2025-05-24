# Curve Number Estimator

Curve Number Estimator uses Subbasin, Land Use, and Soil Type
data (as QGIS exports in CSV format) into SCS Curve Numbers per
Subbasin. This software was made for the Hydrology field.

## Usage

1. Open a watershed delineation application or program e.g. HEC-HMS,
    QGIS, ArcGIS, etc.
2. Intersect the subbasins / watershed with a land use shapefile
    to get a land use - subbasin shapefile
3. Intersect the subbasins / watershed with a soil type shapefile
    to get a soil type - subbasin shapefile
4. Declare the conversion table for soil types to Hydrologic Soil
    Groups
5. Go into the attributes table in GIS software (e.g. QGIS, ArcGIS)
    and calculate the area.
6. Export the attribute by saving the layer as a csv file.  This
    will convert the attributes table into a csv file with areas.
7. Input these csv files into the program along with other required
    csv files (i.e. SCS Curve Number tables, area of land use per
    subbasin, area of soil type per subbasin, scs table, soil type to
    hsg conversion table, etc.)
8. Run the Program

## Documentation

Future updates to improve the programs useability for public use.
Some possible updates include:
1. Graphical User Interface
2. Integration with other watershed analysis programs for seemless
    analysis
3. Integrating the qgis engine for delineation and intersection
    pre-analysis
4. Modularity of each class for use in other future programs

If successful, the program will print and save a dataframe with the 
estimated curve number of each subbasin as well as the area percentage
of impervious surfaces per subbasin.

## Milestones

Started on:     20230710 (July 10, 2023)
Version 1.0.0:  20230711 (July 11, 2023)
