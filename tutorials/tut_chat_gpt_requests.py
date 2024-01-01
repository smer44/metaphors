import requests
import pprint as pp

api_endpoint = "https://api.openai.com/v1/completions"

api_key = "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"

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer "+ api_key
}

request_data = {
    "model" : "text-davinci-003",
    "prompt" : "Create a plot for a sci-fi movie",
    "max_tokens" : 2000,
    "temperature" : 0.8,

}

response =requests.post(api_endpoint,headers = headers,json = request_data )

print(response.status_code)

text = response.json()['choices'][0]["text"]
pp.pprint(type(text))
pp.pprint(text)
