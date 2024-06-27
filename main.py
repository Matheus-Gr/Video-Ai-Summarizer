from Summy import Summy
import time
from print_color import print
import torch

if torch.cuda.is_available():
    print(f"Using {torch.cuda.get_device_name(0)}", color="green")
else:
    print("Using CPU, may face low speed", color="red")

URL = 'https://www.youtube.com/watch?v=YdEq2nVhBgk'
email = "matheus-gr@hotmail.com"
max_c = 600
min_c = 300
mod = "small"
voice = "media/voices/matheus.wav"

start = time.time()
smy = Summy()
smy.run(URL, whisper_model=mod, max_characters=max_c,
        email=email, voice=voice, clean=False)


print(f"Duration {(time.time() - start):.2f}s", color="green")  # Calcule time
