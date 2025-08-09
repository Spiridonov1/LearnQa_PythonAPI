class TestExample:
    def test_phrase_length(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, "The phrase must be shorter than 15 characters"