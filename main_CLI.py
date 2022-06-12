import src.MainClass as Main #MineCraft
import src.ElectricalBill as EB
import src.SheetRenderer as SR

username = "temp"
mainProgram = Main.MainClass(programModules={
	"ElectricalBill": EB.ElectricalBill(username),
	"GUIRenderer": None,
	"SheetRenderer": SR.SheetTextRenderer(5, 5, defaultText=True, cellSpacing=1, cellSize=19)
})

def main():
	mainProgram.runMain()

if __name__ == "__main__":
	#Runs the program:
	main()