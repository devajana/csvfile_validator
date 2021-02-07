# CSV Validator

A simple Flask web application that allows the user to upload a .CSV file. On successful file upload, the application performs the following validations:

Checks whether the uploaded is a .CSV and not any other format.
Check whether the .CSV file has exactly 10 rows and 3 columns.
Checks whether the data is present in each cell (.CSV file is "complete").

## Installing requirements
The requirements for the application are mentioned in the 'requirements.txt' file.
>> Execute command to install:
#####        pip3 install -r requirements.txt

## Executing the application
To the run the application, execute the command 
#####        flask run
