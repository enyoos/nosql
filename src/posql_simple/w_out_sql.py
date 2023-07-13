import json
import threading
import time
import uuid
from os.path import exists, isfile, isfile
import os
from pathlib import Path

LOCK = threading.Lock()


# special to handling the char
class UInt8:
    def __init__ ( self, value ):
        self.value = value

    def __int__(self):
        if ( self.value < 32 ):
            return 126
        elif ( self.value > 126 ):
            return 32

    def __repr__(self):
        return "the current value : " + self.value



# the cypher class
class Cypher:
     
    @staticmethod
    def generate_random_id():
        return str(uuid.uuid4().fields[-1])[:5]

    @staticmethod
    def __gen_cypher ( content : str, offset : int ) -> str :
        changed_content = "" 
        for ch in content:
            if ( ch == '\n'):
                changed_content += '\n'
            else :
                changed_content += str ( Cypher.__offset_ch( ch, offset ) )

        return changed_content

    @staticmethod
    def __offset_ch( ch : str , offset : int ) -> str :
        ascii_code = ord ( ch )
        return chr ( int ( UInt8(ascii_code + offset ) ))

    @staticmethod
    def __offset_ch_inv( ch : str, offset : int ) -> str :
        ascii_code = ord ( ch )
        return chr ( abs ( int ( UInt8( ascii_code - offset ) ) ) ) 

    @staticmethod
    def __gen_decypher( content : str , key : int ):
        org_content = ""
        for ch in content:
            if not ( ch == '\n'):
                org_content += str ( Cypher.__offset_ch_inv( ch, key ) )
            else:
                org_content += '\n'
        return org_content

    @staticmethod
    def gen_cipher_file( file_handler , key):
        # r+ for reading and writing
        # leave all the closing to the caller
        contents = file_handler.readlines()
        print ( "teh content of the file : ", contents )
        # this is a list of sentences
        crypted_contents = []

        for content in contents:
            crypted_contents.append(Cypher.__gen_cypher( content, key ))

        file_handler.write( ''.join( crypted_contents ) )

    @staticmethod
    def gen_decypher_file( file_handler, key) -> str :
        contents = file_handler.readlines()
        org_contents = []
        
        for content in contents :
            org_contents.append ( Cypher.__gen_decypher( content, key ) )
    
        return ''.join( org_contents )  # joining the space will add a space between each element

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
            y.write(obj_serialized) # transforms the __data props into a string
            length_byte_written = len( obj_serialized ) * 8
            log_message = "data saved on file {fname} [written : {data_length} bytes ]".format(fname=self.path, data_length=length_byte_written)
            if (debug):
                print (log_message )
            Cypher.gen_cipher_file(y, self.__pass )
            y.close()

    # private method ( with the two underscores )
    @staticmethod
    def __parse_file_content( filename : str, key : str ) :
        with open(filename , "r+") as y:
            __decrypted_data = Cypher.gen_decypher_file(y, key)
            str__ = '\n'.join(__decrypted_data) # the readlines mehtod returns an array ( so you must polish it first )
            __data = json.loads( str__ )
            y.close()
            return __data

    # throws an exception
    @staticmethod
    def load(path : str, decrypt_pass : str ) :
        # we need to check if the file is encrypted ( if yes, then decrypt )
        if (exists( path ) ):
            if path[-4:] == ".pst":
                __data = Database.__parse_file_content( path )
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
    db = Database("hello wordl", path="h.pst")
    cllct = Collection( collect_name="clients")
    db.bind_new_collection( cllct )
    # ascii_code_ch = ord( ch )
    # _ = chr ( ascii_code_ch + 66 )
    # print ( _ , type ( _ ))
    # with open( 'h.pst', 'w') as f : # creates a file just in the write mode
    #     print ( f )