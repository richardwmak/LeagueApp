import pytest  # noqa
import lfm_vis.model.api as data


class TestDataMethods(object):  # noqa
    """Test data methods.
    """

    def test_url_generator_no_xml(self):  # noqa
        api_request = data.ApiRequest()

        # config = configparser.ConfigParser()
        # config.read("../lastfm_visualiser/secrets.ini")
        # api_key = config["api"]["key"]
        api_key = api_request.api_key

        method_dict = {"key1": "val1",
                       "key2": "val2"}

        url = api_request.generate_api_url(method_dict)
        expected_url = "http://ws.audioscrobbler.com/2.0/?api_key=%s?format=json?key1=val1?key2=val2" % api_key

        assert url == expected_url
