import json

data = (
    "{\"messages\":[{\"message\":\"This is the first message\",\"timestamp\":\"2021-06-04 16:40:53\"},"
        "{\"message\":\"And this is a second message\",\"timestamp\":\"2021-06-04 16:41:01\"}]}"
)
parsed_text = json.loads(data)
print(parsed_text['messages'][1]["message"])