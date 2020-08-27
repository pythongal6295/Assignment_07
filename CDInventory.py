#------------------------------------------#
# Title: CDInventory.py (Assignment 07)
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
#Assignment 06
# KKauffman, 17 Aug 2020, Created File, wrote code for all TODOs,
#debugging 'a' menu functions
#KKauffman, 18 Aug 2020, fixed 'a' menu functions, formatting edits,
#KKauffman, 19 Aug 2020 formatting edits, added details to docstrings
#Assignment 07
#KKauffman, 24 Aug 2020 edited based on DKlos' recommendations 
#(e.g. removed dependance on global variables), added error handling for reading file
#KKauffman, 25 Aug 2020 Added error handling for user inputs, 
#changed all saving/loading to pickling/unpickling
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dicts to hold data
dicRow = {}  # dict of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Collect and process user inputs"""

    @staticmethod
    def create_table(strID, strTitle, strArtist, table):
        """Function to take list of user inputs and put them in a dictionary (dicRow)
        
        Arg: 
            table/list to store user inputs
            Taken from unpacked tuple returned by IO.user_inputs()
            strID: User's inputted CD ID
            strTitle: User's inputted CD title
            strArtist: User's inputted CD Artist
        
        Return:
            None
            
        """
        
        dicRow = {'ID': strID, 'Title': strTitle, 'Artist': strArtist}
        table.append(dicRow)

    @staticmethod
    def delete_data(id_to_remove, table):
        """Function to delete CD data from memory
        
        Arg:
            table/list that data will be deleted from
            CD ID that the user wants deleted
        
        Return:
            None
        
        """
        
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == id_to_remove:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('\nThe CD was removed.\n')
        else:
            print('\nCould not find this CD!\n')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            objFile = open(file_name, 'rb')
            table = pickle.load(objFile) 
            objFile.close()
        except IOError:
        #If function can't find the file, then this code will execute
            print('\nCD Inventory file does not yet exist. Creating a new file now.')
            objFile = open(file_name, 'rb')
            objFile.close()
        return table
            
    @staticmethod
    def write_file(file_name, table):
        """Function to write data to file
        
        Takes each row from lsttable and separates the items in it by a comma
        and adds a \n at the end
        
        Args:
            file_name (string): name of file data is saved to
            table (lists of dicts): 2D data structure that holds the data
            
        Returns: print statement confirming save is complete
        
        """
        objFile = open(file_name, 'wb')
        pickle.dump(table, objFile) #Look at file to ensure it was saved 
        objFile.close()
        return print('\nYour data has been saved.')

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""
            
    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\nCD Inventory Menu\n\n[l] Load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to file\n[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print()
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        print()
        
    @staticmethod
    def user_inputs():
        """Function to gather the user's inputs for CD ID, CD Title, and CD Artist
        
        Arg: none
        
        Return: a tuple of the three user inputs (entryID, entryTitle, entryArtist)
        
        """
        #Will catch if the user enters an noninteger for the ID. Loop will continue to prompt them.
        entryID = ''
        while True:
            try:
                entryID = int(input('Enter ID: ').strip())
                break
            except ValueError:
                print('\nOops! You must enter an integer for the CD ID.')
                continue
        
        entryTitle = input('What is the CD\'s title? ').strip()
        entryArtist = input('What is the Artist\'s name? ').strip()
        return (entryID, entryTitle, entryArtist)


# 1. When program starts, read in the currently saved Inventory

print('\nWelcome to your CD Inventory!')
        

lstTbl = FileProcessor.read_file(strFileName, lstTbl) 


# 2. start main loop

while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled\n')
        if strYesNo.lower() == 'yes':
            print('\nreloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('\ncanceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.\n')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.3 process add a CD
    elif strChoice == 'a':
        
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.user_inputs() #Assigned return to variables and unpacked this tuple
        
        # 3.3.2 Add item to the table
        DataProcessor.create_table(strID, strTitle, strArtist, lstTbl) #Arguments are unpacked tuple from IO.user_inputs()
        continue  # start loop back at top.
    
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.5 process delete a CD
    elif strChoice == 'd':
        
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        
        # 3.5.1.2 ask user which ID to remove
        intIDDel = ''
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except ValueError:
                print('\nUh oh! You must enter an integer for the CD ID.\n')
                continue
        
        # 3.5.2 search thru table and delete CD
        DataProcessor.delete_data(intIDDel, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    
    # 3.6 process save inventory to file
    elif strChoice == 's':
        
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        
        # 3.6.2 Process choice
        if strYesNo == 'y':
            
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
            
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')