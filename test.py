import requests 

# https://your-heroku-app-name.herokuapp.com/predict
# http://localhost:5000/predict
resp = requests.post("http://localhost:5000/research_paper/", params={'keyword': 'machine learning'})
# resp = requests.post("http://localhost:5000/google_news/")

print(resp.text)