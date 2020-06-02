import requests
from bs4 import BeautifulSoup


class scraper:
    def __init__(self):
        url = requests.get("https://www.metoffice.gov.uk/weather/forecast/gcpqpumd9#?date=2020-05-03")
        if url.status_code == 200:
            self.soup = BeautifulSoup(url.content, 'html.parser')
    
    def getTemperature(self):
        temperatures = [row.text for row in self.soup.find(class_="first-day").find_all(class_='step-feels-like')]
        temperatures = [int(item.replace('\n', '').replace('°', '')) for item in temperatures]
        #averageTemperature = sum(temperatures) / len(temperatures)
        bias = (max(temperatures) - min(temperatures)) * 0.66
        #self.temperature = min(temperatures) + bias
        self.temperature = max(temperatures)
    
    def getWindSpeed(self):
        speeds = [row.text for row in self.soup.find(class_="first-day").find_all(class_='speed')]
        speeds = [int(item.replace('\n', '')) for item in speeds]
        #averageSpeed = sum(speeds) / len(speeds)
        bias = (max(speeds) - min(speeds)) * 0.66
        self.speed = min(speeds) + bias
    
    def getUV(self):
        uvs = [row.text for row in self.soup.find(class_="first-day").find(class_="detailed-view step-uv").find_all('td')]
        uvs = [int(item.replace('\n', '').replace('-', '0')) for item in uvs]
        self.uv = max(uvs)
    
    def scaler(self, comparator, d):
        scale = 0
        for key in d.keys():
            if comparator > key:
                scale += d[key]
                break
        return scale

    def findClothes(self):
        self.getWindSpeed()
        self.getTemperature()
        self.getUV()
        tempScale = {20:3, 15:2, 10:1, 5:-2}
        scale = self.scaler(self.temperature, tempScale)
        uvScale = {5:2, 2:1, 0:-1}
        scale += self.scaler(self.uv, uvScale)
        speedScale = {25:-3, 15:-2, 10:0, 5:2}
        scale += self.scaler(self.speed, speedScale)

        if scale < -2: return 'Trousers, long-sleeve t-shirt and a jumper'
        elif scale < 0: return 'Tracksuit and long-sleeve t-shirt'
        elif scale < 2: return 'Tracksuit and t-shirt'
        else: return 'Shorts and t-shirt'


if __name__ == '__main__':
    s = scraper()
    outputs = dict()
    outputs['clothes'] = s.findClothes()
    outputs['temperature'] = int(s.temperature)
    outputs['speed'] = int(s.speed)

    
