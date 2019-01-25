from libs.pentestlymodule import PentestlyModule

class Module(PentestlyModule):

    meta = {
        'name': 'Your module name goes here',
        'author': 'Developer name goes here',
        'description': 'Description of the module goes here',
        'query': 'SQL QUERY whose result is passed to your module',
        'options': (
            ('Option1', 'Default Value', Required-True/False, 'Description of option'),
        ),
    }

    def module_pre(self):
        # Stuff to always happen before your module

    def module_run(self, data):
        # data is the result from the SQL query set in the options
        
        ### Few magic functions
        # self.query - Perform an SQL query on the internal database
        self.query("select * from pentestly_creds")
        
        # self.output - print default information to the user
        self.output("Performed an SQL query")

        # self.alert - print successful message to the user
        self.success("Yay! We performed successful work")

    def module_post(self):
        # Stuff to happen after your module
