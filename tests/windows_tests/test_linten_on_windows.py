from typing import Final

import linten

MOCK_REPLY: Final = "windows runtime reply"


def test_using_linten_on_windows() -> None:
    response: Final = linten.completion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "windows smoke"}],
        mock_response=MOCK_REPLY,
    )
    assert response.choices[0].message.content == MOCK_REPLY
    assert response.choices[0].message.role == "assistant"
    assert response.choices[0].finish_reason == "stop"
    assert response.model == "gpt-4o"
