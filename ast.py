import sys

def _repr(obj):
    """
    Get the representation of an object, with dedicated pprint-like format for lists.
    """
    if isinstance(obj, list):
        return '[' + (',\n '.join((_repr(e).replace('\n', '\n ') for e in obj))) + '\n]'
    else:
        return repr(obj)

class Node(object):
    __slots__ = ()
    """ Abstract base class for AST nodes.
    """
    def __repr__(self):
        """ Generates a python representation of the current node
        """
        result = self.__class__.__name__ + '('

        indent = ''
        separator = ''
        for name in self.__slots__[:-2]:
            result += separator
            result += indent
            result += name + '=' + (_repr(getattr(self, name)).replace('\n', '\n  ' + (' ' * (len(name) + len(self.__class__.__name__)))))

            separator = ','
            indent = '\n ' + (' ' * len(self.__class__.__name__))

        result += indent + ')'

        return result

    def children(self):
        """ A sequence of all children that are Nodes
        """
        pass

    def show(self, buf=sys.stdout, offset=0, attrnames=False, nodenames=False, showcoord=False, _my_node_name=None):
        """ Pretty print the Node and all its attributes and
            children (recursively) to a buffer.

            buf:
                Open IO buffer into which the Node is printed.

            offset:
                Initial offset (amount of leading spaces)

            attrnames:
                True if you want to see the attribute names in
                name=value pairs. False to only see the values.

            nodenames:
                True if you want to see the actual node names
                within their parents.

            showcoord:
                Do you want the coordinates of each Node to be
                displayed.
        """
        lead = ' ' * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__+ ' <' + _my_node_name + '>: ')
        else:
            buf.write(lead + self.__class__.__name__+ ': ')

        if self.attr_names:
            if attrnames:
                nvlist = [(n, getattr(self,n)) for n in self.attr_names]
                attrstr = ', '.join('%s=%s' % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ', '.join('%s' % v for v in vlist)
            buf.write(attrstr)

        if showcoord:
            buf.write(' (at %s)' % self.coord)
        buf.write('\n')

        for (child_name, child) in self.children():
            child.show(
                buf,
                offset=offset + 2,
                attrnames=attrnames,
                nodenames=nodenames,
                showcoord=showcoord,
                _my_node_name=child_name)

class NodeVisitor(object):
    """ A base NodeVisitor class for visiting c_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.

        For example:

        class ConstantVisitor(NodeVisitor):
            def __init__(self):
                self.values = []

            def visit_Constant(self, node):
                self.values.append(node.value)

        Creates a list of values of all the constant nodes
        encountered below the given node. To use it:

        cv = ConstantVisitor()
        cv.visit(node)

        Notes:

        *   generic_visit() will be called for AST nodes for which
            no visit_XXX method was defined.
        *   The children of nodes for which a visit_XXX was
            defined will not be visited - if you need this, call
            generic_visit() on the node.
            You can use:
                NodeVisitor.generic_visit(self, node)
        *   Modeled after Python's own AST visiting facilities
            (the ast module of Python 3.0)
    """

    _method_cache = None

    def visit(self, node):
        """ Visit a node.
        """

        if self._method_cache is None:
            self._method_cache = {}

        visitor = self._method_cache.get(node.__class__.__name__, None)
        if visitor is None:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            self._method_cache[node.__class__.__name__] = visitor

        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for c in node:
            self.visit(c)

class Constant(Node):
    __slots__ = ('type', 'value', 'coord', '__weakref__')
    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('type', 'value', )

class If(Node):
    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')
    def __init__(self, cond, iftrue, iffalse, coord=None):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.iftrue is not None: nodelist.append(("iftrue", self.iftrue))
        if self.iffalse is not None: nodelist.append(("iffalse", self.iffalse))
        return tuple(nodelist)

    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.iftrue is not None:
            yield self.iftrue
        if self.iffalse is not None:
            yield self.iffalse

    attr_names = ()

class For(Node):
    __slots__ = ('id', 'cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, id, cond, stmt, coord=None):
        self.id = id
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.id is not None: nodelist.append(("init", self.init))
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.stmt is not None: nodelist.append(("stmt", self.stmt))
        return tuple(nodelist)

    def __iter__(self):
        if self.id is not None:
            yield self.id
        if self.cond is not None:
            yield self.cond
        if self.stmt is not None:
            yield self.stmt

    attr_names = ()

class While(Node):
    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.stmt is not None: nodelist.append(("stmt", self.stmt))
        return tuple(nodelist)

    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.stmt is not None:
            yield self.stmt

    attr_names = ()

class Do(Node):
    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.stmt is not None: nodelist.append(("stmt", self.stmt))
        return tuple(nodelist)

    def __iter__(self):
        if self.cond is not None:
            yield self.cond
        if self.stmt is not None:
            yield self.stmt

    attr_names = ()

class Break(Node):
    __slots__ = ('coord', '__weakref__')
    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    def __iter__(self):
        return
        yield

    attr_names = ()

class Return(Node):
    __slots__ = ('expr', 'coord', '__weakref__')
    def __init__(self, expr, coord=None):
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    def __iter__(self):
        if self.expr is not None:
            yield self.expr

    attr_names = ()

class Next(Node):
    __slots__ = ('coord', '__weakref__')
    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()

    def __iter__(self):
        return
        yield

    attr_names = ()

class Assignment(Node):
    __slots__ = ('op', 'lvalue', 'rvalue', 'coord', '__weakref__')
    def __init__(self, op, lvalue, rvalue, coord=None):
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.coord = coord

    def children(self):
        nodelist = []
        if self.lvalue is not None: nodelist.append(("lvalue", self.lvalue))
        if self.rvalue is not None: nodelist.append(("rvalue", self.rvalue))
        return tuple(nodelist)

    def __iter__(self):
        if self.lvalue is not None:
            yield self.lvalue
        if self.rvalue is not None:
            yield self.rvalue

    attr_names = ('op', )

class ID(Node):
    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)

    def __iter__(self):
        return
        yield

    attr_names = ('name', )

class Conditional(Node):
    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')
    def __init__(self, cond, iftrue, iffalse, coord=None):
        self.cond= cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord

    def children(self):
        nodelist = []
        if self.cond is not None: nodelist.append(("cond", self.cond))
        if self.iftrue is not None: nodelist.append(("iftrue", self.iftrue))
        if self.iffalse is not None: nodelist.append(("iffalse", self.iffalse))
        return tuple(nodelist)
    
    def __iter__(self):
        if self.cond is None:
            yield self.cond
        if self.iftrue is not None:
            yield self.iftrue
        if self.iffalse is not None:
            yield self.iffalse
    
    attr_names = ()

class TypeDecl(Node):
    __slots__ = ('declname', 'quals', 'type', 'coord', '__weakref__')
    def __init__(self, declname, quals, type, coord=None):
        self.declname = declname
        self.quals = quals
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type

    attr_names = ('declname', 'quals', )

class Typedef(Node):
    __slots__ = ('name', 'quals', 'storage', 'type', 'coord', '__weakref__')
    def __init__(self, name, quals, storage, type, coord=None):
        self.name = name
        self.quals = quals
        self.storage = storage
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type

    attr_names = ('name', 'quals', 'storage', )

class Typename(Node):
    __slots__ = ('name', 'quals', 'type', 'coord', '__weakref__')
    def __init__(self, name, quals, type, coord=None):
        self.name = name
        self.quals = quals
        self.type = type
        self.coord = coord

    def children(self):
        nodelist = []
        if self.type is not None: nodelist.append(("type", self.type))
        return tuple(nodelist)

    def __iter__(self):
        if self.type is not None:
            yield self.type

    attr_names = ('name', 'quals', )

class UnaryOp(Node):
    __slots__ = ('op', 'expr', 'coord', '__weakref__')
    def __init__(self, op, expr, coord=None):
        self.op = op
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None: nodelist.append(("expr", self.expr))
        return tuple(nodelist)

    def __iter__(self):
        if self.expr is not None:
            yield self.expr

    attr_names = ('op', )

class InterpreterBlock(Node):
    __slots__ = ('statement', 'block', 'coord', '__weakref__')
    def __init__(self, statement, block, coord=None):
        self.statement = statement
        self.block = block
        self.coord = coord

    def children(self):
        nodelist = []
        if self.statement is not None: nodelist.append(("statement", self.statement))
        if self.block is not None: nodelist.append(("block", self.block))
        return tuple(nodelist)

    def __iter__(self):
        if self.statement is not None:
            yield self.statement
        if self.block is not None:
            yield self.block

    attr_names = ('Interpreter', )

class LogicalOR(Node):
    __slots__ = ('first', 'second', 'coord', '__weakref__')
    def __init__(self, first, second, coord=None):
        self.first = first
        self.second = second
        self.coord = coord

    def children(self):
        nodelist = []
        if self.first is not None: nodelist.append(("first", self.first))
        if self.second is not None: nodelist.append(("second", self.second))
        return tuple(nodelist)

    def __iter__(self):
        if self.first is not None:
            yield self.first
        if self.second is not None:
            yield self.second
        
    attr_names = ("OR", )

class LogicalAND(Node):
    __slots__ = ('first', 'second', 'coord', '__weakref__')
    def __init__(self, first, second, coord=None):
        self.first = first
        self.second = second
        self.coord = coord

    def children(self):
        nodelist = []
        if self.first is not None: nodelist.append(("first", self.first))
        if self.second is not None: nodelist.append(("second", self.second))
        return tuple(nodelist)

    def __iter__(self):
        if self.first is not None:
            yield self.first
        if self.second is not None:
            yield self.second
        
    attr_names = ("AND", )

class Equality(Node):
    __slots__ = ('operator', 'left', 'right', 'coord', '__weakref__')
    def __init__(self, operator, left, right, coord=None):
        self.operator = operator
        self.left = left
        self.right = right

    def children(self):
        nodelist = []
        if self.operator is not None: nodelist.append(("operator", self.operator))
        if self.left is not None: nodelist.append(("left", self.left))
        if self.right is not None: nodelist.append(("right", self.right))
        return tuple(nodelist)

    def __iter__(self):
        if self.operator is not None:
            yield self.operator
        if self.left is not None:
            yield self.left
        if self.right is not None:
            yield self.right

    attr_names = ("Equality",)

class Relational(Node):
    __slots__ = ('operator', 'left', 'right', 'coord', '__weakref__')
    def __init__(self, operator, left, right, coord=None):
        self.operator = operator
        self.left = left
        self.right = right

    def children(self):
        nodelist = []
        if self.operator is not None: nodelist.append(("operator", self.operator))
        if self.left is not None: nodelist.append(("left", self.left))
        if self.right is not None: nodelist.append(("right", self.right))
        return tuple(nodelist)

    def __iter__(self):
        if self.operator is not None:
            yield self.operator
        if self.left is not None:
            yield self.left
        if self.right is not None:
            yield self.right

    attr_names = ("Relational",)

class BasicOperators(Node):
    __slots__ = ('operator', 'left', 'right', 'coord', '__weakref__')
    def __init__(self, operator, left, right, coord=None):
        self.operator = operator
        self.left = left
        self.right = right

    def children(self):
        nodelist = []
        if self.operator is not None: nodelist.append(("operator", self.operator))
        if self.left is not None: nodelist.append(("left", self.left))
        if self.right is not None: nodelist.append(("right", self.right))
        return tuple(nodelist)

    def __iter__(self):
        if self.operator is not None:
            yield self.operator
        if self.left is not None:
            yield self.left
        if self.right is not None:
            yield self.right

    attr_names = ("BasicOperators",)

class Sequence(Node):
    __slots__ = ('beginning', 'end', 'coord', '__weakref__')
    def __init__(self, operator, beginning, end, coord=None):
        self.beginning = beginning
        self.end = end

    def children(self):
        nodelist = []
        if self.beginning is not None: nodelist.append(("beginning", self.beginning))
        if self.end is not None: nodelist.append(("end", self.end))
        return tuple(nodelist)

    def __iter__(self):
        if self.beginning is not None:
            yield self.beginning
        if self.end is not None:
            yield self.end

    attr_names = ("Sequence",)

class Exp(Node):
    __slots__ = ('left', 'right', 'coord', '__weakref__')
    def __init__(self, operator, left, right, coord=None):
        self.left = left
        self.right = right

    def children(self):
        nodelist = []
        if self.left is not None: nodelist.append(("left", self.left))
        if self.right is not None: nodelist.append(("right", self.right))
        return tuple(nodelist)

    def __iter__(self):
        if self.left is not None:
            yield self.left
        if self.right is not None:
            yield self.right

    attr_names = ("Exp",)

class Array(Node):
    __slots__ = ('one', 'second', 'coord', '__weakref__')
    def __init__(self, operator, one, second, coord=None):
        self.one = one
        self.second = second

    def children(self):
        nodelist = []
        if self.one is not None: nodelist.append(("one", self.one))
        if self.second is not None: nodelist.append(("second", self.second))
        return tuple(nodelist)

    def __iter__(self):
        if self.one is not None:
            yield self.one
        if self.second is not None:
            yield self.second

    attr_names = ("Array",)

class ObjectCall(Node):
    __slots__ = ('identifier', 'coord', '__weakref__')
    def __init__(self, identifier, coord=None):
        self.identifier = identifier

    def children(self):
        nodelist = []
        if self.identifier is not None: nodelist.append(("identifier", self.identifier))
        return tuple(nodelist)

    def __iter__(self):
        if self.identifier is not None:
            yield self.identifier
    
    attr_names = ("ObjectCall",)

class Function(Node):
    __slots__ = ('function', 'returnType', 'fId', 'paramLst', 'stmt', 'coord', '__weakref__')
    def __init__(self, function, returnType, fId, paramLst, stmt, coord=None):
        self.function = function
        self.returnType = returnType
        self.fId = fId
        self.paramLst = paramLst
        self.stmt = stmt

    def children(self):
        nodelist = []
        if self.function is not None: nodelist.append(('function', self.function))
        if self.returnType is not None: nodelist.append(('returnType', self.returnType))
        if self.fId is not None: nodelist.append(('fId', self.fId))
        if self.paramLst is not None: nodelist.append(('paramLst', self.paramLst))
        if self.stmt is not None: nodelist.append(('stmt', self.stmt))
        return tuple(nodelist)

    def __iter__(self):
        if self.function is not None:
            yield self.function
        if self.returnType is not None:
            yield self.returnType
        if self.fId is not None:
            yield self.fId
        if self.paramLst is not None:
            yield self.paramLst
        if self.stmt is not None:
            yield self.stmt

    attr_names = ("Function", )

class ObjectClassSpec(Node):
    __slots__ = ('identifier', 'coord', '__weakref__')
    def __init__(self, identifier, coord=None):
        self.identifier = identifier

    def children(self):
        nodelist = []
        if self.identifier is not None: nodelist.append(("identifier", self.identifier))
        return tuple(nodelist)

    def __iter__(self):
        if self.identifier is not None:
            yield self.identifier
    
    attr_names = ("ObjectClassSpec",)

class ParamList(Node):
    __slots__ = ('identifier', 'coord', '__weakref__')
    def __init__(self, identifier, coord=None):
        self.identifier = identifier

    def children(self):
        nodelist = []
        if self.identifier is not None: nodelist.append(("identifier", self.identifier))
        return tuple(nodelist)

    def __iter__(self):
        if self.identifier is not None:
            yield self.identifier
    
    attr_names = ("ParamList",)

class ParamOption(Node):
    __slots__ = ('one', 'second', 'coord', '__weakref__')
    def __init__(self, operator, one, second, coord=None):
        self.one = one
        self.second = second

    def children(self):
        nodelist = []
        if self.one is not None: nodelist.append(("one", self.one))
        if self.second is not None: nodelist.append(("second", self.second))
        return tuple(nodelist)

    def __iter__(self):
        if self.one is not None:
            yield self.one
        if self.second is not None:
            yield self.second

    attr_names = ("ParamOption",)

class ParamSpec(Node):
    __slots__ = ('tspec', 'fID', 'valueOption', 'coord', '__weakref__')
    def __init__(self, tspec, fID, valueOption, coord=None):
        self.tspec = tspec
        self.fID = fID
        self.valueOption = valueOption

    def children(self):
        nodelist = []
        if self.tspec is not None: nodelist.append(("tspec", self.tspec))
        if self.fID is not None: nodelist.append(("fID", self.fID))
        if self.valueOption is not None: nodelist.append(("valueOption", self.valueOption))
        return tuple(nodelist)

    def __iter__(self):
        if self.tspec is not None:
            yield self.tspec
        if self.fID is not None:
            yield self.fID
        if self.valueOption is not None:
            yield self.valueOption

    attr_names = ("ParamSpec", )
