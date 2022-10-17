from ..core import ChepyCore
from typing import Any, Literal, TypeVar, Union

yaml: Any
DataFormatT = TypeVar('DataFormatT', bound='DataFormat')

class DataFormat(ChepyCore):
    def __init__(self, *data: Any) -> None: ...
    state: Any = ...
    def eval_state(self: DataFormatT) -> DataFormatT: ...
    def bytes_to_ascii(self: DataFormatT) -> DataFormatT: ...
    def list_to_str(self: DataFormatT, join_by: Union[str, bytes]=...) -> DataFormatT: ...
    def str_list_to_list(self: DataFormatT) -> DataFormatT: ...
    def join(self: DataFormatT, by: Union[str, bytes]=...) -> DataFormatT: ...
    def join_list(self: DataFormatT, by: Union[str, bytes]=...) -> DataFormatT: ...
    def json_to_dict(self: DataFormatT) -> DataFormatT: ...
    def dict_to_json(self: DataFormatT) -> DataFormatT: ...
    def dict_get_items(self: DataFormatT, *keys: str) -> DataFormatT: ...
    def yaml_to_json(self: DataFormatT) -> DataFormatT: ...
    def json_to_yaml(self: DataFormatT) -> DataFormatT: ...
    def base58_encode(self: DataFormatT) -> DataFormatT: ...
    def base58_decode(self: DataFormatT) -> DataFormatT: ...
    def base85_encode(self: DataFormatT) -> DataFormatT: ...
    def base85_decode(self: DataFormatT) -> DataFormatT: ...
    def base16_encode(self: DataFormatT) -> DataFormatT: ...
    def base16_decode(self: DataFormatT) -> DataFormatT: ...
    def base32_encode(self: DataFormatT) -> DataFormatT: ...
    def base32_decode(self: DataFormatT) -> DataFormatT: ...
    def to_int(self: DataFormatT) -> DataFormatT: ...
    def to_bytes(self: DataFormatT) -> DataFormatT: ...
    def from_bytes(self: DataFormatT) -> DataFormatT: ...
    def base64_encode(self: DataFormatT, custom: str=...) -> DataFormatT: ...
    def base64_decode(self: DataFormatT, custom: str=..., url_safe: bool=...) -> DataFormatT: ...
    def decode_bytes(self: DataFormatT, errors: Literal['ignore', 'backslashreplace', 'replace']=...) -> DataFormatT: ...
    def to_hex(self: DataFormatT, delimiter: str=..., join_by: str=...) -> DataFormatT: ...
    def from_hex(self: DataFormatT, delimiter: str=...) -> DataFormatT: ...
    def hex_to_int(self: DataFormatT) -> DataFormatT: ...
    def hex_to_binary(self: DataFormatT) -> DataFormatT: ...
    def hex_to_str(self: DataFormatT, ignore: bool=...) -> DataFormatT: ...
    def str_to_hex(self: DataFormatT) -> DataFormatT: ...
    def int_to_hex(self: DataFormatT) -> DataFormatT: ...
    def int_to_str(self: DataFormatT) -> DataFormatT: ...
    def binary_to_hex(self: DataFormatT) -> DataFormatT: ...
    def normalize_hex(self: DataFormatT, is_bytearray: Any=...) -> DataFormatT: ...
    def str_from_hexdump(self: DataFormatT) -> DataFormatT: ...
    def to_hexdump(self: DataFormatT) -> DataFormatT: ...
    def from_hexdump(self: DataFormatT) -> DataFormatT: ...
    def url_encode(self: DataFormatT, safe: str=...) -> DataFormatT: ...
    def url_decode(self: DataFormatT) -> DataFormatT: ...
    def bytearray_to_str(self: DataFormatT, encoding: str=..., errors: str=...) -> DataFormatT: ...
    def str_to_list(self: DataFormatT) -> DataFormatT: ...
    def str_to_dict(self: DataFormatT) -> DataFormatT: ...
    def to_charcode(self: DataFormatT, join_by: str=..., base: int=...) -> DataFormatT: ...
    def from_charcode(self: DataFormatT, delimiter: str=..., join_by: str=..., base: int=...) -> DataFormatT: ...
    def to_decimal(self: DataFormatT) -> DataFormatT: ...
    def from_decimal(self: DataFormatT, delimiter: str=..., join_by: str=...) -> DataFormatT: ...
    def to_binary(self: DataFormatT, join_by: str=...) -> DataFormatT: ...
    def from_binary(self: DataFormatT, delimiter: str=...) -> DataFormatT: ...
    def to_octal(self: DataFormatT, join_by: str=...) -> DataFormatT: ...
    def from_octal(self: DataFormatT, delimiter: str=..., join_by: str=...) -> DataFormatT: ...
    def to_html_entity(self: DataFormatT) -> DataFormatT: ...
    def from_html_entity(self: DataFormatT) -> DataFormatT: ...
    def to_punycode(self: DataFormatT) -> DataFormatT: ...
    def from_punycode(self: DataFormatT) -> DataFormatT: ...
    def encode_bruteforce(self: DataFormatT) -> DataFormatT: ...
    def decode_bruteforce(self: DataFormatT) -> DataFormatT: ...
    def to_braille(self: DataFormatT) -> DataFormatT: ...
    def from_braille(self: DataFormatT) -> DataFormatT: ...
    def trim(self: DataFormatT) -> DataFormatT: ...
    def convert_to_nato(self: DataFormatT, join_by:str) -> DataFormatT: ...
    def swap_strings(self: DataFormatT, by:int) -> DataFormatT: ...
    def to_string(self: DataFormatT) -> DataFormatT: ...
    def select(self: DataFormatT, start: int, end: int) -> DataFormatT: ...
    def length(self: DataFormatT) -> DataFormatT: ...
    def to_leetcode(self: DataFormatT, replace_space: str=...) -> DataFormatT: ...
    def substitute(self: DataFormatT, x: str=..., y: str=...) -> DataFormatT: ...
    def remove_nonprintable(self: DataFormatT, replace_with: bytes = ...): ...
    def base91_encode(self: DataFormatT) -> DataFormatT: ...
    def base91_decode(self: DataFormatT) -> DataFormatT: ...
    def swap_endianness(self: DataFormatT) -> DataFormatT: ...
