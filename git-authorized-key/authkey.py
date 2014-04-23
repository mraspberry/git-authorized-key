def create_authorized_key(key_string):
    """Takes a string as-is from an authorized_keys or id_*.pub file
       and creates an AuthorizedKey object out of it"""

    key_type,key_text,key_comment = key_string.split()
    return AuthorizedKey(key_type,key_text,key_comment)

class AuthorizedKey (object):
    def __init__(self,key_type,key_text,key_comment):
        self._validate_key_type(key_type)
        self.key_type = key_type
        self.key_text = key_text
        self.key_comment = key_comment

    def __str__(self):
        authkey = ' '.join([self.key_type,self.key_text,self.key_comment])
        return authkey

    def _validate_key_type(self,key_type):
        valid_types = ['ecdsa-sha','ssh-rsa','ssh-dss','ssh-ed25519']
        valid = False
        for valid_key_type in valid_types:
            if key_type.startswith(valid_key_type):
                valid = True
        if not valid:
            msg = "key_type must be one of: {0}".format(valid_types)
            raise ValueError(msg)
