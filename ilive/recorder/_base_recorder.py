# coding=utf-8
import requests
import os
import time
import re
from .flv_checker import Flv

recorders = {}


def recorder(liver):
    assert liver != None
    def clazz(cls):
        recorders[liver] = cls
        cls.liver = liver
        return cls   
    return clazz 

class BaseRecorder:

    def __init__(self, short_id, cookies = None, \
                 save_folder = '../download', \
                 flv_save_folder = None, \
                 delete_origin_file = False, check_flv = True,\
                 file_name_format = "{name}-{shortId} 的{liver}直播{startTime}-{endTime}",\
                 time_format = "%Y%m%d_%H-%M",\
                 debug = False):
        self.short_id = str(short_id)
        self.cookies = cookies
        self.delete_origin_file = delete_origin_file
        self.check_flv = check_flv
        
        self.save_folder = save_folder.rstrip('\\').rstrip('/')
        self.flv_save_folder = flv_save_folder
        self.file_name_format = file_name_format
        self.time_format = time_format
        self.debug = debug
        
        
        
        self.downloaded = 0
        self.downloadFlag = True
    
#     def getRoomInfo(self):
#         roomInfo = {}
#         roomInfo['short_id'] = self.short_id
#         roomInfo['room_id'] = searchObj.group(1)
#         roomInfo['live_status'] = searchObj.group(1)
#         roomInfo['room_title'] = searchObj.group(1)
#         roomInfo['room_description'] = searchObj.group(1)
#         roomInfo['room_owner_id'] = searchObj.group(1)
#         roomInfo['room_owner_name'] = searchObj.group(1)
#         if roomInfo['live_status'] == '1':
#             roomInfo['live_rates'] = quality
#         return roomInfo
        
#     def getLiveUrl(self, qn):
#         if not hasattr(self, 'roomInfo'):
#             self.getRoomInfo()
#         if self.roomInfo['live_status'] != '1':
#             print('当前没有在直播')
#             return None
#         self.live_url = ""
#         self.live_qn = ""
#         return self.live_url
    
    def startRecord(self, path = None, qn = 0, headers = None):
        try:
            if not hasattr(self, 'live_url'):
                self.getLiveUrl(qn)
            if hasattr(self, 'download_headers'):
                headers = self.download_headers
                
            if path == None:
                # 如果没有指定path，根据自定义文件名来生成
                roomInfo = self.roomInfo
                filename = self.file_name_format.replace("{name}", roomInfo['room_owner_name'])
                filename = filename.replace("{shortId}", roomInfo['short_id'])
                filename = filename.replace("{roomId}", roomInfo['room_id'])
                filename = filename.replace("{liver}", self.liver)
                filename = filename.replace("{seq}", '0')
                current_time = time.strftime(self.time_format, time.localtime())
                filename = filename.replace("{startTime}", current_time)
                filename = re.sub(r"[\/\\\:\?\"\<\>\|\t']", '_', filename)
                
                if not os.path.exists(self.save_folder):
                    os.makedirs(self.save_folder)
                
                path = os.path.abspath('{}/{}.flv'.format(self.save_folder, filename))
            
            first_chunk = True
            retry_count = 0
            max_retries = 5
            
            while self.downloadFlag:
                if first_chunk:
                    mode = "wb"
                    first_chunk = False
                else:
                    mode = "ab"
                    print("检测到流断开，正在重新获取直播地址...")
                    time.sleep(3)
                    live_url = self.getLiveUrl(qn)
                    
                    if live_url is None:
                        if retry_count >= max_retries:
                            print("主播已下播，停止录制")
                            break
                        retry_count += 1
                        print("获取直播地址失败，10秒后重试(%d/%d)..." % (retry_count, max_retries))
                        time.sleep(10)
                        continue
                
                if self.debug:
                    print("[debug] 下载URL: %s" % self.live_url)
                chunk_count = 0
                with open(path, mode) as file:
                    response = requests.get(self.live_url, stream=True, headers=headers, timeout=120)
                    for data in response.iter_content(chunk_size=1024*1024):
                        if not self.downloadFlag:
                            break
                        if data:
                            file.write(data)
                            self.downloaded += len(data)
                            chunk_count += 1
                    response.close()
                
                if not self.downloadFlag:
                    break
                
                if chunk_count == 0:
                    if retry_count >= max_retries:
                        print("主播已下播，停止录制")
                        break
                    retry_count += 1
                    print("未获取到直播数据，10秒后重试(%d/%d)..." % (retry_count, max_retries))
                    time.sleep(10)
                    continue
                
                retry_count = 0
            
            if '{endTime}' in path:
                current_time = time.strftime(self.time_format, time.localtime())
                filename = filename.replace("{endTime}", current_time)
                filename = re.sub(r"[\/\\\:\*\?\"\<\>\|\s']", '_', filename)
                new_path = os.path.abspath('{}/{}.flv'.format(self.save_folder, filename))
                os.rename(path, new_path)
                path = new_path
            
            if self.downloaded > 0 and self.check_flv:
                print("正在校准时间戳")
                flv = Flv(path, self.flv_save_folder, self.debug)
                flv.check()
                if self.delete_origin_file:
                    os.remove(path)
            
            self.downloadFlag = False
            
        except Exception as e:
            print(e)
            self.downloadFlag = False
            raise e
            
    def stopRecord(self):
        self.downloadFlag = False

