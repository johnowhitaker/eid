Hi TIm,
You'll see I have a copy of your spreadsheet there as well, called elephants.xlsx, and the app expects a folder or shortcut to a folder called 'photos' in the app folder. You can replace that with yours - you'll just have to open load_ellie_data.py in a text editor and replace `EID_FORM(os.getcwd() + "/elephants.xlsx", 3, os.getcwd()+"/photos")` with `EID_FORM(\PATH\TO\YOUR\SPREADSHEET", 3, "\PATH\TO\YOUR\PHOTOS\FOLDER")`

The only changes I made to the spreadsheet were to add a * to the column headings for notes and stuff - that lets my program know not to use those in the filter.

I need to do a lot of work making the code better - most of it is just hacked together in a rush :P

Let me know any errors you hit!
