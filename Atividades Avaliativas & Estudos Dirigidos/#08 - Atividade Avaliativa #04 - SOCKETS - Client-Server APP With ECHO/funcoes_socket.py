import datetime
import subprocess

def hora_atual():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def trace_route(url):
    try:
        result = subprocess.run(['tracert', '-d', url], capture_output=True, text=True, shell=True)
        return result.stdout
    except Exception as e:
        return str(e)

def vigenere(text, key):
    """Criptografa a mensagem usando o algoritmo de Vigenère."""
    def shift_char(c, k):
        if c.isalpha():
            shift = ord(k) - ord('A') if c.isupper() else ord(k) - ord('a')
            base = ord('A') if c.isupper() else ord('a')
            return chr((ord(c) - base + shift) % 26 + base)
        return c
    
    key = key.upper()
    encrypted = ''.join(shift_char(c, key[i % len(key)]) for i, c in enumerate(text))
    return encrypted
