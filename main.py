"""
BLS test vectors generator
"""

from typing import Tuple, Any, Callable, Dict, Generator

import argparse
from pathlib import Path
import json
from ruamel.yaml import YAML

from hashlib import sha256

from py_ecc.bls12_381 import (
    G1,
    G2,
    FQ,
    FQ2,
    add,
    multiply,
    neg,
    is_inf
)


def to_bytes32(i):
    return i.to_bytes(32, byteorder='big')


def hash(x):
    return sha256(x).digest()


def encode_hex(value: bytes) -> str:
    return value.hex()


def int_to_big_endian(value: int) -> bytes:
    return value.to_bytes((value.bit_length() + 7) // 8, byteorder='big')


def int_to_hex(n: int, byte_length: int = None) -> str:
    byte_value = int_to_big_endian(n)
    if byte_length:
        byte_value = byte_value.rjust(byte_length, b'\x00')
    return encode_hex(byte_value)


def hex_to_int(x: str) -> int:
    return int(x, 16)


# gas costs
# TODO to change
BLS12_G1ADD_GAS = 600
BLS12_G2ADD_GAS = 4500
BLS12_G1MUL_GAS = 12000
BLS12_G2MUL_GAS = 55000
BLS12_MAP_FP_TO_G1_GAS = 5500
BLS12_MAP_FP2_TO_G2_GAS = 110000

# random point in G1
P1 = (
    FQ(
        2642749686785829596817345696055666872043783053155481581788492942917249902143862050648544313423577373440886627275814  # noqa: E501
    ),  # noqa: E501
    FQ(
        3758365293065836235831663685357329573226673833426684174336991792633405517674721205716466791757730149346109800483361  # noqa: E501
    ),  # noqa: E501
)


# random point in G2
P2 = (
    FQ2(
        [
            2492164500931426079025163640852824812322867633561487327988861767918782925114618691347698906331033143057488152854311,  # noqa: E501
            1296003438898513467811811427923539448251934100547963606575856033955925534446513985696904241181481649924224027073384,  # noqa: E501
        ]
    ),
    FQ2(
        [
            2403995578136121235978187296860525416643018865432935587266433984437673369013628886898228883216954086902460896225150,  # noqa: E501
            2021783735792747140008634321371188179203707822883609206755922036803500907979420976539856007028648957203721805595729,  # noqa: E501
        ]
    ),
)


HASH_G1_MESSAGES = [
    (b'',
     '00000000000000000000000000000000156c8a6a2c184569d69a76be144b5cdc5141d2d2ca4fe341f011e25e3969c55ad9e9b9ce2eb833c81a908e5fa4ac5f03',
     '00000000000000000000000000000000184bb665c37ff561a89ec2122dd343f20e0f4cbcaec84e3c3052ea81d1834e192c426074b02ed3dca4e7676ce4ce48ba',
     '0000000000000000000000000000000004407b8d35af4dacc809927071fc0405218f1401a6d15af775810e4e460064bcc9468beeba82fdc751be70476c888bf3'),
    (b'abc',
     '00000000000000000000000000000000147e1ed29f06e4c5079b9d14fc89d2820d32419b990c1c7bb7dbea2a36a045124b31ffbde7c99329c05c559af1c6cc82',
     '00000000000000000000000000000000009769f3ab59bfd551d53a5f846b9984c59b97d6842b20a2c565baa167945e3d026a3755b6345df8ec7e6acb6868ae6d',
     '000000000000000000000000000000001532c00cf61aa3d0ce3e5aa20c3b531a2abd2c770a790a2613818303c6b830ffc0ecf6c357af3317b9575c567f11cd2c'),
    (b'abcdef0123456789',
     '0000000000000000000000000000000004090815ad598a06897dd89bcda860f25837d54e897298ce31e6947378134d3761dc59a572154963e8c954919ecfa82d',
     '000000000000000000000000000000001974dbb8e6b5d20b84df7e625e2fbfecb2cdb5f77d5eae5fb2955e5ce7313cae8364bc2fff520a6c25619739c6bdcb6a',
     '0000000000000000000000000000000015f9897e11c6441eaa676de141c8d83c37aab8667173cbe1dfd6de74d11861b961dccebcd9d289ac633455dfcc7013a3'),
    (b'q128_qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq',
     '0000000000000000000000000000000008dccd088ca55b8bfbc96fb50bb25c592faa867a8bb78d4e94a8cc2c92306190244532e91feba2b7fed977e3c3bb5a1f',
     '000000000000000000000000000000000a7a047c4a8397b3446450642c2ac64d7239b61872c9ae7a59707a8f4f950f101e766afe58223b3bff3a19a7f754027c',
     '000000000000000000000000000000001383aebba1e4327ccff7cf9912bda0dbc77de048b71ef8c8a81111d71dc33c5e3aa6edee9cf6f5fe525d50cc50b77cc9'),
    (b'a512_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
     '000000000000000000000000000000000dd824886d2123a96447f6c56e3a3fa992fbfefdba17b6673f9f630ff19e4d326529db37e1c1be43f905bf9202e0278d',
     '000000000000000000000000000000000e7a16a975904f131682edbb03d9560d3e48214c9986bd50417a77108d13dc957500edf96462a3d01e62dc6cd468ef11',
     '000000000000000000000000000000000ae89e677711d05c30a48d6d75e76ca9fb70fe06c6dd6ff988683d89ccde29ac7d46c53bb97a59b1901abf1db66052db')
]

HASH_G2_MESSAGES = [
    (b'',
     '0000000000000000000000000000000007355d25caf6e7f2f0cb2812ca0e513bd026ed09dda65b177500fa31714e09ea0ded3a078b526bed3307f804d4b93b04',
     '0000000000000000000000000000000002829ce3c021339ccb5caf3e187f6370e1e2a311dec9b75363117063ab2015603ff52c3d3b98f19c2f65575e99e8b78c',
     '0000000000000000000000000000000000e7f4568a82b4b7dc1f14c6aaa055edf51502319c723c4dc2688c7fe5944c213f510328082396515734b6612c4e7bb7',
     '00000000000000000000000000000000126b855e9e69b1f691f816e48ac6977664d24d99f8724868a184186469ddfd4617367e94527d4b74fc86413483afb35b',
     '000000000000000000000000000000000caead0fd7b6176c01436833c79d305c78be307da5f6af6c133c47311def6ff1e0babf57a0fb5539fce7ee12407b0a42',
     '000000000000000000000000000000001498aadcf7ae2b345243e281ae076df6de84455d766ab6fcdaad71fab60abb2e8b980a440043cd305db09d283c895e3d')
]


def expect_exception(func, *args):
    try:
        func(*args)
    except Exception:
        pass
    else:
        raise Exception("should have raised exception")


def case01_add_G1():
    # Commutativity
    result_comm1 = add(G1, P1)
    result_comm2 = add(P1, G1)
    assert result_comm1 == result_comm2
    # Identity element
    result_identity_G1 = add(G1, None)
    assert G1 == result_identity_G1
    result_identity_P1 = add(P1, None)
    assert P1 == result_identity_P1
    # Additive negation
    result_neg_G1 = add(G1, neg(G1))
    assert (is_inf(result_neg_G1))
    result_neg_P1 = add(P1, neg(P1))
    assert (is_inf(result_neg_P1))
    # Doubling
    result_doubling_G1 = add(G1, G1)
    assert result_doubling_G1 == multiply(G1, 2)
    result_doubling_P1 = add(P1, P1)
    assert result_doubling_P1 == multiply(P1, 2)

    yield 'add_G1_bls', [
        {
        "Input": int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)) + int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)),
        "Name": "bls_g1add_g1+p1",
        "Expected": int_to_hex(int(result_comm1[0]), 64) + (int_to_hex(int(result_comm1[1]), 64)),
        "Gas": BLS12_G1ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)) + int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)),
        "Name": "bls_g1add_p1+g1",
        "Expected": int_to_hex(int(result_comm2[0]), 64) + (int_to_hex(int(result_comm2[1]), 64)),
        "Gas": BLS12_G1ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)) + int_to_hex(0, 64) + int_to_hex(0, 64),
        "Name": "bls_g1add_(g1+0=g1)",
        "Expected": int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)),
        "Gas": BLS12_G1ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)) + int_to_hex(0, 64) + int_to_hex(0, 64),
        "Name": "bls_g1add_(p1+0=p1)",
        "Expected": int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)),
        "Gas": BLS12_G1ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)) + int_to_hex(int(neg(G1)[0]), 64) + (int_to_hex(int(neg(G1)[1]), 64)),
        "Name": "bls_g1add_(g1-g1=0)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G1ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)) + int_to_hex(int(neg(P1)[0]), 64) + (int_to_hex(int(neg(P1)[1]), 64)),
        "Name": "bls_g1add_(p1-p1=0)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G1ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)) + int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)),
        "Name": "bls_g1add_(g1+g1=2*g1)",
        "Expected": int_to_hex(int(result_doubling_G1[0]), 64) + (int_to_hex(int(result_doubling_G1[1]), 64)),
        "Gas": BLS12_G1ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)) + int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)),
        "Name": "bls_g1add_(p1+p1=2*p1)",
        "Expected": int_to_hex(int(result_doubling_P1[0]), 64) + (int_to_hex(int(result_doubling_P1[1]), 64)),
        "Gas": BLS12_G1ADD_GAS,
        "NoBenchmark": False
        }
    ]


def case02_add_G2():
    # Commutativity
    result_comm1 = add(G2, P2)
    result_comm2 = add(P2, G2)
    assert result_comm1 == result_comm2
    # Identity element
    result_identity_G2 = add(G2, None)
    assert G2 == result_identity_G2
    result_identity_P2 = add(P2, None)
    assert P2 == result_identity_P2
    # Additive negation
    result_neg_G2 = add(G2, neg(G2))
    assert (is_inf(result_neg_G2))
    result_neg_P2 = add(P2, neg(P2))
    assert (is_inf(result_neg_P2))
    # Doubling
    result_doubling_G2 = add(G2, G2)
    assert result_doubling_G2 == multiply(G2, 2)
    result_doubling_P2 = add(P2, P2)
    assert result_doubling_P2 == multiply(P2, 2)
    yield 'add_G2_bls', [
        {
        "Input": int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64) + int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64),
        "Name": "bls_g2add_g2+p2",
        "Expected": int_to_hex(int(result_comm1[0].coeffs[0]), 64) + int_to_hex(int(result_comm1[0].coeffs[1]), 64) + int_to_hex(int(result_comm1[1].coeffs[0]), 64) + int_to_hex(int(result_comm1[1].coeffs[1]), 64),
        "Gas": BLS12_G2ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64) + int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64),
        "Name": "bls_g2add_p2+g2",
        "Expected": int_to_hex(int(result_comm2[0].coeffs[0]), 64) + int_to_hex(int(result_comm2[0].coeffs[1]), 64) + int_to_hex(int(result_comm2[1].coeffs[0]), 64) + int_to_hex(int(result_comm2[1].coeffs[1]), 64),
        "Gas": BLS12_G2ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64),
        "Name": "bls_g2add_(g2+0=g2)",
        "Expected": int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64),
        "Gas": BLS12_G2ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64),
        "Name": "bls_g2add_(p2+0=p2)",
        "Expected": int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64),
        "Gas": BLS12_G2ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64) + int_to_hex(int(neg(G2)[0].coeffs[0]), 64) + int_to_hex(int(neg(G2)[0].coeffs[1]), 64) + int_to_hex(int(neg(G2)[1].coeffs[0]), 64) + int_to_hex(int(neg(G2)[1].coeffs[1]), 64),
        "Name": "bls_g2add_(g2-g2=0)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G2ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64) + int_to_hex(int(neg(P2)[0].coeffs[0]), 64) + int_to_hex(int(neg(P2)[0].coeffs[1]), 64) + int_to_hex(int(neg(P2)[1].coeffs[0]), 64) + int_to_hex(int(neg(P2)[1].coeffs[1]), 64),
        "Name": "bls_g2add_(p2-p2=0)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G2ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64) + int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64),
        "Name": "bls_g2add_(g2+g2=2*g2)",
        "Expected": int_to_hex(int(result_doubling_G2[0].coeffs[0]), 64) + int_to_hex(int(result_doubling_G2[0].coeffs[1]), 64) + int_to_hex(int(result_doubling_G2[1].coeffs[0]), 64) + int_to_hex(int(result_doubling_G2[1].coeffs[1]), 64),
        "Gas": BLS12_G2ADD_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64) + int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64),
        "Name": "bls_g2add_(p2+p2=2*p2)",
        "Expected": int_to_hex(int(result_doubling_P2[0].coeffs[0]), 64) + int_to_hex(int(result_doubling_P2[0].coeffs[1]), 64) + int_to_hex(int(result_doubling_P2[1].coeffs[0]), 64) + int_to_hex(int(result_doubling_P2[1].coeffs[1]), 64),
        "Gas": BLS12_G2ADD_GAS,
        "NoBenchmark": False
        }
    ]


def case03_mul_G1():
    # Doubling
    result_doubling_G1 = add(G1, G1)
    assert result_doubling_G1 == multiply(G1, 2)
    result_doubling_P1 = add(P1, P1)
    assert result_doubling_P1 == multiply(P1, 2)

    yield 'mul_G1_bls', [
        {
        "Input": int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)) + int_to_hex(int(2), 32),
        "Name": "bls_g1mul_(g1+g1=2*g1)",
        "Expected": int_to_hex(int(result_doubling_G1[0]), 64) + (int_to_hex(int(result_doubling_G1[1]), 64)),
        "Gas": BLS12_G1MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)) + int_to_hex(int(2), 32),
        "Name": "bls_g1mul_(p1+p1=2*p1)",
        "Expected": int_to_hex(int(result_doubling_P1[0]), 64) + (int_to_hex(int(result_doubling_P1[1]), 64)),
        "Gas": BLS12_G1MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)) + int_to_hex(int(1), 32),
        "Name": "bls_g1mul_(1*g1=g1)",
        "Expected": int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)),
        "Gas": BLS12_G1MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)) + int_to_hex(int(1), 32),
        "Name": "bls_g1mul_(1*p1=p1)",
        "Expected": int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)),
        "Gas": BLS12_G1MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G1[0]), 64) + (int_to_hex(int(G1[1]), 64)) + int_to_hex(int(0), 32),
        "Name": "bls_g1mul_(0*g1=inf)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G1MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P1[0]), 64) + (int_to_hex(int(P1[1]), 64)) + int_to_hex(int(0), 32),
        "Name": "bls_g1mul_(0*p1=inf)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G1MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(int(17), 32),
        "Name": "bls_g1mul_(x*inf=inf)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G1MUL_GAS,
        "NoBenchmark": False
        }
    ]


def case04_mul_G2():
    # Doubling
    result_doubling_G2 = add(G2, G2)
    assert result_doubling_G2 == multiply(G2, 2)
    result_doubling_P2 = add(P2, P2)
    assert result_doubling_P2 == multiply(P2, 2)
    yield 'mul_G2_bls', [
        {
        "Input": int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64) + int_to_hex(int(2), 32),
        "Name": "bls_g2mul_(g2+g2=2*g2)",
        "Expected": int_to_hex(int(result_doubling_G2[0].coeffs[0]), 64) + int_to_hex(int(result_doubling_G2[0].coeffs[1]), 64) + int_to_hex(int(result_doubling_G2[1].coeffs[0]), 64) + int_to_hex(int(result_doubling_G2[1].coeffs[1]), 64),
        "Gas": BLS12_G2MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64) + int_to_hex(int(2), 32),
        "Name": "bls_g2mul_(g2+g2=2*g2)",
        "Expected": int_to_hex(int(result_doubling_P2[0].coeffs[0]), 64) + int_to_hex(int(result_doubling_P2[0].coeffs[1]), 64) + int_to_hex(int(result_doubling_P2[1].coeffs[0]), 64) + int_to_hex(int(result_doubling_P2[1].coeffs[1]), 64),
        "Gas": BLS12_G2MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64) + int_to_hex(int(1), 32),
        "Name": "bls_g2mul_(1*g2=g2)",
        "Expected": int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64),
        "Gas": BLS12_G2MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64) + int_to_hex(int(1), 32),
        "Name": "bls_g2mul_(1*p2=p2)",
        "Expected": int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64),
        "Gas": BLS12_G2MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(G2[0].coeffs[0]), 64) + int_to_hex(int(G2[0].coeffs[1]), 64) + int_to_hex(int(G2[1].coeffs[0]), 64) + int_to_hex(int(G2[1].coeffs[1]), 64) + int_to_hex(int(0), 32),
        "Name": "bls_g2mul_(0*g2=inf)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G2MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(int(P2[0].coeffs[0]), 64) + int_to_hex(int(P2[0].coeffs[1]), 64) + int_to_hex(int(P2[1].coeffs[0]), 64) + int_to_hex(int(P2[1].coeffs[1]), 64) + int_to_hex(int(0), 32),
        "Name": "bls_g2mul_(0*p2=inf)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G2MUL_GAS,
        "NoBenchmark": False
        },
        {
        "Input": int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(int(17), 32),
        "Name": "bls_g2mul_(x*inf=inf)",
        "Expected": int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64) + int_to_hex(0, 64),
        "Gas": BLS12_G2MUL_GAS,
        "NoBenchmark": False
        }
    ]


# Credit
# test vectors taken from
# https://github.com/cfrg/draft-irtf-cfrg-hash-to-curve/blob/main/poc/vectors/BLS12381G1_XMD%3ASHA-256_SSWU_NU_.json
def case05_map_fp_to_G1():

    yield 'map_fp_to_G1_bls', [
        {
        "Input": HASH_G1_MESSAGES[0][1],
        "Name": "bls_g1map_" + encode_hex(HASH_G1_MESSAGES[0][0])[0:16],
        "Expected": HASH_G1_MESSAGES[0][2] + HASH_G1_MESSAGES[0][3],
        "Gas": BLS12_MAP_FP_TO_G1_GAS,
        "NoBenchmark": False
        },
        {
        "Input": HASH_G1_MESSAGES[1][1],
        "Name": "bls_g1map_" + encode_hex(HASH_G1_MESSAGES[1][0])[0:16],
        "Expected": HASH_G1_MESSAGES[1][2] + HASH_G1_MESSAGES[1][3],
        "Gas": BLS12_MAP_FP_TO_G1_GAS,
        "NoBenchmark": False
        },
        {
        "Input": HASH_G1_MESSAGES[2][1],
        "Name": "bls_g1map_" + encode_hex(HASH_G1_MESSAGES[2][0])[0:16],
        "Expected": HASH_G1_MESSAGES[2][2] + HASH_G1_MESSAGES[2][3],
        "Gas": BLS12_MAP_FP_TO_G1_GAS,
        "NoBenchmark": False
        },
        {
        "Input": HASH_G1_MESSAGES[3][1],
        "Name": "bls_g1map_" + encode_hex(HASH_G1_MESSAGES[3][0])[0:16],
        "Expected": HASH_G1_MESSAGES[3][2] + HASH_G1_MESSAGES[3][3],
        "Gas": BLS12_MAP_FP_TO_G1_GAS,
        "NoBenchmark": False
        },
        {
        "Input": HASH_G1_MESSAGES[4][1],
        "Name": "bls_g1map_" + encode_hex(HASH_G1_MESSAGES[4][0])[0:16],
        "Expected": HASH_G1_MESSAGES[4][2] + HASH_G1_MESSAGES[4][3],
        "Gas": BLS12_MAP_FP_TO_G1_GAS,
        "NoBenchmark": False
        }
    ]


# Credit
# test vectors taken from
# https://github.com/cfrg/draft-irtf-cfrg-hash-to-curve/blob/main/poc/vectors/BLS12381G2_XMD%3ASHA-256_SSWU_NU_.json
def case06_map_fp2_to_G2():
    yield 'map_fp2_to_G2_bls', [
        {
        "Input": HASH_G2_MESSAGES[0][1] + HASH_G2_MESSAGES[0][2],
        "Name": "bls_g2map_" + encode_hex(HASH_G2_MESSAGES[0][0])[0:16],
        "Expected": HASH_G2_MESSAGES[0][3] + HASH_G2_MESSAGES[0][4] + HASH_G2_MESSAGES[0][3] + HASH_G2_MESSAGES[0][4],
        "Gas": BLS12_MAP_FP2_TO_G2_GAS,
        "NoBenchmark": False
        }
    ]


test_kinds: Dict[str, Generator[Tuple[str, Any], None, None]] = {
    'add_G1': case01_add_G1,
    'add_G2': case02_add_G2,
    'mul_G1': case03_mul_G1,
    'mul_G2': case04_mul_G2,
    'map_fp_to_G1': case05_map_fp_to_G1,
    'map_fp2_to_G2': case06_map_fp2_to_G2
}


def validate_output_dir(path_str):
    path = Path(path_str)

    if not path.exists():
        raise argparse.ArgumentTypeError("Output directory must exist")

    if not path.is_dir():
        raise argparse.ArgumentTypeError("Output path must lead to a directory")

    return path


def validate_encoding(encoding_str: str) -> Tuple[str, Callable[[Path, Any], None]]:
    encoding_str = encoding_str.lower()

    if encoding_str == "yaml" or encoding_str == "yml":
        yaml = YAML(pure=True)
        yaml.default_flow_style = None

        def _represent_none(self, _):
            return self.represent_scalar('tag:yaml.org,2002:null', 'null')

        yaml.representer.add_representer(type(None), _represent_none)

        def yaml_dumper(out_path: Path, data: Any) -> None:
            with out_path.open(file_mode) as f:
                yaml.dump(data, f)

        return ".yaml", yaml_dumper

    if encoding_str == "json":
        def json_dumper(out_path: Path, data: Any) -> None:
            with out_path.open(file_mode) as f:
                json.dump(data, f)

        return ".json", json_dumper

    raise argparse.ArgumentTypeError(f"Unrecognized encoding: {encoding_str}, expected 'json' or 'yaml'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="gen-bls",
        description="Generate BLS test vectors",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        required=True,
        type=validate_output_dir,
        help="directory into which the generated test vector files will be dumped"
    )
    parser.add_argument(
        "-e",
        "--encoding",
        dest="encoding",
        required=False,
        default='yaml',
        type=validate_encoding,
        help="encoding for output data"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help="if set re-generate and overwrite test files if they already exist",
    )

    args = parser.parse_args()

    output_dir = args.output_dir
    print(f"Generating tests into {output_dir}")

    if not args.force:
        file_mode = "x"
    else:
        file_mode = "w"

    extension, output_dumper = args.encoding

    for test_kind_name, test_kind_gen in test_kinds.items():
        test_dir = Path(output_dir) / Path('bls') / Path(test_kind_name)
        test_dir.mkdir(parents=True, exist_ok=True)

        for (case_name, case_content) in test_kind_gen():
            case_filepath = test_dir / Path(case_name + extension)

            if case_filepath.exists():
                if not args.force:
                    print(f'Skipping already existing test: {case_filepath}')
                    continue
                else:
                    print(
                        f'Warning, test case {case_filepath} already exists, test will be overwritten with new version')

            print(f'Generating test: {case_filepath}')

            # Lazy-evaluate test cases where necessary
            if callable(case_content):
                case_content = case_content()

            output_dumper(case_filepath, case_content)
