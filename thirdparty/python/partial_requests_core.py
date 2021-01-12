...
try:

r=requests.get(url=myurl, auth(myuser,mysession), verify=False, proxies=dictProxy, params=payload, timeout=90)
print r.url
