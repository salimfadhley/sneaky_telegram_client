from sneaky_client.t_me_links import get_t_me_hashes


def test_extract0():
    input_text: str = "Hello world telegram.me/joinchat/AAAAAEkk2WdoDrB4-Q8-gg https://t.me/joinchat/bdddf"
    result = list(get_t_me_hashes(input_text))

    assert result == ["AAAAAEkk2WdoDrB4-Q8-gg", "bdddf"]


def test_extract1():
    input_text: str = "26.200 Q MEMBERS THANQQQ! GOD BLESS YOU ALL. #WWG1WGA\n\nhttps://t.me/QNewsOfficialTV"
    result = list(get_t_me_hashes(input_text))
    assert result == ["QNewsOfficialTV"]


def test_extract2():
    input_text: str = "    https://t.me/joinchat/VGNrOwP_y0yQvAZs  "
    result = list(get_t_me_hashes(input_text))
    assert result == ["VGNrOwP_y0yQvAZs"]
