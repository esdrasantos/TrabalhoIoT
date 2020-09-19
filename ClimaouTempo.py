import weathercom

cidade="Novo Hamburgo"
weatherDetails = weathercom.getCityWeatherDetails(city=cidade, queryType="daily-data")
print(f'Cidade: {weatherDetails[weatherDetails.find("city")+8:weatherDetails.find("longitude")-4]}')
temperatura=weatherDetails[weatherDetails.find("temperature")+14:weatherDetails.find("temperatureMax")-3]
print(f'Temperatura: {temperatura}ºC')
temperaturamax=weatherDetails[weatherDetails.find("temperatureMax")+25:weatherDetails.find("uvIndex")-3]
print(f'Temperatura máxima desde as 7 da manhã: {temperaturamax}ºC')
sensacao=weatherDetails[weatherDetails.find("feelsLike")+12:weatherDetails.find("gust")-3]
print(f'Sensação térmica: {sensacao}ºC')
umidade=weatherDetails[weatherDetails.find("humidity")+11:weatherDetails.find("icon")-3]
print(f'Umidade relativa do ar: {umidade}%')
precip=weatherDetails[weatherDetails.find("precip24")+15:weatherDetails.find("snowD")-3]
print(f'Precipitação do dia: {precip}mm')
vento=weatherDetails[weatherDetails.find("windSpeed")+11:weatherDetails.find("windDir")-3]
print(f'Velocidade do vento: {vento}km/h')
