class APIException(Exception): pass
class WebException(Exception): pass
class InternalException(APIException): pass

"""

CTF Platform Error Code Reference.

    1.	User logged in successfully, but the document associated with that user doesn't have a userID. If the competition hasn't started, just make a new account. Otherwise, have one of the mods generate a new userID.
    2.	TODO

"""