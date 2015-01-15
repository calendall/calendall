
def local_url_loader(*args, **kwargs):
    """This mock returns in a string the file. Used for premailer"""
    result = None
    with open(args[0].lstrip('/'), 'r') as f:
        result = f.read()
    return result
