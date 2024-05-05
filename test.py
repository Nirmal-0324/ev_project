import requests
a=str(float((requests.get( "https://api.thingspeak.com/channels/2491345/fields/1/last.json").json().get('field1'))[:-1])/100)+','+(str(float((requests.get( "https://api.thingspeak.com/channels/2491345/fields/2/last.json").json().get('field2'))[:-1])/100))
glink= "https://www.google.com/maps?q="+a
print(glink)


#print("https://www.google.com/maps?q={"+(requests.get( "https://api.thingspeak.com/channels/2491345/fields/1/last.json").json().get('field1'))[:-1]+"},{"+(requests.get( "https://api.thingspeak.com/channels/2491345/fields/2/last.json").json().get('field2'))[:-1]+"}")