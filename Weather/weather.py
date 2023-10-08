import requests
from time import sleep


def weather_main():
	par = {
		"lang": "ua",
		"lat": 50.4500336,
		"lon": 30.5241361,
		"appid": "84061a2a5ff54b490d63bd38d557b06d",
		"units": "metric"
	}

	print("Зачекайте.", end="")
	sleep(0.6)
	print(".", end="")
	sleep(0.6)
	print(".")

	r = requests.get('https://api.openweathermap.org/data/2.5/weather?', params=par)

	data = r.json()

	descript = data.get("weather")[0].get("description")
	temp = data.get("main").get("temp")
	hum = data.get("main").get("humidity")
	wind_speed = data.get("wind").get("speed")

	result = '{:<15}  {:>10}\n'.format("Зараз:", descript.capitalize())
	result += '-'*30+"\n"
	result += '{:<15}  {:>5} {:<5}\n'.format("Температура:", round(temp), '(*C)')
	result += '{:<15}  {:>5} {:<5}\n'.format("Вологість:", round(hum), "%")
	result += '{:<15}{:>5} {:<5}'.format("Швидкість вітру:", round(wind_speed), 'm/s')
	print(result)
	print("______Дані надав openweathermap.org______")


if __name__ == "__main__":
	weather_main()
