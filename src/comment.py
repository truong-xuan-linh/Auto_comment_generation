from src.model.model import CommentGenerator
from src.model.text_process import TextPreprocess

class GetComment():
    def __init__(self) -> None:
        """Get Comment init funtion
        """
        self.CommentGenerator = CommentGenerator()
        self.text_preprocess = TextPreprocess()
        self.inputs = {}
        
    def generator(self, info):
        """Generation function

        Args:
            info (Dict): info extract from kafka message

        Returns:
            List: List of comment
        """
        
        content = info["content"]
        content = self.text_preprocess.preprocess(content)
        medias = info["medias"]
        if not medias:
            medias = [None]
        
        print(medias)
        typfeed = info["type_generation"]
        num_comments = info["num_comments"]
        mapper = {
            0: "bảng tin",
            1: "trải nghiệm"
        }
        
        comments_prefix = ["thứ một", 
                          "thứ hai",
                          "thứ ba"]
        
        comments = []
        for i, comment_prefix in enumerate(comments_prefix):
            content_w_prefix = f"{mapper[typfeed]}: {comment_prefix}: {content}"
            self.inputs[f"content_{i}"] = self.CommentGenerator.get_text_feature(content_w_prefix) 
        
        while len(comments) < num_comments:
            for i, media in enumerate(medias):
                print(i)
                if i not in self.inputs:
                    self.inputs[i] = self.CommentGenerator.get_image_feature_from_url(media, is_local=True)
                image_feature, image_mask = self.inputs[i]
                for i in range(len(comments_prefix)):
                    content_feature, content_mask = self.inputs[f"content_{i}"]
                    comment = self.CommentGenerator.inference(content_feature, content_mask, image_feature, image_mask)[0]
                    comments.append(comment)
                    comments = list(set(comments))
                    if len(comments) >= num_comments:
                        return comments
        