import re

class TextPreprocess():
  def __init__(self, teencode_dir="./storage/teencode.txt"):
    self.get_teencode(teencode_dir)

  def get_teencode(self, teencode_dir):
    with open(teencode_dir, "r", encoding="utf-8") as f:
      teencode_original = f.readlines()
    teencode_json = {}
    for teencode in teencode_original:
        key, value = teencode.split("\t")
        value = value.replace("\n", "")
        teencode_json[key] = value
    self.teencode_json = teencode_json

  def teencode_normalize(self, text):
    text_split = text.split()
    return " ".join([self.teencode_json.get(txt, txt) for txt in text_split])

  def clean_text(self, text):
    # Xóa hashtag (dấu #)
    text = re.sub(r'#\w+', '', text)

    # Xóa liên kết (URL)
    text = re.sub(r'http\S+', '', text)

    # Xóa các ký tự số
    text = re.sub(r'\d+', '', text)

    # Xóa ký tự đặc biệt
    text = re.sub(r'[^\w\s]', '', text)

    text = " ".join(text.split())
    text = text.lower()
    return text

  def preprocess(self, text):
    cleaned_text = self.clean_text(text)
    cleaned_text = self.teencode_normalize(cleaned_text)
    return cleaned_text