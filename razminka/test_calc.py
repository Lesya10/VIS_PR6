import pytest
from calc import summa, skidka, srednee

# --- P1 ---
def test_summa_polozhitelnye():
    assert summa(2, 3) == 5

def test_summa_s_nulem():
    assert summa(0, 7) == 7

# --- P2 ---
def test_skidka_10_procentov():
    # 1000 руб, скидка 10% -> итог 900.00
    assert skidka(1000, 10) == 900.00

# --- P3 ---
def test_skidka_slishkom_bolshaya():
    with pytest.raises(ValueError):
        skidka(1000, 95)

def test_srednee_pustoy_spisok():
    with pytest.raises(ValueError):
        srednee([])

# --- P4 ---
@pytest.mark.parametrize("data, expected", [
    ([5], 5),
    ([2, 4], 3),
    ([1, 2, 3, 4], 2.5),
    ([-2, 2], 0)
])
def test_srednee_parametrizaciya(data, expected):
    assert srednee(data) == expected