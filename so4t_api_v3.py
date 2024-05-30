# Standard Python libraries
import json

# Third-party libraries
import requests


class V3Client(object):

    def __init__(self, url, token, proxy=None):

        print("Initializing API v3 client...")

        if not url: # check if URL is provided; if not, exit
            print("Missing required argument. Please provide a URL.")
            raise SystemExit

        if not token: # check if API token is provided; if not, exit
            print("Missing required argument. Please provide an API token.")
            raise SystemExit
        else:
            self.token = token
            self.headers = {'Authorization': f'Bearer {self.token}'}

        if "stackoverflowteams.com" in url: # Stack Overflow Business or Basic
            self.team_slug = url.split("https://stackoverflowteams.com/c/")[1]
            self.api_url = f"https://api.stackoverflowteams.com/v3/teams/{self.team_slug}"
        else: # Stack Overflow Enterprise
            self.api_url = url + "/api/v3"

        self.proxies = {'https': proxy} if proxy else {'https': None}

        self.ssl_verify = self.test_connection() # test the API connection

    
    def test_connection(self):

        endpoint = "/tags"
        endpoint_url = self.api_url + endpoint
        ssl_verify = True

        print("Testing API v3 connection...")
        try:
            response = requests.get(endpoint_url, headers=self.headers, 
                                    proxies=self.proxies)
        except requests.exceptions.SSLError:
            print("SSL error. Trying again without SSL verification...")
            response = requests.get(endpoint_url, headers=self.headers, verify=False, 
                                    proxies=self.proxies)
            ssl_verify = False
        
        if response.status_code == 200:
            print("API connection successful")
            return ssl_verify
        else:
            print("Unable to connect to API. Please check your URL and API token.")
            print(f"Status code: {response.status_code}")
            print(f"Response from server: {response.text}")
            raise SystemExit


    def edit_question(self, question_id, title, body, tags):
        # tags is a list of strings
        # title, body, and tags will overwrite the existing values

        method = "put"
        endpoint = f"/questions/{question_id}"
        params = {
            'title': title,
            'body': body,
            'tags': tags,
        }
        response = self.send_api_call(method, endpoint, params)

        return response


    def get_all_questions(self):
            
            method = "get"
            endpoint = "/questions"
            params = {
                'page': 1,
                'pagesize': 100,
            }
            questions = self.send_api_call(method, endpoint, params)
    
            return questions


    def get_all_tags(self):

        method = "get"
        endpoint = "/tags"
        params = {
            'page': 1,
            'pagesize': 100,
        }
        tags = self.send_api_call(method, endpoint, params)

        return tags


    def get_tag_smes(self, tag_id):

        method = "get"
        endpoint = f"/tags/{tag_id}/subject-matter-experts"
        smes = self.send_api_call(method, endpoint)

        return smes


    def get_all_users(self):
        
        method = "get"
        endpoint = "/users"
        params = {
            'page': 1,
            'pagesize': 100,
        }
        users = self.send_api_call(method, endpoint, params)

        return users
    

    def get_all_user_groups(self):

        method = "get"
        endpoint = "/user-groups"
        params = {
            'page': 1,
            'pagesize': 100,
        }
        user_groups = self.send_api_call(method, endpoint, params)

        return user_groups
    

    def get_all_communities(self):
            
        method = "get"
        endpoint = "/communities"
        params = {
            'page': 1,
            'pagesize': 100,
        }
        communities = self.send_api_call(method, endpoint, params)

        return communities
    

    def get_all_collections(self):
                
        method = "get"
        endpoint = "/collections"
        params = {
            'page': 1,
            'pagesize': 100,
        }
        collections = self.send_api_call(method, endpoint, params)

        return collections


    def send_api_call(self, method, endpoint, params={}):

        get_response = getattr(requests, method, None) # get the method from the requests library
        endpoint_url = self.api_url + endpoint

        data = []
        while True:
            if method == 'get':
                response = get_response(endpoint_url, headers=self.headers, params=params, 
                                        verify=self.ssl_verify, proxies=self.proxies)
            else:
                response = get_response(endpoint_url, headers=self.headers, json=params, 
                                        verify=self.ssl_verify, proxies=self.proxies)

            if response.status_code not in [200, 201, 204]:
                print(f"API call to {endpoint_url} failed with status code {response.status_code}")
                print(response.text)
                raise SystemExit
                        
            try:
                json_data = response.json()
            except json.decoder.JSONDecodeError: # some API calls do not return JSON data
                print(f"API request successfully sent to {endpoint_url}")
                return

            if type(params) == dict and params.get('page'): # check request for pagination
                print(f"Received page {params['page']} from {endpoint_url}")
                data += json_data['items']
                if params['page'] == json_data['totalPages']:
                    break
                params['page'] += 1
            else:
                print(f"API request successfully sent to {endpoint_url}")
                data = json_data
                break

        return data
