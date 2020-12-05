import logging

def getlog(name : str):
    """Create logger object with predefined stream handler & formatting

    Parameters
    ----------
    name : str
        module __name__

    Returns
    -------
    logging.logger
    
    Examples
    --------
    >>> from __init__ import getlog
    >>> log = getlog(__name__)
    """    
    fmt_stream = logging.Formatter('%(levelname)-7s %(lineno)-4d %(name)-26s %(message)s')
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt_stream)

    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    log.addHandler(sh)

    return log