from src.exception.exception import UndoServiceException


class UndoController:
    def __init__(self):
        self._history = []
        self._index = 0
        self._duringUndoRedo = False

    def recordOperation(self, operation):
        """
        Method for recording an operation
        :param operation:
        :return:
        """
        if self._duringUndoRedo == True:
            return
        self._history.append(operation)
        self._index += 1

    def undo(self):
        """
        Method for the undo service
        :return:
        """
        if self._index == 0:
            raise UndoServiceException("You cannot compute more undos\n")
        self._duringUndoRedo = True
        self._index -= 1
        self._history[self._index].undo()
        self._duringUndoRedo = False

    def redo(self):
        """
        Method for the redo service
        :return:
        """
        if self._index == len(self._history):
            raise UndoServiceException("You cannot compute more redos\n")
        self._duringUndoRedo = True
        self._history[self._index].redo()
        self._index += 1
        self._duringUndoRedo = False


class FunctionCall:
    """
    Class for calling a function
    """
    def __init__(self, function, *parameters):
        self._function = function
        self._params = parameters

    def call(self):
        self._function(*self._params)


class Operation:
    """
    Operation class
    """
    def __init__(self, undoFunction, redoFunction):
        self._undo = undoFunction
        self._redo = redoFunction

    def undo(self):
        self._undo.call()

    def redo(self):
        self._redo.call()


class CascadeOperation:
    """
    Class for cascading an operation
    """
    def __init__(self, op1, op2):
        self._op1 = op1
        self._op2 = op2

    def undo(self):
        self._op2._undo.call()
        self._op1._undo.call()

    def redo(self):
        self._op2._redo.call()
        self._op1._redo.call()
