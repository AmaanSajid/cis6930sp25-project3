from src.classifier import label


def test_human(monkeypatch):
    monkeypatch.setattr("src.classifier.EN_WORDS",
                        {"hello", "world", "from", "earth"})
    assert label("hello world from earth") == "human"


def test_alien(monkeypatch):
    monkeypatch.setattr("src.classifier.EN_WORDS", {"hello"})
    assert label("zblarg wugga") == "alien"
