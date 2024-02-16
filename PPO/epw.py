import pandas as pd

def get_random_weather_data(epw_file,row_index):
    # Read the EPW file into a pandas DataFrame
    df = pd.read_csv(epw_file, skiprows=8, header=None, sep=',', engine='python')

    # Extract specific values from the selected row (adjust column indices as needed)
    temperature_outside = df.iloc[row_index, 6]
    humidity = df.iloc[row_index, 7]
    wind_direction = df.iloc[row_index, 20]
    wind_speed = df.iloc[row_index, 21]

    return temperature_outside, humidity, wind_direction, wind_speed

# Example usage
#epw_file_path = 'E:\\ITECH\\23W\\Studio\\CampusLab_RL\\epw\\DEU_BW_Stuttgart-Schnarrenberg.107390_TMYx.epw'
#temperature, humidity, wind_direction, wind_speed = get_random_weather_data(epw_file_path,100)

#print(f'Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s')
