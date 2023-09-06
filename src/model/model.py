import os
import torch
import requests
from PIL import Image

from utils.config import Config
from src.model.init import download_model
from transformers import AutoImageProcessor, ViTModel, AutoTokenizer, T5EncoderModel

class CommentGenerator():
    def __init__(self) -> None:
        
        self.config = Config("./config/comment_generator.yaml").__get_config__()
        download_model(self.config['model']['url'], self.config['model']['dir'])
        
        #Get model
        self.tokenizer = AutoTokenizer.from_pretrained("VietAI/vit5-base")
        self.model = torch.load(self.config["model"]["dir"], map_location=torch.device(self.config["model"]['device']))        
        
        
        #Image
        self.vit_image_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224-in21k")
        self.vit_model = ViTModel.from_pretrained("google/vit-base-patch16-224-in21k")
        self.vit_model.to(self.config["model"]["device"])
        
        #Content
        self.vit5_model = T5EncoderModel.from_pretrained("VietAI/vit5-base")
        self.vit5_model.to(self.config["model"]["device"])
        
    def get_text_feature(self, content):
        inputs = self.tokenizer(content,
                            padding="max_length",
                            truncation=True,
                            max_length=self.config["model"]["input_maxlen"],
                            return_tensors="pt").to(self.config["model"]["device"])
        with torch.no_grad():
            outputs = self.vit5_model(**inputs)
        last_hidden_states = outputs.last_hidden_state
        return last_hidden_states.to(self.config["model"]["device"]), inputs.attention_mask.to(self.config["model"]["device"])
        

    def get_image_feature_from_url(self, image_url, is_local=False):
        if not image_url:
            print(f"WARNING not image url {image_url}")
            return torch.zeros((1, 197, 768)).to(self.config["model"]["device"]), torch.zeros((1, 197)).to(self.config["model"]["device"])
        if not is_local:
            try:
                images = Image.open(requests.get(image_url, stream=True).raw).convert("RGB")
            except:
                print(f"READ IMAGE ERR: {image_url}")
                return torch.zeros((1, 197, 768)).to(self.config["model"]["device"]), torch.zeros((1, 197)).to(self.config["model"]["device"])
        else:
            images = Image.open(image_url).convert("RGB")
        inputs = self.vit_image_processor(images, return_tensors="pt").to(self.config["model"]["device"])
        with torch.no_grad():
            outputs = self.vit_model(**inputs)
        last_hidden_states = outputs.last_hidden_state
        attention_mask = torch.ones((last_hidden_states.shape[0], last_hidden_states.shape[1]))

        return last_hidden_states.to(self.config["model"]["device"]), attention_mask.to(self.config["model"]["device"])

    def inference(self, content_feature, content_mask, image_feature, image_mask):
        
        inputs_embeds = torch.cat((image_feature[0], content_feature[0]), 0)
        inputs_embeds = torch.unsqueeze(inputs_embeds, 0)
        attention_mask = torch.cat((image_mask[0], content_mask[0]), 0)
        attention_mask = torch.unsqueeze(attention_mask, 0)
        with torch.no_grad():
            generated_ids = self.model.generate(
                inputs_embeds=inputs_embeds,
                attention_mask=attention_mask,
                num_beams=2,
                max_length=self.config["model"]["output_maxlen"],
                # num_return_sequences=2
                # skip_special_tokens=True,
                # clean_up_tokenization_spaces=True
            )
        comments = [self.tokenizer.decode(generated_id, skip_special_tokens=True) for generated_id in generated_ids]
        return comments