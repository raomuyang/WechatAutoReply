# __*__coding__*__

hello = ["你好", "您好", "hello", "HELLO", "Hello"]

def isSayHello(str):
    """
    :param str:
    :return:
    1 short hello
    0 lang hello
    -1 not say hello

    """
    for h in hello:
        if h not in str:
            continue
        if str.__len__() > 5:
            return 0
        else:
            return 1
    return -1

