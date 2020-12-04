# -*- coding: utf-8 -*-

import http.client, urllib.parse, json

# **********************************************
# *** Update or verify the following values. ***
# **********************************************

# Replace the subscriptionKey string value with your valid subscription key.
subscriptionKey = "enter key here"

# Verify the endpoint URI.  At this writing, only one endpoint is used for Bing
# search APIs.  In the future, regional endpoints may be available.  If you
# encounter unexpected authorization errors, double-check this value against
# the endpoint for your Bing Web search instance in your Azure dashboard.
host = "api.cognitive.microsoft.com"
path = "/bing/v7.0/search"

term = "Microsoft Cognitive Services"

def BingWebSearch(search):
    "Performs a Bing Web search and returns the results."

    headers = {'Ocp-Apim-Subscription-Key': subscriptionKey}
    conn = http.client.HTTPSConnection(host)
    query = urllib.parse.quote(search)
    conn.request("GET", path + "?q=" + query, headers=headers)
    response = conn.getresponse()
    headers = [k + ": " + v for (k, v) in response.getheaders()
                   if k.startswith("BingAPIs-") or k.startswith("X-MSEdge-")]
    return headers, response.read().decode("utf8")

if len(subscriptionKey) == 32:

    print('Searching the Web for: ', term)

    headers, result = BingWebSearch(term)
    print("\nRelevant HTTP Headers:\n")
    print("\n".join(headers))
    print("\nJSON Response:\n")
    print(json.dumps(json.loads(result), indent=4))

else:

    print("Invalid Bing Search API subscription key!")
    print("Please paste yours into the source code.")
    
    
    
    
    
    
    ,
    "webPages": {
        "value": [
            {
                "id": "https://api.cognitive.microsoft.com/api/v7/#WebPages.0",
                "dateLastCrawled": "2017-12-16T02:23:00.0000000Z",
                "displayUrl": "www.minijuegos.com/juego/doom-i7363",
                "name": "Doom Online - MiniJuegos.com",
                "url": "http://www.minijuegos.com/juego/doom-i7363",
                "snippet": "Jugar a Doom Online. \u00bfQui\u00e9n no conoce el Doom? Desde que id Software crease este juego en primera persona en los a\u00f1os 90, han creado varias versiones en flash ..."

