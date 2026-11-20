import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from blockchain_lab.a3 import address_from_public
from blockchain_lab.a4 import UTXOLedger, LedgerError, sign_transaction

@pytest.fixture
def funded():
    key=Ed25519PrivateKey.generate()
    address=address_from_public(key.public_key())
    ledger=UTXOLedger()
    txid=ledger.add_genesis(address,100)
    return key,address,ledger,txid

def test_valid_spend(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":90}])
    assert l.apply(tx)["fee"]==10

def test_fee_calculation(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":77}])
    assert l.apply(tx)["fee"]==23

def test_input_missing(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":"f"*64,"index":0}],[{"owner":a,"value":1}])
    with pytest.raises(LedgerError,match="missing"):l.apply(tx)

def test_duplicate_input(funded):
    k,a,l,t=funded
    i={"txid":t,"index":0}
    tx=sign_transaction(k,[i,i],[{"owner":a,"value":1}])
    with pytest.raises(LedgerError,match="duplicate"):l.apply(tx)

def test_double_spend(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":90}])
    l.apply(tx)
    with pytest.raises(LedgerError):l.apply(tx)

def test_overspend_rejected(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":101}])
    with pytest.raises(LedgerError,match="less"):l.apply(tx)

def test_zero_output_rejected(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":0}])
    with pytest.raises(LedgerError,match="invalid output"):l.apply(tx)

def test_negative_output_rejected(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":-1}])
    with pytest.raises(LedgerError):l.apply(tx)

def test_bad_signature_rejected(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":90}])
    tx["signature"]="00"*64
    with pytest.raises(LedgerError,match="bad signature"):l.apply(tx)

def test_altered_outputs_signature_rejected(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":90}])
    tx["outputs"][0]["value"]=89
    with pytest.raises(LedgerError,match="bad signature"):l.apply(tx)

def test_wrong_signer_rejected(funded):
    k,a,l,t=funded
    other=Ed25519PrivateKey.generate(); b=address_from_public(other.public_key())
    tx=sign_transaction(other,[{"txid":t,"index":0}],[{"owner":b,"value":90}])
    with pytest.raises(LedgerError,match="wrong signer"):l.apply(tx)

def test_atomic_state_after_bad_signature(funded):
    k,a,l,t=funded; before=l.snapshot()
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":90}]); tx["signature"]="00"
    with pytest.raises(LedgerError):l.apply(tx)
    assert l.snapshot()==before

def test_atomic_state_after_overspend(funded):
    k,a,l,t=funded; before=l.snapshot()
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":110}])
    with pytest.raises(LedgerError):l.apply(tx)
    assert l.snapshot()==before

def test_multiple_outputs(funded):
    k,a,l,t=funded
    other=Ed25519PrivateKey.generate(); b=address_from_public(other.public_key())
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":a,"value":40},{"owner":b,"value":50}])
    assert l.apply(tx)["fee"]==10

def test_empty_inputs_rejected(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[],[{"owner":a,"value":1}])
    with pytest.raises(LedgerError):l.apply(tx)

def test_empty_outputs_rejected(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[])
    with pytest.raises(LedgerError):l.apply(tx)

def test_bad_address_output_rejected(funded):
    k,a,l,t=funded
    tx=sign_transaction(k,[{"txid":t,"index":0}],[{"owner":"bad","value":1}])
    with pytest.raises(LedgerError):l.apply(tx)

def test_snapshot_roundtrip(funded,tmp_path):
    k,a,l,t=funded; path=tmp_path/"state.json"; l.save(path)
    copy=UTXOLedger(); copy.load(path); assert copy.snapshot()==l.snapshot()

def test_largest_first_selection(funded):
    k,a,l,t=funded
    l.add_genesis(a,40)
    selected,total=l.select_coins(a,50)
    assert total>=50 and selected[0][0]>=selected[-1][0]

def test_insufficient_coin_selection(funded):
    k,a,l,t=funded
    with pytest.raises(LedgerError,match="insufficient"):l.select_coins(a,101)
