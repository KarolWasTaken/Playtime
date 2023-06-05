import customtkinter
import variables
import matplotlib.pyplot as plt
import numpy as np
import os, sys

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x475")
app.title("Playtime")
app.resizable(False, False)



def Percentage_On():
    percentage = variables.Percentage
    if percentage == False:
        percentage = True
    else:
        percentage = False
    variables.Percentage = percentage
    #print(f"Percentage: {variables.Percentage}")

def Hours_On():
    hours = variables.Hours
    if hours == False:
        hours = True
    else:
        hours = False
    variables.Hours = hours
    #print(f"Hours: {variables.Hours}")

def comboboxSelect(choice):
    gameName.delete(0, 'end')
    gameName.insert(0, choice)
    gameHours.delete(0, 'end')
    gameHours.insert(0, variables.gameData[choice])
    errorLabel.configure(text = "Edit your field\nor set hours to 0 to remove field.")

def Add_Entry():
    try:
        intGameHours = int(gameHours.get())
        
        # remove field
        if(intGameHours == 0) and (gameName.get() in variables.displayGameNames):
            variables.gameData.pop(gameName.get())
            variables.displayGameNames.remove(gameName.get())
            gameHours.delete(0, 'end')
            gameName.delete(0, 'end')
            errorLabel.configure(text = "Field removed")
            
            combobox.set("Game Entries")
            combobox.configure(values = variables.displayGameNames)
            if(len(variables.displayGameNames) <= 0):
                finaliseButton.configure(state = "disabled")

        # edit field 
        elif(intGameHours > 0) and (gameName.get() in variables.displayGameNames):
            variables.gameData[gameName.get()] = intGameHours
            gameName.delete(0, 'end')
            gameHours.delete(0, 'end')
            errorLabel.configure(text = "Field edited")
            combobox.set("Game Entries")
            combobox.configure(values = variables.displayGameNames)
        
        # guard against 0 hr input
        elif(intGameHours <= 0) and (gameName.get() not in variables.displayGameNames):
            gameHours.delete(0, 'end')
            errorLabel.configure(text = "Game must have more than 0 hours")
        
        # add field
        else:
            variables.gameData[gameName.get()] = intGameHours
            #print(f"{gameName.get()} - {gameHours.get()}hrs")

            variables.displayGameNames.append(gameName.get())
            combobox.configure(state = "normal")
            combobox.configure(values = variables.displayGameNames)
            finaliseButton.configure(state = "normal")

            gameName.delete(0, 'end')
            gameHours.delete(0, 'end')
            errorLabel.configure(text = "Added")
    except:
        errorLabel.configure(text = "Hours must be a number")
        errorLabel.pack(pady=10, padx=10)
        gameHours.delete(0, 'end')
    
def create_Chart():
    sortedDictionary = {}
    sorted(variables.gameData, key=variables.gameData.get, reverse=True)
    for key, value in sorted(variables.gameData.items(), key=lambda kv: kv[1], reverse=True):
        #print("%s: %s" % (key, value))
        sortedDictionary[key] = value

    keysList = list(sortedDictionary.keys())
    hourList = []
    for value in sortedDictionary.values():
        hourList.append(value)
    
    myExplode = []
    for x in range(0,len(sortedDictionary)):
        if x == 0:
            myExplode.append(0.1)
        else:
            myExplode.append(0)
    
    finalGameNames = []
    gameNameWithHours = []
    if variables.Hours == True:
        for x in range(0,len(hourList)):
            gameNameWithHours.append(keysList[x] + "\n(" + str(hourList[x]) +"hrs)" )
        finalGameNames = gameNameWithHours
    else:
        finalGameNames = keysList
    y = np.array(hourList)
    plt.rcParams['font.size'] = 8.0
    if variables.Percentage == True:
        plt.pie(y, labels = finalGameNames, explode = myExplode, shadow=True, autopct='%1.2f%%')
    else:
        plt.pie(y, labels = finalGameNames, explode = myExplode, shadow=True)
    plt.show()
    


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text= "Playtime Plotter")
label_1.pack(pady=10, padx=10)

combobox = customtkinter.CTkComboBox(frame_1, values=variables.displayGameNames, justify=customtkinter.CENTER, command=comboboxSelect)
combobox.pack(pady=10, padx=10)
combobox.set("Game Entries")

percentageCheckbox = customtkinter.CTkCheckBox(master=frame_1, command=Percentage_On, text="Percentage")
percentageCheckbox.pack(pady=10, padx=10)
hoursCheckbox = customtkinter.CTkCheckBox(master=frame_1, command=Hours_On, text = "Hours")
hoursCheckbox.pack(pady=10, padx=10)

gameName = customtkinter.CTkEntry(master=frame_1, placeholder_text="Game Name")
gameName.pack(pady=10, padx=10)
gameHours = customtkinter.CTkEntry(master=frame_1, placeholder_text="Hours")
gameHours.pack(pady=10, padx=10)


button = customtkinter.CTkButton(master=frame_1, command=Add_Entry, text="Add Entry")
button.pack(pady=10, padx=10)
errorLabel = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.CENTER, text="")
errorLabel.pack(pady=10, padx=10)

finaliseButton = customtkinter.CTkButton(master=frame_1, command=create_Chart, text="Finalise", state="disabled")
finaliseButton.pack(pady=10, padx=10)

app.mainloop()
