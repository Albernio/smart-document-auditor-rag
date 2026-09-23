import pytest

from src.vector_similarity import cosine_similarity


def test_identical_vectors_have_similarity_one() -> None:
    vector = [1.0, 2.0, 3.0]

    similarity = cosine_similarity(vector, vector)

    assert similarity == pytest.approx(1.0)


def test_different_dimensions_raise_value_error() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        cosine_similarity(
            [1.0, 2.0],
            [1.0, 2.0, 3.0],
        )


def test_zero_vector_raises_value_error() -> None:
    with pytest.raises(ValueError, match="zero vectors"):
        cosine_similarity(
            [0.0, 0.0],
            [1.0, 2.0],
        )