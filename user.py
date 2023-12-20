from random import randint


    
    
class User:
    def __init__(self, first_name, last_name,  email, password, role):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role
        



    
            
            
    
        
        
        
# def create_random_user_id(self):
#         data = DatabaseHandler.get_all_data_from_users()   
#         while True:
#             self.user_id = randint(999,9999)
            
#             #checks for duplicate ID
#             if any(user.user_id == self.user_id for user in data):
#                 continue
#             else:
#                 return self.user_id
        
        
