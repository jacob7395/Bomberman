import sys
import time as t
import os
from os import path


def Report_Error(error, fatal=False):
    "Reports errors to the error file located in game dir for this run"
    error_Path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    error_Path += '/' + "Error_Report"

    with open(error_Path, 'a') as error_File:
        date = t.localtime(t.time())
        # time stamp = Day_Month_Year-Hour:Min:Sec
        time_Stamp = "[%2s_%2s_%2s-%2s:%2s:%2s] - " % ((date[2], date[1], (date[0] - 2000), date[3], date[4], date[5]))
        if(fatal == False):
            error_File.write(time_Stamp + error + '\n')
        else:
            error_File.write(time_Stamp + error + ' - FATAL ERROR\n')
            print("Fatal Error - " + error)
            sys.exit(1)


def Make_Error_File():
    "Makes error report file"
    error_Path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    error_Path += '/' + "Error_Report"

    if(path.isfile(error_Path)):
        os.remove(error_Path)
