# BLS 12-381 tests

This repository provides a test-suite for the [EIP-2537: Precompile for BLS12-381 curve operations](https://eips.ethereum.org/EIPS/eip-2537)

The test suite is generated with python, and can be downloaded via the releases.
We suggest the following for integration into your testing pipeline:

```shell
mkdir -p destination/bls-tests
TESTS_VERSION=v0.1.0
wget https://github.com/ethereum/bls12-381-tests/releases/download/${TESTS_VERSION}/bls_tests_json.tar.gz -O - | tar -xz -C destination/bls-tests
# bls_tests_yaml.tar.gz is also available: same tests, formatted as YAML
```

## Resources

- [Finite Field Arithmetic](http://www.springeronline.com/sgw/cda/pageitems/document/cda_downloaddocument/0,11996,0-0-45-110359-0,00.pdf)
- Chapter 2 of [Elliptic Curve Cryptography](http://cacr.uwaterloo.ca/ecc/). Darrel Hankerson, Alfred Menezes, and Scott Vanstone

## Test format

The BLS test suite runner has the following handlers:

- [`BLS12_G1ADD`](formats/add_G1_bls.md)
- [`BLS12_G2ADD`](formats/add_G2_bls.md)
- [`BLS12_G1MUL`](formats/mul_G1_bls.md)
- [`BLS12_G2MUL`](formats/mul_G2_bls.md)
- [`BLS12_MAP_FP_TO_G1`](formats/map_fp_to_G1_bls.md)
- [`BLS12_MAP_FP2_TO_G2`](formats/map_fp2_to_G2_bls.md)

## Test generation

```shell
# Create a virtual environment
python -m venv venv
# Activate the environment
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Create output dir
mkdir out
# Run test generator
python main.py --output-dir=out --encoding=json
```

## License

CC0 1.0 Universal, see [`LICENSE`](./LICENSE) file.
