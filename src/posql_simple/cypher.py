# making up ezz cipher func
sercret_msg = "attacking tonight"
key = 5

# for now the uppercase will not be preserved
def gen_cypher ( content : str, offset : int ) -> str :
    changed_content = "" 
    for ch in content:
        if ( ch == '\n'):
            changed_content += '\n'
        else :
            changed_content += offset_ch( ch, offset )

    return changed_content

def offset_ch( ch : str , offset : int ) -> str :
    ascii_code = ord ( ch )
    return chr ( ascii_code + offset ) 

def offset_ch_inv( ch : str, offset : int ) -> str :
    ascii_code = ord ( ch )
    return chr ( ascii_code - offset ) 

def gen_decypher( content : str , key : int ):
    org_content = ""
    for ch in content:
        if not ( ch == '\n'):
            org_content += offset_ch_inv( ch, key )
        else:
            org_content += '\n'
    return org_content

def gen_cipher_file( f, key):
    # r+ for reading and writing
    contents = readlines( f )
    with open ( f, "w") as somefile :
        # this is a list of sentences
        crypted_contents = []

        for content in contents:
            crypted_contents.append(gen_cypher( content, key ))

        somefile.write( ''.join( crypted_contents ) )
        somefile.close()

def gen_decypher_file( f, key) -> str :
    with open (f, "r") as somefile :
        contents = somefile.readlines()
        org_contents = []
        
        for content in contents :
            org_contents.append ( gen_decypher( content, key ) )
    
        somefile.close()
        return ''.join( org_contents )  # joining the space will add a space between each element

def readlines( f ) -> str :
    with open( f, "r") as somefile:
        str__ = somefile.readlines()
        somefile.close()
        return str__