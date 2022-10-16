class Error(Exception):
    pass

class ActionNotPossibleError(Error):
    """Exception raised for errors in the input.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, action, board, message):
        print('ActionNotPossibleError: ', message, 'Action: ', action, 'on board: ', board)