# ml 서버로 request 전송하기
# https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request
import requests

# 사용자가 일기 create할 때 호출하여 ml 서버로 request 전송, 응답으로 prompt 받음
def send_summary_req(full_diary):
    res = requests.post('http://localhost:8000/ml/summaryDiary/', data = {'full_diary' : full_diary})
    print('res :', res)
    print('res.content', res.content)
    print('res.statuscode :', res.status_code)
    print('res.json :', res.json)
    print('res.text :', res.text)
    prompt = res.content
    return prompt # prompt


# 사용자가 일기 modify할 때 호출하여 ml 서버로 request 전송 
# -> url 응답 받고 반환하여 DB에 저장
# -> 프론트엔드한테 이미지 url 전송
def send_img_create_req(prompt):
    res = requests.post('http://localhost:8000/ml/generateImage/', data = {'prompt' : prompt})
    url = res.content
    return url