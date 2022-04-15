"""This is submodule created for handling database"""
from .load import load
from .data import UsersDB


raw_users, raw_challenges = load()
usersdb = UsersDB(raw_users)
