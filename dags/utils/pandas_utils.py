import utils.config as config
import logging
from functools import partial 
import pandas as pd
TAG = "pandas_utils.py"

def clean_corruptions(full_df, meta_converters):
    """ Function that applies converters to specific columns within the
    dataframe
    """
    for meta_conv in meta_converters:
        if meta_conv['columnas_entrada'] == "all":
            col_names = [col for (col, dtype) in zip(full_df.columns, full_df.dtypes) if dtype == str or dtype == object ]
        else:
            col_names = meta_conv['columnas_entrada']

        for col_name in col_names:
            op_name = meta_conv['operation']
            values = meta_conv['values']

            for val in values:
                if isinstance(val, list):
                    function_to_map = partial(config.CONVERTER_OPERATIONS[op_name], *val)
                else:
                    function_to_map = partial(config.CONVERTER_OPERATIONS[op_name], val)

            logging.info("TAG: {} COL_NAME: {} ".format(TAG, col_name))
            full_df[col_name] = full_df[col_name].map(function_to_map)
        logging.info("TAG: {} FULL_DF: \n {} \n DTYPES \n {} ".format(TAG, full_df, full_df.dtypes))

    # Transform the columns that are possible to convert to numeric
    full_df = try_transform_to_numeric(full_df)

    return full_df

def try_transform_to_numeric(df):
    # Transform the columns that are possible to convert to numeric
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except Exception as e:
            logging.warning("Can not transform to numeric by {}".format(e))
    return df

def custom_strip(full_df):
    col_names = [col for (col, dtype) in zip(full_df.columns, full_df.dtypes) if dtype == object or dtype == string]

    for col_name in col_names:
        function_to_map = lambda x : x.strip()
        full_df[col_name] = full_df[col_name].map(function_to_map)

    return full_df