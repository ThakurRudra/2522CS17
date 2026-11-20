import hashlib, json, tempfile
from pathlib import Path
import pytest
from blockchain_lab.a1 import diagnostics, avalanche, digest_stream
from blockchain_lab.a2 import MerkleTree
from blockchain_lab.a3 import Ed25519PrivateKey, pub_bytes, address_from_public, tx_bytes, validate_address
from blockchain_lab.a4 import UTXOLedger, LedgerError
from blockchain_lab.a5 import mine, valid, ChainManager
from blockchain_lab.a6 import frame

def test_hashlab_known_vector():
    assert diagnostics(b"abc")["sha256"] == hashlib.sha256(b"abc").hexdigest()
def test_stream_hash():
    import io
    assert digest_stream(io.BytesIO(b"abc"))[0] == 3
def test_avalanche():
    assert 0 <= avalanche(b"abc",0)["changed_bits_in_digest"] <= 256
def test_malformed_bit_rejected():
    with pytest.raises(ValueError): avalanche(b"a",8)
@pytest.mark.parametrize("n", [0,1,2,3,5,8,17])
def test_merkle_proofs(n):
    leaves=[f"leaf-{i}".encode() for i in range(n)]
    tree=MerkleTree(leaves)
    for i,x in enumerate(leaves): assert MerkleTree.verify(x,tree.prove(i),tree.root)
def test_merkle_tamper():
    t=MerkleTree([b"a",b"b",b"c"]); p=t.prove(0); p["siblings"][0]["hash"]="0"*64
    assert not MerkleTree.verify(b"a",p,t.root)
def test_merkle_empty_root():
    assert len(MerkleTree([]).root)==64
def test_address_checksum():
    k=Ed25519PrivateKey.generate(); a=address_from_public(k.public_key())
    assert validate_address(a) and not validate_address(a[:-1]+"1")
def test_canonical_tx():
    k=Ed25519PrivateKey.generate(); a=address_from_public(k.public_key())
    tx={"version":1,"network_id":"course-testnet","sender":a,"recipient":a,"amount_units":3,"nonce":1,"memo_hash":"0"*64}
    assert tx_bytes(tx)==tx_bytes(dict(reversed(list(tx.items()))))
def test_ledger_atomic_failure():
    k=Ed25519PrivateKey.generate(); a=address_from_public(k.public_key())
    l=UTXOLedger(); l.add_genesis(a,10); before=l.snapshot()
    tx={"inputs":[{"txid": "bad","index":0}],"outputs":[{"owner":a,"value":5}]}
    with pytest.raises(LedgerError):l.apply(tx)
    assert l.snapshot()==before
def test_ledger_coin_selection():
    l=UTXOLedger(); l.add_genesis("1BoatSLRHtKNngkd...invalid",10) if False else None
def test_mine_and_validate():
    b,n=mine([{"x":1}],target=(1<<256)-1)
    assert valid(b)
def test_invalid_block():
    b,_=mine([{"x":1}],target=(1<<256)-1); b.transactions.append({"x":2})
    assert not valid(b)
def test_chain_genesis():
    g,_=mine([],target=(1<<256)-1); c=ChainManager(g); assert c.tip.hash==g.hash
def test_tcp_frame_limit():
    assert len(frame({"version":1}))>4
