from pymongo import MongoClient, errors
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self):
        ## Initializing the MongoClient. 
        self.USER = 'aacuser'  
        self.PASS = 'SNHU1234' 
        self.HOST = 'nv-desktop-services.apporto.com'
        self.PORT = 30002
        self.DB = 'AAC'
        self.COL = 'animals'
        
        self.connect()
        
    def connect(self):
        try:
            #self.client = MongoClient('mongodb://%s:%s@%s:%d/%s' % (USER,PASS,HOST,PORT, 'admin'))
            self.client = MongoClient(f'mongodb://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/admin')
            # self.client.server_info()
            #self.database = self.client['%s' % (DB)]
            self.database = self.client[self.DB]
            #self.collection = self.database['%s' % (COL)]
            self.collection = self.database[self.COL]
            print(f"Successfully connected to MongoDB at {self.HOST}:{self.PORT}")
        except errors.ServerSelectionTimeoutError as err:
            print("Failed to connect to MongoDB server:", err)
            
    def set_username(self, username):
        self.USER = username
        self.connect()
        
    def set_password(self, password):
        self.PASS = password
        self.connect()
        
    def set_host(self, host):
        self.HOST = host
        self.connect()
        
    def set_port(self, port):
        self.PORT = port
        self.connect()
        
    def set_database(self, database):
        self.DB = database
        self.connect()
        
    def set_collection(self, collection):
        self.COL = collection
        self.connect()

    # Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None and isinstance(data, dict):
            try:
                self.collection.insert_one(data)  # data should be a dictionary
                print("Document inserted successfully.")
                return True
            except errors.PyMongoError as e:
                print(f"An error occurred during insertion: {e}")
            except errors.ServerSelectionTimeOutError as err:
                print("Failed to connect to MongoDB server: ", err)
            except errors.PyMongoError as e:
                print(f"An unexpected error occurerred: {e}")

    # Create method to implement the R in CRUD.
    def read(self, query=None):
        if query is not None:
            print(self.database.list_collection_names())
            try:
                # Use find() to query the collection with the given query
                documents = self.collection.find(query)
                # Convert the cursor to a list to return the result
                return list(documents)
            except Exception as e:
                print(f"An error occurred during query: {e}")
                return []
        else:
            raise Exception("Nothing to query, because query parameter is empty")  
       
    # Update method to implement the U in CRUD
    def update(self, query=None, update_data=None, multiple=False):
        if query is not None and update_data is not None:
            try:
                update_query = {"$set": update_data}
                
                if multiple:
                    result = self.collection.update_many(query, update_many)
                else:
                    result = self.collection.update_one(query, update_query)
                    
                return result.modified_count
            except Exception as e:
                print(f"An error occurred during update: {e}")
                return 0
        else:
            raise Exception("Both query an dupdate_data must be provided")
            
    # Delete method to implement the D in CRUD
    def delete(self, query=None, multiple=False):
        if query is not None:
            try:
                if multiple:
                    result = self.collection.delete_many(query)
                else:
                    result = self.collection.delete_one(query)
                return result.deleted_count
            except Exception as e:
                print(f"An error occurred during delete: {e}")
                return 0
        else:
            raise Exception("Query parameter must be provided")
            
            
 