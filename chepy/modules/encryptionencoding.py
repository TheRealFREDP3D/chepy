import base64
import binascii
import codecs
import itertools
import string
from typing import Literal, TypeVar, Dict, Any

import lazy_import

jwt = lazy_import.lazy_module("jwt")
import pathlib

import regex as re
import json

AES = lazy_import.lazy_module("Crypto.Cipher.AES")
ARC4 = lazy_import.lazy_module("Crypto.Cipher.ARC4")
DES = lazy_import.lazy_module("Crypto.Cipher.DES")
ChaCha20 = lazy_import.lazy_module("Crypto.Cipher.ChaCha20")
DES3 = lazy_import.lazy_module("Crypto.Cipher.DES3")
RSA = lazy_import.lazy_module("Crypto.PublicKey.RSA")
Hash = lazy_import.lazy_module("Crypto.Hash")
PKCS1_15 = lazy_import.lazy_module("Crypto.Signature.pkcs1_15")
PKCS1_OAEP = lazy_import.lazy_module("Crypto.Cipher.PKCS1_OAEP")
Blowfish = lazy_import.lazy_module("Crypto.Cipher.Blowfish")
Padding = lazy_import.lazy_module("Crypto.Util.Padding")
pycipher = lazy_import.lazy_module("pycipher")

from ..core import ChepyCore, ChepyDecorators
from ..extras.combinatons import hex_chars
from .internal.constants import EncryptionConsts

EncryptionEncodingT = TypeVar("EncryptionEncodingT", bound="EncryptionEncoding")


class EncryptionEncoding(ChepyCore):
    """This class handles most operations related to various encryption
    related operations. This class inherits the ChepyCore class, and all the
    methods are also available from the Chepy class

    Examples:
        >>> from chepy import Chepy
        or
        >>> from chepy.modules.encryptionencoding import EncryptionEncoding
    """

    def __init__(self, *data):
        super().__init__(*data)

    def __check_mode(self, mode) -> None:
        assert mode in ["CBC", "OFB", "CTR", "ECB"], "Not a valid mode."

    def _convert_key(
        self, key, iv, key_format: str, iv_format: str
    ) -> EncryptionEncodingT:  # pragma: no cover
        if isinstance(key, str):
            key = key.encode()
        # modify key according to mode
        if key_format == "hex":
            key = binascii.unhexlify(key)
        if key_format == "base64" or key_format == "b64":
            key = base64.b64decode(key)
        if key_format == "utf-8" or key_format == "utf8":
            key = key.decode().encode("utf-8")
        if key_format == "latin-1":
            key = key.decode().encode("latin-1")

        # modify iv according to mode
        if isinstance(iv, str):
            iv = iv.encode()
        if iv_format == "hex":
            iv = binascii.unhexlify(iv)
        if iv_format == "base64" or iv_format == "b64":
            iv = base64.b64decode(iv)
        if iv_format == "utf-8" or iv_format == "utf8":
            key = key.decode().encode("utf-8")
        if iv_format == "latin-1":
            key = key.decode().encode("latin-1")
        else:
            iv = binascii.unhexlify(binascii.hexlify(iv))
        return key, iv

    @ChepyDecorators.call_stack
    def rotate(self, rotate_by: int) -> EncryptionEncodingT:
        """Rotate string by provided number

        Args:
            rotate_by (int): Required. Number to rotate by

        Returns:
            Chepy: The Chepy object.

        Examples:
            In this example, we will rotate by 20

            >>> Chepy("some data").rotate(20).out
            "migy xunu"
        """
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        lookup = str.maketrans(
            lc + uc, lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by]
        )
        self.state = self.state.translate(lookup)
        return self

    @ChepyDecorators.call_stack
    def rotate_bruteforce(self) -> EncryptionEncodingT:
        """Brute force rotation from 1 to 26.
        Returned value is a dict where key is the rotation count.

        Returns:
            Chepy: The Chepy object.

        Examples:
            In this example, we will rotate by 20

            >>> Chepy('uryyb').rotate_bruteforce()
            {
                '1': 'vszzc',
                '2': 'wtaad',
                ...
                '13': 'hello',
                ...
            }
        """
        hold = {}
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        for rotate_by in range(1, 27):
            lookup = str.maketrans(
                lc + uc,
                lc[rotate_by:] + lc[:rotate_by] + uc[rotate_by:] + uc[:rotate_by],
            )
            hold[str(rotate_by)] = self.state.translate(lookup)
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def rot_13(self) -> EncryptionEncodingT:
        """ROT-13 encoding

        A simple caesar substitution cipher which rotates alphabet
        characters by the specified amount (default 13).

        Returns:
            Chepy: The Chepy object.
        """
        self.state = codecs.encode(self._convert_to_str(), "rot_13")
        return self

    @ChepyDecorators.call_stack
    def rot_47(self, rotation: int = 47) -> EncryptionEncodingT:
        """ROT 47 encoding

        A slightly more complex variation of a caesar cipher, which includes
        ASCII characters from 33 '!' to 126 '~'. Default rotation: 47.

        Args:
            rotation (int, optional): Amount to rotate by. Defaults to 14.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some").rot_47().out
            "D@>6"
        """
        decoded_string = ""
        for char in self._convert_to_str():
            if ord(char) >= 33 and ord(char) <= 126:
                decoded_char = chr((ord(char) - 33 + rotation) % 94 + 33)
                decoded_string += decoded_char
            else:
                decoded_string += char  # pragma: no cover
        self.state = decoded_string
        return self

    @ChepyDecorators.call_stack
    def rot_47_bruteforce(self) -> EncryptionEncodingT:
        """ROT 47 bruteforce

        Returns:
            Chepy: The Chepy object.
        """
        hold = {}
        data = self._convert_to_str()
        for r in range(1, 94):
            decoded_string = ""
            for char in data:
                if ord(char) >= 33 and ord(char) <= 126:
                    decoded_char = chr((ord(char) - 33 + r) % 94 + 33)
                    decoded_string += decoded_char
                else:
                    decoded_string += char  # pragma: no cover
            hold[str(r)] = decoded_string
        self.state = hold
        return self

    @ChepyDecorators.call_stack
    def rot_8000(self):
        """Rot8000

        Returns:
            Chepy: The Chepy object.
        """
        data = self._convert_to_str()
        valid_code_points = {
            33: True,
            127: False,
            161: True,
            5760: False,
            5761: True,
            8192: False,
            8203: True,
            8232: False,
            8234: True,
            8239: False,
            8240: True,
            8287: False,
            8288: True,
            12288: False,
            12289: True,
            55296: False,
            57344: True,
        }

        BMP_SIZE = 0x10000

        rotlist = {}  # the mapping of char to rotated char
        hiddenblocks = []
        startblock = 0

        for key, value in valid_code_points.items():
            if value:
                hiddenblocks.append({"start": startblock, "end": key - 1})
            else:
                startblock = key

        validintlist = []  # list of all valid chars
        currvalid = False

        for i in range(BMP_SIZE):
            if i in valid_code_points:
                currvalid = valid_code_points[i]
            if currvalid:
                validintlist.append(i)

        rotatenum = len(validintlist) // 2

        # go through every valid char and find its match
        for i in range(len(validintlist)):
            rotlist[chr(validintlist[i])] = chr(
                validintlist[(i + rotatenum) % (rotatenum * 2)]
            )

        outstring = ""

        for char in data:
            # if it is not in the mappings list, just add it directly (no rotation)
            if char not in rotlist:
                outstring += char  # pragma: no cover
                continue  # pragma: no cover

            # otherwise, rotate it and add it to the string
            outstring += rotlist[char]

        return outstring

    @ChepyDecorators.call_stack
    def xor(
        self,
        key: str,
        key_type: Literal["hex", "utf", "base64"] = "hex",
    ) -> EncryptionEncodingT:
        """XOR state with a key

        Args:
            key (str): Required. The key to xor by
            key_type (str, optional): The key type. Valid values are hex, utf and base64. Defaults to "hex".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("secret").xor(key="secret", key_type="utf").to_hex()
            000000000000
        """
        assert key_type in [
            "utf",
            "hex",
            "base64",
        ], "Valid key types are hex, utf and base64"

        if isinstance(key, int):
            key = str(key)
        if key_type == "utf":
            key = binascii.hexlify(key.encode())
        elif key_type == "base64":
            key = binascii.hexlify(base64.b64decode(key.encode()))
        key = binascii.unhexlify(key)
        x = bytearray(b"")
        try:
            for char, key_val in zip(self._convert_to_str(), itertools.cycle(key)):
                x.append(ord(char) ^ key_val)
        except:
            for char, key_val in zip(self._convert_to_bytes(), itertools.cycle(key)):
                x.append(char ^ key_val)

        self.state = x
        return self

    @ChepyDecorators.call_stack
    def xor_bruteforce(self, length: int = 100) -> EncryptionEncodingT:
        """Brute force single byte xor

        For multibyte xor bruteforce, use chepy.extras.crypto_extras.xor_bruteforce_multi
        function

        Args:
            length (int, optional): How to bytes to bruteforce. Defaults to 100.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("pf`qfw").xor_bruteforce()
            {'00': bytearray(b'pf`qfw'),
            '01': bytearray(b'qgapgv'),
            '02': bytearray(b'rdbsdu'),
            '03': bytearray(b'secret'), # here is our secret xored with the hex key 03
            '04': bytearray(b'tbdubs'),
            '05': bytearray(b'ucetcr'),
            ...}
            >>> c.get_by_key("03").bytearray_to_str()
            secret
            >>> c.xor("03").bytearray_to_str()
            pf`qfw
        """
        original = self.state
        found = {}
        keys = hex_chars()
        self.state = original[:length]
        for key in keys:
            self.xor(key)
            found[key] = self.state
            self.state = original[:length]
        self.state = found
        return self

    @ChepyDecorators.call_stack
    def jwt_decode(self) -> EncryptionEncodingT:
        """Decode a JWT token. Does not verify

        Returns:
            Chepy: The Chepy object.
        """
        self.state = {
            "payload": jwt.decode(self._convert_to_str(), verify=False),
            "header": jwt.get_unverified_header(self._convert_to_str()),
        }
        return self

    @ChepyDecorators.call_stack
    def jwt_verify(
        self, secret: str, algorithm: list = ["HS256"]
    ) -> EncryptionEncodingT:
        """Verify JWT token

        Args:
            secret (str): Required. Secret key for token
            algorithm (list, optional): Array of valid algorithms. Defaults to ["HS256"]

        Returns:
            Chepy: The Chepy object.
        """
        self.state = jwt.decode(
            self._convert_to_str(), key=secret, algorithms=algorithm
        )
        return self

    @ChepyDecorators.call_stack
    def jwt_sign(self, secret: str, algorithms: str = "HS256") -> EncryptionEncodingT:
        """Sign a json/dict object in JWT

        Args:
            secret (str): Required. Secret to sign with
            algorithms (str, optional): Signing algorithm. Defaults to "HS256".

        Returns:
            Chepy: The Chepy object.
        """
        if isinstance(self.state, dict):
            data = self.state
        elif isinstance(self.state, str):
            data = json.loads(self.state)
        self.state = jwt.encode(data, key=secret, algorithm=algorithms)
        return self

    @ChepyDecorators.call_stack
    def jwt_bruteforce(
        self, wordlist: str, b64_encode: bool = False, algorithm: list = ["HS256"]
    ) -> EncryptionEncodingT:
        """Brute force JWT token secret

        This method will use the provided wordlist to try and bruteforce the
        verification.

        Args:
            wordlist (str): Required. Path to a wordlist
            b64_encode (bool, optional): Encoded the words in base64. Defaults to False.
            algorithm (list, optional): Array of valid algorithms. Defaults to ["HS256"].

        Returns:
            Chepy: The Chepy object.
        """
        with open(pathlib.Path(wordlist).expanduser().absolute()) as words:
            for word in words:
                try:
                    word = word.strip()
                    if b64_encode:  # pragma: no cover
                        word = base64.b64encode(word)
                    j = jwt.decode(self._convert_to_str(), word, algorithms=algorithm)
                    self.state = {
                        "paylod": j,
                        "header": jwt.get_unverified_header(self._convert_to_str()),
                        "secret": word,
                    }
                    return self
                except jwt.InvalidSignatureError:
                    continue
            else:  # pragma: no cover
                return self

    @ChepyDecorators.call_stack
    def jwt_token_generate_none_alg(
        self, headers: Dict[str, Any] = {}
    ) -> EncryptionEncodingT:
        """Generate a jwt token with none algorithem

        Args:
            headers (Dict[str, Any], optional): Headers. `alg` key will be overwritten. Defaults to {}.

        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, dict), "State should be a dictionary"
        headers["alg"] = "none"
        encoded_headers = base64.b64encode(json.dumps(headers).encode()).replace(
            b"=", b""
        )
        encoded_payload = base64.b64encode(json.dumps(self.state).encode()).replace(
            b"=", b""
        )
        self.state = encoded_headers + b"." + encoded_payload + b"."
        return self

    @ChepyDecorators.call_stack
    def jwt_token_generate_embedded_jwk(
        self,
        private_key_pem: str,
        private_key_passphrase: str = None,
        headers: dict = {},
        alg: str = "RS256",
    ) -> EncryptionEncodingT:
        """Generate a JWT token with an embedded JWK

        Args:
            private_key_pem (str): Private key to sign token
            private_key_passphrase (str, optional): Private key passphrase. Defaults to None.
            headers (dict, optional): Token headers. Defaults to {}.
            alg (str, optional): Token algorithem. Defaults to "RS256".

        Returns:
            Chepy: The Chepy object.
        """
        payload = self.state
        assert isinstance(payload, dict), "State should be a dictionary"
        private_key = RSA.import_key(private_key_pem, private_key_passphrase)

        n = private_key.n
        e = private_key.e

        jwk_header = {
            "kty": "RSA",
            "e": base64.urlsafe_b64encode(e.to_bytes((e.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("="),
            "n": base64.urlsafe_b64encode(n.to_bytes((n.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("="),
        }
        if headers.get("kid"):
            jwk_header["kid"] = headers.get("kid")
        headers["jwk"] = jwk_header
        headers["alg"] = alg

        encoded_header = (
            base64.urlsafe_b64encode(bytes(json.dumps(headers), "utf-8"))
            .decode("utf-8")
            .rstrip("=")
        )
        encoded_payload = (
            base64.urlsafe_b64encode(bytes(json.dumps(payload), "utf-8"))
            .decode("utf-8")
            .rstrip("=")
        )

        signature_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
        hashed_input = Hash.SHA256.new(signature_input)
        signature = PKCS1_15.new(private_key).sign(hashed_input)

        token = f"{encoded_header}.{encoded_payload}.{base64.urlsafe_b64encode(signature).decode('utf-8').replace('=', '')}"

        self.state = token
        return self

    @ChepyDecorators.call_stack
    def rc4_encrypt(self, key: str, key_format: str = "hex") -> EncryptionEncodingT:
        """Encrypt raw state with RC4

        Args:
            key (str): Required. Secret key
            key_format (str, optional): Key format. Defaults to "hex".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").rc4_encrypt("736563726574").o
            b"9e59bf79a2c0b7d253"
        """
        if isinstance(key, str):
            key = key.encode()
        if key_format == "hex":
            key = binascii.unhexlify(key)
        elif key_format == "base64":
            key = base64.b64decode(key)
        elif key_format == "utf-16-le":
            key = key.decode().encode("utf-16-le")
        elif key_format == "utf-16-be":
            key = key.decode().encode("utf-16-be")
        cipher = ARC4.new(key)
        self.state = binascii.hexlify(cipher.encrypt(self._convert_to_bytes()))
        return self

    @ChepyDecorators.call_stack
    def rc4_decrypt(self, key: str, key_format: str = "hex") -> EncryptionEncodingT:
        """Decrypt raw state with RC4

        Args:
            key (str): Required. Secret key
            key_format (str, optional): Key format. Defaults to "hex".

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("9e59bf79a2c0b7d253").hex_to_str().rc4_decrypt("secret").o
            b"some data"
        """
        if isinstance(key, str):
            key = key.encode()
        if key_format == "hex":
            key = binascii.unhexlify(key)
        elif key_format == "base64":
            key = base64.b64decode(key)
        elif key_format == "utf-16-le":
            key = key.decode().encode("utf-16-le")
        elif key_format == "utf-16-be":
            key = key.decode().encode("utf-16-be")
        cipher = ARC4.new(key)
        self.state = cipher.decrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def des_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with DES

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").des_encrypt("70617373776f7264").o
            b"1ee5cb52954b211d1acd6e79c598baac"

            To encrypt using a differnt mode

            >>> Chepy("some data").des_encrypt("password", mode="CTR").o
            b"0b7399049b0267d93d"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES.new(key, mode=DES.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = DES.new(key, mode=DES.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "CTR":
            cipher = DES.new(key, mode=DES.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES.new(key, mode=DES.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def des_decrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with DES.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("1ee5cb52954b211d1acd6e79c598baac").hex_to_str().des_decrypt("password").o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES.new(key, mode=DES.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = DES.new(key, mode=DES.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CTR":
            cipher = DES.new(key, mode=DES.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES.new(key, mode=DES.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def chacha_encrypt(
        self,
        key: str,
        nonce: str = "0000000000000000",
        key_format: str = "hex",
        nonce_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with ChaCha 20 rounds

        Args:
            key (str): Required. The secret key
            nonce (str, optional): Nonce. Defaults to '0000000000000000'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            nonce_format (str, optional): Format of nonce. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.
        """

        key, nonce = self._convert_key(key, nonce, key_format, nonce_format)

        cipher = ChaCha20.new(key=key, nonce=nonce)
        self.state = cipher.encrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def chacha_decrypt(
        self,
        key: str,
        nonce: str = "0000000000000000",
        key_format: str = "hex",
        nonce_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with ChaCha 20 rounds.

        Args:
            key (str): Required. The secret key
            nonce (str, optional): nonce for certain modes only. Defaults to '0000000000000000'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            nonce_format (str, optional): Format of nonce. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.
        """

        key, nonce = self._convert_key(key, nonce, key_format, nonce_format)

        cipher = ChaCha20.new(key=key, nonce=nonce)
        self.state = cipher.decrypt(self._convert_to_bytes())
        return self

    @ChepyDecorators.call_stack
    def triple_des_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with Triple DES

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").triple_des_encrypt("super secret password !!", mode="ECB").o
            b"f8b27a0d8c837edc8fb00ea85f502fb4"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES3.new(key, mode=DES3.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = DES3.new(key, mode=DES3.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "CTR":
            cipher = DES3.new(key, mode=DES3.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES3.new(key, mode=DES3.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def triple_des_decrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with DES.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("f8b27a0d8c837edce87dd13a1ab41f96")
            >>> c.hex_to_str()
            >>> c.triple_des_decrypt("super secret password !!")
            >>> c.o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = DES3.new(key, mode=DES3.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = DES3.new(key, mode=DES3.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CTR":
            cipher = DES3.new(key, mode=DES3.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = DES3.new(key, mode=DES3.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def aes_encrypt(
        self,
        key: str,
        iv: str = "00000000000000000000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with AES.
        CFB mode reflects Cyberchef and not native python behaviour.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only.
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").aes_encrypt("secret password!", mode="ECB").o
            b"5fb8c186394fc399849b89d3b6605fa3"
        """

        assert mode in ["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"], "Not a valid mode."

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 16))
            return self
        elif mode == "CFB":
            cipher = AES.new(key, mode=AES.MODE_CFB, iv=iv, segment_size=128)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "ECB":
            cipher = AES.new(key, mode=AES.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 16))
            return self
        elif mode == "CTR":
            cipher = AES.new(key, mode=AES.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "GCM":
            cipher = AES.new(
                key,
                mode=AES.MODE_GCM,
                nonce=binascii.unhexlify("00000000000000000000000000000000"),
            )
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = AES.new(key, mode=AES.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def aes_decrypt(
        self,
        key: str,
        iv: str = "00000000000000000000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Decrypt raw state encrypted with DES.
        CFB mode reflects Cyberchef and not native python behaviour.

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only.
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            hex_key (bool, optional): If the secret key is a hex string. Defaults to False.
            hex_iv (bool, optional): If the IV is a hex string. Defaults to True.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("5fb8c186394fc399849b89d3b6605fa3")
            >>> c.hex_to_str()
            >>> c.aes_decrypt("7365637265742070617373776f726421")
            >>> c.o
            b"some data"
        """

        assert mode in ["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"], "Not a valid mode."

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = AES.new(key, mode=AES.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 16)
            return self
        if mode == "CFB":
            cipher = AES.new(key, mode=AES.MODE_CFB, iv=iv, segment_size=128)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "ECB":
            cipher = AES.new(key, mode=AES.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 16)
            return self
        elif mode == "CTR":
            cipher = AES.new(key, mode=AES.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "GCM":
            cipher = AES.new(
                key,
                mode=AES.MODE_GCM,
                nonce=binascii.unhexlify("00000000000000000000000000000000"),
            )
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = AES.new(key, mode=AES.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def blowfish_encrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with Blowfish

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only. Defaults to '0000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> Chepy("some data").blowfish_encrypt("password", mode="ECB").o
            b"d9b0a79853f139603951bff96c3d0dd5"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, iv=iv)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "ECB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_ECB)
            self.state = cipher.encrypt(Padding.pad(self._convert_to_bytes(), 8))
            return self
        elif mode == "CTR":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CTR, nonce=b"")
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_OFB, iv=iv)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def blowfish_decrypt(
        self,
        key: str,
        iv: str = "0000000000000000",
        mode: str = "CBC",
        key_format: str = "hex",
        iv_format: str = "hex",
    ) -> EncryptionEncodingT:
        """Encrypt raw state with Blowfish

        Args:
            key (str): Required. The secret key
            iv (str, optional): IV for certain modes only.
                Defaults to '00000000000000000000000000000000'.
            mode (str, optional): Encryption mode. Defaults to 'CBC'.
            key_format (str, optional): Format of key. Defaults to 'hex'.
            iv_format (str, optional): Format of IV. Defaults to 'hex'.

        Returns:
            Chepy: The Chepy object.

        Examples:
            >>> c = Chepy("d9b0a79853f13960fcee3cae16e27884")
            >>> c.hex_to_str()
            >>> c.blowfish_decrypt("password", key_format="utf-8")
            >>> c.o
            b"some data"
        """

        self.__check_mode(mode)

        key, iv = self._convert_key(key, iv, key_format, iv_format)

        if mode == "CBC":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CBC, iv=iv)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "ECB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_ECB)
            self.state = Padding.unpad(cipher.decrypt(self._convert_to_bytes()), 8)
            return self
        elif mode == "CTR":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_CTR, nonce=b"")
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self
        elif mode == "OFB":
            cipher = Blowfish.new(key, mode=Blowfish.MODE_OFB, iv=iv)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def vigenere_encode(self, key: str) -> EncryptionEncodingT:
        """Vigenere encode

        Args:
            key (str): Key

        Raises:
            ValueError: Key is not alpha
            ValueError: Key is not provided

        Returns:
            Chepy: The Chepy object.
        """
        input_str = self._convert_to_str()
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        key = key.lower()
        output = ""
        fail = 0

        if not key:
            raise ValueError("No key entered")  # pragma: no cover
        if not key.isalpha():
            raise ValueError("The key must consist only of letters")  # pragma: no cover

        for i in range(len(input_str)):
            if input_str[i].isalpha():
                is_upper = input_str[i].isupper()
                input_char = input_str[i].lower()
                key_char = key[(i - fail) % len(key)]
                key_index = alphabet.index(key_char)
                input_index = alphabet.index(input_char)
                encoded_index = (key_index + input_index) % 26
                encoded_char = alphabet[encoded_index]
                output += encoded_char.upper() if is_upper else encoded_char
            else:
                output += input_str[i]
                fail += 1

        self.state = output
        return self

    @ChepyDecorators.call_stack
    def vigenere_decode(self, key: str) -> EncryptionEncodingT:
        """Vigenere decode

        Args:
            key (str): Key

        Raises:
            ValueError: Key is not alpha
            ValueError: Key is not provided

        Returns:
            Chepy: The Chepy object.
        """
        input_str = self._convert_to_str()
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        output = ""
        fail = 0

        if not key:
            raise ValueError("No key entered")  # pragma: no cover
        if not key.isalpha():
            raise ValueError("The key must consist only of letters")  # pragma: no cover

        for i in range(len(input_str)):
            if input_str[i].isalpha():
                is_upper = input_str[i].isupper()
                input_char = input_str[i].lower()
                key_char = key[(i - fail) % len(key)]
                key_index = alphabet.index(key_char)
                input_index = alphabet.index(input_char)
                encoded_index = (input_index - key_index + len(alphabet)) % len(
                    alphabet
                )
                encoded_char = alphabet[encoded_index]
                output += encoded_char.upper() if is_upper else encoded_char
            else:
                output += input_str[i]
                fail += 1

        self.state = output
        return self

    @ChepyDecorators.call_stack
    def affine_encode(self, a: int = 1, b: int = 1) -> EncryptionEncodingT:
        """Encode with Affine ciper

        Args:
            a (int, optional): Multiplier value. Defaults to 1
            b (int, optional): Additive value. Defaults to 1

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("secret").affine_encode().o
            "TFDSFU"
        """
        self.state = pycipher.Affine(a=a, b=b).encipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def affine_decode(self, a: int = 1, b: int = 1) -> EncryptionEncodingT:
        """Decode Affine ciper

        Args:
            a (int, optional): Multiplier value. Defaults to 1
            b (int, optional): Additive value. Defaults to 1

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("TFDSFU").affine_decode().o
            "SECRET"
        """
        self.state = pycipher.Affine(a=a, b=b).decipher(self._convert_to_str())
        return self

    @ChepyDecorators.call_stack
    def atbash_encode(self) -> EncryptionEncodingT:
        """Encode with Atbash ciper

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("secret").atbash_encode().o
            "HVXIVG"
        """
        self.state = pycipher.Atbash().encipher(self._convert_to_str(), keep_punct=True)
        return self

    @ChepyDecorators.call_stack
    def atbash_decode(self) -> EncryptionEncodingT:
        """Decode Atbash ciper

        Returns:
            Chepy: The Chepy oject.

        Examples:
            >>> Chepy("hvxivg").atbash_decode().o
            "SECRET"
        """
        self.state = pycipher.Atbash().decipher(self._convert_to_str(), keep_punct=True)
        return self

    @ChepyDecorators.call_stack
    def to_morse_code(
        self,
        dot: str = ".",
        dash: str = "-",
        letter_delim: str = " ",
        word_delim: str = "\n",
    ) -> EncryptionEncodingT:
        """Encode string to morse code

        Args:
            dot (str, optional): The char for dot. Defaults to ".".
            dash (str, optional): The char for dash. Defaults to "-".
            letter_delim (str, optional): Letter delimiter. Defaults to " ".
            word_delim (str, optional): Word delimiter. Defaults to "\\n".

        Returns:
            Chepy: The Chepy object.
        """
        encode = ""
        morse_code_dict = EncryptionConsts.MORSE_CODE_DICT
        for k, v in morse_code_dict.items():
            morse_code_dict[k] = v.replace(".", dot).replace("-", dash)
        for word in self._convert_to_str().split():
            for w in word:
                encode += morse_code_dict.get(w.upper()) + letter_delim
            encode += word_delim
        self.state = encode
        return self

    @ChepyDecorators.call_stack
    def from_morse_code(
        self,
        dot: str = ".",
        dash: str = "-",
        letter_delim: str = " ",
        word_delim: str = "\n",
    ) -> EncryptionEncodingT:
        """Decode morse code

        Args:
            dot (str, optional): The char for dot. Defaults to ".".
            dash (str, optional): The char for dash. Defaults to "-".
            letter_delim (str, optional): Letter delimiter. Defaults to " ".
            word_delim (str, optional): Word delimiter. Defaults to "\\n".

        Returns:
            Chepy: The Chepy object.
        """
        decode = ""
        morse_code_dict = EncryptionConsts.MORSE_CODE_DICT
        for k, v in morse_code_dict.items():
            morse_code_dict[k] = v.replace(".", dot).replace("-", dash)

        morse_code_dict = {value: key for key, value in morse_code_dict.items()}
        for chars in self._convert_to_str().split(letter_delim):
            if word_delim in chars:
                chars = re.sub(word_delim, "", chars, re.I)
                if morse_code_dict.get(chars) is not None:
                    decode += " " + morse_code_dict.get(chars, "")
                else:  # pragma: no cover
                    decode += " " + chars
            else:
                decode += morse_code_dict.get(chars, "")
        self.state = decode
        return self

    @ChepyDecorators.call_stack
    def rsa_encrypt(self, pub_key_path: str) -> EncryptionEncodingT:
        """Encrypt data with RSA Public key in PEM format

        Args:
            pub_key_path (str): Path to Public key

        Returns:
            Chepy: The Chepy object
        """
        with open(str(self._abs_path(pub_key_path)), "r") as f:
            pub_key = f.read()
            key = RSA.importKey(pub_key)
            cipher = PKCS1_OAEP.new(key)
            self.state = cipher.encrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def rsa_decrypt(self, priv_key_path: str) -> EncryptionEncodingT:
        """Decrypt data with RSA Private key in PEM format

        Args:
            priv_key_path (str): Path to Private key

        Returns:
            Chepy: The Chepy object
        """
        with open(str(self._abs_path(priv_key_path)), "r") as f:
            priv_key = f.read()
            key = RSA.importKey(priv_key)
            cipher = PKCS1_OAEP.new(key)
            self.state = cipher.decrypt(self._convert_to_bytes())
            return self

    @ChepyDecorators.call_stack
    def rsa_sign(self, priv_key_path: str) -> EncryptionEncodingT:
        """Sign data in state with RSA Private key in PEM format

        Args:
            priv_key_path (str): Path to Private key

        Returns:
            Chepy: The Chepy object
        """
        with open(str(self._abs_path(priv_key_path)), "r") as f:
            priv_key = f.read()
            key = RSA.importKey(priv_key)
            h = Hash.SHA256.new(self._convert_to_bytes())
            self.state = PKCS1_15.new(key).sign(h)
            return self

    @ChepyDecorators.call_stack
    def rsa_verify(
        self, signature: bytes, public_key_path: str
    ) -> EncryptionEncodingT:  # pragma: no cover
        """Verify data in state with RSA Public key in PEM format

        Args:
            signature (bytes): The signature as bytes
            public_key_path (str): Path to Private key

        Returns:
            Chepy: The Chepy object
        """
        with open(str(self._abs_path(public_key_path)), "r") as f:
            pub_key = f.read()
            key = RSA.importKey(pub_key)
            h = Hash.SHA256.new(self._convert_to_bytes())
            self.state = PKCS1_15.new(key).verify(h, signature)
            return self

    @ChepyDecorators.call_stack
    def rsa_private_pem_to_jwk(self) -> EncryptionEncodingT:
        """Convert RSA PEM private key to jwk format

        Returns:
            Chepy: The Chepy object.
        """
        # Load the PEM private key
        private_key = RSA.import_key(self._convert_to_str())

        n = private_key.n
        e = private_key.e
        d = private_key.d
        p = private_key.p
        q = private_key.q
        dp = private_key.d % (p - 1)
        dq = private_key.d % (q - 1)
        qi = pow(q, -1, p)

        n_base64url = (
            base64.urlsafe_b64encode(n.to_bytes((n.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        e_base64url = (
            base64.urlsafe_b64encode(e.to_bytes((e.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        d_base64url = (
            base64.urlsafe_b64encode(d.to_bytes((d.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        p_base64url = (
            base64.urlsafe_b64encode(p.to_bytes((p.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        q_base64url = (
            base64.urlsafe_b64encode(q.to_bytes((q.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        dp_base64url = (
            base64.urlsafe_b64encode(dp.to_bytes((dp.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        dq_base64url = (
            base64.urlsafe_b64encode(dq.to_bytes((dq.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )
        qi_base64url = (
            base64.urlsafe_b64encode(qi.to_bytes((qi.bit_length() + 7) // 8, "big"))
            .decode("utf-8")
            .rstrip("=")
        )

        private = {
            "p": p_base64url,
            "kty": "RSA",
            "q": q_base64url,
            "d": d_base64url,
            "e": e_base64url,
            "qi": qi_base64url,
            "dp": dp_base64url,
            "dq": dq_base64url,
            "n": n_base64url,
        }

        public = {"kty": "RSA", "e": e_base64url, "n": n_base64url}
        self.state = {"private": private, "public": public}
        return self

    @ChepyDecorators.call_stack
    def rsa_public_key_from_jwk(self) -> EncryptionEncodingT:
        """Genereate RSA public key in PEM format from JWK

        Raises:
            AssertionError: If n or e not found

        Returns:
            Chepy: The Chepy object.
        """
        assert isinstance(self.state, dict), "State should be a dict"
        jwk_key = self.state
        if not "e" in jwk_key or "n" not in jwk_key:
            raise AssertionError("e or n not found")  # pragma: no cover
        e = int.from_bytes(base64.urlsafe_b64decode(jwk_key["e"] + "=="), "big")
        n = int.from_bytes(base64.urlsafe_b64decode(jwk_key["n"] + "=="), "big")

        public_key = RSA.construct((n, e))

        self.state = public_key.export_key().decode("utf-8")
        return self

    @ChepyDecorators.call_stack
    def monoalphabetic_substitution(
        self, mapping: Dict[str, str] = {}
    ) -> EncryptionEncodingT:
        """Monoalphabetic substitution. Re-map characters

        Args:
            mapping (Dict[str, str], optional): Mapping of characters where key is the character to map and value is the new character to replace with. Defaults to {}.

        Returns:
            Chepy: The Chepy object
        """
        hold = ""
        cipher = self._convert_to_str()
        for c in cipher:
            hold += mapping.get(c.lower(), c)
        self.state = hold
        return self
