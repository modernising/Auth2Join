import json,requests
class Main:
    def __init__(self,guildId = None,botToken = None,clientId = None,uri = None,clientSecret = None):
        self.botToken = botToken
        self.guildId = guildId
        self.clientId = clientId
        self.redirectUri = uri
        self.clientSecret = clientSecret

    def authorizeToken(self,token):
        try:
            params = {
                'client_id': str(self.clientId),
                'response_type': 'code',
                'redirect_uri': str(self.redirectUri),
                'scope': 'guilds.join identify',
            }
            headers = {
                'Authorization': token,
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                }
            payload = {
                'permissions': 0,
                'authorize': True
                }
            authorized = requests.post('https://discord.com/api/v10/oauth2/authorize', headers=headers, params=params, json=payload)
            if authorized.status_code in [201,200,204]:
                return authorized.json()['location'][-30:]
            elif authorized.status_code != [201,200,204]:
                print(authorized.status_code,authorized.json())
                return None 
                pass
        except Exception as authError:
            print(authError)
        finally:
            pass

    def userId(self,token):
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }
        Id = requests.get("https://discord.com/api/v10/users/@me",headers=headers)
        return Id.json()['id']
    
    def Join(self):
        with open('tokens.txt') as tokens:
            loadTokens = tokens.readlines()
            for token in loadTokens:
                print('Loaded %s from tokens.txt' % len(loadTokens))
            try:
                Id = self.userId(token.strip())
                code = self.authorizeToken(token.strip())
                headers = {
                    'Authorization' : 'Bot %s' % self.botToken,
                    'Content-Type': 'application/json',
                    }
                payload = {
                    'access_token' : self.codeToaccessToken(code)
                    }
                joinedToken = requests.put('https://discord.com/api/v8/guilds/%s/members/%s'% (self.guildId,Id), headers=headers, json=payload)
                if joinedToken.status_code in [200,201,204]:
                    print('Joined %s' % token.strip())
                else:
                    print(joinedToken.status_code, joinedToken.text)
            except Exception as joinError:
                print(joinError)
                pass
    def codeToaccessToken(self,code):
        data = {
            'client_id': self.clientId,
            'client_secret': self.clientSecret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirectUri
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        accessToken = requests.post('https://discord.com/api/v10/oauth2/token' , data=data, headers=headers)
        try:
            return accessToken.json()['access_token']
        except:
            return None
if __name__ == '__main__':
    with open("config.json", "r") as oauthInfo:
        config = json.load(oauthInfo)
    Main(guildId=config['guildId'],botToken=config['botToken'],clientId=config['clientId'],clientSecret=config['clientSecret'],uri=config['uri']).Join()
