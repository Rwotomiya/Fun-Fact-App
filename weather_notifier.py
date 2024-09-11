import requests
from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import time

# Function to extract and scrape weather details
def get_weather(city):
    # Replace spaces with hyphens for URL formatting
    city_formatted = city.replace(" ", "-")
    url = f"https://www.weather-forecast.com/locations/{city_formatted}/forecasts/latest"

    try:
        # Make a request to the website
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad responses
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return "HTTP error occurred while fetching weather data."
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
        return "Connection error occurred while fetching weather data."
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
        return "Timeout occurred while fetching weather data."
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
        return "An error occurred while fetching weather data."

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Scraping weather data (Adjust the selector based on the website's structure)
    weather_desc = soup.find('span', class_='phrase')

    if weather_desc:
        return weather_desc.text.strip()
    else:
        return "Could not find weather data."

# Function to display desktop notification
def show_notification(weather_data, city):
    # Initialize notifier object
    toaster = ToastNotifier()

    # Create a message
    message = f"Weather in {city}: {weather_data}"

    # Display the notification with the weather details
    toaster.show_toast("Weather Update", message, duration=10, threaded=True)

# Main execution
if __name__ == "__main__":
    # Replace 'City_Name' with your desired city or get input from the user
    city = "London"  # Example city; you can modify this or use input()

    while True:
        weather_data = get_weather(city)

        if weather_data:
            show_notification(weather_data, city)
        else:
            show_notification("Unable to retrieve weather data.", city)

        # Wait for 30 minutes before the next notification
        time.sleep(1800)
