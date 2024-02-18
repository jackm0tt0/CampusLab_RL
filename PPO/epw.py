import pandas as pd

class weather_data:
    def __init__(self,path):
        self.path = path

    def get_weather_data(self,index):
        # Read the EPW file into a pandas DataFrame
        df = pd.read_csv(self.path, skiprows=8, header=None, sep=',', engine='python')

        # Extract specific values from the selected row (adjust column indices as needed)
        temperature_outside = df.iloc[index, 6]
        humidity = df.iloc[index, 7]
        wind_direction = df.iloc[index, 20]
        wind_speed = df.iloc[index, 21]

        return temperature_outside, humidity, wind_direction, wind_speed

    def get_period(self,index):
        # Read the EPW file into a pandas DataFrame
        df = pd.read_csv(self.path, skiprows=8, header=None, sep=',', engine='python')

        # Extract specific values from the selected row (adjust column indices as needed)
        month = df.iloc[index, 1]
        day = df.iloc[index, 2]
        hour = df.iloc[index, 3]

        return month, day, hour


# Example usage
#epw_file_path = 'E:\\ITECH\\23W\\Studio\\CampusLab_RL\\epw\\DEU_BW_Stuttgart-Schnarrenberg.107390_TMYx.epw'
#temperature, humidity, wind_direction, wind_speed = get_random_weather_data(epw_file_path,100)
#df = pd.read_csv(epw_file_path, skiprows=8, header=None, sep=',', engine='python')
#print(df.iloc[:,2])

#print(f'Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s')
