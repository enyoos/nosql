import json
import threading
import time
import uuid
from os.path import exists, isfile, isfile
import os
from pathlib import Path

LOCK = threading.Lock()

# the cypher class
class Cypher:
     
    @staticmethod
    def generate_random_id():
        return str(uuid.uuid4().fields[-1])[:5]

    @staticmethod
    def gen_cypher ( content : str, offset : int ) -> str :
        changed_content = "" 
        for ch in content:
            if ( ch == '\n'):
                changed_content += '\n'
            else :
                changed_content += ( Cypher.__offset_ch( ch = ch, offset=offset ) )

        return changed_content

    @staticmethod
    def __offset_ch( ch : str , offset : int ) -> str :
        print ( 'the value of the offset var : ', offset )
        ascii_code = int ( ord ( ch ) )
        offset = int( offset ) # this is so weird
        char = chr ( ( (ascii_code + offset ) ))
        return char

    @staticmethod
    def __offset_ch_inv( ch : str, offset : int ) -> str :
        ascii_code = ord ( ch )
        return chr ( abs ( ( ( ascii_code - offset ) ) ) ) 

    @staticmethod
    def gen_decypher( content : str , key : int ):
        org_content = ""
        for ch in content:
            if not ( ch == '\n'):
                org_content += str ( Cypher.__offset_ch_inv( ch, key ) )
            else:
                org_content += '\n'
        return org_content

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
        self.path = path
        print ("[INFO] make sure to remember the pass to decrypt the file...")
        if ( not isfile(self.path )):
            with open( self.path , 'w') as f : f.close()      # creating the file
           
    # persisting the collect obj 
    # Want to debug ( the message on the console ) -> YES ( leave the debug param to true ) : NO  -> ( make false ) 
    def save(self, debug : bool = True ):
        # try and catch ? 
        obj_serialized = json.dumps( self.__data )
        # issue : always on save we write the whole object ( maybe implement some cache ? )
        with open(self.path , "r+") as y:
            y.write(Cypher.gen_cypher(coobj_serialized, self.__pass))
            length_byte_written = len( obj_serialized ) * 8
            log_message = "data saved on file {fname} [written : {data_length} bytes ]".format(fname=self.path, data_length=length_byte_written)
            if (debug):
                print (log_message )
            y.close()

    # throws an exception
    @staticmethod
    def load(path : str, decrypt_pass : str ) :
        # we need to check if the file is encrypted ( if yes, then decrypt )
        if (exists( path ) ):
            if path[-4:] == ".pst":
                with open ( path, "r") as file : 
                    data = file.readlines()
                    data = Cypher.gen_decypher(content=data, key=decrypt_pass)
                    return Database(__data = data, path = path, __pass = decrypt_pass )
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
            
    def get_all_collections(self) -> dict :
        return self.__data

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
                add_thing['_id'] = Cypher.generate_random_id()            
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
    

if __name__ == "__main__":
    print ( "hello wordl " )