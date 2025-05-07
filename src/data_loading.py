import pandas as pd

def load_data(path: str, skiprows: int = 0) -> pd.DataFrame:
    """
    1. Data / CSV Loading
    - Reads CSV (or Excel if you swap to pd.read_excel)
    - Strips column whitespace
    - Parses END DATE to datetime
    """
    if path.lower().endswith(".xlsx"):
        df = pd.read_excel(path, skiprows=skiprows)
    else:
        df = pd.read_csv(path, skiprows=skiprows)
    df.columns = df.columns.str.strip()
    df['END DATE'] = pd.to_datetime(df['END DATE'], errors='coerce')
    return df
