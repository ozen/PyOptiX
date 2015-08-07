from PyOptixCpp import test_sum

def test_connection():
    a = 10
    b = 21

    if test_sum(a, b) == (a + b):
        print("Connection is OK with So file")
    else:
        raise Exception("No connection, check installation")


test_connection()

