from lib.core.settings import LOGGER
from lib.core.settings import HASH_TYPE_REGEX


class HashChecker(object):

    def __init__(self, check_hash):
        self.hash = check_hash
        self.found = False

    def obtain_hash_type(self):
        for algorithm in HASH_TYPE_REGEX:
            if algorithm.match(self.hash):
                self.found = True
                self.enumerate_hash_types(HASH_TYPE_REGEX[algorithm])
        if self.found is False:
            error_message = "Unable to verify hash type "
            error_message += "for hash: '{}'. This could mean ".format(self.hash)
            error_message += "that this is not a valid hash, or that "
            error_message += "this hash is not supported by Pybelt "
            error_message += "yet. If you feel this should be supported "
            error_message += "make an issue regarding this hash."
            LOGGER.error(error_message)
            return

    @staticmethod
    def enumerate_hash_types(items, max_likeliest=3):
        LOGGER.info("{} possible hash types found..".format(len(items)))
        for count, item in enumerate(items, start=1):
            if count <= max_likeliest:
                print("\033[92m[*] Most likely possible hash type: {}\033[0m".format(item))
                if count == max_likeliest:
                    print("")
            else:
                print("\033[33m[*] Least likely possible hash type: {}\033[0m".format(item))
