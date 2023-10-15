from ..core import ChepyCore
from typing import Any, TypeVar, Literal, Dict, Union

jwt: Any
AES: Any
ARC4: Any
DES: Any
DES3: Any
Blowfish: Any
EncryptionEncodingT = TypeVar('EncryptionEncodingT', bound='EncryptionEncoding')
FORMAT = Literal['hex', 'base64', 'utf-8', 'latin-1', 'raw']
RC4_FORMAT = Literal['hex', 'base64', 'utf8', 'utf-16-be', 'utf-16-le']

class EncryptionEncoding(ChepyCore):
    def __init__(self, *data: Any) -> None: ...
    state: Any = ...
    def rotate(self: EncryptionEncodingT, rotate_by: int) -> EncryptionEncodingT: ...
    def rotate_bruteforce(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def rot_13(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def rot_47(self: EncryptionEncodingT, amount: int=...) -> EncryptionEncodingT: ...
    def rot_47_bruteforce(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def rot_8000(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def xor(self: EncryptionEncodingT, key: Union[str, bytearray], key_type: Literal['hex', 'utf', 'base64', 'decimal']=...) -> EncryptionEncodingT: ...
    def xor_bruteforce(self: EncryptionEncodingT, length: int=..., crib: Union[str, bytes, None]=...) -> EncryptionEncodingT: ...
    def jwt_decode(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def jwt_verify(self: EncryptionEncodingT, secret: str, algorithm: list=...) -> EncryptionEncodingT: ...
    def jwt_sign(self: EncryptionEncodingT, secret: str, algorithms: str=...) -> EncryptionEncodingT: ...
    def jwt_token_generate_none_alg(self: EncryptionEncodingT, headers: Dict[str, Any]=...) -> EncryptionEncodingT: ...
    def jwt_token_generate_embedded_jwk(self: EncryptionEncodingT, private_key_pem: str, private_key_passphrase: str = ..., headers: dict = ..., alg: str = Union["RS256", "RS512"]) -> EncryptionEncodingT: ...
    def rc4_encrypt(self: EncryptionEncodingT, key: str, key_format: RC4_FORMAT=...) -> EncryptionEncodingT: ...
    def rc4_decrypt(self: EncryptionEncodingT, key: str, key_format: RC4_FORMAT=...) -> EncryptionEncodingT: ...
    def des_encrypt(self: EncryptionEncodingT, key: str, iv: str=..., mode: Literal["CBC", "OFB", "CTR", "ECB"]=..., key_format: FORMAT=..., iv_format: FORMAT=...) -> EncryptionEncodingT: ...
    def des_decrypt(self: EncryptionEncodingT, key: str, iv: str=..., mode: Literal["CBC", "OFB", "CTR", "ECB"]=..., key_format: FORMAT=..., iv_format: FORMAT=...) -> EncryptionEncodingT: ...
    def chacha_encrypt(self: EncryptionEncodingT, key: str, nonce: str=..., key_format: FORMAT=..., nonce_format: FORMAT=...) -> EncryptionEncodingT: ...
    def chacha_decrypt(self: EncryptionEncodingT, key: str, nonce: str=..., key_format: FORMAT=..., nonce_format: FORMAT=...) -> EncryptionEncodingT: ...
    def triple_des_encrypt(self: EncryptionEncodingT, key: str, iv: str=..., mode: Literal["CBC", "OFB", "CTR", "ECB"]=..., key_format: FORMAT=..., iv_format: FORMAT=...) -> EncryptionEncodingT: ...
    def triple_des_decrypt(self: EncryptionEncodingT, key: str, iv: str=..., mode: Literal["CBC", "OFB", "CTR", "ECB"]=..., key_format: FORMAT=..., iv_format: FORMAT=...) -> EncryptionEncodingT: ...
    def aes_encrypt(self: EncryptionEncodingT, key: Union[bytes, str], iv: str=..., mode: Literal["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"]=..., key_format: FORMAT=..., iv_format: FORMAT=...) -> EncryptionEncodingT: ...
    def aes_decrypt(self: EncryptionEncodingT, key: Union[bytes, str], iv: str=..., mode: Literal["CBC", "CFB", "OFB", "CTR", "ECB", "GCM"]=..., key_format: FORMAT=..., iv_format: FORMAT=...) -> EncryptionEncodingT: ...
    def blowfish_encrypt(self: EncryptionEncodingT, key: str, iv: str=..., mode: Literal["CBC", "OFB", "CTR", "ECB"]=..., key_format: FORMAT=..., iv_format: FORMAT=...) -> EncryptionEncodingT: ...
    def blowfish_decrypt(self: EncryptionEncodingT, key: str, iv: str=..., mode: Literal["CBC", "OFB", "CTR", "ECB"]=..., key_format: FORMAT=..., iv_format: FORMAT=...) -> EncryptionEncodingT: ...
    def vigenere_encode(self: EncryptionEncodingT, key: str) -> EncryptionEncodingT: ...
    def vigenere_decode(self: EncryptionEncodingT, key: str) -> EncryptionEncodingT: ...
    def affine_encode(self: EncryptionEncodingT, a: int=..., b: int=...) -> EncryptionEncodingT: ...
    def affine_decode(self: EncryptionEncodingT, a: int=..., b: int=...) -> EncryptionEncodingT: ...
    def atbash_encode(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def atbash_decode(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def to_morse_code(self: EncryptionEncodingT, dot: str=..., dash: str=..., letter_delim: str=..., word_delim: str=...) -> EncryptionEncodingT: ...
    def from_morse_code(self: EncryptionEncodingT, dot: str=..., dash: str=..., letter_delim: str=..., word_delim: str=...) -> EncryptionEncodingT: ...
    def rsa_encrypt(self: EncryptionEncodingT, public_key: str, is_file: bool=False, passphrase: Union[str, None]=None, cipher:Literal['OAEP', 'PKCS']='OAEP') -> EncryptionEncodingT: ...
    def rsa_decrypt(self: EncryptionEncodingT, private_key: str, is_file: bool=False, passphrase: Union[str, None]=None, cipher:Literal['OAEP', 'PKCS']='OAEP') -> EncryptionEncodingT: ...
    def rsa_sign(self: EncryptionEncodingT, private_key: str, is_file: bool=False, passphrase: Union[str, None]=None, hash_format: Literal['SHA256', 'SHA512', 'SHA1', 'MD5', 'SHA384']='SHA256') -> EncryptionEncodingT: ...
    def rsa_verify(self: EncryptionEncodingT, signature: bytes, public_key: str, is_file: bool=False, passphrase: Union[str, None]=None, hash_format: Literal['SHA256', 'SHA512', 'SHA1', 'MD5', 'SHA384']='SHA256') -> EncryptionEncodingT: ...
    def rsa_private_pem_to_jwk(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def rsa_public_key_from_jwk(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def monoalphabetic_substitution(self: EncryptionEncodingT, mapping: Dict[str, str]=...): ...
    def to_letter_number_code(self: EncryptionEncodingT, join_by: Union[str, bytes]=...) -> EncryptionEncodingT: ...
    def from_letter_number_code(self: EncryptionEncodingT, delimiter: Union[str, bytes, None]=None, join_by: Union[str, bytes]=...) -> EncryptionEncodingT: ...
    def ls47_encrypt(self: EncryptionEncodingT, password: str, padding: int=..., signature: str=...) -> EncryptionEncodingT: ...
    def ls47_decrypt(self: EncryptionEncodingT, password: str, padding: int=...) -> EncryptionEncodingT: ...
    def bifid_encode(self: EncryptionEncodingT, key: Union[bytes, str]='') -> EncryptionEncodingT: ...
    def bifid_decode(self: EncryptionEncodingT, key: Union[bytes, str]='') -> EncryptionEncodingT: ...
    def huffman_encode(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def huffman_decode(self: EncryptionEncodingT, huffman_codes: Dict[str, str]) -> EncryptionEncodingT: ...
    def cetacean_encode(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def cetacean_decode(self: EncryptionEncodingT) -> EncryptionEncodingT: ...
    def rabbit(self: EncryptionEncodingT, key: str, iv: Union[None, str]=...) -> EncryptionEncodingT: ...
    def fernet_encrypt(self: EncryptionEncodingT, key:Union[bytes, str], encode_key: bool=False) -> EncryptionEncodingT: ...
    def fernet_decrypt(self: EncryptionEncodingT, key:Union[bytes, str], encode_key: bool=False) -> EncryptionEncodingT: ...
