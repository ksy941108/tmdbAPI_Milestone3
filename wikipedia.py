import requests

def getURL(input):
    BASE_URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=info&generator=search&formatversion=2&inprop=url&?response"

    params = {
	    "gsrsearch": input
    }

    response = requests.get(
        BASE_URL,
        params = params,
    )

    response = response.json()
    url = response["query"]["pages"][0]["fullurl"]
    return url
