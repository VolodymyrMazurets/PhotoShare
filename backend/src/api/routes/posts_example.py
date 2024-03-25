from flask import Flask, request, jsonify
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import qrcode

app = Flask(__name__)

# Приклад бази даних для зберігання зображень та їх описів
images = {}


@app.route('/images', methods=['POST'])
def upload_image():
    data = request.json
    if 'url' not in data or 'description' not in data:
        return jsonify({'error': 'Недостатньо даних'}), 400
    
    image_url = data['url']
    description = data['description']
    
    # Завантаження зображення на Cloudinary
    response = upload(image_url)
    transformed_url, options = cloudinary_url(response['public_id'], format=response['format'], crop="fill")
    
    # Зберігаємо посилання на трансформоване зображення у базі даних
    images[image_url] = {'description': description, 'transformed_url': transformed_url}
    
    # Генерація QR-коду для посилання
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(transformed_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(f'qr_codes/{image_url}.png')
    
    return jsonify({'message': 'Зображення успішно завантажено', 'transformed_url': transformed_url}), 201


@app.route('/images/<path:image_url>', methods=['PUT'])
def edit_image_description(image_url):
    if image_url not in images:
        return jsonify({'error': 'Зображення не знайдено'}), 404
    
    data = request.json
    if 'description' not in data:
        return jsonify({'error': 'Недостатньо даних'}), 400
    
    new_description = data['description']
    
    # Оновлюємо опис зображення
    images[image_url]['description'] = new_description
    
    return jsonify({'message': 'Опис зображення успішно оновлено'})


@app.route('/images/<path:image_url>', methods=['DELETE'])
def delete_image(image_url):
    if image_url not in images:
        return jsonify({'error': 'Зображення не знайдено'}), 404
    
    # Видаляємо зображення з бази даних
    del images[image_url]
    
    return jsonify({'message': 'Зображення успішно видалено'})


@app.route('/images/<path:image_url>', methods=['GET'])
def get_image(image_url):
    if image_url not in images:
        return jsonify({'error': 'Зображення не знайдено'}), 404
    
    # Повертаємо зображення та його опис
    return jsonify({'url': image_url, 'description': images[image_url]['description'], 'transformed_url': images[image_url]['transformed_url']})


if __name__ == '__main__':
    app.run(debug=True)
