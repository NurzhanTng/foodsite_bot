from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import base64

# Загрузка закрытого ключа из файла
with open('private_key.pem', 'rb') as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,  # Если ключ зашифрован, укажите пароль
    )

print('sosi')
# Зашифрованные данные (полученные с фронтенда)
encrypted_data = "065qhcapL1QKmUCaixdDnoTV88lsfG2aL0VPFxpusR7At1J3DSAG6yc8H5SiumoqiHu3hTq9ciqwkXB19sOixL7ZIpK9CjhdRq7AWRF2hWYowQouM9MTerhfQdWELRSHr4SYqSKyUYDbINcQs+HxI6gV7V79jDGOUF3uqwy/8GgXqa6LGojMz4nEV+LDXkjRMowZmGmjWCiMXk9uSzXBinq+xFGVqWElQZ4hsVSA3dYUqWX+3rnxuHlZ8l6nq/jjSgnlov5qEU2Aa1GyvYdSjG81RwJK98ANHAa+5JlJlrNmyQ2PJ6tFXulFvCIhMBgW6ZFpjCBBQ9F62mMWMQOdlw=="  # Замените на фактические данные

# Декодируем строку из base64
encrypted_data_bytes = base64.b64decode(encrypted_data)

# Расшифровываем данные
decrypted_data = private_key.decrypt(
    encrypted_data_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Преобразуем расшифрованные данные в строку
decrypted_string = decrypted_data.decode('utf-8')

print("Расшифрованные данные:", decrypted_string)
