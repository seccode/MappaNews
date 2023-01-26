import collections,random,requests,tqdm
from PIL import Image, ImageDraw, ImageFont
from chatgpt_wrapper import ChatGPT
bot=ChatGPT()

shortcuts={
"dc":"Washington D.C.",
"la":"Los Angeles",
"ny":"New York City",
}

articles=collections.defaultdict(list)
locs=set()

n_key="761b840832514c7fa005c8f9d78c0693"
g_key="AIzaSyA_xpbVEp9woLniuF8Cl-2TG80wkte6JiU"
url=("https://newsapi.org/v2/everything?q=e&searchIn=content&apiKey="+n_key)
r=requests.get(url)
s=open("template.html").read()
a=r.json()["articles"]
for i,article in tqdm.tqdm(enumerate(a),total=len(a)):
	n=article["source"]["name"]
	t=article["title"]
	u=article["url"]
	location=input(t+"\n")
	if location in shortcuts:
		location=shortcuts[location]
	url=("https://maps.googleapis.com/maps/api/geocode/json?address="+location+"&key="+g_key)
	r=requests.get(url).json()["results"][0]
	loc=r["geometry"]["location"]
	l=(loc["lat"],loc["lng"])
	if l not in locs:
		locs.add(l)
	else:
		while l in locs:
			_lat=(random.randint(0,1000)-500)/500
			_lng=(random.randint(0,1000)-500)/500
			l=(l[0]+_lat,l[1]+_lng)
		locs.add(l)
	articles[n].append((t,u,l))
	s=s.replace("C"+str(i)+"\n","["+str(l[1])+","+str(l[0])+"]"+"\n")
	t=t.replace('"',"'")
	s=s.replace("S"+str(i)+"\n",'"'+n+": "+t[:18]+"..."+'"'+"\n")
	s=s.replace("U"+str(i)+",",'"'+u+'",')
f=open("index.html","w")
f.write(s)
f.close()
