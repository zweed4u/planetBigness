import json, requests, BeautifulSoup
data={}
zip=raw_input('zip code: ')
print
session=requests.session()
coordinateGrab=session.get('http://maps.googleapis.com/maps/api/geocode/json?address='+zip)
formatted_address=coordinateGrab.json()['results'][0]['formatted_address']
lat=str(coordinateGrab.json()['results'][0]['geometry']['location']['lat'])
lng=str(coordinateGrab.json()['results'][0]['geometry']['location']['lng'])
clubLocator=session.get('http://www.planetfitness.com/services/pf/club-locator?lat='+lat+'&lng='+lng)

for clubs in clubLocator.json()['locations']:
	for info in clubs['properties']:
		if info=='postalCode' or info=='address':
			print info,'::',clubs['properties'][info]

		elif info=='label':
			print info,'::',clubs['properties'][info]
			name=clubs['properties'][info]

		elif info=='distance':
			print info,'::',clubs['properties'][info]
			distance=clubs['properties'][info]

		elif info=='clubURL':
			print info,'::',clubs['properties'][info]
			url=clubs['properties'][info]
	data.update({distance:name+'::'+url})
	print 
	print

print 'Selecting closest location...'
clubUrl=data[min(float(s) for s in data.keys())].split('::')[1]
name=data[min(float(s) for s in data.keys())].split('::')[0]
print clubUrl
print
clubPage=session.get(clubUrl)
soup=BeautifulSoup.BeautifulSoup(clubPage.content)
hours=str(soup.findAll("div",{"class":"views-field views-field-field-hours"})[0])
print name
print hours.split('<div class="field-content">')[1].split('</div> </div>')[0].replace('<br />','\n').replace('&amp;','&')
print
