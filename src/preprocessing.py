def extract_needed_columns(data, columns):
    """
    Extracts specific columns from a DataFrame.

    Parameters:
        data (pd.DataFrame): DataFrame containing the spot positions.
        columns (list): A list of column names to extract.

    Returns:
        pd.DataFrame: A DataFrame containing the selected columns, or None if an error occurs.
    """
    try:
        # Check if the requested columns exist in the DataFrame
        missing_columns = [col for col in columns if col not in data.columns]
        if missing_columns:
            print(f"Error: The following columns were not found in the DataFrame: {missing_columns}")
            return None

        # Extract the needed columns
        extracted_data = data[columns]
        print("Columns extracted successfully.")
        return extracted_data

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def group_by_diffraction_pattern(df, column_name):
    """
    Groups a DataFrame based on changes in the specified column.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to detect changes and group by.

    Returns:
        grouped (pd.core.groupby.DataFrameGroupBy): A groupby object, grouped by consecutive changes in the specified column.
    """
    if df is None or df.empty:
        print("Error: DataFrame is empty or None. Cannot group.")
        return None

    if column_name not in df.columns:
        print(f"Error: Column '{column_name}' not found in DataFrame.")
        return None

    # Create a 'group' column to track changes in the specified column
    df.loc[:, 'group'] = (df[column_name] != df[column_name].shift()).cumsum()

    # Group by the 'group' column
    #grouped = df.groupby('group')

    return df
