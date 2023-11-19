"""Placeholder for global variables."""
class GlobalVar():
    logged_in_user = None
    def set_logged_in_user(self, value):
        GlobalVar.logged_in_user = value
        print("value set!") # DEBUG
    
    def get_logged_in_user(self):
        return GlobalVar.logged_in_user
