import requests

class VKPublisher:
    def __init__(self, vk_api_key, group_id):
        self.vk_api_key = vk_api_key
        self.group_id = group_id

    def upload_photo(self, image_url):
        # 1. Получаем upload_url
        upload_url_response = requests.get(
            'https://api.vk.com/method/photos.getWallUploadServer',
            params={
                'access_token': self.vk_api_key,
                'v': '5.236',
                'group_id': self.group_id
            }
        ).json()

        if 'error' in upload_url_response:
            raise Exception(f"VK API ошибка при получении upload_url: {upload_url_response['error']['error_msg']}")

        upload_url = upload_url_response['response']['upload_url']

        # 2. Загружаем фото
        image_data = requests.get(image_url).content
        upload_response_raw = requests.post(upload_url, files={'photo': ('image.jpg', image_data)})

        try:
            upload_response = upload_response_raw.json()
        except Exception as e:
            raise Exception(f'Ошибка загрузки фото: {e}\nОтвет: {upload_response_raw.text}') from e

        # 3. Сохраняем фото на стене
        save_response = requests.get(
            'https://api.vk.com/method/photos.saveWallPhoto',
            params={
                'access_token': self.vk_api_key,
                'v': '5.236',
                'group_id': self.group_id,
                'photo': upload_response['photo'],
                'server': upload_response['server'],
                'hash': upload_response['hash']
            }
        ).json()

        if 'error' in save_response:
            raise Exception(f"VK API ошибка при сохранении фото: {save_response['error']['error_msg']}")

        photo_id = save_response['response'][0]['id']
        owner_id = save_response['response'][0]['owner_id']

        return f'photo{owner_id}_{photo_id}'

    def publish_post(self, content, image_url=None):
        params = {
            'access_token': self.vk_api_key,
            'from_group': 1,
            'v': '5.236',
            'owner_id': f'-{self.group_id}',
            'message': content
        }

        if image_url:
            attachment = self.upload_photo(image_url)
            params['attachments'] = attachment

        # 💡 Оборачиваем запрос в try + логируем
        try:
            res = requests.post('https://api.vk.com/method/wall.post', params=params, timeout=10)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Сетевая ошибка при запросе к VK: {e}")

        print("📡 wall.post статус:", res.status_code)
        print("📝 Ответ:", res.text[:500])

        try:
            response = res.json()
        except Exception as e:
            raise Exception(f'❌ Ошибка при разборе JSON: {e}\nТело ответа: {res.text}') from e

        if 'error' in response:
            raise Exception(f"🛑 VK API ошибка: {response['error']['error_msg']}")

        return response
