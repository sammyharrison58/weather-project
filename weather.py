import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter a City name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet(
            """
                QLabel, QPushButton {
                    font-family: Arial; ;
                    }
                 QLabel#city_label {font-size:40px;
                                    font-style:italic;
                    }
                    QLineEdit#city_input {font-size:40px;
                                        }
                    QPushButton#get_weather_button {font-size:30px;
                                                    font-weight:bold;
                                                  }
                    QLabel#temperature_label {font-size:75px;
                                           }
                    QLabel#emoji_label {font-size:100px;
                                        font-family:Segoe UI Emoji;
                                   }
                    QLabel#description_label {font-size:50px;
                           }
                           """
        )
        self.get_weather_button.clicked.connect(self.fetch_weather)

    def fetch_weather(self):

        api_key = "766768c8f9174c8a0f33e1ab1412a978"
        city = self.city_input.text().strip()
        if not city:
            self.display_error("Please enter a city name")
            return

        url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(
            city, api_key
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if str(data.get("cod")) != "200":
                # OpenWeather returns cod as a number or string; show message
                self.display_error(data.get("message", "Unable to fetch weather"))
                return
            self.display_weather(data)
        except requests.exceptions.RequestException as e:
            match response.status_code:
                case 404:
                    self.display_error("City not found")
                case 401:
                    self.display_error("Invalid API key")
                case 403:
                    self.display_error("Access forbidden")
                case 404:
                    self.display_error("Resource not found")
                case 500:
                    self.display_error("Server error occurred")
                case 503:
                    self.display_error("Service unavailable")
                case _:
                    self.display_error("Network error occurred")
        except requests.exceptions.ConnectionError:
            self.display_error("Network connection error")
        except requests.exceptions.Timeout:
            self.display_error("Request timed out")
        except requests.exceptions.RequestException:
            self.display_error("An error occurred while fetching data")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects")

    def display_weather(self, data):
        temp = data.get("main", {}).get("temp")
        description = ""
        emoji = ""
        weather_list = data.get("weather")
        if weather_list and len(weather_list) > 0:
            weather = weather_list[0]
            description = weather.get("description", "").title()
            main = weather.get("main", "")

            emoji_map = {
                "Clear": "☀️",
                "Clouds": "☁️",
                "Rain": "🌧️",
                "Drizzle": "🌦️",
                "Thunderstorm": "⛈️",
                "Snow": "❄️",
                "Mist": "🌫️",
                "Smoke": "🌫️",
                "Haze": "🌫️",
                "Dust": "🌪️",
                "Fog": "🌫️",
                "Sand": "🌪️",
                "Ash": "🌋",
                "Squall": "💨",
                "Tornado": "🌪️",
            }
            emoji = emoji_map.get(main, "")

        if temp is not None:
            self.temperature_label.setText(f"{temp:.1f}°C")
        else:
            self.temperature_label.setText("")
        self.description_label.setText(description)
        self.emoji_label.setText(emoji)

    def display_error(self, message):
        # Clear existing UI and show the error message
        self.temperature_label.setText("")
        self.emoji_label.setText("")
        self.description_label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
