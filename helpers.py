import random
import string


def random_string(stringLength):
    """Generate a random string video name """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


list_of_errors = {
    'TBF': 'You can download only 1GB video'
}
