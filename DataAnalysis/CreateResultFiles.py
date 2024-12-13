import os
import json
import datetime

responses=['support','oppose','neutral','not relevant','unknown']

input_folder_path = input_file_path = os.path.join(os.path.dirname(__file__), '..' , 'DataCollection', 'tweets')
batch_meta_data_path = os.path.join(os.path.dirname(__file__), 'analysis_result', 'batches_meta_data.json')
batches_path = os.path.join(os.path.dirname(__file__), 'batch_files')

files=os.listdir(input_folder_path)
files.sort()

batches = os.listdir(batches_path)
batches.sort()

def create_result_map(path):
    result_map = {}
    with open(path, 'r') as f:
        for line in f:
            data = json.loads(line)
            result = data["response"]["body"]["choices"][0]["message"]["content"]
            result_str = ''
            if int(result) >= 1 and int(result) <= 5:
                result_str = responses[int(result) - 1]
            else:
                result_str = 'unknown'
            result_map.update({data["custom_id"]: result_str})
    return result_map


def get_batch_analysis_results():
    mylist = []
    meta_data = json.load(open(batch_meta_data_path, 'r'))
    for file in files:
        batch_id = meta_data[file]['batch_id']

        lang = 'EN'

        if 'AR' in file:
            lang = 'AR'

        for batch in batches:
            if batch.split('_output.')[0] == batch_id:
                print('found batch for file:', file)
                result_map = create_result_map(os.path.join(batches_path, batch))
                with open(os.path.join(input_folder_path, file), 'r') as f:
                    data = json.load(f)

                    analysis_result = 'require_manual_review'

                    for tweet in data['data']:
                        if tweet['Tweet ID'] in result_map.keys():
                            analysis_result = result_map[tweet['Tweet ID']]
                        my_dict = {
                            'name': tweet['Name'],
                            'handle': tweet['Handle'],
                            'time': tweet['Timestamp'],
                            'content': tweet['Content'],
                            'likes': tweet['Likes'],
                            'tweet link': tweet['Tweet Link'],
                            'Comments': tweet['Comments'],
                            'Retweets': tweet['Retweets'],
                            'tweet_ID': tweet['Tweet ID'],
                            'Result': analysis_result,
                            'Language': lang,
                            'comment': ''
                        }
                        mylist.append(my_dict)

        def convert_date_time_to_timestamp(date_time):
            # example of format 2024-01-21T23:54:43.000Z
            date_time = date_time.split('T')
            date = date_time[0].split('-')
            time = date_time[1].split(':')
            time[2] = time[2].split('.')[0]
            return datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))


        mylist.sort(key=lambda x: convert_date_time_to_timestamp(x['time']), reverse=True)

    result_path = os.path.join(os.path.dirname(__file__), 'analysis_result', 'results.json')
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(mylist, f, ensure_ascii=False, indent=2)


get_batch_analysis_results()

