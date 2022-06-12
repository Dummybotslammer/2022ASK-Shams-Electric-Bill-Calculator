
class MeterClass():
	def __init__(self, name:str, appliances=None, totalPower=0, SST=0.06, KWTBB=0.016, monthLen=28):
		self.__name = name
		#appliances: Contains a dict of appliances in the following format:
		#{NAME: [WATTAGE, TOTAL HOURS PER DAY, NUMBER OF APPLIANCE]}
		if appliances == None: self.__appliances = {}
		else: self.__appliances = appliances
		#totalPower: the totalPower for this meter, in KWH.
		self.__totalPower = totalPower
		#SST: Should be in its decimal value. I.E. 10% is 0.1
		self.__SST = SST
		#KWTBB: The Renewable energy fund, which is basically a tax:
		self.__KWTBB = KWTBB
		#Defines the days per month:
		self.__monthLen = monthLen
		#Total price:
		self.__totalPrice = 0

	#GETTERS:
	def getName(self):
		return self.__name
		
	def getAppliances(self):
		return self.__appliances

	def getApplianceNames(self):
		return self.__appliances.keys()
	
	def getAppliancesList(self):
		result = []
		
		for x in self.__appliances.keys():
			result.append([x])

		for x in enumerate(self.__appliances.values()):
			result[x[0]].append(x[1][0])
			result[x[0]].append(x[1][1])
			result[x[0]].append(x[1][2])
		return result
	
	def getAppliance(self, name="", index=-1):
		#returns the following: [NAME, WATTAGE, TOTAL HOURS PER DAY, NUMBER OF APPLIANCE]
		if not name == "":
			appliance = self.__appliances[name]
			return [name, appliance[0], appliance[1], appliance[2]]
     
		#TODO: TEST THIS LATER
		elif not index == -1:
			appliance = list(self.__appliances)
			return [appliance[0], appliance[1][0], appliance[1][1], appliance[1][2]]
		
		return None
	
	def getTotalPower(self):
		return self._totalPower

	def getMonthLen(self):
		return self.__monthLen

	def getSST(self):
		return self.__SST

	def getTotalPrice(self):
		return self.__totalPrice

	def getKWTBB(self):
		return self.__KWTBB
		
	#SETTERS:
	def setName(self, arg:str):
		self.__name = arg
		
	def setAppliances(self, appliances:dict):
		self.__appliances = appliances

	def addAppliance(self, name:str, args:list):
		#{NAME: [WATTAGE, TOTAL HOURS PER DAY, NUMBER OF APPLIANCE]}
		if len(args) == 3: self.__appliances[name] = args
		elif len(args) == 2: 
			args.append(1)
			self.__appliances[name] = args
		else: pass

	def removeAppliance(self, name:str):
		try:
			self.__appliances.pop(name)
			return True
		except:
			return None
	
	def clearAppliances(self):
		self.__appliances.clear()
	
	def setTotalPower(self, arg:float):
		#arg should be KWH
		self.__totalPower = arg
	
	def setSST(self, arg:float):
		#SST should be in its decimal value. I.E. 10% is 0.1
		self._SST = arg

	def setMonthLen(self, arg:int):
		self.__monthLen = arg

	def setKWTBB(self, arg:float):
		self.__KWTBB = arg
		
	#--Functions for calculations:--
	def calculateApplianceTotalPower(self):
		self.__totalPower = 0

		#This calcualtes the Kilowatt hours per month
		for x in self.__appliances.values():
			#(WATTAGE * NUMBER OF APPLIANCE * HOURS PER DAY * DAYS IN A MONTH)/1000
			self.__totalPower += (float(x[0]) * float(x[2]) * float(x[1]) * self.__monthLen)/1000
		
		return self.__totalPower
	
	def calculateTotalPrice(self):
		self.__totalPrice = 0
		extraPower = self.__totalPower - 200
		
		#Calculates the rate and total price (rounded off to 2 closest decimals) based on the power consumed:
		#The rates are given in the ASK textbook, page 18.
		#1 - 200 KWH (monthly) = RM0.218
		#201 KWH and above (monthly) = RM0.492
		if extraPower > 0:
			power = self.__totalPower - extraPower
			self.__totalPrice += extraPower * 0.492
			self.__totalPrice += power * 0.218
			self.__totalPrice = round(self.__totalPrice, 2)

		else:
			self.__totalPrice += self.__totalPower * 0.218
			self.__totalPrice = round(self.__totalPrice, 2)
		basePrice = self.__totalPrice
		self.__totalPrice += (basePrice * self.__SST) + (basePrice * self.__KWTBB)
		self.__totalPrice = round(self.__totalPrice, 2)
		#Returns the Total Price and the Base Price (Without tax)
		return [self.__totalPrice, basePrice]
