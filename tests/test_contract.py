def test_contract_source_present():
    from pathlib import Path
    source=Path('contracts/checkpoint_graph.py').read_text()
    assert 'class ProvenanceOrbit' in source
    assert 'def attest' in source
    assert 'run_nondet_unsafe' in source
