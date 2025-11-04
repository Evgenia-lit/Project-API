import json
import requests

def get_cats():
    """Получаем JSON """
    url = "https://cataas.com/api/cats?tags=cute"
    response = requests.get(url)
    return response.json()

def save_cats(cats_data):
    """Сохраняем в папку у себя на компьютере вместе с названием картинки"""
    filenames = []
    for cat in cats_data:
        image_id = cat["id"]
        text = cat["tags"][0]

        image_url = f"https://cataas.com/cat/{image_id}/says/{text}"
        image_response = requests.get(image_url)

        filename = f"{text}_{image_id}.jpg"
        with open(f"images/{filename}", "wb") as f:
            f.write(image_response.content)

        filenames.append(filename)

    return filenames

def create_info_json(cats_data):
    """Создает JSON файл с названием картинки и размером"""
    json_filename = "files_info.json"
    files_info = []

    for cat in cats_data:
        image_id = cat["id"]
        text = cat["tags"][0]
        size = cat.get("size", 0)

        image_filename = f"{text}_{image_id}.jpg"

        file_info = {
            "filename": image_filename,
            "size_bytes": size
        }

        files_info.append(file_info)

    with open(json_filename , "w", encoding="utf-8") as f:
        json.dump(files_info, f, ensure_ascii=False, indent=2)

    return json_filename



def create_folder_ya():
    """Создаем папку на яндекс диске"""
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    params = {
        "path": "pd-fpy-130"
    }
    headers = {
        "Authorization": "000"
    }

    response = requests.put(url, params=params, headers=headers)
    return response

def create_image_folder_ya():
    """Создаем папку для картинок в папке на яндекс диске"""
    url = "https://cloud-api.yandex.net/v1/disk/resources"
    params = {
        "path": "pd-fpy-130/images"
    }
    headers = {
        "Authorization":  "000"
    }

    response = requests.put(url, params=params, headers=headers)
    return response


def upload_link(filename, is_image=True):
    """Получаем ссылку для отправки в папку на яндекс диск"""
    url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    if is_image:
        path = f"pd-fpy-130/images/{filename}"
    else:
        path = f"pd-fpy-130/{filename}"

    params ={
        "path": path
    }
    headers = {
        "Authorization":  "000"
    }
    response = requests.get(url, params=params, headers=headers)
    url_upload = response.json()["href"]
    return url_upload

def downl_file(url_upload, filename, is_image=True):
    """Загружаем в папку на яндекс диск"""
    if is_image:
        with open(f"images/{filename}", "rb") as f:
            response = requests.put(url_upload, files={"file": f})
    else:
        with open(filename, "rb") as f:
            response = requests.put(url_upload, files={"file": f})
    return response

def main():
    """Вызов функций"""
    print("Начинаем загрузку милых котиков...")

    cats_data = get_cats()
    print(f"Получено {len(cats_data)} котов из API")

    saved_filenames = save_cats(cats_data)
    print(f"Сохранено {len(saved_filenames)} картинок локально")

    print("Создаем папки на Яндекс.Диске...")
    folder_response = create_folder_ya()
    print(f"Основная папка: {folder_response.status_code}")

    image_folder_response = create_image_folder_ya()
    print(f"Папка для картинок: {image_folder_response.status_code}")

    print("Загружаем картинки на Яндекс.Диск...")
    for i, filename in enumerate(saved_filenames, 1):
        print(f"[{i}/{len(saved_filenames)}] Загружаем {filename}...")
        upload_url = upload_link(filename)
        result = downl_file(upload_url, filename)
        print(f"Статус: {result.status_code}")

    print("Создаем файл с информацией...")
    json_filename = create_info_json(cats_data)
    print(f"JSON файл создан: {json_filename}")

    print("Загружаем JSON на Яндекс.Диск...")
    json_upload_url = upload_link(json_filename, is_image=False)
    json_result = downl_file(json_upload_url, json_filename, is_image=False)
    print(f"JSON загружен. Статус: {json_result.status_code}")

    print("Все операции завершены успешно!")

if __name__ == "__main__":
    main()

