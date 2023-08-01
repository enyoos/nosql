from w_out_sql import Database, Collection


def add_db ( name : str ) -> Database: return Database(path="test.pst")

if __name__ == "__main__":

    db = Database.load(path="test.pst")
    # db = add_db( "test.pst" )
    cllct = Collection( collect_name="clients")
    db.bind_new_collection( cllct )
    r = {
        "name" : "somename"
    }
    cllct.add_record( r )
    db.save()

    print ( db )