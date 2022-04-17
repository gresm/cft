"""This is submodule created for handling database"""
from .load import load, savedb


usersdb, challengesdb = load()

# check validness of databases
savedb(usersdb)  # users database is invalid
savedb(challengesdb)  # challenges database is invalid
