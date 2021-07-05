# CodeAssessmentOPSWAT
Repository for the coding test given by OPSWAT for SWE Intern Position

### Setup
The command line will be used to run the program, using the Python programming language.
To install, download the files and place them in any suitable location.
Place all the files to be scanned inside the files folder.
Note: 4 sample files are included in the files folder. Ensure the directory layout is correct, where the application can reach the files folder and the files inside. 

The program uses the 'sys', 'hashlib', and 'requests' modules, where 'sys' and 'hashlib' should be built-in. In order to install the 'requests' library, simply run the command 'python -m pip install requests' in your terminal of choice.
Requests library: https://docs.python-requests.org/en/master/

### Running the Program
To run the program, open a command line terminal and navigate to the python file location. Execute the application using the standard python command, passing in the API Key as an argument.
I.e.: 'C:\Path\To\File> python FileScan.py ${APIKEY}'

In the application, enter the filename and extension you wish to scan when prompted for the file_upload.
The application can be closed by using the keyboard interrupt, CTRL+C, at the prompt. 
