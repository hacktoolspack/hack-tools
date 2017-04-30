

class deduplicate:
    def __init__(self, content):
        """
        Removes the duplciate objects in content
        """
        self.content = content
        self.result = self.clean(content)


    def clean(self, seq):
        """
        The following function f7 is from this file.
        www.peterbe.com/plog/uniqifiers-benchmark/uniqifiers_benchmark.py
        :param seq: sequence of list that needs to be cleaned
        """
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
