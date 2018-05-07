import urllib2
import gspread
import sys
from bs4 import BeautifulSoup
from operator import methodcaller
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


credentials = ServiceAccountCredentials.from_json_keyfile_name('craigslist.json', scope)

gc = gspread.authorize(credentials)

sh = gc.open("Cars")
worksheet = sh.get_worksheet(0)

#put craigslist URLs here
listings = []

class car:
	def __init__(self,url):
		self.url = url
		self.price = ''
		self.model = ''
		self.brand = ''
		self.miles = ''
		self.location = ''
		self.year = ''
		self.working = True
	def getPrice(self):
		return int(self.price[1:])

cars = []
brands = ['BMW', 'TOYOTA', 'HONDA', 'HYUNDAI', 'FORD', 'MAZDA', 'NISSAN']

row = 2
for listing in listings:
	cars.append(car(listing))

for x in cars:
	try:
		page = urllib2.urlopen(x.url)
		soup = BeautifulSoup(page,'html.parser')

		x.location = str(soup.find('small').text.strip().replace('(','').replace(')',''))
		x.price = str(soup.find('span',attrs={'class':'price'}).text.strip())

		info = str(soup.find('p',attrs={'class':'attrgroup'}).text.strip())
		for word in info.split():
			brand = "N/A"
			if word.upper() in brands:
				brand = word
				break
		x.brand = brand
		if brand == "N/A":
			x.working = False

		x.year = ''.join(list(filter(str.isdigit, info))[:4])
		x.model = info.replace(x.brand,'').replace(x.year,'')

		atr = soup.find_all('b')
		for a in atr:
			if a.parent.name == 'span' and 'odometer: 'in a.parent:	
				x.miles = str(a.text.strip())
	except:
		x.working = False


try:
	sort = sys.argv[1]
	if sort == 'priceAccending':	
		cars.sort(key = methodcaller('getPrice'))
	elif sort == 'priceDecending':
		cars = sorted(cars,key = lambda car: car.getPrice(),reverse=True)
	elif sort == 'brand':
		cars = sorted(cars,key = lambda car: car.brand,reverse=True)
	elif sort == 'milesAccending':	
		cars.sort(key = lambda car:car.miles)
	elif sort == 'milesDecending':
		cars = sorted(cars,key = lambda car: car.miles,reverse=True)
	elif sort == 'yearAccending':	
		cars.sort(key = lambda car:car.year)
	elif sort == 'yearDecending':
		cars = sorted(cars,key = lambda car: car.year,reverse=True)
	elif sort == 'location':
		cars.sort(key = lambda car: car.location)
except:
	pass

worksheet.update_cell(1,1,"Brand")
worksheet.update_cell(1,2,"Model")
worksheet.update_cell(1,3,"Year")
worksheet.update_cell(1,4,"Miles")
worksheet.update_cell(1,5,"Price")
worksheet.update_cell(1,6,"Location")
worksheet.update_cell(1,7,"Url")

for y in cars:	
	if y.working == False:
		print(y.url+" needs more info.")
	worksheet.update_cell(row,1,y.brand)
	worksheet.update_cell(row,2,y.model)
	worksheet.update_cell(row,3,y.year)
	worksheet.update_cell(row,4,y.miles)
	worksheet.update_cell(row,5,y.price)
	worksheet.update_cell(row,6,y.location)
	worksheet.update_cell(row,7,y.url)
	row+=1
		
