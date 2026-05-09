from .baseX_decoder import BaseDecoder
from .compression_decoder import CompressionUtilsDecoder
from .baseX_compression_decoder import BaseCompressionUtilsDecoder
from .blank_decoder import BlankObfDeobfuscator
from .rendy_decoder import RendyDecoder
from .christian_decoder import ChristianObfDeobfuscator
from .clever_decoder import CleverObfDeobfuscator
from .grandiosee_decoder import GrandioseeObfDeobfuscator
from .xindex_decoder import XindexObfDeobfuscator
from .impostor_decoder import ImpostorObfDeobfuscator

__all__ = [
    "BaseDecoder",
    "CompressionUtilsDecoder",
    "BaseCompressionUtilsDecoder",
    "BlankObfDeobfuscator",
    "RendyDecoder",
    "ChristianObfDeobfuscator",
    "CleverObfDeobfuscator",
    "GrandioseeObfDeobfuscator",
    "XindexObfDeobfuscator",
    "ImpostorObfDeobfuscator",
]


DECODER_REGISTRY = {
    "1": BaseDecoder,
    "2": BaseDecoder,
    "3": BaseDecoder,
    "4": CompressionUtilsDecoder,
    "5": CompressionUtilsDecoder,
    "6": CompressionUtilsDecoder,
    "7": BaseCompressionUtilsDecoder,
    "8": BaseCompressionUtilsDecoder,
    "9": BaseCompressionUtilsDecoder,
    "10": BaseCompressionUtilsDecoder,
    "11": BaseCompressionUtilsDecoder,
    "12": BaseCompressionUtilsDecoder,
    "13": BaseCompressionUtilsDecoder,
    "14": BaseCompressionUtilsDecoder,
    "15": BaseCompressionUtilsDecoder,
    "16": RendyDecoder,
    "17": ChristianObfDeobfuscator,
    "18": BlankObfDeobfuscator,
    "19": CleverObfDeobfuscator,
    "20": GrandioseeObfDeobfuscator,
    "21": XindexObfDeobfuscator,
    "22": ImpostorObfDeobfuscator,
}
