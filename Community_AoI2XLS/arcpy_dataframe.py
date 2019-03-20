import arcpy
import pandas as pd
from pandas import DataFrame


def build_df_from_arcpy(table, index_col=None):
    """
    Build a pandas dataframe from an ArcGIS Feature Class.
    
    Uses the arcpy Search Cursor to loop over a feature class in pandas and
    generate a pandas dataframe. If the dataset is a feature class with a
    geometry it will calculate the length and the area before returning, and
    the geometry will be returned as well-known-text.
    
    :param table: The path to the feature class or table
    :type table: str
    :param index_col: A column to use as the dataframe index. If not supplied
                      for feature classes use the Object ID
    :type index_col: str
    :return: dataframe representation of the feature class. Note this is all in
             memory, so be careful with really big datasets!
    :rtype: pd.DataFrame
    """

    desc = arcpy.Describe(table)
    cursor = arcpy.SearchCursor(table)

    new_data = []

    for row in cursor:
        new_row = {}
        for field in desc.fields:
            new_row[field.aliasName or field.name] = row.getValue(field.name)
        new_data.append(new_row)

    try:
        if not index_col:
            index_col = desc.OIDFieldName

        df = pd.DataFrame(new_data).set_index(index_col)
        df["SHAPEArea"] = df[desc.shapeFieldName].apply(lambda g: g.area)
        df["SHAPELength"] = df[desc.shapeFieldName].apply(lambda g: g.length)
        df[desc.shapeFieldName] = df[desc.shapeFieldName].apply(lambda g: g.WKT)
    except AttributeError:
        # If this is a table in the datbase or on disk, in ArcGIS it won't have
        # either an OID field, nor a geometry
        pass

    return df

def get_field_names(table):
    """
    Get a list of field names not inclusive of the geometry and object id fields.
    :param table: Table readable by ArcGIS
    :return: List of field names.
    """
    # list to store values
    field_list = []

    # iterate the fields
    for field in arcpy.ListFields(table):

        # if the field is not geometry nor object id, add it as is
        if field.type != 'Geometry' and field.type != 'OID':
            field_list.append(field.name)

        # if geomtery is present, add both shape x and y for the centroid
        elif field.type == 'Geometry':
            field_list.append('SHAPE@XY')

    # return the field list
    return field_list



def fields_list(feature_class):

    # variable to store list
    fields = []

    # for every field in the feature class
    for field in arcpy.ListFields(feature_class):

        # if the field is not geometry nor oid
        if field.type != 'Geometry' and field.type != 'OID':

            # append the field name to the list
            fields.append(field.name)

    # return the list of field names
    return fields



def table_to_pandas_dataframe(table, field_names=None):
    """
    Load data into a Pandas Data Frame for subsequent analysis.
    :param table: Table readable by ArcGIS.
    :param field_names: List of fields.
    :return: Pandas DataFrame object.
    """
    # if field names are not specified
    if not field_names:

        # get a list of field names
        field_names = get_field_names(table)

    # create a pandas data frame
    dataframe = DataFrame(columns=field_names)

    # use a search cursor to iterate rows
    with arcpy.da.SearchCursor(table, field_names) as search_cursor:

        # iterate the rows
        for row in search_cursor:

            # combine the field names and row items together, and append them
            dataframe = dataframe.append(
                dict(zip(field_names, row)), 
                ignore_index=True
            )

    # return the pandas data frame
    return dataframe