import json
import threading
import time
import uuid
from os.path import exists, basename
import os
from cypher import gen_cipher_file, gen_decypher_file
from pathlib import Path

LOCK = threading.Lock()

# custom error class
class InvalidFileExtensionError( Exception ):
    "File extension must be .pst"
    pass

class Database:
    # for ezz mig \ you can pass directly the data
    # need to input the password ( for decrypting the file )
    def __init__(self, __pass : str, __data : dict = {}, path : str = "./default.pst"):
        self.__data=__data # this holds all the collections
        self.__pass = __pass # this is the encrypt pass 
        print ("[INFO] make sure to remember the pass to decrypt the file...")
        self.path = path
    
    # persisting the collect obj 
    # Want to debug ( the message on the console ) -> YES ( leave the debug param to true ) : NO  -> ( make false ) 
    def save(self, debug : bool = True ):
        # try and catch ? 
        obj_serialized = json.dumps( self.__data )
        # issue : always on save we write the whole object ( maybe implement some cache ? )
        with open(self.path , "w") as y:
            y.write(obj_serialized) # transforms the __data props into a string
            length_byte_written = len( obj_serialized ) * 8
            log_message = "data saved on file {fname} [written : {data_length} bytes ]".format(fname=self.path, data_length=length_byte_written)
            if (debug):
                print (log_message )
            y.close()

        # this is not good ... ( reopening files to much times )        
        # obviously our lib doesn't take into account synchronized request
        # maybe create a lock for synchronizing those parallel request...

    # private method ( with the two underscores )
    @staticmethod
    def __parse_file_content( filename : str ):
        with open(filename , "r") as y:
            str__ = '\n'.join(y.readlines()) # the readlines mehtod returns an array ( so you must polish it first )
            __data = json.loads( str__ )
            y.close()
            return __data

    # throws an exception
    @staticmethod
    def load(path : str, decrypt_pass : str ) :
        # we need to check if the file is encrypted ( if yes, then decrypt )
        if (exists( path ) ):
            if path[-4:] == ".pst":
                __data = parse_file_content( path )
                return Database(__data , path)
            else :
                raise InvalidFileExtensionError
        else:
            raise FileNotFoundError("file {fname} doesn't exist".format( fname = path))

    def __repr__( self ):
        return "path : {path_name}, collections : {coll}".format( path_name = self.path, coll = self.__data )

    def bind_new_collection(self, collection ):
        self.__data[collection.collect_name] = collection._get_all_slot()
        self.save(debug = False)

    def get_collection(self, coll_name : str ):
        if ( col_name in list(self.__data.keys())):
            return Collection( coll_name, self.__data[coll_name])
        else :
            print ( "[INFO] created new collection into {db_name}, with name {coll_name}".format(db_name = self.path, coll_name = coll_name))
            result = Collection( coll_name )
            self.bind_new_collection( result )
            return result

class Collection:
    def __init__(self, collect_name : str , __container_documents : list = []):
        self.collect_name=collect_name
        self.__container_documents = __container_documents# empty list to stores one all the documents
    
    def add_record(self, record : dict ) -> bool :
        # we need to check / if it has the _id prop
        lock.acquire()
        try : 
            add_thing = record.copy()
            if not ("_id" in list(add_thing.keys())):
                add_thing['_id'] = generate_random_id()            
            self.__container_documents.append(add_thing)
            lock.release() 
            return True 
        except:
            lock.release() 
            return False 
            
    def __repr__(self):
        return str(self.__container_documents)

    def delete_by_id (self, id : int ) -> bool :
        lock.acquire()
        for slot in self.__container_documents :
            if ( slot["_id"] == id ):
                self.__container_documents.remove( slot )
                lock.release() 
                return True 

        lock.release() 
        return False

    # returns a copy object
    # can return a null value
    def find_by_id (self, id : int ) -> dict:
        for  slot in self.__container_documents :
            if ( slot["_id"] == id ):
                return slot.copy()
        return None  

    def update_obj(self, new_obj : dict) -> bool :
        lock.acquire()
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
            lock.acquire()
            return True 

        lock.acquire()
        return False 

    # the user will provide the search function
    # this function can return a null value
    # returns a cpy of the func
    def search_by(self, slot_name : str , slot_value):
        for  slot in self.__container_documents :
            if ( slot[slot_name] == slot_value ):
                return slot.copy() 
        return None

    # getter
    def _get_all_slot(self):
        return self.__container_documents

def generate_random_id():
    return str(uuid.uuid4().fields[-1])[:5]
