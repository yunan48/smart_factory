# 동작 메커님즘
# 컨베이어 동작 + 스톱센서 상승 + 이젝터 후진
# 스톱센서 감지 -> 이미지 처리를 통한 불량 반별(3가지 분류 : LED불량, Moter불량, 양품)
# LED불량 신호(이미지 처리) -> 서보모터(1번) 이동 후 이젝터 전진(PLC) -> 이젝터 전진 센터 &(and) LED불량신호면 -> 1번 창고 적재(Robot)
# Moter불량 신호(이미지 처리) -> 서보모터(2번) 이동 후 이젝터 전진(PLC) -> 이젝터 전진 센터 &(and) Moter불량신호면  -> 2번 창고 적재(Robot)
# 불량 공통 : 적재완료 신호(Robot) -> 다음 검사물품 푸쉬 -> 이하 반복
# 양품 : 컨베이어 동작
# 컨베이어 동작 + 스톱센서 상승 + 이젝터 후진 => PCL에서 동작 

#PLC 연결
# plc.py

from indy_utils import indydcp_client as client

import json
from time import sleep
import threading
import numpy as np

robot_ip = "192.168.3.7"  # Robot (Indy) IP
robot_name = "NRMK-Indy7"  # Robot name (Indy7)
# robot_name = "NRMK-IndyRP2"  # Robot name (IndyRP2)

# Create class object
indy = client.IndyDCPClient(robot_ip, robot_name)

idx_open = 0 #열기
idx_close = 1 #닫기

indy.connect()
print("동작확인")

def motion_done_check():
    while True:
        status = indy.get_robot_status()
        if status['movedone'] ==1:
            print(status['movedone'])
            break
        sleep(0.1)

#캠 촬영 위치 이동
def pick_error():
    indy.task_move_to(pick_error)
    motion_done_check()
    # 추가할 요소 : 이미지 처리 및 신호 받는 코드
    # camsignal 받기
    # print(camsignal)
    
def led_error():
    #safe_connect()
    print("연결완료됨")
    indy.task_move_to(pick_a)
    motion_done_check()
    indy.task_move_to(pick_a) #픽업 aprroach
    motion_done_check()
    indy.set_do(0, True)
    indy.set_do(1, False)
    sleep(2)
    indy.task_move_to(pick_t) #픽업 taget
    motion_done_check()
    indy.set_do(1, True)
    indy.set_do(0, False)
    sleep(2)
    indy.task_move_to(pick_a) #픽업 retract
    motion_done_check()
    sleep(2)
    indy.task_move_to(pick_m) #픽업 retract
    motion_done_check()
    sleep(2)
    indy.task_move_to(pos_1a) #픽업 aprroach_l
    motion_done_check()
    sleep(2)
    indy.task_move_to(pos_1t) #픽업 taget_l
    motion_done_check()
    indy.set_do(0, True)
    indy.set_do(1, False)
    sleep(2)
    indy.task_move_to(pos_1a) #픽업 retract_l
    sleep(2)
    indy.task_move_to(pick_m) #픽업 retract_l

def moter_error():
    safe_connect()
    indy.task_move_to(pick_a) #픽업 aprroach
    motion_done_check()
    indy.set_do(0, True)
    indy.set_do(1, False)
    sleep(1)
    indy.task_move_to(pick_t) #픽업 taget
    motion_done_check()
    indy.set_do(1, True)
    indy.set_do(0, False)
    sleep(2)
    indy.task_move_to(pick_a) #픽업 retract
    motion_done_check()
    sleep(2)
    indy.task_move_to(pick_m) #픽업 retract
    motion_done_check()
    sleep(2)
    indy.task_move_to(pos_2a) #픽업 aprroach_l
    motion_done_check()
    sleep(2)
    indy.task_move_to(pos_2t) #픽업 taget_l
    motion_done_check()
    indy.set_do(0, True)
    indy.set_do(1, False)
    sleep(2)
    indy.task_move_to(pos_2a) #픽업 retract_l
    sleep(2)
    indy.task_move_to(pick_m) #픽업 retract_l

def hole_error():
    safe_connect()
    indy.task_move_to(pick_a) #픽업 aprroach
    motion_done_check()
    indy.set_do(0, True)
    indy.set_do(1, False)
    sleep(2)
    indy.task_move_to(pick_t) #픽업 taget
    motion_done_check()
    indy.set_do(1, True)
    indy.set_do(0, False)
    sleep(2)
    indy.task_move_to(pick_a) #픽업 retract
    motion_done_check()
    sleep(2)
    indy.task_move_to(pick_m) #픽업 retract
    motion_done_check()
    sleep(2)
    indy.task_move_to(pos_3a) #픽업 aprroach_l
    motion_done_check()
    sleep(2)
    indy.task_move_to(pos_3t) #픽업 taget_l
    motion_done_check()
    indy.set_do(0, True)
    indy.set_do(1, False)
    sleep(2)
    indy.task_move_to(pos_3a) #픽업 retract_l
    sleep(2)
    indy.task_move_to(pick_m) #픽업 retract_l

# 위치 
# 불량 픽업 위치
pick_a = [0.3991060454300791, -0.10753734800887241, 0.39779587897360696, 0.12016955198298504, -179.3758212798854, 0.04887285227331112]
pick_t = [0.3992417164574616, -0.10752162317489064, 0.22730376289242868, 0.11538520098637317, -179.4176781066186, 0.05002709032196934]
pick_m = [0.3991060454300791, 0.41421084677940057, 0.39779587897360696, 0.12016955198298504, -179.3758212798854, 0.04887285227331112]

#LED_OFF
pos_1a = [-0.044814834694690144, 0.41421084677940057, 0.39169320913985056, -178.65834723671796, 0.8784068428694837, 179.74794026246545]
pos_1t = [-0.04766562000789014, 0.41936693571364553, 0.23768168939003945, 179.5351213240986, -0.17909398811095578, 179.86238783015958]
#MOTOR_OFF
pos_2a = [0.07045472819517755, 0.42096989188215034, 0.39169320913985056, -176.791096714392, 0.8109338965399241, 179.95651522207834]
pos_2t = [0.06861294922605105, 0.42828954781091355, 0.23768168939003945, -179.99229474525356, 0.001493424340373042, 179.99765941000294]
#HOLE
pos_3a = [0.18827174344515377, 0.42728045838669265, 0.39169320913985056, -179.98733068688915, -0.001201412840938475, 179.99707118356403]
pos_3t = [0.18827174344515377, 0.42728045838669265, 0.23768168939003945, -179.98733068688915, -0.001201412840938475, 179.99707118356403]


import pymcprotocol
import time
import os

# PLC 연결을 모듈 레벨에서 한 번만!
PLC1 = pymcprotocol.Type3E()
# PLC2 = pymcprotocol.Type3E()  # PLC 2개 사용하여 연결시

PLC1.connect("192.168.3.150", 5010)
# PLC2.connect("192.168.3.160", 5010) # 예시
print("[PLC]")
lock = None  # 필요하면 threading.Lock()

def is_robot_connected():
    return hasattr(indy, "sock") and indy.sock is not None

def safe_connect():
    try:
        if not is_robot_connected():
            indy.connect()
            print("[ROBOT] 연결 완료")
    except Exception as e:
        print("[ROBOT] 연결 실패:", e)

def safe_disconnect():
    try:
        if is_robot_connected():
            indy.disconnect()
            print("[ROBOT] 연결 종료")
    except Exception as e:
        print("[ROBOT] 연결 종료 실패:", e)

        
last_signal = None

def handle_detection_result(camsignal):
    global last_signal
    current_plc1 = PLC1
    current_plc2 = PLC2

    # ✅ 중복 camsignal 처리 방지
    if camsignal == last_signal:
        print(f"❗중복 camsignal [{camsignal}] 감지 → 처리 생략")
        return
    last_signal = camsignal  # 새 camsignal 기록
    

    try:
        
        if camsignal == "l-off":
            print("LED_OFF")
            current_plc1.batchwrite_bitunits(headdevice="X21", values=[1])
            time.sleep(5)
            current_plc1.batchwrite_bitunits(headdevice="X21", values=[0])
            time.sleep(5)
            current_plc1.batchwrite_bitunits(headdevice="X30", values=[1])
            time.sleep(5)   
            current_plc1.batchwrite_bitunits(headdevice="X30", values=[0])     
        elif camsignal == "m-off":
            print("MOTOR_OFF")
            current_plc1.batchwrite_bitunits(headdevice="X22", values=[1])
            time.sleep(5)
            current_plc1.batchwrite_bitunits(headdevice="X22", values=[0])
            time.sleep(5)
            current_plc1.batchwrite_bitunits(headdevice="X30", values=[1])
            time.sleep(5)   
            current_plc1.batchwrite_bitunits(headdevice="X30", values=[0])  
        elif camsignal == "not":
            print("HOLE")
            current_plc1.batchwrite_bitunits(headdevice="X23", values=[1])  # 예시 주소
            time.sleep(5)
            current_plc1.batchwrite_bitunits(headdevice="X23", values=[0])
            time.sleep(5)
            current_plc1.batchwrite_bitunits(headdevice="X30", values=[1])
            time.sleep(5)   
            current_plc1.batchwrite_bitunits(headdevice="X30", values=[0])  
        elif camsignal == "l-on" or camsignal == "m-on":
            print("양품")
            current_plc1.batchwrite_bitunits(headdevice="X20", values=[1])
            time.sleep(5)
            current_plc1.batchwrite_bitunits(headdevice="X20", values=[0])
            time.sleep(5)
            current_plc1.batchwrite_bitunits(headdevice="X30", values=[1])
            time.sleep(5)   
            current_plc1.batchwrite_bitunits(headdevice="X30", values=[0])  
        else:
            print("Unknown 상태")
    except Exception as e:
        print(f"[PLC 통신 에러] {e}")

def robot_loop():
    current_plc1 = PLC1

    while True:
        try:
            if not current_plc1._is_connected:
                print("[PLC] 연결이 끊어졌습니다. 재연결 시도...")
                current_plc1.connect("192.168.3.150", 5010)

            values1 = current_plc1.batchread_bitunits(headdevice="X21", readsize=1)
            values2 = current_plc1.batchread_bitunits(headdevice="X22", readsize=1)
            values3 = current_plc1.batchread_bitunits(headdevice="X23", readsize=1)

            if values1[0]:
                print("[PLC] X21 감지됨: LED 불량 로봇 동작 시작")
                safe_connect()
                time.sleep(1)
                led_error()
                safe_disconnect()
                while current_plc1.batchread_bitunits("X21", 1)[0]:
                    time.sleep(0.2)

            elif values2[0]:
                print("[PLC] X22 감지됨: MOTOR 불량 로봇 동작 시작")
                safe_connect()
                time.sleep(1)
                moter_error()
                safe_disconnect()
                while current_plc1.batchread_bitunits("X22", 1)[0]:
                    time.sleep(0.2)

            elif values3[0]:
                print("[PLC] X23 감지됨: HOLE 불량 로봇 동작 시작")
                safe_connect()
                time.sleep(1)
                hole_error()
                safe_disconnect()
                while current_plc1.batchread_bitunits("X23", 1)[0]:
                    time.sleep(0.2)
            time.sleep(0.1)

        except Exception as e:
            print(f"[ROBOT 루프 오류] {e}")
            time.sleep(1)

last_check_time = 0  # 마지막 Danger 체크 시간

def check_safe_danger_signal():
    global last_check_time
    current_plc1 = PLC1

    now = time.time()
    if now - last_check_time < 3:
        return  # 3초 안 지났으면 무시

    signal_file = "./safe_logs/danger_signal.txt"
    if os.path.exists(signal_file):
        print("[PLC] ⚠️ SAFE Danger 감지 → Y125 ON")

        try:
            current_plc1.batchwrite_bitunits(headdevice="X25", values=[1])
            time.sleep(3)
            current_plc1.batchwrite_bitunits(headdevice="X25", values=[0])
            print("[PLC] 🟢 Y125 OFF 처리 완료")
        except Exception as e:
            print("[PLC] 🚨 Y125 제어 중 오류:", e)

        os.remove(signal_file)
        last_check_time = now  # 마지막 실행 시간 갱신

def read_plc_bit(device_name):
    current_plc1 = PLC1
    try:
        result = PLC1.batchread_bitunits(device_name, 1)
        return result[0] == 1
    except Exception as e:
        print(f"[PLC 읽기 오류] {device_name}: {e}")
        return False
# PLC1.close()   # PLC 종료시
# PLC2.close()   # PLC 2개 사용시 종료 할때

