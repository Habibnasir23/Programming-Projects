import requests, bs4
from twilio.rest import Client

'''
This function is used to scrape the weather website. 
It uses a dictionary of keywords and checks if they are present in the forecast. 
If the keywords are present, then an appropriate message is sent.
For example if the forecast says 'rain' then the text message will warn to take an umbrella.
The numerical value of the temperature is also checked and sent as a message. 
'''


def weather_check():
    # the weather website to scrape
    url = 'https://forecast.weather.gov/MapClick.php?lat=40.19348000000008&lon=-92.57900999999998#.YsSC5nbMJPY'
    # use the get method to scrape the website
    res2 = requests.get(url)
    # checking if the scraping was successful
    res2.raise_for_status()
    # parsing the html content
    soup2 = bs4.BeautifulSoup(res2.text, 'html.parser')
    # getting the element using the css class
    weather_elem = soup2.select('#detailed-forecast-body > div:nth-child(1) > div.col-sm-10.forecast-text')
    # getting the text part of the element
    weather = weather_elem[0].getText()

    # dictionary to represent the weather keywords and their respective messages
    weather_dictionary = {'rain': 'It\'s raining outside take an umbrella!', 'chance of showers and thunderstorms':
                          'It\'s about to shower! Be prepared', 'sunny':
                          'It\'s going to be sunny today! Wear light clothes!', 'clear':
                          'The weather looks clear today'}

    # checking if the keys are present in the weather array. if the keys match then send the
    # respective value as the message
    for k in weather_dictionary.keys():
        if k in weather.lower():
            textmyself(weather_dictionary[k])

    # using the css class to get the temperature
    temperature_elem = soup2.select('#current_conditions-summary > p.myforecast-current-sm')
    temperature = temperature_elem[0].getText()
    # getting the int value of the temperature
    temperature_int = int(''.join(filter(str.isdigit, temperature)))

    textmyself('The temperature is ' + str(temperature_int))


'''
This function is used to send messages to the recipient
It takes a string as a parameter that contains the message to be sent
'''


def textmyself(message):
    # account id to verify the recipient
    accountSID = 'AC18f96f58161d0d98e2d8a98771c8567f'
    # authentication token to verify the recipient
    authToken = 'e76d74eb091c56431f368b9202f2bfb1'
    # recipients real number
    myNumber = '+14753321424'
    # recipient's twilio number
    twilioNumber = '+19705095797'
    # accessing the recipient using ID and token
    twilioCli = Client(accountSID, authToken)
    # sending the message to the recipient
    twilioCli.messages.create(body=message, from_=twilioNumber, to=myNumber)


weather_check()
