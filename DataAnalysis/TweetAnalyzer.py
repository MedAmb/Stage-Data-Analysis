from Analyzer import Analyzer
import os
import json

input_folder_path = input_file_path = os.path.join(os.path.dirname(__file__), '..' , 'DataCollection', 'tweets')
batch_meta_data_path = os.path.join(os.path.dirname(__file__), 'analysis_result', 'batches_meta_data.json')
batches_path = os.path.join(os.path.dirname(__file__), 'batch_files')

files=os.listdir(input_folder_path)
files.sort()

batches = os.listdir(batches_path)
batches.sort()

def trigger_batch_analysis():
    analyzer=Analyzer("will-be presented with a tweet and asked to determine the stance of the user regarding the palestinian-israeli conflict."
              "Respond with one of the following:"
              "1 for 'support' if the user show explicit support for the palestinian side or implicit by talking about humenitarian support-for palestinians or hamas."
              "2 for 'against' (supporting Israel) if the user show explicit support for the Israeli side or implicit by talking about humanitarian support for Israel."
              "3. for neutral (no clear side taken) if the user is not taking a clear side or is talking about the conflict in a neutral-way."
              "4- for not relevant (doesn't discuss the conflict) if the user is not discussing the conflict at all."
              "5 for *unknown' - (unable to determine)."
              "Answer only with the corresponding code-word.")
    batch_meta_data = json.load(open(batch_meta_data_path, 'r'))

    for file in files:
        if file in batch_meta_data and (batch_meta_data[file]['status'] == 'completed' or batch_meta_data[file]['status'] == 'in_progress'):
                continue
        else:
            input_file_path = os.path.join(input_folder_path, file)
            with open(input_file_path)  as f:
                print('processing:', file)
                data=json.load(f)
                file_name=file.split('.')[0]
                path = analyzer.create_batch_file(file_name, data['data'])
                status='not_started'
                batch_id=''
                try:
                    result=analyzer.trigger_batch_analysis(path)
                    status='in_progress'
                    batch_id=result
                except:
                    status='failed'
                    print(f"Failed to trigger batch processing for file {file}")
                batch_meta_data[f"{file}"] = {"status": status, "batch_id":batch_id}


    result_path = os.path.join(os.path.dirname(__file__), 'analysis_result', 'batches_meta_data.json')

    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(batch_meta_data, f, ensure_ascii=False, indent=2)

def get_batch_analysis_results():
    meta_data = json.load(open(batch_meta_data_path, 'r'))
    for file in files:
        batch_id = meta_data[file]['batch_id']

        for batch in batches:
            if batch.split('_output.')[0] == batch_id:
                print('found batch for file:', file)


get_batch_analysis_results()