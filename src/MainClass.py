import src.ElectricalBill as EB
import src.MeterClass as MC
import src.UtilFunctions as UF
import sys
import colorama as colour

#The MainClass also serves as its own RUDIMENTARY command interpreter.
#The MainClass will contain the following objects (modules):
#-ElectricalBill (As Invoice objects)
#-GUIRenderer (for the GUI)
#-CLI Rendering will use FUNCTIONS
#-File storage class
#-Might want to add a function for simply calculating the price of a certain kWh
class MainClass():
	def __init__(self, programModules=None):
		#--RUNTIME DATA:--
		if programModules == None: self.__programModules = {}
		else: self.__programModules = programModules
		
		#--INTERPRETER DATA:--
		self.__command = ""
		self.__parameters = []
		#This dictionary contains the minimum amount of parameters that a command takes. These parameters are passed in a list. NOTE: Optional parameters are handled differently (They have a -1 parameter length). An example would be the 'info' command.
		self.__minCommandParamLen = {
			"help": 0,
			"clr": 0,
			"clear": 0,
			"cls": 0,
			"quit": 0,
			"exit": 0,
			"print": 1,
			"kwh2rm": 1,
			"kwhd2rm": 1,
			"create": 1,
			"info": -1, 
			"delete": 1,
			"del": 1,
			"remove": 1,
			"rem": 1,
			"edit": 1,
			"move": 3,
			"checkout": 1,
		}

		#This dictionary lists the recognized commands in the CLI:
		self.__commandList = {
			"help": self.help,
			"clr": UF.clearScreen,
			"clear": UF.clearScreen,
			"cls" : UF.clearScreen,
			"quit": sys.exit,
			"exit": sys.exit,
			"print": self.print,
			"kwh2rm": self.kwh2rm,
			"kwhd2rm": self.kwhd2rm,
			"create": self.create,
			"info": self.info,
			"delete": self.remove,
			"del": self.remove,
			"remove": self.remove,
			"rem": self.remove,
			"edit": self.edit,
			"move": self.move,
			"checkout": self.checkout,
		}

	#GETTERS:
	def getProgramModules(self):
		return self.__programModules
		
	#SETTERS:
	def setProgramModules(self, args:list):
		self.__programModules = args

	def addProgramModule(self, key:str, value:object):
		self.__programModules[key] = value

	def addProgramModules(self, args:dict):
		self.__programModules.update(args)

	#---CLI COMMANDS:--
	def parseInput(self):
		#Parses and sorts the CLI input given.
		#This code will cause the previously inputted command to be sent again, if an empty string is given as input.
		parsedCommand = UF.parsedInput(">")
		if not parsedCommand == None:
			if len(parsedCommand) > 0:
				self.__command = parsedCommand[0]
				del parsedCommand[0]
				self.__parameters = parsedCommand
			
	def runParsedCommand(self):
		#This function will double-check the amount of parameters passed, and run the respective command given. It will also pass any errors or mistakes. (Uses minCommandParamLen and commandList to verify the input given).
		if not self.__command in self.__commandList:
			UF.printError("Unrecognized command.")
			return None
		
		minCommandParamLen = self.__minCommandParamLen[self.__command]
		commandOutput = 0
		if (minCommandParamLen > 0 or minCommandParamLen == -1) and len(self.__parameters) >= minCommandParamLen:
			commandOutput = self.__commandList[self.__command](self.__parameters)

		elif minCommandParamLen == 0:
			self.__commandList[self.__command]()

		else:
			UF.printError("Too few parameters were passed.")

		#Throws an error if the wrong data type is given in parameters.
		if commandOutput == -1:
			UF.printError("Bad input/parameters were given.")

	#--INTERPRETED COMMAND FUNCTIONS:--
	def help(self):
		UF.printTitle("List of Recognized Commands:", colour.Fore.MAGENTA)
		helpList = [
			"help - Lists the the entire list of recognized commands.",
			"clr/clear/cls - Clears the screen's contents.",
			"quit/exit - Exits the program.",
			"print - A test command that outputs the given parameter.",
			"kwh2rm <total kWh> - A calculation command that calculates the total price to be paid, based on the given total energy consumption within a month, in units of kWh.",
			"kwhd2rm <daily kWh> - A calculation command that calculates the total price to be paid, based on the daily energy consumption, in units of kWh.",
			"create <object tag> - Initializes and creates an object, based on the tag given.",
			"info <meter name> - If no <meter name> is given, then general information will be displayed. Otherwise, the program will display detailed information about the meter mentioned.",
			"delete/del/remove/rem <meter name> - Removes the appliace that is referenced.",
			"delete/del/remove/rem <meter name> <appliance name> - Removes an appliance from the meter referenced.",
			"edit <meter name> - Prompts the user to edit the settings of the meter refereced.",
			"edit <meter name> <appliance name> - Prompts the user to edit the settings of the appliance refereced.",
			"move <original meter> <appliance name> <destination meter> - Moves an appliance from the original meter to the destination meter.",
			"checkout <meter name> - Displays the final invoice for the given meter, at the end of the month.",
							 ]
		for x in helpList:
			print(x + "\n")
			
	def print(self, args:list):
		#args[0] - output
		print(str(args[0]))

	def kwh2rm(self, args:list):
		#Parameter Check:
		#args[0] - monthly KWHs
		kwh = UF.strToFloat(args[0])
		if None in [kwh]:
			return -1
		
		prices = UF.calculatePriceFromKWH(kwh, self.__programModules["ElectricalBill"].getSST(), self.__programModules["ElectricalBill"].getKWTBB())
		print("Your monthly bill according to our rates would total to:\nRM{0} (Excluding Tax)\nRM{1} (Inlcuding Tax, i.e. SST and KWTBB)".format(prices[1], prices[0]))

	def kwhd2rm(self, args:list):
		#Parameter Check:
		#args[0] - daily KWHs
		kwh = UF.strToFloat(args[0])
		if None in [kwh]:
			return -1

		kwh *= self.__programModules["ElectricalBill"].getMonthLen()
		prices = UF.calculatePriceFromKWH(kwh, self.__programModules["ElectricalBill"].getSST(), self.__programModules["ElectricalBill"].getKWTBB())
		print("Your monthly bill according to our rates would total to:\nRM{0} (Excluding Tax)\nRM{1} (Inlcuding Tax, i.e. SST and KWTBB)".format(prices[1], prices[0]))

	def create(self, args:list):
		#Parameter Check:
		#args[0] - object name/tag
		objName = args[0].lower()

		if objName == "a":
			#Input Prompt:
			prompts = ["Please input a name:",
								 "Please input the wattage:",
								 "Please input he hours used per day:", #Add option for total hours per month!
								 #"Number of said appliance:"
								 "Please input the name of the parent meter:"
								]
			settings = UF.inquiryInput(prompts, [str, float, float, str])
			if settings == ".c":
				print("Quit Operation.")
			
			elif None in settings:
				UF.printError("Invalid input given.")

			elif settings[2] > 24:
				UF.printError("Invalid 'Hours used per day' parameter passed to the 'create' command. There are only 24 hours in a day!")
				
			elif settings[3] in self.__programModules["ElectricalBill"].getMeterNames():
				self.__programModules["ElectricalBill"].addApplianceToMeter(settings[3], settings[0], [settings[1], settings[2]])
				print("\nNew appliance successfully created. Inserted into meter with name '{0}'.".format(settings[3]))

			else:
				print("\nStoring new appliance into unassigned appliance list.")
				self.__programModules["ElectricalBill"].addUnassignedAppliance([settings[0], settings[1], settings[2]])
			
		#Creates a meter object with custom settings:
		elif objName == "m":
			#Input Prompt:
			prompts = ["Please input a name for the new meter:",
								 "Please input the SST percentage (In decimals):",
								 "Please input the KWTBB percentage (In decimals):",
								 "Please input the days per billing month:"
								]
			settings = UF.inquiryInput(prompts, [str, float, float, int])
			if settings == ".c":
				print("Quit Operation.")
			
			elif None in settings:
				UF.printError("Invalid input given.")
				
			else:
				self.__programModules["ElectricalBill"].addMeter(MC.MeterClass(settings[0], SST=settings[1], KWTBB=settings[2], monthLen=settings[3]))
				
		#Creates a meter object with default settings:
		elif objName == "md":
			#Input Prompt:
			name = UF.cleanInput("Please input a name for the new meter:")
			if not name == ".c":
				self.__programModules["ElectricalBill"].addMeter(MC.MeterClass(name))
				
		else: UF.printError("Unknown object type named '{0}'.".format(objName))
		
	def info(self, args:list=[]):
		#NOTE: This command has optional parameters.
		#Parameter Check:
		#args[0] - Name of the Meter object.

		#Shows general information:
		if args == []:
			UF.printTitle("\n--GENERAL INFORMATION:--", colour.Fore.WHITE)
			print("User Info:")
			UF.printList("Unassigned Appliances", self.__programModules["ElectricalBill"].getUnassignedAppliances())
			UF.printList("Electric Meters", self.__programModules["ElectricalBill"].getMeterNames())

		elif len(args) > 0:
			meter = self.__programModules["ElectricalBill"].getMeterByName(args[0])
			
			if not meter == None:
				UF.printTitle("\n--" + meter.getName() + " (Electric Meter):--", colour.Fore.WHITE)
				
				applianceInfo = []
				for x in list(meter.getAppliancesList()):
					applianceInfo.append("{0}{1}{2}: \n\tWattage: {3}\n \tHours Used Per Day: {4}\n".format(colour.Fore.GREEN, x[0], colour.Fore.WHITE, x[1], x[2]))
					#I would insert "\tNumber of  said Appliance: {3}\n" to show the number of a given appliance, but since it's not implemented I'll exclude it.
				
				UF.printList("Connected Appliances ({0})".format(len(applianceInfo)), applianceInfo)
				print("\n", end="")
				
				UF.printTitle("--Billing Information & Estimations:--", colour.Fore.WHITE)
				SST = str(meter.getSST() * 100) + "%"
				KWTBB = str(meter.getKWTBB() * 100) + "%"
				UF.printPairs(["Service Tax Rate", "KWTBB rate"], [SST, KWTBB])
				
				meter.calculateApplianceTotalPower()
				prices = meter.calculateTotalPrice()
				UF.printPairs(["Monthly Bill Cost (Excluding Tax)", "Total Monthly Bill Cost (Including Tax, i.e. SST & KWTBB)"], ["RM "+str(prices[1]), "RM "+str(prices[0])])

			else:
				UF.printError("Meter with name '{0}' cannot be found.".format(args[0]))
		
		else:
			UF.printError("Parameters given to the 'info' command are unrecognized.")

	def remove(self, args:list):
		#Parameter Check:
		#args[0] - Meter Name 
		#args[1] - Appliance Name
		if len(args) == 1:
			if not self.__programModules["ElectricalBill"].removeMeter(args[0]) == None:
				UF.printAffirmation("Successfully removed electric meter with name '{0}'.".format(args[0]))
			else:
				UF.printError("Unknown meter '{0}'.".format(args[0]))
			
		elif len(args) >= 2:
			if not self.__programModules["ElectricalBill"].removeMeterAppliance(args[0], args[1]) == None:
				UF.printAffirmation("Successfully removed appliance with name '{0}' from electric meter '{1}'.".format(args[1], args[0]))
			else:
				UF.printError("Unknown meter '{0}' and or appliance '{1}'.".format(args[0], args[1]))

	def edit(self, args:list):
		#Parameter Check:
		#args[0] - Meter Name
		#args[1] - Appliance Name
		meter = self.__programModules["ElectricalBill"].getMeterByName(args[0])
		if len(args) == 1 and (not meter == None):
			newName = UF.cleanInput("Please enter a new name for the meter:")
			SST = meter.getSST()
			KWTBB = meter.getKWTBB()
			monthLen = meter.getMonthLen()
			
			if newName == ".c":
				print("Quit Operation.")
			
			elif len(newName) == 0:
				UF.printError("Invalid input given.")
			
			else:
				self.__programModules["ElectricalBill"].editMeter(args[0], newName, SST, KWTBB, monthLen)
	
				#After this bit, add some code to give the user an option to edit the meter settings as well.
				advancedEdit = UF.affirmationInput("Do you want to edit the meter's advanced settings? (Y/N):")

				if advancedEdit:
					prompts = ["Please input a new SST percentage (In decimals):",
									 	"Please input a new KWTBB percentage (In decimals):",
									 	"Please input the new amount of days per billing month:"
										]
					settings = UF.inquiryInput(prompts, [float, float, int])
					SST = settings[0]
					KWTBB = settings[1]
					monthLen = settings[2]
				
					self.__programModules["ElectricalBill"].editMeter(newName, newName, SST, KWTBB, monthLen)
				
				UF.printAffirmation("\nSuccessfully edited meter.")
				
		#In the case that len(args) >= 2
		elif len(args) >= 2 and (not meter == None):
			if args[1] in meter.getApplianceNames():
				prompts = ["Please input a new name for the appliance:",
									 "Please input the new wattage:",
									 "Please input the new amount of hours used per day:"
									]
				settings = UF.inquiryInput(prompts, [str, float, float])
				#Was supposed to add a number of appliances option, but that will be deprecated for now.
				if settings == ".c":
					print("Quit Operation.")
			
				elif None in settings:
					UF.printError("Invalid input given.")

				elif settings[2] > 24:
					UF.printError("Invalid 'Hours used per day' parameter passed to the 'create' command. There are only 24 hours in a day!")

				else:
					newApplianceName = settings[0]
					newApplianceData = [settings[1], settings[2], 1]
					
					self.__programModules["ElectricalBill"].removeMeterAppliance(args[0], args[1])
					self.__programModules["ElectricalBill"].addApplianceToMeter(args[0], newApplianceName, newApplianceData)
					UF.printAffirmation("Successfully edited the appliance's properties.")
				
			else:
				UF.printError("Unknown appliance.")

		elif len(args) >= 2 and (str(args[0]).lower() == "unassigned"):
			prompts = ["Please input a new name for the appliance:",
									 "Please input the new wattage:",
									 "Please input the new amount of hours used per day:"
									]
			settings = UF.inquiryInput(prompts, [str, float, float])
			
			if settings == ".c":
				print("Quit Operation.")
			
			elif None in settings:
				UF.printError("Invalid input given.")

			elif settings[2] > 24:
				UF.printError("Invalid 'Hours used per day' parameter passed to the 'create' command. There are only 24 hours in a day!")

			else:
				newApplianceData = [settings[0], settings[1], settings[2], 1]
				self.__programModules["ElectricalBill"].removeUnassignedAppliance(args[1])
				self.__programModules["ElectricalBill"].addUnassignedAppliance(newApplianceData)
				UF.printAffirmation("Successfully edited the appliance's properties.")
		
		else:
			UF.printError("Unknown electric meter.")

	def move(self, args:list):
		#Parameter Check:
		#args[0] - Original Meter Name
		#args[1] - Appliance Name
		#args[2] - Destination Meter Name
		originalMeterName = args[0]
		applianceName = args[1]
		destinationMeterName = args[2]
		meterNames = self.__programModules["ElectricalBill"].getMeterNames()
		unassignedApplianceNames = self.__programModules["ElectricalBill"].getUnassignedAppliances().keys()

		originalMeter = self.__programModules["ElectricalBill"].getMeterByName(originalMeterName)
		if (not originalMeter == None) and (destinationMeterName in meterNames):
			if applianceName in originalMeter.getApplianceNames():
				applianceData = originalMeter.getAppliance(applianceName)
				applianceData = [applianceData[1], applianceData[2], applianceData[3]]
				self.__programModules["ElectricalBill"].removeMeterAppliance(originalMeterName, applianceName)
				self.__programModules["ElectricalBill"].addApplianceToMeter(destinationMeterName, applianceName, applianceData)
				UF.printAffirmation("Successfully moved appliance from '{0}' to '{1}'.".format(originalMeterName, destinationMeterName))

			else:
				UF.printError("Unrecognized appliance name.")
				
		elif originalMeterName == "unassigned" and (destinationMeterName in meterNames):
			unassignedAppliances = self.__programModules["ElectricalBill"].getUnassignedAppliances()
			if applianceName in unassignedApplianceNames:
				applianceData = unassignedAppliances[applianceName]
				self.__programModules["ElectricalBill"].removeUnassignedAppliance(applianceName)
				self.__programModules["ElectricalBill"].addApplianceToMeter(destinationMeterName, applianceName, applianceData)
				UF.printAffirmation("Successfully moved appliance from the unassigned list to '{0}'.".format(destinationMeterName))

			else:
				UF.printError("Unrecognized appliance name.")
		
		else:
			UF.printError("Unrecognized electric meter names.")
		
	def checkout(self, args:list):
		#Parameter Check:
		#args[0] - Meter Name
		meterName = args[0]
		username = self.__programModules["ElectricalBill"].getName()
		if meterName in self.__programModules["ElectricalBill"].getMeterNames():
			UF.printTitle("\n--CHECKOUT RECEIPT: " + meterName + ":--", colour.Fore.WHITE)
			print("{0}To be paid by {1}.{2}".format(colour.Back.BLUE, username, colour.Style.RESET_ALL))
			
			#Print a list of appliances. Then after that you print the total price.
			meter = self.__programModules["ElectricalBill"].getMeterByName(meterName)
			applianceInfo = []
			for x in list(meter.getAppliancesList()):
				applianceInfo.append("{0}{1}{2}: \n\tWattage: {3}\n \tHours Used Per Day: {4}\n".format(colour.Fore.GREEN, x[0], colour.Fore.WHITE, x[1], x[2]))

			UF.printList("Connected Appliances ({0})".format(len(applianceInfo)), applianceInfo)
			print("\n", end="")

			#Prints the Power Consumption Data and the charging divisions:
			totalPower = meter.calculateApplianceTotalPower()
			powerTable = []
			if totalPower > 200: powerTable = [["1-200 kWh (RM0.218)", 200], [">200 kWh (RM0.492)", totalPower-200]]
			else: powerTable = [["1-200 kWh (RM0.218)", totalPower], [">200 kWh (RM0.492)", 0]]
			self.__programModules["SheetRenderer"].RenderSheet("{0}Power Consumption Data{1} {2}{3}(Tariff Block & Rate, Consumption Per Block [kWh]){4}".format(colour.Style.BRIGHT, colour.Style.RESET_ALL, colour.Style.NORMAL, colour.Back.CYAN, colour.Style.RESET_ALL), powerTable)
			print("\n")
			
			#Prints the prices and billing info:
			UF.printTitle("--Billing Information:--", colour.Fore.WHITE)
			SST = str(meter.getSST() * 100) + "%"
			KWTBB = str(meter.getKWTBB() * 100) + "%"
			UF.printPairs(["Service Tax Rate", "KWTBB rate"], [SST, KWTBB])
			
			meter.calculateApplianceTotalPower()
			prices = meter.calculateTotalPrice()
			UF.printPairs(["This Month's Cost (Excluding Tax)", "This Month's Total Cost (Including Tax, i.e. SST & KWTBB)"], ["RM "+str(prices[1]), "RM "+str(prices[0])])

		else:
			UF.printError("Unrecognized electric meter with name '{0}'.".format(meterName))
			
	#--MAIN METHOD:--
	def runMain(self):
		newname = input("Username: ")
		self.__programModules["ElectricalBill"].setName(newname)
		UF.clearScreen()
		UF.printTitle("Welcome to Sham's Electrical Bill Counter!", colour.Fore.MAGENTA)
		print("Type 'help' in the command line to fetch the list of available commands!\n")
		while True:
			self.parseInput()
			self.runParsedCommand()
