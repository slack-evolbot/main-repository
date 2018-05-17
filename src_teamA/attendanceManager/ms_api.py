# coding: utf-8
import requests
import json
import glob
import time
import os

MS_API_BASE_URL = "https://eastasia.api.cognitive.microsoft.com/face/v1.0/" #APIのURL(東アジア用)
MS_API_GROUP_URL = MS_API_BASE_URL + "persongroups/"
MS_API_DETECT_URL = MS_API_BASE_URL + "detect"
MS_API_IDENTIFY_URL = MS_API_BASE_URL + "identify"
KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" #MS Face APIの値を設定

class Candidate:
    personId = None
    confidence = None

class MsApi():
    #グループ作成
    def create_group(self, group_name, group_id):
        print("グループ作成開始")
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': KEY
        }
        data = { 
            'name': group_name,
            'userData': 'test group id'
        }
        url = MS_API_GROUP_URL + group_id
        res = requests.put(url , headers=headers, data=json.dumps(data))
        print("グループ作成完了")

    #人物作成
    def create_person(self, person_name, group_id):
        print("Person作成開始")
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': KEY
        }
            
        data = { 
            'name': person_name,
            'userData': 'test person name'
        }

        url = MS_API_GROUP_URL + group_id + "/persons"
        res = requests.post(url , headers=headers, data=json.dumps(data))
        print(res.text)
        print("Person作成完了")
        return res.json()
    
    #人物削除
    def delete_person(self, person_id, group_id):
        print("Person削除開始")
        headers = {
            'Ocp-Apim-Subscription-Key': KEY
        }
            
        data = { 
            'personGroupId': group_id,
            'personId': person_id
        }

        url = MS_API_GROUP_URL + group_id + "/persons/" + person_id
        res = requests.delete(url , headers=headers, data=json.dumps(data))
        print(res.text)
        print("Person削除完了")

    #人物写真登録
    def add_person_photo(self, group_id, person_id):
        print("写真登録開始")
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': KEY
        }
        
        train_img_list = glob.glob("./training_img/*")
        
        print(str(len(train_img_list)) + "枚の写真を登録します（登録後の写真データは削除します）")
        for img in train_img_list:
            data = open(img, 'rb').read()
            url = MS_API_GROUP_URL + group_id + "/persons/" + person_id + "/persistedFaces"
            try:
                res = requests.post(url , headers=headers, data=data)
            except:
                time.sleep(5)
                res = requests.post(url , headers=headers, data=data)
            print(res.text)
            if("persistedFaceId" in res.text):
                os.remove(img) #登録完了後のデータは削除
            time.sleep(3) #API制限(20回/1分)のため3秒間隔で実行
        print("写真登録完了")

    #トレーニング開始
    def train(self, group_id):
        print("学習開始")
        headers = {
            'Ocp-Apim-Subscription-Key': KEY
        }
        url = MS_API_GROUP_URL + group_id + "/train"
        res = requests.post(url , headers=headers)
        print(res.text)
        print("学習終了")

    #トレーニング状況確認
    def get_training_status(self, group_id):
        headers = {
            'Ocp-Apim-Subscription-Key': KEY
        }
        url = MS_API_GROUP_URL + group_id + "/training"
        res = requests.get(url , headers=headers)
        print(res.text)

    #人物検出
    def detect_person(self, img_path):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': KEY,
        }
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,facialHair,glasses,emotion,smile'
        }
        res = requests.post(MS_API_DETECT_URL ,headers = headers,params = params,data = open(img_path,'rb'))
        return res.json()

    #人物特定
    def identify_person(self, face_ids, group_id):
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': KEY
        }
        data = { 
            'faceIds': face_ids,
            'personGroupId': group_id,
            'maxNumOfCandidatesReturned': 10,
            'confidenceThreshold': 0.5
        }
        res = requests.post(MS_API_IDENTIFY_URL , headers=headers, data=json.dumps(data))
        return res.json()

    #指定人物の確信度を取得
    def check_person(self, identify_results, person_id):
        max_conficence = 0
        for identify in identify_results:
            for candidate in identify["candidates"]:
                if(candidate["personId"] == person_id):
                    if(candidate["confidence"] > max_conficence):
                        max_conficence = candidate["confidence"]
        return max_conficence
    
    #最も似ている候補を取得
    def get_most_candidate(self, identify_results):
        candidate = Candidate()
        if len(identify_results[0]["candidates"]) == 0:
            return None
        candidate.personId = identify_results[0]["candidates"][0]["personId"]
        candidate.confidence = identify_results[0]["candidates"][0]["confidence"]
        return candidate
    
