from openai import OpenAI

class PostGenerator:
    def __init__(self, openai_key, tone, topic):
        self.client = OpenAI(api_key=openai_key)
        self.tone = tone
        self.topic = topic

    def generate_post(self):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты высококвалифицированный SMM специалист, который помогает в генерации текста для постов с заданной теме тематикой и заданном тоне."},
                {"role": "user", "content": f"Сгенерировать пост с темой {self.topic} и тоном {self.tone}"},
            ]
        )
        return response.choices[0].message.content

    def generate_post_image_description(self):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты ассистент, который составит промт для генерации изображения. Ты должен составлять промт на заданную тематику" },
                {"role": "user", "content": f"Сгенерировать изображение для соцсетей с темой {self.topic}"},
            ]
        )
        return response.choices[0].message.content
