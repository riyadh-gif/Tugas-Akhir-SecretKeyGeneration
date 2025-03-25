import pyaes
import binascii
from PIL import Image
import os


key_bob1 = b'\xc8ji\xd8w\xea^\xcd\xe3\xcc\xf3\x8b\xe9\x95\x0bi'  
key_bob2 = b'\xc8ji\xd8w\xea^\xcd\xe3\xcc\xf3\x8b\xe9\x95\z9ac'        


def encrypt_image(image_path, key):
    \
    with open(image_path, 'rb') as img_file:
        image_data = img_file.read()

    
    aes = pyaes.AESModeOfOperationCTR(key)
    ciphertext = aes.encrypt(image_data)  

    return ciphertext


def decrypt_image(ciphertext, key):
   
    aes = pyaes.AESModeOfOperationCTR(key)
    decrypted_data = aes.decrypt(ciphertext)  

    return decrypted_data


def save_image(image_data, output_path):
    with open(output_path, 'wb') as img_file:
        img_file.write(image_data)


def encrypt_images_in_directory(directory_path, key):
    for filename in os.listdir(directory_path):
       
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            image_path = os.path.join(directory_path, filename)
            print(f"Enkripsi gambar: {image_path}")
            encrypted_data = encrypt_image(image_path, key)
            
            
            encrypted_image_path = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}_encrypted.enc")
            with open(encrypted_image_path, 'wb') as enc_file:
                enc_file.write(encrypted_data)
            print(f"Gambar dienkripsi dan disimpan sebagai {encrypted_image_path}")


def decrypt_images_in_directory(directory_path, key):
    for filename in os.listdir(directory_path):
       
        if filename.lower().endswith('_encrypted.enc'):
            encrypted_image_path = os.path.join(directory_path, filename)
            print(f"Dekripsi gambar: {encrypted_image_path}")
            
            
            with open(encrypted_image_path, 'rb') as enc_file:
                encrypted_data = enc_file.read()
            
            # Dekripsi gambar
            decrypted_data = decrypt_image(encrypted_data, key)
            
            
            decrypted_image_path = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}_decrypted.jpg")
            save_image(decrypted_data, decrypted_image_path)
            print(f"Gambar didekripsi dan disimpan sebagai {decrypted_image_path}")


if __name__ == "__main__":
    directory_path = r"gambar"  

   
    encrypt_images_in_directory(directory_path, key_bob1)

 
    decrypt_images_in_directory(directory_path, key_bob1)
