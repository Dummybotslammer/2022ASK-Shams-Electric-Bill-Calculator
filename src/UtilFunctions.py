import re #Regular Expressions and formatting library
import os
import colorama as colour #Spice up the output!

#Any and all general-purpose functions/methods are stored here.

#--SAFE TYPE CONVERSION FUNCTIONS:--
def strToInt(arg:str):
	if arg.isnumeric(): return int(arg)
		
	else: return None

def strToFloat(arg:str):
	try:
		arg = float(arg)
		return arg
	
	except:
		return None
		

#--INPUT FUNCTIONS:--
#Removes extra whitespace from any input:
def affirmationInput(inputPrompt:str):
	result = input(inputPrompt)
	result = result.lower().strip()
	if result == "y": return True
	else: return False
		
def cleanInput(inputPrompt:str):
	result = input(colour.Style.BRIGHT + inputPrompt + colour.Style.RESET_ALL)
	if not result.lower() == ".c": return result.strip()
	else: return ".c"

def whitespaceFreeInput(inputPrompt:str):
	result = input(colour.Style.BRIGHT + inputPrompt + colour.Style.RESET_ALL)
	if not result.lower() == ".c": return result.replace(" ", "")
	else: return ".c"

def strippedInput(inputPrompt:str):	
	result = input(colour.Style.BRIGHT + inputPrompt + colour.Style.RESET_ALL)
	if not result.lower() == ".c":
		result = result.strip()
		return re.sub(" +", " ", result)
	else: return ".c"

def parsedInput(inputPrompt:str):
	result = strippedInput(inputPrompt)
	if not result == None: 
		result = result.split()
		beginIndex = -1
		for x in enumerate(result):
			if "'" in x[1]:
				if beginIndex == -1:
					beginIndex = x[0]

				endIndex = x[0] + 1
				result[beginIndex : endIndex] = [' '.join(result[beginIndex : endIndex])]
				result[beginIndex] = result[beginIndex].replace("'", "")
		return result
	else: return ".c"

def inquiryInput(prompts:list, types:list):
	answers = []
	for x in enumerate(prompts):
		if types[x[0]] == int:
			answer = whitespaceFreeInput(x[1])
			if answer == ".c": return ".c"
			answer = strToInt(answer)
			
		elif types[x[0]] == str:
			answer = cleanInput(x[1])
			if answer == ".c": return ".c"
			
		elif types[x[0]] == float:
			answer = whitespaceFreeInput(x[1])
			if answer == ".c": return ".c"
			answer = strToFloat(answer)
		
		else:
			answer = None
			
		answers.append(answer)
	return answers

#--OUTPUT/CLI RENDERING FUNCTIONS:--
def printAffirmation(text:str):
	print(colour.Fore.GREEN +  text + colour.Style.RESET_ALL)
	
def printList(title:str, items:list):
	print("\n{0}:".format(title))
	for x in enumerate(items):
		print(colour.Style.DIM + "{0}. {1}".format(x[0], x[1]) + colour.Style.RESET_ALL)

def printPairs(right:list, left:list):
	for x in enumerate(right):
		print("{0}: {1}{2}{3}".format(x[1], colour.Style.DIM, left[x[0]], colour.Style.RESET_ALL))
	
def printError(arg:str):
	print(colour.Back.YELLOW + "ERROR:" + colour.Style.RESET_ALL + " " +  arg)

def printTitle(arg:str, fore:colour.Fore):
	print(colour.Style.BRIGHT + fore + arg + colour.Style.RESET_ALL)

def clearScreen():
  #For Windows
  if os.name == 'nt':
    _ = os.system('cls')
  
  #For Mac and Linux(here, os.name is 'posix')
  else:
    _ = os.system('clear')
  
#--CALCULATION FUNCTIONS:--
def calculatePriceFromKWH(power:float, SST:float, KWTBB:float):
	price = 0
	extraPower = power - 200
		
	#Calculates the rate and total price (rounded off to 2 closest decimals) based on the power consumed:
	#The rates are given in the ASK textbook, page 18.
	#1 - 200 KWH (monthly) = RM0.218
	#201 KWH and above (monthly) = RM0.492
	if extraPower > 0:
		power -= extraPower
		price += extraPower * 0.492
		price += power * 0.218
		price = round(price, 2)

	else:
		price += power * 0.218
		price = round(price, 2)
	finalPrice = price + (price * SST) + (price * KWTBB)
	finalPrice = round(finalPrice, 2)
	return [finalPrice, price]
