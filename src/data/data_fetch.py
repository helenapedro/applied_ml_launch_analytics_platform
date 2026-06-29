import pandas as pd
from data.data import fetch_rockets_data,fetch_launchpads_data, fetch_payloads_data, fetch_cores_data, fetch_initial_spacex_data

ROCKETS_COLUMNS = ['name', 'height', 'mass']
LAUNCHPADS_COLUMNS = ['name', 'longitude', 'latitude', 'booster_name']
PAYLOADS_COLUMNS = ['name', 'mass_kg', 'orbit']
CORES_COLUMNS = [
    'Core Serial Number',
    'Times Reused',
    'RTLS Landing Attempts',
    'Successful RTLS Landings',
    'ASDS Landing Attempts',
    'Successful ASDS Landings',
    'Core Version (Block)',
    'Current Status',
]

def fetch_initial_data():
    initial_data = fetch_initial_spacex_data()
    if initial_data:
        df = pd.DataFrame(initial_data)

        df = df.map(
            lambda x: str(x) if not isinstance(x, (str, int, float, bool, type(None))) else x
        )

        pd.set_option('display.max_columns', None)
        return df
    else:
        return pd.DataFrame(columns=["name", "success", "payloads", "launchpad", "flight_number", "cores"]) 


def fetch_and_process_data():
    rockets_data = fetch_rockets_data() or []
    launchpads_data = fetch_launchpads_data() or []
    payloads_data = fetch_payloads_data() or []
    cores_data = fetch_cores_data() or []
    initial_data = fetch_initial_data()

    # Convert to DataFrames
    rockets_df = pd.DataFrame(rockets_data)
    launchpads_df = pd.DataFrame(launchpads_data)
    payloads_df = pd.DataFrame(payloads_data)
    cores_df = pd.DataFrame(cores_data)
    initial_data = pd.DataFrame(initial_data)
    

    # Define a function to convert unsupported data types
    def convert_df_types(df):
        if isinstance(df, pd.DataFrame):
            return df.map(lambda x: x if isinstance(x, (str, int, float, bool)) else str(x))
        raise ValueError("Input is not a valid DataFrame")

    # Create a mapping of rocket IDs to booster names
    rocket_id_to_booster_name = {
        rocket.get('id'): rocket.get('name')
        for rocket in rockets_data
        if isinstance(rocket, dict)
    }

     # Add booster names to launchpads DataFrame
    launchpad_booster_names = [
        rocket_id_to_booster_name.get(launchpad.get('rockets', [None])[0], 'Unknown Booster')
        if launchpad.get('rockets') else 'No Rockets'
        for launchpad in launchpads_data
        if isinstance(launchpad, dict)
    ]

    launchpads_df['booster_name'] = launchpad_booster_names

    # Select specific columns for each DataFrame
    rockets_df = rockets_df.reindex(columns=ROCKETS_COLUMNS)
    launchpads_df = launchpads_df.reindex(columns=LAUNCHPADS_COLUMNS)
    payloads_df = payloads_df.reindex(columns=PAYLOADS_COLUMNS)
    cores_df = cores_df.reindex(columns=['serial', 'reuse_count', 'rtls_attempts', 'rtls_landings', 'asds_attempts', 'asds_landings', 'block', 'status'])
    
     # Rename columns in cores_df for clarity
    cores_df = cores_df.rename(columns = {
        'serial': 'Core Serial Number',
        'reuse_count': 'Times Reused',
        'rtls_attempts': 'RTLS Landing Attempts',
        'rtls_landings': 'Successful RTLS Landings',
        'asds_attempts': 'ASDS Landing Attempts',
        'asds_landings': 'Successful ASDS Landings',
        'block': 'Core Version (Block)',
        'status': 'Current Status'
    }).reindex(columns=CORES_COLUMNS)

    return (
        # Convert DataFrames using the function
        convert_df_types(rockets_df),
        convert_df_types(launchpads_df),
        convert_df_types(payloads_df),
        convert_df_types(cores_df),
    )

