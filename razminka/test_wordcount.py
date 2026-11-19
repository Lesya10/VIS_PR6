import pytest
from wordcount import chastota

@pytest.fixture
def fayl_s_tekstom(tmp_path):
    put = tmp_path / "text.txt"
    put.write_text("Мама мыла раму. Рама, мама, рама!", encoding="utf-8")
    return put

def test_chastota_slov(fayl_s_tekstom):
    res = chastota(fayl_s_tekstom)
    assert res["мама"] == 2
    assert res["рама"] == 2

def test_net_znakov_prepinaniya(fayl_s_tekstom):
    res = chastota(fayl_s_tekstom)
    assert "рама," not in res
    assert "раму." not in res

def test_chetyre_raznyh_slova(fayl_s_tekstom):
    res = chastota(fayl_s_tekstom)
    assert len(res) == 4