import hashlib
from lib.core.settings import LOGGER


class HashCracker(object):

    results = {}
    cracked = False

    def __init__(self, hash, wordlist=open("lib/text_files/wordlist.txt").readlines(), type=None):
        self.hash = hash
        self.words = wordlist
        self.type = type

    def try_all_algorithms(self):
        """ Try every algorithm available on the computer using the 'algorithms_available' functions from hashlib
        an example of this functions would be:
        >>> print(hashlib.algorithms_available)
        set(['SHA1', 'SHA224', 'SHA', 'SHA384', ...])
        >>> HashCracker("9a8b1b7eee229046fc2701b228fc2aff", type=None).try_all_algorithms()
        {..., 'dc1e4c61bea0e5390c140fb1299a68a0f31b7af51f90abbd058f09689a8bb823': ['1 endow', 'sha256'],
        '362b004395a3f52d9a0132868bd180bd': ['17 fellowship', 'MD5'],
        '03195f6b6fa8dc1951f4944aed8cc4582cd72321': ['lovingkindness', 'RIPEMD160'], ..."""
        for alg in hashlib.algorithms_available:
            for word in self.words:
                data = hashlib.new(alg)
                data.update(word.strip())
                self.results[data.hexdigest()] = [word.strip(), alg]
        LOGGER.info("Created %i hashes, verifying against given hash (%s)" % (len(self.results), self.hash))
        if self.verify_hashes() is False:
            LOGGER.fatal("Unable to verify hash: %s" % self.hash)
        else:
            return self.verify_hashes()

    def try_certain_algorithm(self):
        """ Use a certain type of algorithm to do the hashing, md5, sha256, etc..
        >>> HashCracker("9a8b1b7eee229046fc2701b228fc2aff", type="md5").try_certain_algorithm()
        {... ,'9a8b1b7eee229046fc2701b228fc2aff': ['want', 'md5'], ...} """
        data = hashlib.new(self.type)
        for word in self.words:
            data.update(word.strip())
            self.results[data.hexdigest()] = [word.strip(), self.type]
        LOGGER.info("Created %i hashes to verify.." % len(self.results.keys()))
        LOGGER.info("Attempting to crack hash (%s).." % self.hash)
        if self.verify_hashes() is False:
            error_message = "Unable to verify %s against %i different hashes." % (self.hash, len(self.results))
            error_message += " You used algorithm: %s you can attempt all algorithms " % str(self.type).upper()
            error_message += "available on the system by running with 'all' as the hash type. "
            error_message += "IE: python pybelt.py -c 9a8b1b7eee229046fc2701b228fc2aff:all"
            LOGGER.fatal(error_message)
            exit(1)

    def verify_hashes(self):
        """ Verify if the hashes match, as long as the hash is in the results dict, it will be found
        >>> print(self.results)
        {... ,'9a8b1b7eee229046fc2701b228fc2aff': ['want', 'md5'], ... }
        >>> HashCracker("9a8b1b7eee229046fc2701b228fc2aff", type="md5").verify_hashes()
        [06:08:49 INFO] Original Hash: 9a8b1b7eee229046fc2701b228fc2aff
                        Algorithm Used: MD5
                        Plain Text: want """
        spacer = " " * 16
        while self.cracked is False:
            for h in self.results.keys():
                if self.hash == h:
                    hash_results = "Original Hash: %s" % self.hash
                    hash_results += "\n%sAlgorithm Used: %s" % (spacer, self.results[self.hash][1].upper())
                    hash_results += "\n%sPlain Text: %s" % (spacer, self.results[self.hash][0])
                    LOGGER.info(hash_results)
                    self.cracked = True
        return

