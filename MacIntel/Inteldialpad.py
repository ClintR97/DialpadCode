import csv
import os
import urllib.request
from tkinter import Tk # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import ttk
from tkinter import *
from tkinter import filedialog as fd
from tkinter.filedialog import askdirectory
import ssl
import certifi
from urllib.request import urlopen
import tkinter as tk
import urllib.error
from tkinter.messagebox import showinfo


# create a tkinter GUI window
root = tk.Tk()

# set the title of the window
root.title('Select source call log csv')

# make the window resizable, but only in the horizontal direction
root.resizable(True, False)

# set the size of the window
root.geometry('300x150')

# create a tkinter variable to store the name of the selected file
select_filename_var = StringVar()

# create a label to display the name of the selected file
label = tk.Label(root,textvariable=select_filename_var,fg='red' , anchor='center')
label.grid(row=3,column=1) 

# set the initial value of the label to an empty string
select_filename_var.set("")

# create a tkinter variable to store the path of the selected directory
filepath_var = StringVar()

# create a label to display the path of the selected directory
label = tk.Label(root,textvariable=filepath_var,fg='red' , anchor='center')
label.grid(row=7,column=1) 

# set the initial value of the label to an empty string
filepath_var.set("")

# create a function to close the GUI window
def close():
    root.destroy()

# create a function to select a csv file using the tkinter file dialog
def select_file():

    filename = fd.askopenfilename(
        title='Select csv File',
        initialdir='/',
        filetypes= (
        ('csv files', '*.csv'),
        ('All files', '*.*')
    ))

    # if a file is selected, update the label to display the name of the file
    if(filename):
        select_filename_var.set(filename)

        # open the file and print its contents to the console
        fob=open(filename,'r')
        print(fob.read())

    # show a pop-up message with the name of the selected file
    select_filename_var.set(filename)

    showinfo(
        title='Selected File',
        message=filename
    )

# create a tkinter button to select a csv file
select_button = ttk.Button(
    root,
    text='Select csv File',
    command=select_file
)

# place the button in the window using the grid layout manager
select_button.place(relx=0.50, rely=0.33, anchor=CENTER)

# create a function to select a download directory using the tkinter file dialog
# The function below is called when the user clicks the download button to select a directory.
def download_dir():
    # Open a file dialog window to allow the user to select a download location.
    select_dir = fd.askdirectory(title="Select Download Location", initialdir="/")
    # Set the value of the filepath variable to the selected directory.
    filepath_var.set(select_dir)
    # Display the selected directory to the user in a message box.
    showinfo(title='Selected Directory', message=select_dir)

# Create a "Select Download Location" button that calls the download_dir() function when clicked.
download_button = ttk.Button(
    root,
    text='Select Download Location',
    command=download_dir
)
download_button.place(relx=0.50, rely=0.66, anchor=CENTER)

# Create a "Next" button that calls the "close" function when clicked.
close_button = Button(root, text = 'Next', command = close)
close_button.grid(row=10, column=1, sticky='SE')

# Run the tkinter application.
root.mainloop()

# Get the values of the select_filename_var and filepath_var variables as strings.
select_filename = select_filename_var.get()
filepath = filepath_var.get()

# Define a function that creates a new folder based on the name of the person in a given row of the CSV file.
def create_folder(row):
    # Get the name of the person in the current row.
    name = row['name']
    # Create a new directory path by concatenating the download location with the person's name.
    dst_path = filepath + "/" + name
    # Print out the download location and the name of the person for whom a folder is being created.
    print("Download location set to:", dst_path)
    print("Creating folder for:", name)
    # If the directory doesn't already exist, create it.
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    # Return the path to the new folder.
    return dst_path

# Define a function that counts the number of lines in the CSV file.
def line_count():
    # Open the CSV file and count the number of lines, subtracting one for the header row.
    with open(select_filename) as file:
        count = len(file.readlines()) - 1
        file.close
        return count

# Open the CSV file and iterate through each row.
with open(select_filename) as csvfile:
    # Use the csv.DictReader() function to create a dictionary from each row.
    callLog = csv.DictReader(csvfile)
    # Call the line_count() function to get the total number of rows in the file.
    log_total = line_count()
    # Iterate through each row in the CSV file.
    for count, row in enumerate(callLog, start=1):
        # If this is the first row in the file, create a folder for the person in the row.
        if count == 1:
            dest_folder = create_folder(row)
            # Use the date, external phone number, and file extension to create a new filename.
            new_filename = f"{dest_folder}"+"/"+ f"{row['date']}".replace("/", "-").replace(":", "-").replace(" ", "_") + "_" + f"{row['external_number']}.mp3"
        # Get the URL of the recording for the current row.
        request = row['recording_url']
        # Open the URL using urllib and create a new filename based on the date and external phone number.
        urlopen(request, context=ssl.create_default_context(cafile=certifi.where()))
        try:
            urllib.request.urlretrieve(row['recording_url'], new_filename)
            # added this to add more details to out error outputs when we get them. 
        except urllib.error.HTTPError as error:
            print(error)
            print("Failed to download " + f"{row['recording_url']}")
        print("Saving number",count, "of", log_total)
    print("Job completed!")

