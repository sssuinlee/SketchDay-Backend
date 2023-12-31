# ml 서버로 request 전송하기
# https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request
import requests
import re
import json

# 사용자가 일기 create할 때 호출하여 ml 서버로 request 전송, 응답으로 prompt 받음
def send_summary_req(full_diary, diary_id):
    payload = {'full_diary' : full_diary, 'diary_id' : diary_id}
    res = requests.post('http://localhost:8000/ml/summaryDiary/', 
                        data=json.dumps(payload),
                         headers = {'Content-type': 'application/json'})
    prompt = res.json()['prompt']
    return prompt, res.status_code # prompt


# 사용자가 일기 modify할 때 호출하여 ml 서버로 request 전송 
# -> url 응답 받고 반환하여 DB에 저장
# -> 프론트엔드한테 이미지 url 전송
def send_img_create_req(prompt, diary_id):
    payload = {'prompt' : prompt, 'diary_id' : diary_id}
    res = requests.post('http://localhost:8000/ml/generateImage/create', 
                        data = json.dumps(payload), 
                        headers = {'Content-type': 'application/json'})
    raw_url = res.json()['url']
    url = extract_url(raw_url)
    return url

  
def extract_url(input_string):
    pattern = r'\[\'(.*?)\''
    bracket_strings = re.findall(pattern, input_string)
    url = bracket_strings[0]
    return url


#######################################################################
def send_summary_req_img(url_list, diary_id):
    print(url_list)
    payload = {"req_urls" : url_list, 'diary_id' : diary_id}
    res = requests.post('http://localhost:8000/ml/summaryDialogue/', 
                        data=json.dumps(payload), 
                        headers = {'Content-type': 'application/json'})
    print('res.statuscode :', res.status_code)
    print('res.json()', res.json()['prompt'])
    summary_dialogue = res.json()['full_dialog'] # 요약된 일기
    prompt = res.json()['prompt'] # 프롬프트
    return prompt, summary_dialogue 
