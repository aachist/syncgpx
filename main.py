from fastapi import FastAPI, Request
import json
import os

app = FastAPI()

# Папка, куда будут сохраняться полученные треки
SAVE_DIR = "received_tracks"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.post("/sync-tracks")
async def receive_tracks(request: Request):
    try:
        # Принимаем JSON-данные от вашего Android-приложения
        payload = await request.json()
        
        # Для теста: выводим в консоль облака, что пришло
        print(f"Получены данные: {payload}")
        
        # Сохраняем в файл на сервере (например, под именем трека или по времени)
        # Если в вашем JSON есть id трека, можно использовать его
        track_id = payload.get("track_id", "unknown_track")
        
        file_path = os.path.join(SAVE_DIR, f"track_{track_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
            
        return {"status": "success", "message": "Данные успешно синхронизированы"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def read_root():
    return {"status": "working", "info": "GPS Tracker Sync Server"}
