import random
import string


def random_username(prefix, maxlen):
    symbols = string.ascii_letters
    return (prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])).strip()

def test_signup_new_account(app):
    username = random_username("user_", 10)
    email = username + "@localhost"
    password = "test"
    app.james.ensure_user_exists(username, password)
    app.signup.new_user(username, email, password)
    app.session.login(username, password)
    assert app.session.is_logged_in_as(username)
    app.session.logout()