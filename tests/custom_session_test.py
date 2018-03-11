import pytest
import lfm_vis.model.custom_session as custom_session


class TestSessionMethods(object):
    """Test session methods.
    """

    def test_check_key_true(self):  # noqa
        session = custom_session.Session()
        session.session = {"key1": "val1",
                           "key2": "val2"}

        assert session.check_key("key1") is True

    def test_check_key_false(self):  # noqa
        session = custom_session.Session()
        session.session = {"key1": "val1",
                           "key2": "val2"}

        assert session.check_key("key3") is False

    def test_select_key_KeyError(self):  # noqa
        session = custom_session.Session()
        session.session = {"key1": "val1",
                           "key2": "val2"}

        with pytest.raises(custom_session.SessionKeyException):
            session.select_key("key3")

    def test_select_key_that_exists(self):  # noqa
        session = custom_session.Session()
        session.session = {"key1": "val1",
                           "key2": "val2"}

        assert session.select_key("key1") is "val1"

    def test_clear_session(self):  # noqa
        session = custom_session.Session()
        session.session = {"key1": "val1",
                           "key2": "val2"}

        session.clear_session()

        assert len(session.session.keys()) is 0
