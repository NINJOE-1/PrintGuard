# By Basma Aboushaer
# Simulated temperature readings for testing
simulated_temperatures = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]

# Define the acceptable temperature range
acceptable_range = (32, 37)  # Acceptable temperatures are between 32 and 37 degrees Celsius inclusive

# Function to check the temperature against the acceptable range
def check_temperature(temp):
    if temp < acceptable_range[0]:
        return f"Error: Temperature {temp}°C is below the acceptable range!"
    elif temp > acceptable_range[1]:
        return f"Error: Temperature {temp}°C is above the acceptable range!"
    else:
        return f"Temperature {temp}°C is within the acceptable range."

# Iterate over the simulated temperature readings and print the check result
results = [check_temperature(temp) for temp in simulated_temperatures]
results
