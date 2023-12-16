"""random_password module."""
import secrets
import string


def random_password(length=10):
    """
    Generate a random temporary password.

    Parameters:
    - length (int): The length of the password. Default is 10.

    Returns:
    str: The generated temporary password.
    """
    characters = string.ascii_letters + string.digits 
    temporary_password = ''.join(secrets.choice(characters) for _ in range(length))
    return temporary_password

if __name__ == '__main__':
    password = random_password()
    print(password)
    print()
