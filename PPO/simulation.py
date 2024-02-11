import pandas as pd

###############################NEED CHECK##################################
###############################NEED CHECK##################################

def get_random_weather_data(epw_file):
    # Read the EPW file into a pandas DataFrame
    df = pd.read_csv(epw_file, skiprows=8, header=None, sep=',', engine='python')

    # Choose a random row
    random_row = df.sample(1)

    # Extract specific values from the selected row (adjust column indices as needed)
    temperature_outside = random_row.iloc[0, 6]
    humidity = random_row.iloc[0, 7]
    wind_speed = random_row.iloc[0, 21]

    return temperature_outside, humidity, wind_speed

# Example usage
epw_file_path = 'E:\\ITECH\\23W\\Studio\\CampusLab_RL\\epw\\DEU_BW_Stuttgart-Schnarrenberg.107390_TMYx.epw'
temperature, humidity, wind_speed = get_random_weather_data(epw_file_path)

print(f'Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s')
