# project

Looking for contributions.

## What ?
really simple no-sql database ( for small projects ) using json.

## Documentation
read the docs.md file.

## Quickstart ( simple example )
```python
from w_out_sql import Database, Collection
my_password = "hello world" # for cipher coding ( key )
path = "./default.pst"      # use the pst extension
my_db = Database (__pass =  password, path = path)
my_collection_name = "clients"
my_collection = Collection ( collect_name = my_collection_name) # creating the collection
db.bind_new_collection(my_collection) # binding the collection to the db

client1 = {
    "name" : "hello world"
}
my_collection.add_record( client1 )  # adding a record to the collection
db.save()                            # saving ( writes data to the file )
```

# Documentation
## Database ( class )
__init__ method requires pass ( for encrypting and decrypting ),
optionally a dict full of collections,
and the path of the file ( where to store the content ).

``save`` method is saving the data in the file,
takes one positional argument for debuging purpose ( default value : True ).

``load`` returns a Database object. The arguments are path ( the path of the file ) and the decrypt_pass.
Throws FileNotFoundError err if the file doesn't exist and ( or ) InvalidFileExtensionError ( if the file extension doesn't match  the .pst ).

``bind_new_collection`` binds the collection to the database object ( for data persistence ). Takes a collection as Param.

``get_collection`` returns a collection object. Args : coll_name ( name of the collection ).
``get_collections`` returns a dict with all the collections. 

## Collection
__init__ method requires a name ( collect_name ),
and a list of the json records ( the data persisted ) which is optinal.


``add_record`` method takes one positional argument which is the json obj that you want to store. Returns a boolean ( True,
if the transaction is OK, and false if it's not ok ).
Each object is **padded** with the "_id" entry ( uuid generated string ).
You can add your own custom "_id" entry.

``delete_by_id`` method takes one positional param which is the id ( making a linear search ). Like the ``add_record`` method, it returns a boolean.

``find_by_id`` same as ``delete_by_id`` ; returning **deep copy** of the dict ( avoid mutability ) or else None.

``update_obj`` : takes two positional args : new_obj ( the obj to persist, must contain an "_id" entry , or else throwing an error ),
returning a bool.

``search_by`` : takes two positional args : slot_name which is the name of the entry you want ( for instance the "name" entry of,
each dict ) and the slot_value. Returns None if not found.

``get_all_slot`` : returns a list of all the entries.

**this lib supports multithreading queries by using synchronization.**