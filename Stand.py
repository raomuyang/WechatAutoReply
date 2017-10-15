# __*__coding__*__

hello = ["你好", "您好", "hello", "HELLO", "Hello", "嗨", "嘿", "哈喽"]


def is_say_hello(msg):
    """
    :param msg:
    :return:
    1 short hello
    0 lang hello
    -1 not say hello
    """
    for h in hello:
        if h not in msg:
            continue
        if msg.__len__() > 5:
            return 0
        else:
            return 1
    return -1

