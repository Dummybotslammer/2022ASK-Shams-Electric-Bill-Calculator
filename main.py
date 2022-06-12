import main_CLI as CLI
import src_GUI.FinalRelease as GUI
import src.UtilFunctions as UF
import colorama

#Initializes the colorama ANSI correction on Windows systems.
colorama.init()

#Clears the screen to ensure that colorama ANSI correction is in effect.
UF.clearScreen()

#bootMode = False - Boots into CLI
#bootMode = True - Boots into GUI
bootMode = None

#Prompt the user, and ask for which mode do they want to boot into:
bootPrompt = input("{0}{1}Sham's Electric Bill Calculator - Boot Menu:{2}\n1. CLI MODE\n2. GUI MODE\n{3}>".format(
        colorama.Back.MAGENTA, colorama.Style.BRIGHT, colorama.Back.BLACK, colorama.Style.RESET_ALL
        ))
bootPrompt = bootPrompt.strip()
while bootMode == None:
        if bootPrompt.isnumeric():
                bootPrompt = int(bootPrompt)
                if bootPrompt == 1:
                        bootMode = False
                        break
                elif bootPrompt == 2:
                        bootMode = True
                        break
                else: UF.printError("Unknown Boot Mode.")

        else:
                UF.printError("Invalid input. Numeric inputs only.")
        bootPrompt = input("{0}{1}Boot into:{2}\n1. CLI MODE\n2. GUI MODE\n>".format(colorama.Fore.MAGENTA, colorama.Style.BRIGHT, colorama.Style.RESET_ALL))
        bootPrompt = bootPrompt.strip()

if bootMode:
        UF.clearScreen()
        GUI.main()

else:
        UF.clearScreen()
        CLI.main()
