s=open("index.html","r").read()
h=open("f","r").readlines()
for i,line in enumerate(h):
	s=s.replace("S"+str(i)+",",'"'+line.split('src="')[1].split('" alt')[0]+'",')

f=open("index.html","w")
f.write(s)
f.close()
