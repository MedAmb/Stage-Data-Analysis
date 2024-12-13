# Importer les libraries nécessaires
from openai import OpenAI
import os
import json
import time

responses=['support','oppose','neutral','not relevant','unknown']

# Creer Une Analyzeur qui GPT 3 pourra utiliser pour analyser les tweets
class Analyzer:

    # __init__ prends en parametre le prompt initial qui va données à GPT3 le contexte de la conversation
    def __init__(self, prompt:str):
        self.prompt = prompt
        self.openai_api_key = ''
        self.client = OpenAI(api_key=self.openai_api_key)

    def create_batch_file(self, file_name:str, tweets):
        #path is this file's directory/batch_files/file_name.jsonl
        tweet_ids = set()
        path = os.path.join(os.path.dirname(__file__), 'batch_files', file_name + '.jsonl')
        with open(path, 'w') as f:
            i = 1
            for tweet in tweets:
                tweet_id = tweet["Tweet ID"]
                if tweet_id in tweet_ids:
                    print(f"Detected duplicate tweet in set with id {tweet_id}. Discarding...")
                    continue  # Skip duplicate tweet
                tweet_ids.add(tweet_id)
                sanitize_tweet_content = tweet['Content'].replace("'", "").replace('"', "").replace('\n', "")
                tweet_prompt=(
            f"Analyze the following tweet by @{tweet['Handle']} ({tweet['Name']}):"
            f"'{sanitize_tweet_content}'")

                line = '{"custom_id": "' + tweet["Tweet ID"] + '", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": "' + self.prompt + '"}, {"role": "user", "content": "Analyze the following tweet: ' + tweet_prompt + '"}], "max_tokens": 10, "temperature": 0}}\n'
                if self.validate_jsonl_line(line, i, tweet_id):
                    f.write(line)
                i = i + 1


        if self.validate_jsonl_file(path):
            return path
        else:
            raise ValueError("The created batch file is not a valid JSONL file.")

    def validate_jsonl_line(self, line, line_number, tweet_id):
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Line {line_number} failed validation at {e.colno}. Tweet id: {tweet_id}")
            return False
        return True

    def validate_jsonl_file(self, file_path):
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                try:
                    json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"Line {line_number} failed validation: {line.strip()}")
                    print(f"Reason: {e}")
                    return False
        return True

    def trigger_batch_analysis(self, batch_file_path):

        batch_input_file = self.client.files.create(
            file=open(batch_file_path, "rb"),
            purpose="batch"
        )

        batch_input_file_id = batch_input_file.id

        batch_object = self.client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
            metadata={
            "description": "Internship"
            }
        )

        batch_id = batch_object.id

        #wait for the batch to complete
        batch = None
        while True:
            batch = self.client.batches.retrieve(batch_id)
            if batch.status == "in_progress":
                break
            elif batch.status == "failed" or batch.status == "cancelled" or batch.status == "expired":
                print(f"Batch failed or was cancelled: {batch.status}")
                print(f"Errors:\n-{batch.errors}")
                raise Exception(f"Batch failed or was cancelled: {batch.status}")
            else:
                print(f"Batch status: {batch.status}")
                print(f"Processed {batch.request_counts.completed} out of {batch.request_counts.total}")
                time.sleep(10)

        return batch.id

    def get_batch_analysis_results(self, batch_id):
        output_map = {}
        file_response = self.client.files.content(batch_id)
        for line in file_response.iter_lines():
                print(f"Line: {line}")
                response = json.loads(line)
                if response["response"]["status"] == 200:
                    result = int(response["response"]["body"]["choices"][0]["message"]["content"])
                    result_str = ''
                    if result >= 1 and result <= 5:
                        result_str = responses[result - 1]
                    else:
                        result_str = 'unknown'
                dict_entry = {response["custom_id"]: result_str}
                print(f"OpenAI response:{dict_entry}")
        output_map.update(dict_entry)
        return output_map
