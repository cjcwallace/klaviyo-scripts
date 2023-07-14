import json, requests
from itertools import islice

from private_api_key import key

klaviyo_list = "U5R6fG"
headers = {
    "accept": "application/json",
    "revision": "2023-06-15",
    "Authorization": f"Klaviyo-API-Key {key}"
}

 
def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def write_list_profiles_to_file():
    bigData = []

    url = f"https://a.klaviyo.com/api/lists/{klaviyo_list}/profiles/?page[cursor]"

    while url != None:
        try:
            response = requests.get(url, headers=headers)
            response_json = json.loads(response.text)
            bigData.append(response_json['data'])
            url = response_json['links']['next']
            print(f"{url=}")
        except Exception as e:
            print(e)


    with open('all_list_profiles', 'w+', encoding="utf-8") as f:
        f.write(json.dumps(bigData, indent=4))


def identify_bot_accounts():
    bot_accounts = {}

    with open('all_list_profiles', encoding="utf-8") as f:
        data = json.load(f)
        for chunk in data:
            for profile in chunk:
                location = profile['attributes']['location']
                first_name = profile['attributes']['first_name']
                last_name = profile['attributes']['last_name']
                last_event_date = profile['attributes']['last_event_date']
                timezone = profile['attributes']['location']['timezone']
                phone_number = profile['attributes']['phone_number']
                if (
                    location['address1'] == None and
                    location['address2'] == None and
                    location['city'] == None and
                    location['zip'] == None and
                    location['country'] == 'United States' and
                    first_name == last_name and
                    first_name != None and
                    last_name != None and
                    timezone == None and
                    phone_number == None and
                    '$consent' not in profile['attributes']['properties']
                ):                
                    # bot_accounts[profile['id']] = f"{first_name}, {last_name} - {profile['attributes']['email']}"
                    bot_accounts[profile['attributes']['email']] = {
                        'name': f"{first_name}, {last_name}",
                        'id': profile['id']
                    }

    print(len(bot_accounts))
    print(len(bot_accounts)/9355)

    with open('bot_accounts', 'w+', encoding="utf-8") as f:
        f.write(json.dumps(bot_accounts, indent=4))
    
    return bot_accounts

def suppress_bot_accounts_from_list(bot_accounts):
    url = "https://a.klaviyo.com/api/profile-suppression-bulk-create-jobs/"
    headers["content-type"] = "application/json"

    emails = list(bot_accounts.keys())

    for i in range(0, len(emails), 100):
        suppressions = []
        for j in range(i, i+100):
            if (j < len(emails)):
                suppressions.append({"email": emails[j]})
        payload = { "data": {
            "type": "profile-suppression-bulk-create-job",
            "attributes": { "suppressions": suppressions }
        } }

        # response = requests.post(url, json=payload, headers=headers)
        # print(suppressions)


def unsubscribe_bot_accounts_from_list(bot_accounts):
    url = "https://a.klaviyo.com/api/profile-unsubscription-bulk-create-jobs/"
    headers["content-type"] = "application/json"
        
    emails = list(bot_accounts.keys())

    for i in range(0, len(emails), 100):
        unsubscriptions = []
        for j in range(i, i+100):
            if (j < len(emails)):
                unsubscriptions.append({"email": emails[j]})

        payload = { "data": { 
            "type": "profile-unsubscription-bulk-create-job",
            "list_id": klaviyo_list,
            "emails": unsubscriptions 
        } }


bot_accounts = identify_bot_accounts()
print(f"{len(bot_accounts)=}")
suppress_bot_accounts_from_list(bot_accounts)