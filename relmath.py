
from tabulate import tabulate
from wcwidth import wcswidth
from contextlib import contextmanager
import inspect

class LogLevel:
    NOTHING = 0
    FATAL = 1
    ERROR = 2
    WARNING = 3
    INFO = 4
    DEBUG = 5

class State:

    s = None

    def __init__(self):
        self._format_level = 0
        self.verbosity = LogLevel.INFO

        self._quotes = [False]
        #self._local_vars = []  # list of dicts
        self._frames = []
        self._old_local_var_keys = []  # list of sets (of keys)

    def push_env(self):
        """ NOTE: USE *ONLY* IN MAIN !
                  ELSEWHERE PREFER WITH STATEMENTS
        """
        self._push_env(2)

    def _push_env(self, stack_depth):
        """ NOTE: USE *ONLY* IN MAIN !
                  ELSEWHERE PREFER WITH STATEMENTS
        """
        f=inspect.stack()[stack_depth].frame  
        #state._local_vars.append(f.f_locals)
        self._frames.append(f)
        self._old_local_var_keys.append(set(f.f_locals.keys()))
        self._format_level += 2
    
    def pop_env(self):
        debug('local vars diff = %s' % self.local_vars())
        self._format_level -= 2
        self._frames.pop()
        self._old_local_var_keys.pop()
    
    def find_expr_name(self, expr):
        """
            Return the last name associated to an expression.
            If not found, return the empty string.
        """
        i = len(self._frames) - 1
        for frame in reversed(self._frames):
            diff_keys = frame.f_locals.keys() - self._old_local_var_keys[i]
            # NOTE: using 'is' instead of equality to prevent double naming
            # See https://github.com/DavidLeoni/relmath/wiki/Taking-variables-names-from-environment
            for k in diff_keys:
                if expr is frame.f_locals[k]:
                    return k
            for k in frame.f_globals.keys():
                if expr is frame.f_globals[k]:
                    return k
            i -= 1
        return ""

    def expr_name(self, expr):
        """ Return the last name associated to an expression.
            If not found, raises NameError
        """
        n = self.find_expr_name(expr)
        if not n:
            raise NameError("Couldn't find a name for given expression !")

    def local_vars(self):
        ret = {}

        """
        i = len(self._local_vars) - 1

        for loc_vars in reversed(self._local_vars):
            diff_keys = loc_vars.keys() - self._old_local_var_keys[i]
            for k in diff_keys:
                if k not in ret:
                    ret[k] = loc_vars[k]
            i -= 1
        return ret
        """
        i = len(self._frames) - 1

        for frame in reversed(self._frames):
            diff_keys = frame.f_locals.keys() - self._old_local_var_keys[i]
            for k in diff_keys:
                if k not in ret:
                    ret[k] = frame.f_locals[k]
            i -= 1
        return ret


    def q(self):
        """ Return True if system is operating under quotation, False otherwise
        """
        return self._quotes[-1]

State.s = State()
    

@contextmanager
def quote(state=State.s):
    debug('quoted')
    
    state._quotes.append(True)
    state._format_level += 2
    yield 
    state._format_level -= 2   
    
    
    debug('/quoted')
    state._quotes.pop()


@contextmanager
def let(state=State.s):

    """ DIRTY stack manipulation, 
    
        had to do this as other solution works only in global script and not inside functions:

        @contextmanager
        def let(local_vars, p=S):
        
            old_locs = {key:value for (key,value) in local_vars.items()}
            yield
            debug('local vars diff = %s' % (local_vars.keys() - old_locs.keys()))

        Called with
    
        with let(locals()):
            baobab = 'w'

    """
    state._push_env(3)    # because of implicit __enter__ call
    yield
    state.pop_env()

@contextmanager
def unquote(state=State.s):
    debug('unquoted')
    state._quotes.append(False)
    state._format_level += 2
    yield 
    state._format_level -= 2   
    debug('/unquoted')
    state._quotes.pop()



def sheight(s):
    """ Return the height of provided text block.
        Min height is one.
    """
    return s.strip().count("\n") + 1

def swidth(s):
    """ Return the width of provided text block.
        Min height is one.
    """

    return max( [wcswidth(row) for row in s.strip().split('\n')] ) 


def sjoin(s1,s2, valign='top'):
    """ Horizontally joins two blocks of text possibly containing \n
        and retrun the newly formed block as a string
    """

    h1 = sheight(s1)
    h2 = sheight(s2)

    # TODO hack for one liners, prevents weird results as ['M*M.T\n  \n \n']: 
    if h1 == 1 and h2 == 1:
        return s1 + s2

    if valign == 'center' and h2 > h1:
        left_extra_rows =  (h2-h1) // 2
    else:
        left_extra_rows =  0


    rows1 = ['\n']*left_extra_rows + s1.split('\n')
    rows2 = s2.split('\n')
    ret = ""
    left_width = swidth(s1)
    for i in range(min(len(rows1), len(rows2))):
        ret += "%-*s%s\n" % (left_width,rows1[i].strip('\n'),rows2[i])

    if len(rows1) > len(rows2):
        for j in range(i+1, len(rows1)):
            ret += rows1[j] + '\n'
    else:
        for j in range(i+1, len(rows2)):
            ret += " "*left_width + rows2[j] + '\n'
    return ret

def format_log(msg=""):
    pad = " "* State.s._format_level
    return pad + str(msg).replace('\n','\n' + pad)

def fatal(msg, ex=None):
    """ Prints error and exits (halts program execution immediatly)
    """
    if State.s.verbosity >= LogLevel.FATAL:    

        if ex == None:
            exMsg = ""
        else:
            exMsg = " \n  " + repr(ex)
        s = format_log("\n\n    FATAL ERROR! %s%s\n\n" % (msg,exMsg))
        print(s)
    exit(1)

def log_error(msg, ex=None):
    """ Prints error but does not rethrow exception
    """
    if ex == None:
        exMsg = ""
        the_ex = Exception(msg)
    else:
        exMsg = " \n  " + repr(ex)
    the_ex = ex
    s = format_log("\n\n    ERROR! %s%s\n\n" % (msg,exMsg))
    print(s)

def error(msg, ex=None):
    """ Prints error and reraises Exception
    """
    if State.s.verbosity >= LogLevel.ERROR:    

        log_error(msg, ex)
        if ex != None:
            raise new_ex
        else:
            raise Exception(msg)

def warn(msg, ex=None):
    if State.s.verbosity >= LogLevel.WARNING:    
        if ex == None:
            exMsg = ""
        else:
            exMsg = " \n  " + repr(ex)

        s = format_log("\n\n   WARNING: %s%s\n\n" % (msg,exMsg))
        print(s)

def info(msg=""):
    if State.s.verbosity >= LogLevel.INFO:
        print(format_log(msg))

def debug(msg=""):
    
    if State.s.verbosity >= LogLevel.DEBUG:
        print(format_log("DEBUG=%s" % msg))




class Expr:
    def __init__(self):
        pass

    @property
    def dom(self):
        raise NotImplementedError("IMPLEMENT ME!")      

    @property
    def cod(self):
        raise NotImplementedError("IMPLEMENT ME!")      

    def transpose(self):
        if State.s.q():
            return T(self)
        else:
            s = self.simp()
            if s == self:
                return T(self)
            else:
                return s.T

    T = property(transpose, None, None, "Matrix transposition.")

    def simp(self):
        return self

    def __eq__(self, expr2):
        return  expr2 != None \
                and self.__class__ == expr2.__class__

class BinOp(Expr):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def python_token(self):
        raise NotImplementedError("IMPLEMENT ME!")      

    def python_method(self):
        raise NotImplementedError("IMPLEMENT ME!")      

    def __str__(self):
        return sjoin(str(self.left), sjoin(str(self.python_token()), str(self.right), valign='center'))

    def __repr__(self):
        
        return "%s(%s,%s)" % (self.__class__.__name__, repr(self.left),repr(self.right))


    def latex(self):
        raise NotImplementedError("IMPLEMENT ME!")    

    def __eq__(self, binop2):
        return  super().__eq__(binop2) \
                and self.left == binop2.left \
                and self.right == binop2.right



class RelMul(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
    

    def latex(self):
        raise NotImplementedError("IMPLEMENT ME!")    

    @property
    def dom(self):
        return self.left.dom

    @property
    def cod(self):
        return self.right.cod


    def python_token(self):
        return '*'

    def python_method(self):
        return '__mul__'

    def simp(self):
        with unquote():
            lsimp = self.left.simp()
            rsimp = self.right.simp()
            return lsimp * rsimp

class RelAdd(BinOp):
    def __init__(self, left, right):
        super().__init__(left, right)
    

    def latex(self):
        raise NotImplementedError("IMPLEMENT ME!")    

    @property
    def dom(self):
        return self.left.dom

    @property
    def cod(self):
        return self.right.cod

    def python_token(self):
        return '+'

    def python_method(self):
        return '__add__'

    def simp(self):
        with unquote():
            lsimp = self.left.simp()
            rsimp = self.right.simp()
            return lsimp + rsimp


class UnOp(Expr):
    def __init__(self, val):
        super().__init__()
        self.val = val

    def python_token(self):
        raise NotImplementedError("IMPLEMENT ME!")    


    def latex(self):
        raise NotImplementedError("IMPLEMENT ME!")    

    def __str__(self):
        s = str(self.val)
        return sjoin(self.python_token(), str(self.val), valign='center')

    def __repr__(self):

        return "%s(%s)" % (self.__class__.__name__ , repr(self.val))

    def __eq__(self, unop2):
        return  super().__eq__(unop2) \
                and self.val == unop2.val


class T(UnOp):


    def python_token(self):
        raise NotImplementedError

    def python_method(self):
        return '.T'

    def __str__(self):
        return sjoin(str(self.val), self.python_method())

    @property
    def dom(self):
        return self.val.cod

    @property
    def cod(self):
        return self.val.dom
   
    def simp(self):
        with unquote():
            return self.val.simp().T

    def latex(self):
        raise NotImplementedError("IMPLEMENT ME!")    


class Neg(UnOp):

    def python_token(self):
        return '-'

    def python_method(self):
        return '__neg__'


    def simp(self):
        with unquote():
            return -self.val

    def latex(self):
        raise NotImplementedError("IMPLEMENT ME!")    

    @property
    def dom(self):
        return self.val.dom

    @property
    def cod(self):
        return self.val.cod

class Val(Expr):
    def __init__(self, val):
        ""
        super().__init__()
        self._val = val

    @property
    def val(self):
        return self._val
        
    def __eq__(self, v2):
        return  super().__eq__(v2)      \
                and self.val == v2.val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__ , repr(self.val))


class Dioid(Val):
    def __init__(self, val):
        ""        
        super().__init__(val)
        
    def __add__(self, d2):
        raise NotImplementedError("IMPLEMENT ME!")
    
    def __mul__(self, d2):
        raise NotImplementedError("IMPLEMENT ME!")    

    def __neg__(self):
        """ NOTE: in a dioid, negation is _not_ mandatory. See page 7 of Graphs, Dioids and Semirings book
        """
        raise NotImplementedError("Not available for this dioid !")

    def s(self):
        raise NotImplementedError("IMPLEMENT ME!")    
                
    def zero(self):
        raise NotImplementedError("IMPLEMENT ME!")    
        
    def one(self):
        raise NotImplementedError("IMPLEMENT ME!")    
        
    
class RD(Dioid):
    def __init__(self, val):
        super().__init__(val)
    
    def zero(self):
        return RD(0)
    
    def one(self):
        return RD(1)
    
    def s(self):
        return "TODO R^ set "

    def __neg__(self):
        """ NOTE: in a dioid, negation is _not_ mandatory. See page 7 of Graphs, Dioids and Semirings book
        """
        return RD(- self.val)
        
    def __add__(self, d2):
        return RD(self.val + d2.val)
    
    def __mul__(self, d2):
        return RD(self.val * d2.val)

    def __str__(self):
        cand = str(self.val)
        formatted = "%.2f" % self.val
        if len(cand) > len(formatted):
            return formatted + (' ...')
        else:
            return cand

    def __round__(self, ndigits=0):
        return RD(round(self.val, ndigits))
    
class BD(Dioid):
    def __init__(self, val):
        super().__init__(val)
    
    def zero(self):
        return BD(False)
    
    def one(self):
        return BD(True)
    
    def s(self):
        return "TODO R^ set "

    def __neg__(self):
        """ NOTE: in a dioid, negation is _not_ mandatory. See page 7 of Graphs, Dioids and Semirings book
        """
        return BD(not self.val)
        
    def __add__(self, d2):
        return BD(self.val or d2.val)
    
    def __mul__(self, d2):
        return BD(self.val and d2.val)


class Rel(Expr):
    
    def __init__(self,  g, dom, cod):
        "" 
        super().__init__()
        if type(g) is not list:
            raise ValueError("Expected a list of lists, got instead type %s" % type(g))
        if len(g) == 0:
            raise ValueError("Expected at least one row, got instead %s" % g)
        if type(g[0]) is not list:
            raise ValueError("Expected a list of lists, got instead first row type %s" % type(g[0]))
        if len(g[0]) == 0:
            raise ValueError("Expected at least one column, got instead %s" % g)
        if len(dom) != len(g):
            raise ValueError("dom has different size than g rows! dom=%s g=%s" % (len(dom), len(g)))
        if len(cod) != len(g[0]):
            raise ValueError("cod has different size than g columns! cod=%s g=%s" % (len(cod), len(g[0])))

        # fixing values

        for row in g:
            for j in range(len(row)):
                el = row[j]
                if not isinstance(el, Dioid):
                    if type(el) == float or type(el) == int:
                        row[j] = RD(el)
                    elif type(el) == bool:
                        row[j] = BD(el)
                    else:
                        raise ValueError("Found unrecognized type %s for element %s" % (type(el), el))            

        self.g = g
        self._dom = dom
        self._cod = cod        
    
    @property
    def dom(self):
        return self._dom

    @property
    def cod(self):
        return self._cod

    def nodes(self):
        """ Ordered list of unique nodes. First dom, then cod
        """
        inter = set(self.dom).intersection(self.cod)
        if len(inter) > 0:
            return [x for x in self.dom if x not in inter] + self.cod
        else:
            return self.dom + self.cod

    def dioid(self):
        """ TODO assumes graph has at least one element
        """
        return self.g[0][0]


    def map(self, f):
        """ Maps f to all elements of the matrix
        """
        res_g = []
        for row in self.g:
            new_row = []
            res_g.append(new_row)
            for x in row:
                new_row.append(f(x))
        return Rel(res_g, self.dom, self.cod)

    def __round__(self, ndigits=0):
        if not isinstance(self.dioid(), RD):
            raise ValueError("Unsupported dioid for round function: %s" % type(self.dioid()))
        
        return self.map(lambda x: round(x, ndigits))
        

    def __add__(self, r2):
        if State.s.q():
            return RelAdd(self, r2)
        else:

            res_g = []
            for i in range(len(self.dom)):
                row = []
                res_g.append(row)
                for j in range(len(self.cod)):
                    row.append(self.g[i][j] + r2.g[i][j])
            return Rel(res_g, self.dom, self.cod)
                
    def __mul__(self, r2):
        """ we don't consider __matmul__ for now (dont like the '@')
        """
        if r2 == None:
            raise ValueError("Can't multiply by None !")
        if State.s.q():
            return RelMul(self, r2)
        else:
            res_g = []
            
            for i in range(len(self.dom)):
                row = []
                res_g.append(row)
                for j in range(len(r2.cod)):
                    val = self.dioid().zero()
                    for k in range(len(self.cod)):
                        val += self.g[i][k] * r2.g[k][j]
                    row.append(val)
            return Rel(res_g, self.dom, r2.cod)

    def __str__(self):
        n = State.s.find_expr_name(self)
        if State.s.q() and n:
            return n
        else:
            
            data = []
            header = [" "]
            header.extend(self.cod)
            data.append(header)
            for i in range(len(self.g)):
                row = [self.dom[i]]
                row.extend(self.g[i])
                data.append(row)
            
            return tabulate(data, tablefmt="fancy_grid")
            
    def __repr__(self):
        return "Rel(%s,%s,%s)" % (repr(self.g), repr(self.dom), repr(self.cod))
    
    def transpose(self):
        if State.s.q():
            return T(self)
        else:
            res_g = []
            for i in range(len(self.cod)):
                row = []
                res_g.append(row)
                for j in range(len(self.dom)):
                    row.append(self.g[j][i])

            return Rel(res_g, self.cod, self.dom)
    T = property(transpose, None, None, "Matrix transposition.")
    
    def __neg__(self):
        if State.s.q():
            return Neg(self)
        else:
            res_g = []
            for i in range(len(self.dom)):
                row = []
                res_g.append(row)
                for j in range(len(self.cod)):
                    row.append(-self.g[i][j])

            return Rel(res_g, self.dom, self.cod)

    def __eq__(self, rel2):
        return  super().__eq__(rel2) and \
                self.g == rel2.g and     \
                self.dom == rel2.dom and \
                self.cod == rel2.cod
