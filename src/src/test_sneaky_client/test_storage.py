import datetime

from sneaky_client.storage import remove_none_and_binary


def test_strip_nulls_and_binaries0():
    input = {"a": None, "b": b"xxx"}
    assert remove_none_and_binary(input) == {}


def test_strip_nulls_and_binaries1():
    input = {
        "_": "UpdateNewChannelMessage",
        "message": {
            "_": "MessageService",
            "id": 3815,
            "peer_id": {"_": "PeerChannel", "channel_id": 1184475466},
            "date": datetime.datetime(
                2021, 1, 30, 23, 2, 5, tzinfo=datetime.timezone.utc
            ),
            "action": {
                "_": "MessageActionChatEditPhoto",
                "photo": {
                    "_": "Photo",
                    "id": 5814224845414708998,
                    "access_hash": -7523482161276257128,
                    "file_reference": b"\x02F\x99\xa9J\x00\x00\x0e\xe7`\x15\xe5m\xec\t\xc2\x1d\xaa\x13\xd2\x98>V{m$\xdc\xdcT",
                    "date": datetime.datetime(
                        2021, 1, 30, 23, 2, 5, tzinfo=datetime.timezone.utc
                    ),
                    "sizes": [],
                    "dc_id": 4,
                    "has_stickers": False,
                    "video_sizes": [],
                },
            },
            "out": False,
            "mentioned": False,
            "media_unread": False,
            "silent": False,
            "post": False,
            "legacy": False,
            "from_id": {"_": "PeerUser", "user_id": 1569414994},
        },
        "pts": 4725,
        "pts_count": 1,
    }

    expected = {
        "_": "UpdateNewChannelMessage",
        "message": {
            "_": "MessageService",
            "id": 3815,
            "peer_id": {"_": "PeerChannel", "channel_id": 1184475466},
            "date": datetime.datetime(
                2021, 1, 30, 23, 2, 5, tzinfo=datetime.timezone.utc
            ),
            "action": {
                "_": "MessageActionChatEditPhoto",
                "photo": {
                    "_": "Photo",
                    "id": 5814224845414708998,
                    "access_hash": -7523482161276257128,
                    "date": datetime.datetime(
                        2021, 1, 30, 23, 2, 5, tzinfo=datetime.timezone.utc
                    ),
                    "sizes": [],
                    "dc_id": 4,
                    "has_stickers": False,
                    "video_sizes": [],
                },
            },
            "out": False,
            "mentioned": False,
            "media_unread": False,
            "silent": False,
            "post": False,
            "legacy": False,
            "from_id": {"_": "PeerUser", "user_id": 1569414994},
        },
        "pts": 4725,
        "pts_count": 1,
    }

    assert remove_none_and_binary(input) == expected


def test_strip_nulls_and_binaries2():
    inp = {
        "_": "UpdateNewChannelMessage",
        "message": {
            "_": "MessageService",
            "id": 3879,
            "peer_id": {"_": "PeerChannel", "channel_id": 1184475466},
            "date": datetime.datetime(
                2021, 1, 30, 23, 16, 45, tzinfo=datetime.timezone.utc
            ),
            "action": {
                "_": "MessageActionChatEditPhoto",
                "photo": {
                    "_": "Photo",
                    "id": 5814534276333548741,
                    "access_hash": -1943018724937053799,
                    "file_reference": b"\x02F\x99\xa9J\x00\x00\x0f'`\x15\xe8\xdd'R.\xab_\xfc\x15i\t\x0b\xbb0\xbf\x92\xc4\xf6",
                    "date": datetime.datetime(
                        2021, 1, 30, 23, 16, 45, tzinfo=datetime.timezone.utc
                    ),
                    "sizes": [],
                    "dc_id": 4,
                    "has_stickers": False,
                    "video_sizes": [],
                },
            },
            "out": False,
            "mentioned": False,
            "media_unread": False,
            "silent": False,
            "post": False,
            "legacy": False,
            "from_id": {"_": "PeerUser", "user_id": 1341933933},
        },
        "pts": 4790,
        "pts_count": 1,
    }

    expected = {
        "_": "UpdateNewChannelMessage",
        "message": {
            "_": "MessageService",
            "id": 3879,
            "peer_id": {"_": "PeerChannel", "channel_id": 1184475466},
            "date": datetime.datetime(
                2021, 1, 30, 23, 16, 45, tzinfo=datetime.timezone.utc
            ),
            "action": {
                "_": "MessageActionChatEditPhoto",
                "photo": {
                    "_": "Photo",
                    "id": 5814534276333548741,
                    "access_hash": -1943018724937053799,
                    "date": datetime.datetime(
                        2021, 1, 30, 23, 16, 45, tzinfo=datetime.timezone.utc
                    ),
                    "sizes": [],
                    "dc_id": 4,
                    "has_stickers": False,
                    "video_sizes": [],
                },
            },
            "out": False,
            "mentioned": False,
            "media_unread": False,
            "silent": False,
            "post": False,
            "legacy": False,
            "from_id": {"_": "PeerUser", "user_id": 1341933933},
        },
        "pts": 4790,
        "pts_count": 1,
    }

    assert remove_none_and_binary(inp) == expected
