from TwitterSearch import *
# Source: https://github.com/ckoepp/TwitterSearch
import json

token = '787936570968043520-o1bHGOmR4AEuNoafsWoROAQIQIbwz3i'
token_key = 's3vsnQAAuyLmhKYirZ0HIKRpreO8VsF84qAMDHfdmmmGG'
con_secret = 'LJ0wq7eWPRSmdJVIoxQtYxyuy'
con_secret_key = 'CH811T3P1n7ofmPtd0POaML4vfGvKKIz7wLV212wKf3kRdp1i8'


# Put in token, token_key, con_secret, con_secret_key
t = Twitter(auth=OAuth(token, token_key, con_secret, con_secret_key))

x = t.search.tweets(q="#overwatch")
print json.dumps(x)
