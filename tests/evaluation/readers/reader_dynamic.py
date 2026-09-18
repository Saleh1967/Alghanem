"""قارئٌ صوريٌّ يفتح طريقًا خارج الاستيراد المُصرَّح؛ يُرصَد ولا يُجمَّد."""

from __future__ import annotations

import importlib


def read(payload_bytes: bytes) -> object:
    """يستورد وحدةً وقتَ التشغيل، فيخرق الحدَّ المُصرَّح."""

    return importlib.import_module("alghanem.arabic.madlul_alone_formal")
