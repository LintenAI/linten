from dotenv import load_dotenv

load_dotenv()

import linten

from autoevals.llm import *

###################

# linten completion call
question = "which country has the highest population"
response = linten.completion(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": question}],
)
print(response)
# use the auto eval Factuality() evaluator

print("calling evaluator")
evaluator = Factuality()
result = evaluator(
    output=response.choices[0]["message"][
        "content"
    ],  # response from linten.completion()
    expected="India",  # expected output
    input=question,  # question passed to linten.completion
)

print(result)
