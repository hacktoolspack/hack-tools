from lib.colour import colours


class Report:
    def __init__(self, msg, result=False):
        """
        Handles the message and report it back to console
        :param msg    : String type message
        :param result : the boolean object indicating if the url is vulnerable
        """
        if result:
            print("{}{}{}".format(colours.FAIL, msg, colours.ENDC))
        else:
            print(msg)
