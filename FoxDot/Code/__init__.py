from __future__ import division
from types import CodeType, FunctionType, TypeType
from traceback import format_exc as error_stack
from ..Patterns.Operations import modi

import when_statements, player_objects, sample_players
import assignments


"""
    Live Object
    ===========

    Base for any self-scheduling objects

"""

class LiveObject(object):

    foxdot_object = True
    isAlive = True
    
    metro = None
    step  = None
    n     = 0
    
    def kill(self):
        self.isAlive = False
        return self

    def __call__(self):
        self.metro.schedule(self, self.metro.now() + float(modi(self.step, self.n)))
        self.n += 1
        return self

"""
    FoxCode
    =======
    Handles the execution of FoxDot code
    
"""

class FoxCode:
    namespace={}
    def __call__(self, code, verbose=True):
        """ Takes a string of FoxDot code and executes as Python """

        ns = self.namespace

        try:

            if type(code) != CodeType:

                code = process(code, ns)

                if verbose: print stdout(code)

                if not code:

                    return

                else:

                    code = compile(code, "FoxDot", "exec")

            exec code in ns

        except:

            print error_stack()

            raise # raise the error to any foxdot code that executes foxdot code

        return

execute = FoxCode()

"""
    FoxDot Syntax Checking
    ----------------------

    - Check for "When Statements"
    - Check for creation of "Player" and "Sample Player" objects
"""

FoxDotSyntax = [ when_statements ]
                 #player_objects,
                 #sample_players ]

def process(text, ns={}):
    """ Iterates over the modules that replace FoxDot syntax with Python """
    
    for syntax in FoxDotSyntax:

        text = syntax.find(text)

    text = assignments.check(text, ns)

    return text

def _namespace(obj):
    return globals().get(obj, None)


def stdout(code):
    """ Imitates the Python IDE output style """
    
    console_text = code.strip().split("\n")

    return ">>> %s" % "\n>>> ".join(console_text)

""" These functions return information about an imported module """

def classes(module):
    """ Returns a list of class names defined in module """
    return [name for name, data in vars(module).items() if type(data) == TypeType]

def instances(module, cls):
    """ Returns a list of instances of cls from module """
    return [name for name, data in vars(module).items() if isinstance(data, cls)]

def functions(module):
    """ Returns a list of function names defined in module """
    return [name for name, data in vars(module).items() if type(data) == FunctionType]
