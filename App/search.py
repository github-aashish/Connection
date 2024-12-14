from deepface import DeepFace
data_search = DeepFace.find(img_path="./hrithik3.jpg",db_path="./db")
print(data_search[0]['identity'])