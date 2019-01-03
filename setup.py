import cx_Freeze, os

#change these to user appropriate tcl and tk folders
os.environ['TCL_LIBRARY'] = r'C:\Users\Scott\AppData\Local\Programs\Python\Python37\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Scott\AppData\Local\Programs\Python\Python37\tcl\tk8.6'

filenames = []
for filename in os.listdir('cards'):
        if filename.endswith('.jpg'):
            filenames.append('cards/'+filename)
for filename in os.listdir('misc'):
        if filename.endswith('.jpg'):
            filenames.append('misc/'+filename)

#or blackjack_one-file.py
executables = [cx_Freeze.Executable('blackjack.py')]

cx_Freeze.setup(
    name = "Blackjack",
    options = {"build_exe":{"packages":["pygame"],"include_files":filenames}},
    description = 'Simple Blackjack game made with Pygame.',
    executables = executables
)