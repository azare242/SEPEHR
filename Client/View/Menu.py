Menu = {
    'main': """Welcome to SEPEHR
    1.LogIn
    2.SignUp
    x.Exit""",
    'login-m': """--Login--
    1.Login
    2.Forgot Password
    x.back""",
    'signup-m': """--SignUp--
    1.SignUp
    x.back""",
    'search': """--Search By--
    1.Username
    2.First name
    3.Last name
    4.phone number
    5.e-mail
    x.exit
    """
}


def get_user_menu(fname, lname, **kwargs):
    return f"""--WELCOME {fname} {lname}
    you have {kwargs['m_count']} unread messages and {kwargs['p_count']} pending friends requests
    1.Send Message
    2.Read Messages
    3.Search Users
    4.Add Friend
    5.Remove Friend
    6.Blocks
    7.DELETE ACCOUNT
    0.logout"""
