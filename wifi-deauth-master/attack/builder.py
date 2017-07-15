from impl import FixedClientDeauthAttack,\
                 SniffedClientDeauthAttack,\
                 GlobalDisassociationAttack


class WiFiDeauthAttackBuilder(object):
    
    '''This object finds the appropriate attack for the options supplied by the
    user.'''
    
    @classmethod
    def build_from(cls, options):
        subclasses = WiFiDeauthAttackWrapper.__subclasses__()
        candidates = filter(lambda subclass: subclass.handles(options),
                            subclasses)
        return candidates[0](options)
        
        
class WiFiDeauthAttackWrapper(object):
    
    @classmethod
    def handles(cls, options):
        raise NotImplementedError
    
    def __init__(self, options):
        self.options = options
        
    def _get_attack_implementor(self):
        raise NotImplementedError        
        
    def run(self):
        attack = self._get_attack_implementor()
        executions = self.options.executions
        persistence_times = self.options.persistence_times
        return attack.run(executions, persistence_times)
        
        
class FixedClientDeauthAttackWrapper(WiFiDeauthAttackWrapper):
    
    @classmethod
    def handles(cls, options):
        return len(options.client) > 0
    
    def _get_attack_implementor(self):
        interface = self.options.interface
        bssid = self.options.bssid
        client = self.options.client
        return FixedClientDeauthAttack(interface, bssid, [client])
    
    
class GlobalDisassociationAttackWrapper(WiFiDeauthAttackWrapper):
    
    @classmethod
    def handles(cls, options):
        return len(options.client) == 0 and not options.should_sniff
    
    def _get_attack_implementor(self):
        interface = self.options.interface
        bssid = self.options.bssid
        return GlobalDisassociationAttack(interface, bssid)    
    
    
class SniffedClientDeauthAttackWrapper(WiFiDeauthAttackWrapper):
    
    @classmethod
    def handles(cls, options):
        return len(options.client) == 0 and options.should_sniff
    
    def _get_attack_implementor(self):
        interface = self.options.interface
        bssid = self.options.bssid
        timeout = self.options.timeout
        return SniffedClientDeauthAttack(interface, bssid, timeout)   