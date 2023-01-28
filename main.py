import collections,random,requests,tqdm
import numpy as np
from PIL import Image, ImageFont, ImageDraw

shortcuts={
"dc":"Washington D.C.",
"la":"Los Angeles",
"ny":"New York City",
"sf":"San Francisco",
"l":"London",
"s":"Seattle",
}

logo_map={
"finance.yahoo.com":"yahoo",
"patch.com":"patch",
"politico.com":"politico",
"nypost.com":"ny",
"sfchronicle.com":"sf",
"nbcnews.com":"nbc",
"chicagotribune.com":"chicago",
"vice.com":"vice",
"cnbc.com":"cnbc",
"usnews.com":"us",
"theatlantic.com":"atlantic",
"abcnews.go.com":"abc",
"people.com":"people",
"seattletimes.com":"seattle",
"businessinsider.com":"bi",
"independent.co.uk":"independent",
"express.co.uk":"express",
"today.com":"today",
"bloomberg.com":"bloomberg",
"reuters.com":"reuters",
"inquirer.com":"inquirer",
"thehill.com":"hill",
"bbc.co.uk":"bbc",
"bbc.com":"bbc",
"forbes.com":"forbes",
"washingtonexaminer.com":"examiner",
"nydailynews.com":"nydaily",
"dailymail.co.uk":"dailymail",
"breitbart.com":"breitbart",
"theverge.com":"verge",
"foxnews.com":"fox",
"cbsnews.com":"cbs",
"apnews.com":"ap",
"chron.com":"chron",
"latimes.com":"la",
"miamiherald.com":"miami",
"buzzfeed.com":"buzzfeed",
}

locs=set()

g_key="AIzaSyA_xpbVEp9woLniuF8Cl-2TG80wkte6JiU"
s=open("template.html").read()

url=("https://api.goperigon.com/v1/all?apiKey=bf76b697-22ac-4cde-a763-0155c7822272&from=2023-01-26&sourceGroup=top100&showNumResults=true&excludeLabel=Opinion&excludeLabel=Paid News&excludeLabel=Roundup&excludeLabel=Press Release&sortBy=date&size=50")
a=requests.get(url).json()["articles"]
A=[]

for i,article in tqdm.tqdm(enumerate(a),total=len(a)):
	n,t,u=article["source"]["domain"],article["title"],article["url"]
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
			_lat=(random.randint(0,1000)-500)/1000
			l=(l[0]+_lat,l[1])
		locs.add(l)

	img=np.zeros([45,900,3],dtype=np.uint8)
	img.fill(255)
	im=Image.fromarray(img)
	start=(0,0)
	if n in logo_map:
		logo=Image.open("logos/"+logo_map[n]+".png")
		w,h=logo.size
		x=int(w*45/h)
		logo=logo.resize((x,45),Image.Resampling.LANCZOS)
		im.paste(logo,(0,0,x,45))
		start=(start[0]+x+5,start[1])
	draw=ImageDraw.Draw(im)
	font=ImageFont.truetype("/Library/Fonts/Arial.ttf",36)
	draw.text(start,t,(0,0,0),font=font)
	im.save("headlines/"+str(i)+".png")
	s=s.replace("U"+str(i)+",",'"'+u+'"'+",")
	s=s.replace("C"+str(i)+"}","["+str(l[1])+","+str(l[0])+"]}")

f=open("index.html","w")
f.write(s)
f.close()
