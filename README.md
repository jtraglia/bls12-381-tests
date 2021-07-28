# BLS Test Generator

The [BLS Signature APIs](../../../specs/phase0/beacon-chain.md#bls-signatures)

Information on the format of the tests can be found in the [BLS test formats documentation](../../formats/bls/README.md).

## Resources

- [IETF BLS Signature Scheme](https://datatracker.ietf.org/doc/draft-irtf-cfrg-bls-signature/)
- [Finite Field Arithmetic](http://www.springeronline.com/sgw/cda/pageitems/document/cda_downloaddocument/0,11996,0-0-45-110359-0,00.pdf)
- Chapter 2 of [Elliptic Curve Cryptography](http://cacr.uwaterloo.ca/ecc/). Darrel Hankerson, Alfred Menezes, and Scott Vanstone

## Test format

The BLS test suite runner has the following handlers:

- [`aggregate_verify`](./aggregate_verify.md)
- [`aggregate`](./aggregate.md)
- [`fast_aggregate_verify`](./fast_aggregate_verify.md)
- [`sign`](./sign.md)
- [`verify`](./verify.md)

*TODO*: Signature-verification and aggregate-verify test cases are not yet supported.
