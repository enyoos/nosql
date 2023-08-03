import json
import threading
import time
import uuid
from os.path import exists, isfile, isfile
import os
from pathlib import Path

LOCK = threading.Lock()
# bool

# custom error class
class InvalidFileExtensionError( Exception ):
    "File extension must be .pst"
    pass

class Database:
    WC_MSG = True
    DEBUG = True
    # for ezz mig \ you can pass directly the data
    # need to input the password ( for decrypting the file )
    def __init__(self, data: dict = {}, path : str = "./default.pst"):
        self.__data= data # this holds all the collections
        self.path = path
        if ( Database.WC_MSG ):
            print ( "thanks for using this library..." )
          
    @staticmethod
    def offW ( ):
        Database.WC_MSG = not ( Database.WC_MSG )

    @staticmethod
    def offD ( ):
        Database.DEBUG = not ( Database.DEBUG )

    # persisting the collect obj 
    # Want to debug ( the message on the console ) -> YES ( leave the debug param to true ) : NO  -> ( make false ) 
    def save(self):
        # try and catch ? 
        obj_serialized = json.dumps( self.__data )
        # issue : always on save we write the whole object ( maybe implement some cache ? )
        with open(self.path , "w") as y:
            y.write(obj_serialized)
            length_byte_written = len( obj_serialized ) * 8
            log_message = "data saved on file {fname} [written : {data_length} bytes ]".format(fname=self.path, data_length=length_byte_written)
            if (Database.DEBUG):
                print (log_message )
            y.close()

    # throws an exception
    @staticmethod
    def load(path : str) :
        # we need to check if the file is encrypted ( if yes, then decrypt )
        if (exists( path ) ):
            if path[-4:] == ".pst":
                with open ( path, "r") as file : 
                    data = file.readlines()
                    data = ''.join( data )
                    data = json.loads( str ( data ) )
                    return Database(data= data, path = path )
            else :
                raise InvalidFileExtensionError
        else:
            raise FileNotFoundError("file {fname} doesn't exist".format( fname = path))

    def __repr__( self ):
        return "path : {path_name}, collections : {coll}".format( path_name = self.path, coll = self.__data )

    def bind_new_collection(self, collection ):
        self.__data[collection.collect_name] = collection.get_all_slot()
        self.save()

    def get_collection(self, coll_name : str ):
        if ( coll_name in list(self.__data.keys())):
            return Collection( coll_name, self.__data[coll_name])
        else :
            print ( "[INFO] this is collection doesn't exist")
            print ( "[INFO] created new collection into {db_name}, with name {coll_name}".format(db_name = self.path, coll_name = coll_name))
            result = Collection( coll_name )
            self.bind_new_collection( result )
            return result
            
    def get_all_collections(self) -> dict :
        return self.__data

class Collection:
    def __init__(self, collect_name : str , __container_documents : list = []): # by default is list ( not None )
        self.collect_name=collect_name
        self.__container_documents = __container_documents# empty list to stores one all the documents
    
    def add_record(self, record : dict ) -> bool :
        # we need to check / if it has the _id prop
        LOCK.acquire()
        try : 
            add_thing = record.copy()
            if not ("_id" in list(add_thing.keys())):
                add_thing['_id'] = self.generate_random_id()            
            self.__container_documents.append(add_thing)
            LOCK.release() 
            return True 
        except:
            LOCK.release() 
            return False 
            
    def __repr__(self):
        return str(self.__container_documents)

    def delete_by_id (self, id : int ) -> bool :
        LOCK.acquire()
        for slot in self.__container_documents :
            if ( slot["_id"] == id ):
                self.__container_documents.remove( slot )
                LOCK.release() 
                return True 

        LOCK.release() 
        return False

    # returns a copy object
    # can return a null value
    def find_by_id (self, id : int ) -> dict:
        for  slot in self.__container_documents :
            if ( slot["_id"] == id ):
                return slot.copy()
        return None  

    def update_obj(self, new_obj : dict) -> bool :
        LOCK.acquire()
        counter = 0
        cpy_new_obj = new_obj.copy() # immutability
        target_id = cpy_new_obj["_id"]
        found = False
        for  slot in self.__container_documents :
            if ( slot["_id"] == target_id ):
                found = True
                break 

            counter += 1 

        if found : 
            self.__container_documents[counter] = cpy_new_obj
            LOCK.release()
            return True 

        LOCK.release()
        return False 

    # the user will provide the search function
    # this function can return a null value
    # returns a cpy of the func
    def search_by(self, slot_name : str , slot_value):
        for  slot in self.__container_documents :
            if ( slot[slot_name] == slot_value ):
                return slot.copy() 
        return None

    def generate_random_id( self, ) -> str:
        return str ( uuid.uuid4() )

    # getter
    def get_all_slot(self):
        return self.__container_documents

