# About
Udly - Udemy Downloader GUI

This GUI tool will work over the latest branches of the Udemy Downloader made by Puyodead1

This tool is not to be confused with a full-fledge way to obtain courses as, is just an abstraction layer on top of the downloader program. 

# How to Use?
Put all the files in the udemy-downloader folder.

Then run ```pip install -r requirements.txt``` using the CLI tool of your choice.

You must have the downloader setup with keys and everything or this won't download courses.

Then just run the ```udly.py``` normally.

Browser can be selected using the UI only, if doesn't work please use the further customization instructions.

# Know Bugs
Known bugs include,
1. Script not stopping, using the `Stop Udly Button`
2. Double output of script using the `Start Udly Button` multiple times.
3. The UI buttons are currently not of use - this will change later. Till then follow the further customization instructions.

# Further Customization
Use the ```command = ["python", "main.py", "-c", course_link, ...]``` line of the `udly.py` script to customize the results wanted.

Please follow the command instructions listed on the udemy-downloader github for it. 
