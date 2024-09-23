#!/usr/bin/env python
# -*- coding: utf-8 -*-
#     __                                           _             __   _    
#    / /_  __  __   ______________ _____  __  __  (_)_  ______  / /__(_)__ 
#   / __ \/ / / /  / ___/ ___/ __ `/_  / / / / / / / / / / __ \/ //_/ / _ \
#  / /_/ / /_/ /  / /__/ /  / /_/ / / /_/ /_/ / / / /_/ / / / / ,< / /  __/
# /_.___/\__, /   \___/_/   \__,_/ /___/\__, /_/ /\__,_/_/ /_/_/|_/_/\___/ 
#       /____/                         /____/___/                          
#
###############################################################################
# Download huge collections of wordlist:#
#http://ul.to/folder/j7gmyz#
##########################################################################
#
####################################################################
# Need daylie updated proxies?#
#http://j.mp/Y7ZZq9#
################################################################
#
######################################################
#### flash proxy test ######
###################################################
#
import base64
import cStringIO
import httplib
import socket
import subprocess
import sys
import unittest

try:
    from hashlib import sha1
except ImportError:
    # Python 2.4 uses this name.
    from sha import sha as sha1

# Special tricks to load a module whose filename contains a dash and doesn't end
# in ".py".
import imp
dont_write_bytecode = sys.dont_write_bytecode
sys.dont_write_bytecode = True
flashproxy = imp.load_source("flashproxy", "flashproxy-client")
parse_socks_request = flashproxy.parse_socks_request
handle_websocket_request = flashproxy.handle_websocket_request
WebSocketDecoder = flashproxy.WebSocketDecoder
WebSocketEncoder = flashproxy.WebSocketEncoder
sys.dont_write_bytecode = dont_write_bytecode
del dont_write_bytecode
del flashproxy

LOCAL_ADDRESS = ("127.0.0.1", 40000)
REMOTE_ADDRESS = ("127.0.0.1", 40001)

class TestSocks(unittest.TestCase):
    def test_parse_socks_request_empty(self):
        self.assertRaises(ValueError, parse_socks_request, "")
    def test_parse_socks_request_short(self):
        self.assertRaises(ValueError, parse_socks_request, "\x04\x01\x99\x99\x01\x02\x03\x04")
    def test_parse_socks_request_ip_userid_missing(self):
        dest, port = parse_socks_request("\x04\x01\x99\x99\x01\x02\x03\x04\x00")
        dest, port = parse_socks_request("\x04\x01\x99\x99\x01\x02\x03\x04\x00userid")
        self.assertEqual((dest, port), ("1.2.3.4", 0x9999))
    def test_parse_socks_request_ip(self):
        dest, port = parse_socks_request("\x04\x01\x99\x99\x01\x02\x03\x04userid\x00")
        self.assertEqual((dest, port), ("1.2.3.4", 0x9999))
    def test_parse_socks_request_hostname_missing(self):
        self.assertRaises(ValueError, parse_socks_request, "\x04\x01\x99\x99\x00\x00\x00\x01userid\x00")
        self.assertRaises(ValueError, parse_socks_request, "\x04\x01\x99\x99\x00\x00\x00\x01userid\x00abc")
    def test_parse_socks_request_hostname(self):
        dest, port = parse_socks_request("\x04\x01\x99\x99\x00\x00\x00\x01userid\x00abc\x00")

class DummySocket(object):
    def __init__(self, read_fd, write_fd):
        self.read_fd = read_fd
        self.write_fd = write_fd
        self.readp = 0

    def read(self, *args, **kwargs):
        self.read_fd.seek(self.readp, 0)
        data = self.read_fd.read(*args, **kwargs)
        self.readp = self.read_fd.tell()
        return data

    def readline(self, *args, **kwargs):
        self.read_fd.seek(self.readp, 0)
        data = self.read_fd.readline(*args, **kwargs)
        self.readp = self.read_fd.tell()
        return data

    def recv(self, size, *args, **kwargs):
        return self.read(size)

    def write(self, data):
        self.write_fd.seek(0, 2)
        self.write_fd.write(data)

    def send(self, data, *args, **kwargs):
        return self.write(data)

    def sendall(self, data, *args, **kwargs):
        return self.write(data)

    def makefile(self, *args, **kwargs):
        return self

def dummy_socketpair():
    f1 = cStringIO.StringIO()
    f2 = cStringIO.StringIO()
    return (DummySocket(f1, f2), DummySocket(f2, f1))

class HTTPRequest(object):
    def __init__(self):
        self.method = "GET"
        self.path = "/"
        self.headers = {}

def transact_http(req):
    l, r = dummy_socketpair()
    r.send("%s %s HTTP/1.0\r\n" % (req.method, req.path))
    for k, v in req.headers.items():
        r.send("%s: %s\r\n" % (k, v))
    r.send("\r\n")
    protocols = handle_websocket_request(l)

    resp = httplib.HTTPResponse(r)
    resp.begin()
    return resp, protocols

class TestHandleWebSocketRequest(unittest.TestCase):
    DEFAULT_KEY = "0123456789ABCDEF"
    DEFAULT_KEY_BASE64 = base64.b64encode(DEFAULT_KEY)
    MAGIC_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    @staticmethod
    def default_req():
        req = HTTPRequest()
        req.method = "GET"
        req.path = "/"
        req.headers["Upgrade"] = "websocket"
        req.headers["Connection"] = "Upgrade"
        req.headers["Sec-WebSocket-Key"] = TestHandleWebSocketRequest.DEFAULT_KEY_BASE64
        req.headers["Sec-WebSocket-Version"] = "13"

        return req

    def assert_ok(self, req):
        resp, protocols = transact_http(req)
        self.assertEqual(resp.status, 101)
        self.assertEqual(resp.getheader("Upgrade").lower(), "websocket")
        self.assertEqual(resp.getheader("Connection").lower(), "upgrade")
        self.assertEqual(resp.getheader("Sec-WebSocket-Accept"), base64.b64encode(sha1(self.DEFAULT_KEY_BASE64 + self.MAGIC_GUID).digest()))
        self.assertEqual(protocols, [])

    def assert_not_ok(self, req):
        resp, protocols = transact_http(req)
        self.assertEqual(resp.status // 100, 4)
        self.assertEqual(protocols, None)

    def test_default(self):
        req = self.default_req()
        self.assert_ok(req)

    def test_missing_upgrade(self):
        req = self.default_req()
        del req.headers["Upgrade"]
        self.assert_not_ok(req)

    def test_missing_connection(self):
        req = self.default_req()
        del req.headers["Connection"]
        self.assert_not_ok(req)

    def test_case_insensitivity(self):
        """Test that the values of the Upgrade and Connection headers are
        case-insensitive."""
        req = self.default_req()
        req.headers["Upgrade"] = req.headers["Upgrade"].lower()
        self.assert_ok(req)
        req.headers["Upgrade"] = req.headers["Upgrade"].upper()
        self.assert_ok(req)
        req.headers["Connection"] = req.headers["Connection"].lower()
        self.assert_ok(req)
        req.headers["Connection"] = req.headers["Connection"].upper()
        self.assert_ok(req)

    def test_bogus_key(self):
        req = self.default_req()
        req.headers["Sec-WebSocket-Key"] = base64.b64encode(self.DEFAULT_KEY[:-1])
        self.assert_not_ok(req)

        req.headers["Sec-WebSocket-Key"] = "///"
        self.assert_not_ok(req)

    def test_versions(self):
        req = self.default_req()
        req.headers["Sec-WebSocket-Version"] = "13"
        self.assert_ok(req)
        req.headers["Sec-WebSocket-Version"] = "8"
        self.assert_ok(req)

        req.headers["Sec-WebSocket-Version"] = "7"
        self.assert_not_ok(req)
        req.headers["Sec-WebSocket-Version"] = "9"
        self.assert_not_ok(req)

        del req.headers["Sec-WebSocket-Version"]
        self.assert_not_ok(req)

    def test_protocols(self):
        req = self.default_req()
        req.headers["Sec-WebSocket-Protocol"] = "base64"
        resp, protocols = transact_http(req)
        self.assertEqual(resp.status, 101)
        self.assertEqual(protocols, ["base64"])
        self.assertEqual(resp.getheader("Sec-WebSocket-Protocol"), "base64")

        req = self.default_req()
        req.headers["Sec-WebSocket-Protocol"] = "cat"
        resp, protocols = transact_http(req)
        self.assertEqual(resp.status, 101)
        self.assertEqual(protocols, ["cat"])
        self.assertEqual(resp.getheader("Sec-WebSocket-Protocol"), None)

        req = self.default_req()
        req.headers["Sec-WebSocket-Protocol"] = "cat, base64"
        resp, protocols = transact_http(req)
        self.assertEqual(resp.status, 101)
        self.assertEqual(protocols, ["cat", "base64"])
        self.assertEqual(resp.getheader("Sec-WebSocket-Protocol"), "base64")

def read_frames(dec):
    frames = []
    while True:
        frame = dec.read_frame()
        if frame is None:
            break
        frames.append((frame.fin, frame.opcode, frame.payload))
    return frames

def read_messages(dec):
    messages = []
    while True:
        message = dec.read_message()
        if message is None:
            break
        messages.append((message.opcode, message.payload))
    return messages

class TestWebSocketDecoder(unittest.TestCase):
    def test_rfc(self):
        """Test samples from RFC 6455 section 5.7."""
        TESTS = [
            ("\x81\x05\x48\x65\x6c\x6c\x6f", False,
                [(True, 1, "Hello")],
                [(1, u"Hello")]),
            ("\x81\x85\x37\xfa\x21\x3d\x7f\x9f\x4d\x51\x58", True,
                [(True, 1, "Hello")],
                [(1, u"Hello")]),
            ("\x01\x03\x48\x65\x6c\x80\x02\x6c\x6f", False,
                [(False, 1, "Hel"), (True, 0, "lo")],
                [(1, u"Hello")]),
            ("\x89\x05\x48\x65\x6c\x6c\x6f", False,
                [(True, 9, "Hello")],
                [(9, u"Hello")]),
            ("\x8a\x85\x37\xfa\x21\x3d\x7f\x9f\x4d\x51\x58", True,
                [(True, 10, "Hello")],
                [(10, u"Hello")]),
            ("\x82\x7e\x01\x00" + "\x00" * 256, False,
                [(True, 2, "\x00" * 256)],
                [(2, "\x00" * 256)]),
            ("\x82\x7f\x00\x00\x00\x00\x00\x01\x00\x00" + "\x00" * 65536, False,
                [(True, 2, "\x00" * 65536)],
                [(2, "\x00" * 65536)]),
            ("\x82\x7f\x00\x00\x00\x00\x00\x01\x00\x03" + "ABCD" * 16384 + "XYZ", False,
                [(True, 2, "ABCD" * 16384 + "XYZ")],
                [(2, "ABCD" * 16384 + "XYZ")]),
        ]
        for data, use_mask, expected_frames, expected_messages in TESTS:
            dec = WebSocketDecoder(use_mask = use_mask)
            dec.feed(data)
            actual_frames = read_frames(dec)
            self.assertEqual(actual_frames, expected_frames)

            dec = WebSocketDecoder(use_mask = use_mask)
            dec.feed(data)
            actual_messages = read_messages(dec)
            self.assertEqual(actual_messages, expected_messages)

            dec = WebSocketDecoder(use_mask = not use_mask)
            dec.feed(data)
            self.assertRaises(WebSocketDecoder.MaskingError, dec.read_frame)

    def test_empty_feed(self):
        """Test that the decoder can handle a zero-byte feed."""
        dec = WebSocketDecoder()
        self.assertEqual(dec.read_frame(), None)
        dec.feed("")
        self.assertEqual(dec.read_frame(), None)
        dec.feed("\x81\x05H")
        self.assertEqual(dec.read_frame(), None)
        dec.feed("ello")
        self.assertEqual(read_frames(dec), [(True, 1, u"Hello")])

    def test_empty_frame(self):
        """Test that a frame may contain a zero-byte payload."""
        dec = WebSocketDecoder()
        dec.feed("\x81\x00")
        self.assertEqual(read_frames(dec), [(True, 1, u"")])
        dec.feed("\x82\x00")
        self.assertEqual(read_frames(dec), [(True, 2, "")])

    def test_empty_message(self):
        """Test that a message may have a zero-byte payload."""
        dec = WebSocketDecoder()
        dec.feed("\x01\x00\x00\x00\x80\x00")
        self.assertEqual(read_messages(dec), [(1, u"")])
        dec.feed("\x02\x00\x00\x00\x80\x00")
        self.assertEqual(read_messages(dec), [(2, "")])

    def test_interleaved_control(self):
        """Test that control messages interleaved with fragmented messages are
        returned."""
        dec = WebSocketDecoder()
        dec.feed("\x89\x04PING\x01\x03Hel\x8a\x04PONG\x80\x02lo\x89\x04PING")
        self.assertEqual(read_messages(dec), [(9, "PING"), (10, "PONG"), (1, u"Hello"), (9, "PING")])

    def test_fragmented_control(self):
        """Test that illegal fragmented control messages cause an error."""
        dec = WebSocketDecoder()
        dec.feed("\x09\x04PING")
        self.assertRaises(ValueError, dec.read_message)

    def test_zero_opcode(self):
        """Test that it is an error for the first frame in a message to have an
        opcode of 0."""
        dec = WebSocketDecoder()
        dec.feed("\x80\x05Hello")
        self.assertRaises(ValueError, dec.read_message)
        dec = WebSocketDecoder()
        dec.feed("\x00\x05Hello")
        self.assertRaises(ValueError, dec.read_message)

    def test_nonzero_opcode(self):
        """Test that every frame after the first must have a zero opcode."""
        dec = WebSocketDecoder()
        dec.feed("\x01\x01H\x01\x02el\x80\x02lo")
        self.assertRaises(ValueError, dec.read_message)
        dec = WebSocketDecoder()
        dec.feed("\x01\x01H\x00\x02el\x01\x02lo")
        self.assertRaises(ValueError, dec.read_message)

    def test_utf8(self):
        """Test that text frames (opcode 1) are decoded from UTF-8."""
        text = u"Hello World or ÎšÎ±Î»Î·Î¼Î­ÏÎ± ÎºÏŒÏƒÎ¼Îµ or ã“ã‚“ã«ã¡ã¯ ä¸–ç•Œ or \U0001f639"
        utf8_text = text.encode("utf-8")
        dec = WebSocketDecoder()
        dec.feed("\x81" + chr(len(utf8_text)) + utf8_text)
        self.assertEqual(read_messages(dec), [(1, text)])

    def test_wrong_utf8(self):
        """Test that failed UTF-8 decoding causes an error."""
        TESTS = [
            "\xc0\x41", # Non-shortest form.
            "\xc2", # Unfinished sequence.
        ]
        for test in TESTS:
            dec = WebSocketDecoder()
            dec.feed("\x81" + chr(len(test)) + test)
            self.assertRaises(ValueError, dec.read_message)

    def test_overly_large_payload(self):
        """Test that large payloads are rejected."""
        dec = WebSocketDecoder()
        dec.feed("\x82\x7f\x00\x00\x00\x00\x01\x00\x00\x00")
        self.assertRaises(ValueError, dec.read_frame)

class TestWebSocketEncoder(unittest.TestCase):
    def test_length(self):
        """Test that payload lengths are encoded using the smallest number of
        bytes."""
        TESTS = [(0, 0), (125, 0), (126, 2), (65535, 2), (65536, 8)]
        for length, encoded_length in TESTS:
            enc = WebSocketEncoder(use_mask = False)
            eframe = enc.encode_frame(2, "\x00" * length)
            self.assertEqual(len(eframe), 1 + 1 + encoded_length + length)
            enc = WebSocketEncoder(use_mask = True)
            eframe = enc.encode_frame(2, "\x00" * length)
            self.assertEqual(len(eframe), 1 + 1 + encoded_length + 4 + length)

    def test_roundtrip(self):
        TESTS = [
            (1, u"Hello world"),
            (1, u"Hello \N{WHITE SMILING FACE}"),
        ]
        for opcode, payload in TESTS:
            for use_mask in (False, True):
                enc = WebSocketEncoder(use_mask = use_mask)
                enc_message = enc.encode_message(opcode, payload)
                dec = WebSocketDecoder(use_mask = use_mask)
                dec.feed(enc_message)
                self.assertEqual(read_messages(dec), [(opcode, payload)])

def format_address(addr):
    return "%s:%d" % addr

class TestConnectionLimit(unittest.TestCase):
    def setUp(self):
        self.p = subprocess.Popen(["./flashproxy-client", format_address(LOCAL_ADDRESS), format_address(REMOTE_ADDRESS)])

    def tearDown(self):
        self.p.terminate()

#     def test_remote_limit(self):
#         """Test that the client transport plugin limits the number of remote
#         connections that it will accept."""
#         for i in range(5):
#             s = socket.create_connection(REMOTE_ADDRESS, 2)
#         self.assertRaises(socket.error, socket.create_connection, REMOTE_ADDRESS)

if __name__ == "__main__":
    unittest.main()
