## Importing modules

from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os

def clear():
    """
    OS command to simply clear the terminal.
    """
    ## Windows
    if os.name == 'nt':
        _ = os.system('cls')
    ## Mac and Linux
    else:
        _ = os.system('clear')

## Setting CD to file location
os.chdir(os.path.dirname(os.path.abspath(__file__)))

## Loading the puffin data
puffinData = pd.read_csv("puffins.csv")

## Dropping any rows with Nas present
## Dropping the columns 'measurement_year' and 'sex'
puffinData.dropna(inplace=True)
del puffinData["sex"]
del puffinData["measurement_year"]

## Changing the values within the table to numerical
## atlantic = 1
## horned = 2
## tufted = 3
puffinData['species'] = puffinData['species'].replace(['atlantic'],1)
puffinData['species'] = puffinData['species'].replace(['horned'],2)
puffinData['species'] = puffinData['species'].replace(['tufted'],3)

## Making the relevent x and y data subsets
puffinData_X = puffinData[['bill_length_mm',  'bill_depth_mm',  'wing_length_cm',  'body_mass_kg']]
puffinData_Y = puffinData['species']


## Training the classifier
train, test = train_test_split(puffinData, test_size = 0.3, stratify = puffinData['species'],random_state = 42)
train_X, test_X, train_y, test_y = train_test_split(puffinData_X.values,puffinData_Y, random_state=42)


## Making the classifier
KNC_Pipeline = GridSearchCV(
    make_pipeline(
        StandardScaler(),
        PCA(),
        KNeighborsClassifier(n_neighbors=5)
    ),
    {
        "pca__n_components" : range(1, 4),
    }
)

## Fitting the classifier
KNC_Pipeline.fit(train_X, train_y)


## Clearing the terminal
clear()

## Asking the user if they want to save the analysed data to a file
fileOrUserInput = ""
while fileOrUserInput not in ["file", "user"]:
    fileOrUserInput = input(
        "Are the prediction values in a file or from user input?\n"
        "Please enter file or user: "
        ).lower()
    if fileOrUserInput not in ["file", "user"]:
        print(f"\nError: {fileOrUserInput} not valid input, please enter 'file' or 'user'\n")

## Clearing the terminal
clear()

def ansToDataframe(listAnswer):
    """
    This function turns a passed list to a pandas dataframe
    """
    pandasDataframeAnswer = pd.DataFrame (listAnswer, columns = ['species','bill_length_mm',  'bill_depth_mm',  'wing_length_cm',  'body_mass_kg'])
    return pandasDataframeAnswer

def KNC_Prediction(listUserValues):
    """
    This function predicts the species of bird, based on the four passed parameters.

    Args:
        listUserValues : contains the following:
                billLength : Float
                billDepth : Float
                wingLength : Float
                bodyMass : Float

    Returns:
        'atlantic', 'horned', or 'tufted' : String

    Examples:
        >>> [38.4,19.9,20.7,3.9]
            
        atlantic
    """
    species = ['atlantic','horned','tufted']
    number = KNC_Pipeline.predict([listUserValues])[0]
    return species[number-1]

def userInput():
    """
    This function is used to take user input pass it to KNC_Prediction.

    Args:
        None

    Returns:
        'atlantic', 'horned', or 'tufted'
    """

    ## Checking how the user wants to input information
    clear()
    singleOrList = ""
    while singleOrList not in ["list", "ie"]:
        singleOrList = input(
            "Are you entering input as a list or individual entries?"
            "\nPlease enter 'list' or 'ie'"
        ).lower()
        if singleOrList not in ["list", "ie"]:
            print(f"\nError: {singleOrList} not valid input, please enter 'list' or 'ie'\n")



    if singleOrList == 'ie':
        ## Taking user inputted values
        billLength = input("Enter bill length in mm: ")
        billDepth = input("Enter bill depth in mm: ")
        wingLength = input("Enter wing length  in cm: ")
        bodyMass = input("Enter body mass  in kg: ")
        
        ## Storing these values in a list
        listUserValues = [billLength, billDepth, wingLength, bodyMass]
    else:
        listUserValues = input("Please paste your entries as a list separated by commas, for example:\n"
        "38.4,19.9,20.7,3.9\n\n"
        ).split(',')
        while len(listUserValues) != 4:
            print(
                "Error, length of input exceeds 4.\n"
                "Please enter 4 numbers, separated by commas."
            )
            listUserValues = input("Please paste your entries as a list separated by commas, for example:\n"
                "38.4,19.9,20.7,3.9\n\n"
                ).split(',')
        
    ## Checking all values can be valid floats, if not then returning Error
    indexPosition = 0
    for i in listUserValues:
        try:
            float(i)
            listUserValues[indexPosition] = float(i)
            indexPosition+=1
        except:
            print(f"Error: '{i}' could not be converted to float")
            quit()

    return [KNC_Prediction(listUserValues)]+listUserValues


def fileInput():
    count = 0
    ## Finding the files to analyse
    for dirpath, subdirs, files in os.walk("Data_To_Analyse"):
        for file in files:
            if len(os.listdir(dirpath)) > 1:
                print(
                    "Error: multiple files present in folder\n"
                    "Please ensure one file is present at a time"
                )
                quit()

            ## Finding the right files
            if file.endswith(".csv"):
                fileHeader  = open(os.path.join(dirpath, file)).readline().rstrip().split(',')

                ## Checking to see if the correct amount of columns are present
                if len(fileHeader) > 4:
                    print(
                        f"Error - file: '{file}' has more then 4 columns\n"
                        "Please remove any extra columns, so the file reads as follows:\n"
                        "['bill_length_mm',  'bill_depth_mm',  'wing_length_cm',  'body_mass_kg']"
                        )
                    quit()
                count += 1

                newBirdData = []

                ## Loading data
                with open(os.path.join(dirpath, file)) as file:
                    newBirdData_file = [line.rstrip() for line in file]
                    for row in newBirdData_file:
                        newBirdData.append(row.split(','))

                ## Checks if first column contains incorrect data
                for i in range(len(newBirdData[0])):
                    try:
                        float(newBirdData[0][i])
                    except:
                        print(f"First row contained strings, these are being removed...")
                        del newBirdData[0]

            ## Predicting the species
            result = [r for r in map(KNC_Prediction, [i for i in newBirdData])]
            i=0

            ## Joining the predicted species and original data
            while i < len(newBirdData):
                newBirdData[i] = [result[i]] + newBirdData[i]
                i+=1


    return newBirdData



## Asking the user if they want to save the output
## and printing the results
if fileOrUserInput == 'file':
    ans = fileInput()
    print(f"Your predicted species are:")
    for i in range(len(ans)):
        print(ans[i][0])
else:
    ans = [userInput()]
    print(f"Your predicted species is:")
    print(f"{ans[0][0]}\n")

## Changing the result to a pandas dataframe
ans = ansToDataframe(ans)

saveToFile =""
while saveToFile not in ["y", "n","yes","no"]:
    saveToFile = input(
        "Would you like these results saved to a file? "
        ).lower()
    if saveToFile not in ["y", "n","yes","no"]:
        print(f"\nError: {saveToFile} not valid input, please enter 'y' or 'n'\n")

if saveToFile in [ "n","no"]:
    quit()
else:
        fileSave = input("What would you like to name this file: \nPlease note, spaces will be replaced with '_' and output file will be '.csv'\n")
        fileSave = fileSave.replace(" ", "_") + '.csv'
        print("Saving out now...\nOutput file is in 'Output_Prediction' directory")
        ans.to_csv(f'Output_Prediction/{fileSave}')