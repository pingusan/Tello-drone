pip install mavproxy


from dronekit import connect, VehicleMode, LocationGlobalRelative
import time

# ドローンに接続
connection_string = '/dev/ttyUSB0'  # ドローンの接続ポートに合わせて変更
vehicle = connect(connection_string, wait_ready=True)

# 目的地の座標 (緯度、経度、高度)
target_location = LocationGlobalRelative(35.123456, 139.789012, 10)  # 例として適切な座標を設定

# アーム (プロペラの回転) とGUIDEDモードへの変更
vehicle.mode = VehicleMode("GUIDED")
vehicle.armed = True

# 離陸
target_altitude = 10  # 離陸する高度 (メートル)
vehicle.simple_takeoff(target_altitude)

# 離陸待機
while not vehicle.is_armable:
    time.sleep(1)

while not vehicle.armed:
    time.sleep(1)

# 目的地への移動
vehicle.simple_goto(target_location)

# 移動待機
while True:
    remaining_distance = vehicle.location.global_relative_frame.distance_to(target_location)
    if remaining_distance <= 1:
        print("目的地に到着しました")
        break
    time.sleep(1)

# ドローンの制御を解除
vehicle.mode = VehicleMode("RTL")

# 着陸待機
while vehicle.armed:
    time.sleep(1)

# ドローンとの接続を閉じる
vehicle.close()
