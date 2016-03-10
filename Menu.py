# this file is for the different menus that may pop up during the program. For now, it's blank, but it won't be for long.
import subprocess
logo = ('' +
        '\n                                      .                                         '+
        '\n                                      .                                         '+
        '\n                                      .                                         '+
        '\n                                      .                                         '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n            .IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII             '+
        '\n        IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII.        '+
        '\n  IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII    '+
        '\n  IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII   '+
        '\n IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII  '+
        '\nIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n                                      I                                         '+
        '\n                                 ==========.                                    '+
        '\n                              ================                                  '+
        '\n                             .=================                                 '+
        '\n                             ==================                                 '+
        '\n                                                                                '
        )



def startUpMenu():


    print('Program: BalsaSimulator')

    print("\n\n\nCreated by Vishakh Pradeep Kumar 2016."+
    "\nEmail: vkumar@gatech.edu \n\n")
    print(logo)

    subprocess.call(['sleep 2'], shell=True)

def endProgram():

    subprocess.call('echo "End of program"', shell=True)
