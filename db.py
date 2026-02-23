# Made by Maheen Abbasi for the 291 mini-project 1 on Feb. 23 2026

"""
This file will contain helper functions related to the db

Rules: db filename from commandline only; no hardcoding; parameterized queries
"""

# imports
import sqlite3
import sys

"""
Basic function to allow the user to provide the name of the db file to open.
Will open the db file and create a connection, or send an error if a connection could not be made.

Input: N/A
Output: N/A
"""
def connect():
    # user provides 1 arg, remind them of format -> sys.argv[0] = script name; sys.argv[1] = db file
    if len(sys.argv) != 2:
        print("Useage: python main.py <database_file>")
        sys.exit(1)

    # file should be the first in the list of args given by user
    file = sys.argv[1]

    try:
        # open the db file and create a connection object
        conn = sqlite3.connect(file)
        conn.row_factory = sqlite3.Row
        return conn
    
    except Exception as e:
        print("Couldn't connect to db:", e)
        sys.exit(1)