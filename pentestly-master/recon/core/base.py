from __future__ import print_function

__author__    = '@ctfhacker'
__email__     = 'cory.duplantis@praetorian.com'

import errno
import imp
import json
import os
import random
import re
import shutil
import sys
import __builtin__

# import framework libs
from recon.core import framework

# set the __version__ variable based on the VERSION file
execfile(os.path.join(sys.path[0], 'VERSION'))

# using stdout to spool causes tab complete issues
# therefore, override print function
# use a lock for thread safe console and spool output
from threading import Lock
_print_lock = Lock()
# spooling system
def spool_print(*args, **kwargs):
    with _print_lock:
        if framework.Framework._spool:
            framework.Framework._spool.write('%s\n' % (args[0]))
            framework.Framework._spool.flush()
        if 'console' in kwargs and kwargs['console'] is False:
            return
        # new print function must still use the old print function via the backup
        __builtin__._print(*args, **kwargs)
# make a builtin backup of the original print function
__builtin__._print = print
# override the builtin print function with the new print function
__builtin__.print = spool_print

KEY_RESOURCES = [
]

#=================================================
# BASE CLASS
#=================================================

class Recon(framework.Framework):

    def __init__(self, mode):
        framework.Framework.__init__(self, 'base')
        self._mode = mode
        self._name = 'pentestly'
        self._prompt_template = '%s[%s] > '
        self._base_prompt = self._prompt_template % ('', self._name)
        # establish dynamic paths for framework elements
        self.app_path = framework.Framework.app_path = sys.path[0]
        self.data_path = framework.Framework.data_path = os.path.join(self.app_path, 'data')
        self.core_path = framework.Framework.core_path = os.path.join(self.app_path, 'core')
        self.options = self._global_options
        self._init_global_options()
        self._init_home()
        self.init_workspace('default')
        if self._mode == Mode.CONSOLE:
            self.show_banner()
        self.analytics = False

    #==================================================
    # SUPPORT METHODS
    #==================================================

    def _init_global_options(self):
        self.register_option('debug', False, True, 'enable debugging output')
        self.register_option('threads', 10, True, 'number of threads (where applicable)')
        self.register_option('timeout', 10, True, 'socket timeout (seconds)')
        self.register_option('verbose', True, True, 'enable verbose output')

    def _init_home(self):
        self._home = framework.Framework._home = os.path.join(os.path.expanduser('~'), '.pentestly')
        # initialize home folder
        if not os.path.exists(self._home):
            os.makedirs(self._home)

    def _load_modules(self):
        self.loaded_category = {}
        self._loaded_modules = framework.Framework._loaded_modules
        # crawl the module directory and build the module tree
        for path in [os.path.join(x, 'modules') for x in (self.app_path, self._home)]:
            for dirpath, dirnames, filenames in os.walk(path):
                # remove hidden files and directories
                filenames = [f for f in filenames if not f[0] == '.']
                dirnames[:] = [d for d in dirnames if not d[0] == '.']
                if len(filenames) > 0:
                    for filename in [f for f in filenames if f.endswith('.py')]:
                        is_loaded = self._load_module(dirpath, filename)
                        mod_category = 'disabled'
                        if is_loaded:
                            mod_category = re.search('/modules/([^/]*)', dirpath).group(1)
                        # store the resulting category statistics
                        if not mod_category in self.loaded_category:
                            self.loaded_category[mod_category] = 0
                        self.loaded_category[mod_category] += 1

    def _load_module(self, dirpath, filename):
        mod_name = filename.split('.')[0]
        mod_dispname = '/'.join(re.split('/modules/', dirpath)[-1].split('/') + [mod_name])
        mod_loadname = mod_dispname.replace('/', '_')
        mod_loadpath = os.path.join(dirpath, filename)
        mod_file = open(mod_loadpath)
        try:
            # import the module into memory
            mod = imp.load_source(mod_loadname, mod_loadpath, mod_file)
            __import__(mod_loadname)
            # add the module to the framework's loaded modules
            self._loaded_modules[mod_dispname] = sys.modules[mod_loadname].Module(mod_dispname)
            return True
        except ImportError as e:
            # notify the user of missing dependencies
            self.error('Module \'%s\' disabled. Dependency required: \'%s\'' % (mod_dispname, e.message[16:]))
        except:
            # notify the user of errors
            self.print_exception()
            self.error('Module \'%s\' disabled.' % (mod_dispname))
        # remove the module from the framework's loaded modules
        self._loaded_modules.pop(mod_dispname, None)
        return False

    def _menu_egg(self, params):
        eggs = [
                'Number? Really? What do you think this is?',
                'Roses are red, violets are blue..',
                'Do you know what you are doing?',
                '*grunt* *grunt* Nope. I got nothin\'.',
                'Type that number again for super secret mode.',
                'This is not Metasploit.',
                'I think we need to go back to HowToH@ck 101.',
                'Something something do more CTFs something something',
                'Attempting to start Metasploit...',
                'ctfhacker.com is the place to be.'
                ]
        print(random.choice(eggs))
        return 

    #==================================================
    # WORKSPACE METHODS
    #==================================================

    def init_workspace(self, workspace):
        workspace = os.path.join(self._home, 'workspaces', workspace)
        new = False
        try:
            os.makedirs(workspace)
            new = True
        except OSError as e:
            if e.errno != errno.EEXIST:
                self.error(e.__str__())
                return False
        # set workspace attributes
        self.workspace = framework.Framework.workspace = workspace
        self.prompt = self._prompt_template % (self._base_prompt[:-3], self.workspace.split('/')[-1])
        # configure new database or conduct migrations
        self._create_db() if new else self._migrate_db()
        # load workspace configuration
        self._init_global_options()
        self._load_config()
        # load modules after config to populate options
        self._load_modules()
        return True

    def delete_workspace(self, workspace):
        path = os.path.join(self._home, 'workspaces', workspace)
        try:
            shutil.rmtree(path)
        except OSError:
            return False
        if workspace == self.workspace.split('/')[-1]:
            self.init_workspace('default')
        return True

    def _get_workspaces(self):
        dirnames = []
        path = os.path.join(self._home, 'workspaces')
        for name in os.listdir(path):
            if os.path.isdir(os.path.join(path, name)):
                dirnames.append(name)
        return dirnames

    def _get_snapshots(self):
        snapshots = []
        for f in os.listdir(self.workspace):
            if re.search('^snapshot_\d{14}.db$', f):
                snapshots.append(f)
        return snapshots

    def _create_db(self):
        self.query('CREATE TABLE IF NOT EXISTS ports (ip_address TEXT, host TEXT, port TEXT, protocol TEXT, module TEXT)')
        self.query('CREATE TABLE IF NOT EXISTS dashboard (module TEXT PRIMARY KEY, runs INT)')
        self.query("CREATE TABLE IF NOT EXISTS pentestly_creds (host TEXT, access TEXT, username TEXT, password TEXT, domain TEXT, process TEXT, logged_in TEXT, success TEXT, execute TEXT, module TEXT)")
        self.query("CREATE TABLE IF NOT EXISTS pentestly_shares (host TEXT, username TEXT, readwrite TEXT, readonly TEXT, noaccess TEXT, module TEXT)")
        self.query('PRAGMA user_version = 0')

    def _migrate_db(self):
        db_version = lambda self: self.query('PRAGMA user_version')[0][0]

    #==================================================
    # SHOW METHODS
    #==================================================

    def show_banner(self):
        banner = open(os.path.join(self.data_path, 'banner.txt')).read()
        banner_len = len(max(banner.split('\n'), key=len)) / 2
        print(framework.Colors.N + banner + framework.Colors.N)
        # print('{0:^{1}}'.format('%s[%s v%s, %s]%s' % (framework.Colors.G, self._name, __version__, __author__, framework.Colors.N), banner_len+8)) # +8 compensates for the color bytes
        # print('%s[%s v%s, %s]%s' % (framework.Colors.B, self._name, __version__, __author__, framework.Colors.N), banner_len+8) # +8 compensates for the color bytes
        print('')
        counts = [(self.loaded_category[x], x) for x in self.loaded_category]
        count_len = len(max([str(x[0]) for x in counts], key=len))
        for count in sorted(counts, reverse=True):
            cnt = '[%d]' % (count[0])
            print('%s%s %s modules%s' % (framework.Colors.B, cnt.ljust(count_len+2), count[1].title(), framework.Colors.N))
            # create dynamic easter egg command based on counts
            setattr(self, 'do_%d' % count[0], self._menu_egg)
        print('')

    #==================================================
    # COMMAND METHODS
    #==================================================

    def do_reload(self, params):
        '''Reloads all modules'''
        self.output('Reloading...')
        self._load_modules()

    def do_workspaces(self, params):
        '''Manages workspaces'''
        if not params:
            self.help_workspaces()
            return
        params = params.split()
        arg = params.pop(0).lower()
        if arg == 'list':
            self.table([[x] for x in self._get_workspaces()], header=['Workspaces'])
        elif arg in ['add', 'select']:
            if len(params) == 1:
                if not self.init_workspace(params[0]):
                    self.output('Unable to initialize \'%s\' workspace.' % (params[0]))
            else: print('Usage: workspace [add|select] <name>')
        elif arg == 'delete':
            if len(params) == 1:
                if not self.delete_workspace(params[0]):
                    self.output('Unable to delete \'%s\' workspace.' % (params[0]))
            else: print('Usage: workspace delete <name>')
        else:
            self.help_workspaces()

    def do_snapshots(self, params):
        '''Manages workspace snapshots'''
        if not params:
            self.help_snapshots()
            return
        params = params.split()
        arg = params.pop(0).lower()
        if arg == 'list':
            snapshots = self._get_snapshots()
            if snapshots:
                self.table([[x] for x in snapshots], header=['Snapshots'])
            else:
                self.output('This workspace has no snapshots.')
        elif arg == 'take':
            from datetime import datetime
            snapshot = 'snapshot_%s.db' % (datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
            src = os.path.join(self.workspace, 'data.db')
            dst = os.path.join(self.workspace, snapshot)
            shutil.copyfile(src, dst)
            self.output('Snapshot created: %s' % (snapshot))
        elif arg == 'load':
            if len(params) == 1:
                # warn about overwriting current state
                if params[0] in self._get_snapshots():
                    src = os.path.join(self.workspace, params[0])
                    dst = os.path.join(self.workspace, 'data.db')
                    shutil.copyfile(src, dst)
                    self.output('Snapshot loaded: %s' % (params[0]))
                else:
                    self.error('No snapshot named \'%s\'.' % (params[0]))
            else: print('Usage: snapshots [load] <name>')
        elif arg == 'delete':
            if len(params) == 1:
                if params[0] in self._get_snapshots():
                    os.remove(os.path.join(self.workspace, params[0]))
                    self.output('Snapshot removed: %s' % (params[0]))
                else:
                    self.error('No snapshot named \'%s\'.' % (params[0]))
            else: print('Usage: snapshots [delete] <name>')
        else:
            self.help_snapshots()

    def do_load(self, params):
        '''Loads specified module'''
        try:
            self._validate_options()
        except framework.FrameworkException as e:
            self.error(e.message)
            return
        if not params:
            self.help_load()
            return
        # finds any modules that contain params
        modules = [params] if params in self._loaded_modules else [x for x in self._loaded_modules if params in x]
        # notify the user if none or multiple modules are found
        if len(modules) != 1:
            if not modules:
                self.error('Invalid module name.')
            else:
                self.output('Multiple modules match \'%s\'.' % params)
                self.show_modules(modules)
            return
        # load the module
        mod_dispname = modules[0]
        # loop to support reload logic
        while True:
            y = self._loaded_modules[mod_dispname]
            # send analytics information
            mod_loadpath = os.path.abspath(sys.modules[y.__module__].__file__)
            # if (self._home not in mod_loadpath) and self.analytics:
                # self._send_analytics(mod_dispname)
            # return the loaded module if in command line mode
            if self._mode == Mode.CLI:
                return y
            # begin a command loop
            y.prompt = self._prompt_template % (self.prompt[:-3], mod_dispname.split('/')[-1])
            try:
                y.cmdloop()
            except KeyboardInterrupt:
                print('')
            if y._exit == 1:
                return True
            if y._reload == 1:
                self.output('Reloading...')
                # reload the module in memory
                is_loaded = self._load_module(os.path.dirname(mod_loadpath), os.path.basename(mod_loadpath))
                if is_loaded:
                    # reload the module in the framework
                    continue
                # shuffle category counts?
            break

    do_use = do_load

    #==================================================
    # HELP METHODS
    #==================================================

    def help_workspaces(self):
        print(getattr(self, 'do_workspaces').__doc__)
        print('')
        print('Usage: workspaces [list|add|select|delete]')
        print('')

    def help_snapshots(self):
        print(getattr(self, 'do_snapshots').__doc__)
        print('')
        print('Usage: snapshots [list|take|load|delete]')
        print('')

    #==================================================
    # COMPLETE METHODS
    #==================================================

    def complete_workspaces(self, text, line, *ignored):
        args = line.split()
        options = ['list', 'add', 'select', 'delete']
        if 1 < len(args) < 4:
            if args[1].lower() in options[2:]:
                return [x for x in self._get_workspaces() if x.startswith(text)]
            if args[1].lower() in options[:2]:
                return []
        return [x for x in options if x.startswith(text)]

    def complete_snapshots(self, text, line, *ignored):
        args = line.split()
        options = ['list', 'take', 'load', 'delete']
        if 1 < len(args) < 4:
            if args[1].lower() in options[2:]:
                return [x for x in self._get_snapshots() if x.startswith(text)]
            if args[1].lower() in options[:2]:
                return []
        return [x for x in options if x.startswith(text)]

#=================================================
# SUPPORT CLASSES
#=================================================

class Mode(object):
   '''Contains constants that represent the state of the interpreter.'''
   CONSOLE = 0
   CLI     = 1
   GUI     = 2
   
   def __init__(self):
       raise NotImplementedError('This class should never be instantiated.')
