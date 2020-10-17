import requests

x = requests.post("http://207.148.86.204:5000/predict?model=nondeterm", files = {"reflectance" : open("270416_Sue.csv", "rb")})

print(x.text)