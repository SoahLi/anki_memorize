import json
import os

import requests

# url = "http://192.168.1.165:11434/api/generate"
# payload = {
#    "model": "gemma4:e4b",
#    "system": """
#      You are a an assistant that helps parse transcripts to extract any useful information to tranform into flashcards.
#      given a transcript in srt format, extract all keywords, concepts, and important information that can be used to create simple flashcards.
#      For each ___, return a json object with the question format, which should be a simple question that can be answered with a single word or phrase.
#      qfmt: str - the question to be answered
#      afmt: str - a simple answer to the question, followed by a more detailed explanation if necessary.
#      markers: array of array of strings - an array of arrays, where each inner array contains a start and end time in the format "hh:mm:ss,ms" that indicates when the information is mentioned in the transcript.
#      score: int between 1 and 10 - a score indicating the relevance of the flashcard, with 10 being the most relevant and 1 being the least relevant. Prioritize concrete facts and definitions over more abstract concepts.
#     """,
#    "format": "json",
#    "think": True,
#    "prompt": prompt_text,
#    # "prompt": ' Some species of ants can form "living bridges" using their own bodies. When faced with a gap in their path, certain ants (like Eciton burchellii, a type of army ant) link together leg-to-leg to create a bridge that other ants can cross. What’s fascinating is that the bridge isn\'t permanent—it dynamically assembles and disassembles as needed, with individual ants joining or leaving without disrupting the overall structure, all guided by collective sensing and chemical signals.',
#    "stream": False,
# }


url = "https://api.deepseek.com/chat/completions"
with open("prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

API_KEY = "sk-7475c00d24be4652bf71434471a6aa77"
headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
messages = [
    {
        "role": "system",
        "content": system_prompt,
    }
]

examples_dir = "examples"
for example_num in os.listdir(examples_dir):
    example_path = os.path.join(examples_dir, example_num, "prompt")
    prompt_file = os.path.join(example_path, "prompt")
    answer_file = os.path.join(example_path, "answer")
    if os.path.isfile(prompt_file) and os.path.isfile(answer_file):
        with open(prompt_file, "r", encoding="utf-8") as pf:
            prompt_text = pf.read()
        with open(answer_file, "r", encoding="utf-8") as af:
            answer_text = af.read()
        messages.append({"role": "user", "content": prompt_text})
        messages.append({"role": "assistant", "content": answer_text})


examples_dir = "examples"
for example_num in os.listdir(examples_dir):
    example_path = os.path.join(
        examples_dir,
        example_num,
    )
    prompt_file = os.path.join(example_path, "prompt.txt")
    answer_file = os.path.join(example_path, "answer.txt")
    if os.path.isfile(prompt_file) and os.path.isfile(answer_file):
        with open(prompt_file, "r", encoding="utf-8") as pf:
            prompt_text = pf.read()
        with open(answer_file, "r", encoding="utf-8") as af:
            answer_text = af.read()
        messages.append({"role": "user", "content": prompt_text})
        messages.append({"role": "assistant", "content": answer_text})


with open("transcript.txt", "r", encoding="utf-8") as f:
    messages.append(
        {
            "role": "user",
            "content": f.read(),
        }
    )
payload = {
    "model": "deepseek-reasoner",
    "thinking": {"type": "enabled"},
    "messages": messages,
    "response_format": {"type": "json_object"},
    "stream": False,
}


print(json.dumps(payload, indent=4, separators=(",", ": ")))

# response = requests.post(url, json=payload)
response = requests.post(url, headers=headers, json=payload)
# print(response.text)  # Print raw response for debugging

# If response is multiple JSON objects (one per line):
try:
    results = [
        json.loads(line) for line in response.text.strip().split("\n") if line.strip()
    ]
    # Write results to a file with pretty formatting
    with open("output.json", "w") as f:
        json.dump(results, f, indent=4)

    print(results)
    print(results[0]["choices"][0]["message"]["content"])
except Exception as e:
    print("Error parsing JSON:", e)
