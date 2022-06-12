import src.MeterClass as MC

#An ElectricalBill object serves as a container for meters, from which invoices are generated.
class ElectricalBill():
	#I was planning to use inheritance to avoid duplicate code between ElectricalBill and MeterClass, but decided against it because im lazy.
	def __init__(self, name: str, meters=None, appliances=None, SST=0.06, KWTBB=0.016, monthLen=28):
		#The name would be the username/logname of the user
		self.__name = name
		#meters: contains all the meters that are being accounted for.
		if meters == None: self.__meters = {}
		else: self.__meters = meters
		#appliances: contains all of the unassigned appliances:
		#SlIGHT OVERSIGHT BY ME, BUT THE UNASSIGNED APPLIANCES ONLY HAS 2 DATA PARAMETERS
		if appliances == None: self.__appliances = {}
		else: self.__appliances = appliances
		#SST:
		self.__SST = SST
		#KWTBB:
		self.__KWTBB = KWTBB
		#monthLen: determines the length of each billing month.
		self.__monthLen = monthLen
		
    #totalPrice: the total price of all the meters.
		self.__totalPrice = 0
		#totalPower: the total power of all the meters.
		self.__totalPower = 0

#GETTERS:
	def getName(self):
		return self.__name

	def getMeters(self):
		return self.__meters

	def getMeterByName(self, arg: str):
		"""
		meter = None
		#Does a linear search:
		for x in self.__meters:
			if x.getName() == arg:
				meter = x
				return meter
			return None
		"""
		try:
			meter = self.__meters[arg]
			return meter

		except:
			return None

	def getMeterNames(self):
		"""
		temp = []
		for x in self.__meters:
			temp.append(x.getName())
		return temp
		"""
		return self.__meters.keys()

	def getUnassignedAppliances(self):
		return self.__appliances
	
	def getSST(self):
		return self.__SST

	def getKWTBB(self):
		return self.__KWTBB
	
	def getMonthLen(self):
		return self.__monthLen

	def getTotalPrice(self):
		return self.__totalPrice

	def getTotalPower(self):
		return self.__totalPower

#SETTERS:
	def setName(self, arg: str):
		self.__name = arg

	def setMeters(self, args: dict):
		self.__meters = args

	def addMeter(self, arg: MC.MeterClass):
		#This line of code WILL overwrite any meters with the same name.
		self.__meters[arg.getName()] = arg

	def removeMeter(self, arg:str):
		try:
			self.__meters.pop(arg)
			return True
		except:
			return None

	def editMeter(self, meterName:str, newMeterName:str, SST:float, KWTBB:float, monthLen:int):
		if meterName in self.__meters.keys():
			newMeter = self.__meters[meterName]
			newMeter.setSST(SST)
			newMeter.setKWTBB(KWTBB)
			newMeter.setMonthLen(monthLen)
			newMeter.setName(newMeterName)

			del self.__meters[meterName]
			self.__meters.update({newMeterName: newMeter})
			return True
		else:
			return None
	
	def clearMeters(self):
		self.__meters.clear()

	def removeMeterAppliance(self, meterName:str, applianceName:str):
		if meterName in self.__meters.keys():
			result = self.__meters[meterName].removeAppliance(applianceName)
			return result
		else:
			return None
	
	def addApplianceToMeter(self, meterName:str, applianceName:str, applianceData:list):
		if meterName in self.__meters.keys(): 
			meterWithNewAppliance = self.__meters[meterName]
			meterWithNewAppliance.addAppliance(applianceName, applianceData)
			self.__meters.update({meterName: meterWithNewAppliance})
	
	def setUnassignedAppliances(self, args: dict):
		self.__appliances = args

	def removeUnassignedAppliance(self, name:str):
		try:
			self.__appliances.pop(name)
			return True
		except:
			return None
	
	def addUnassignedAppliance(self, args:list):
		#This line of code WILL overwrite any appliances with the same name.
		self.__appliances[str(args[0])] = [float(args[1]), float(args[2])]

	def clearUnassignedAppliances(self):
		self.__appliances.clear()
	
	def setSST(self, arg:float):
		self.__SST = arg

	def setKWTBB(self, arg:float):
		self.__KWTBB = arg
	
	def setMonthLen(self, arg:int):
		self.__monthLen = arg

#--These functions are used to retrieve grouped/categorized data from each of the meters:--
	def calculateTotalPowerSum(self):
		#IN KWH
		self.__totalPower = 0

		for x in self.__meters:
			x.calculateApplianceTotalPower()
			self.__totalPower += x.getTotalPower()
		return self.__totalPower
	
	def calculateTotalPricesSum(self):
		self.__totalPrice = 0
		basePrice = 0
		
		for x in self.__meters:
			x.calculateApplianceTotalPower()
			x.calculateTotalPrice()
			prices = x.getTotalPrice()
			basePrice += prices[0]
			self.__totalPrice += prices[1]
		#Returns the Total Price and the Base Price (Without tax)
		return [self.__totalPrice, basePrice]
