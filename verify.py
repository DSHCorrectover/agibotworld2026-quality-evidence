#!/usr/bin/env python3
"""verify.py — third-party verification of the evidence receipt.
Verifies the Ed25519 signature over the canonical evidence.json bytes using the
published pubkey. Exit 0 = authentic and unmodified since signing.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

ev = open(os.path.join(HERE, "evidence", "evidence.json"), "rb").read()
sig = open(os.path.join(HERE, "evidence", "receipt.sig"), "rb").read()
pub = serialization.load_pem_public_key(open(os.path.join(HERE, "evidence", "pubkey.pem"), "rb").read())
try:
    pub.verify(sig, ev)
    d = json.loads(ev)
    print("SIGNATURE VALID")
    print("object:", d["object"]["repo"], "| revision:", d["object"]["revision_sha"])
    print("census:", d["census"]["files"], "files,", d["census"]["directories"], "dirs,", d["census"]["total_tb"], "TB")
    print("parquet crosscheck:", d["census"]["publisher_parquet_crosscheck"])
    for f in d["findings_summary"]:
        print(" finding:", f)
    for h in d["held"]:
        print(" held:", h["dim"])
    sys.exit(0)
except Exception as e:
    print("SIGNATURE INVALID:", e)
    sys.exit(1)
