import unittest
import mock

from rocketchat.api import RocketChatAPI
from rocketchat.calls.send_message import SendMessage


from .data import PUBLIC_ROOM_TEST


class APITestCase(object):

    def setUp(self):
        self.settings = {'username': 'something',
                         'password': 'something',
                         'domain': 'https://www.example.com'}
        self.api = RocketChatAPI(settings=self.settings)


class SendMessageTestCase(APITestCase, unittest.TestCase):

    @mock.patch('rocketchat.calls.base.RocketChatBase.set_auth_token')
    @mock.patch('rocketchat.calls.base.RocketChatBase.set_auth_headers')
    def test_send_message_payload(self, set_auth_headers_mock, set_auth_mock):
        set_auth_mock.return_value = None
        set_auth_headers_mock.return_value = None

        send_message = SendMessage(settings=self.settings)

        self.assertEqual(send_message.build_payload(message='Test message'),
                         {'msg': 'Test message'})

    @mock.patch('rocketchat.calls.base.RocketChatBase.set_auth_token')
    @mock.patch('rocketchat.calls.base.RocketChatBase.set_auth_headers')
    @mock.patch('requests.Session.request')
    def test_send_message_api(self, request_mock, set_auth_headers_mock, set_auth_mock):
        set_auth_mock.return_value = None
        set_auth_headers_mock.return_value = None

        mock_response = mock.Mock()
        mock_response.json.return_value = {}
        request_mock.return_value = mock_response

        self.api.send_message('12312', 'Test message')


class GetPublicRoomTestCase(APITestCase, unittest.TestCase):

    @mock.patch('rocketchat.calls.base.RocketChatBase.set_auth_token')
    @mock.patch('rocketchat.calls.base.RocketChatBase.set_auth_headers')
    @mock.patch('requests.Session.request')
    def test_get_public_rooms(self, mock_request, set_auth_headers_mock, set_auth_mock):
        set_auth_mock.return_value = None
        set_auth_headers_mock.return_value = None

        mock_response = mock.Mock()
        mock_response.json.return_value = PUBLIC_ROOM_TEST

        mock_request.return_value = mock_response

        pub_rooms = self.api.get_public_rooms()
        self.assertEqual(pub_rooms[0]['name'], 'Test Room')
        self.assertEqual(pub_rooms[0]['id'], '123456')
