"""
Donut
Copyright (c) 2022-present NAVER Corp.
MIT License
"""
import json
import os
import re
from typing import Any, List

import numpy as np
from elements import Background, Document
from PIL import Image
from synthtiger import components, layers, templates


class SynthDoG(templates.Template):
    def __init__(self, config=None, split_ratio: List[float] = [0.8, 0.1, 0.1]):
        super().__init__(config)
        if config is None:
            config = {}

        self.quality = config.get("quality", [95, 95])  # 固定高质量输出
        self.landscape = config.get("landscape", 0)
        self.short_size = config.get("short_size", [1240, 1754])
        self.aspect_ratio = config.get("aspect_ratio", [1, 1.414])
        self.background = Background(config.get("background", {}))
        self.document = Document(config.get("document", {}))
        self.effect = components.Iterator(
            [
                components.Switch(components.RGB()),
                components.Switch(components.Shadow()),
                components.Switch(components.Contrast()),
                components.Switch(components.Brightness()),
                # 移除了 MotionBlur 和 GaussianBlur
            ],
            **config.get("effect", {}),
        )
        
        # 新增文本特效配置
        self.text_effect = components.Iterator([
            components.Switch(components.Rotate()),
            components.Switch(components.ElasticDistortion()),
            # 移除了 GaussianBlur
        ], **config.get("text_effect", {}))

        # 配置文本数量范围
        self.text_count_config = config.get("document", {}).get("text_count", {"min": 30, "max": 50})

        # config for splits
        self.splits = ["train", "validation", "test"]
        self.split_ratio = split_ratio
        self.split_indexes = np.random.choice(3, size=10000, p=split_ratio)

        # 存储已有的 image_ids 和下一个可用的 ID
        self.existing_image_ids = set()
        self.next_image_id = 0
        
        
        # 新增属性：期望生成的总图像数量
        self.total_images_to_generate = 20000
        self.generated_images_count = 0
    def generate(self):
        if self.generated_images_count >= self.total_images_to_generate:
            return None  # 不再生成更多图像
        landscape = np.random.rand() < self.landscape
        short_size = np.random.randint(self.short_size[0], self.short_size[1] + 1)  
        aspect_ratio = np.random.uniform(self.aspect_ratio[0], self.aspect_ratio[1])
        long_size = int(short_size * aspect_ratio)
        size = (long_size, short_size) if landscape else (short_size, long_size)

        bg_layer = self.background.generate(size)
        
        # 根据配置随机决定文本数量
        text_count = np.random.randint(self.text_count_config['min'], self.text_count_config['max'] + 1)
        
        
        paper_layer, text_layers, texts = self.document.generate(size, num_texts=text_count)

        document_group = layers.Group([*text_layers, paper_layer])
        
        
        # # 对文本图层单独应用特效
        # for text_layer in text_layers:
        #     self.text_effect.apply([text_layer])  # 应用文本特效
        
        
        # # 对文本图层单独应用形状变形和特效
        # for text_layer in text_layers:
        #     self.shape.apply([text_layer])  # 应用形状变形
        #     self.text_effect.apply([text_layer])  # 应用文本特效
            
        document_space = np.clip(size - document_group.size, 0, None)
        document_group.left = np.random.randint(document_space[0] + 1)
        document_group.top = np.random.randint(document_space[1] + 1)
        roi = np.array(paper_layer.quad, dtype=int)

        layer = layers.Group([*document_group.layers, bg_layer]).merge()
        # self.effect.apply([layer])  # 应用全局特效

        image = layer.output(bbox=[0, 0, *size])
        
        
        #label = " ".join(texts)
        label = "\n".join(texts) 
        label = label.strip()
        #label = re.sub(r"\s+", " ", label)
        quality = np.random.randint(self.quality[0], self.quality[1] + 1)
        # 收集所有文本层的 bbox
        bboxes = [text_layer.bbox for text_layer in text_layers]
        if bboxes:
            all_xs = [bbox[0] for bbox in bboxes] + [bbox[0] + bbox[2] for bbox in bboxes]
            all_ys = [bbox[1] for bbox in bboxes] + [bbox[1] + bbox[3] for bbox in bboxes]

            # 确保所有的坐标值都是float类型，以便正确地计算最小和最大值
            min_x = min(all_xs)
            max_x = max(all_xs)
            min_y = min(all_ys)
            max_y = max(all_ys)

            page_bbox = [
                int(min_x),  # 左上角 x
                int(min_y),  # 左上角 y
                int(max_x),  # 右下角 x
                int(max_y)   # 右下角 y
            ]
        else:
            # 如果没有文本框，页面级别的文本框设为整个图像尺寸，并确保是整数
            page_bbox = [0, 0, int(size[0]), int(size[1])]  
        # 如果需要收集字符级别的 bbox，可以遍历 text_layers 并收集每个字符的 bbox
        # char_bboxes = []
        # for text_layer in text_layers:
        #     char_bboxes.extend([char_layer.bbox for char_layer in text_layer.layers])
        
        data = {
            "image": image,
            "label": label,
            "quality": quality,
            "roi": roi,
            "bboxes": bboxes,
            "page_bbox": page_bbox
        }
        self.generated_images_count += 1


        return data

    def init_save(self, root):
        if self.generated_images_count > self.total_images_to_generate:
            return  # 如果数据为空或已经超出生成数量，则不保存
        os.makedirs(root, exist_ok=True)
        metadata_filepath = os.path.join(root, "metadata.jsonl")
        
        # 如果 metadata.jsonl 文件存在，则读取并加载现有的 image_ids
        if os.path.exists(metadata_filepath):
            with open(metadata_filepath, 'r', encoding='utf-8') as fp:
                for line in fp:
                    metadata = json.loads(line)
                    image_filename = os.path.basename(metadata['image_filepath'])
                    image_id = int(image_filename.rsplit('_', 1)[1].split('.')[0])  # 提取 image_id
                    self.existing_image_ids.add(image_id)
            
            # 计算下一个可用的 image_id
            if self.existing_image_ids:
                self.next_image_id = max(self.existing_image_ids) + 1
            else:
                self.next_image_id = 0
            
            # 更新已经生成的图像数量
            self.generated_images_count = len(self.existing_image_ids)
        else:
            self.generated_images_count = 0
    def save(self, root, data, idx):
        image = data["image"]
        label = data["label"]
        quality = data["quality"]
        roi = data["roi"]
        bboxes = data["bboxes"]
        page_bbox = data.get("page_bbox", None)  # 获取页面级别的 bbox

        output_dirpath = root  # 所有文件保存在同一个目录
        
        # 使用预先计算好的 next_image_id，并更新它
        image_id = self.next_image_id
        self.next_image_id += 1

        # 更新 existing_image_ids 集合
        self.existing_image_ids.add(image_id)
        
        image_filename = f"image_{image_id}.jpg"
        image_filepath = os.path.join(output_dirpath, image_filename)
        image = Image.fromarray(image[..., :3].astype(np.uint8))
        image.save(image_filepath, quality=quality)

        labels = label.splitlines()

        if len(labels) != len(bboxes):
            raise ValueError("The number of labels does not match the number of bounding boxes.")

        ocr_data_withs = []
        ocr_data = []
        for idx, (bbox, text) in enumerate(zip(bboxes, labels), start=1):  # 每个text对应一个bbox，idx为序号
            coords = [int(bbox[0]), int(bbox[1]), int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])]
            ocr_item_s = {"coords": coords, "text": text, "order": idx}  # 添加 'order' 字段
            ocr_item = {"coords": coords, "text": text} 
            ocr_data_withs.append(ocr_item_s)
            ocr_data.append(ocr_item)
            
        metadata_order = {
            "image_filepath": image_filepath,
            "ground_truth": {
                "ocr": ocr_data_withs
            }
        }
        metadata = {
            "image_filepath": image_filepath,
            "ground_truth": {
                "ocr": ocr_data
            }
        }

        # 新增的 metadata_page 数据
        metadata_page = {
            "image_filepath": image_filepath,
            "ground_truth": {
                "ocr": ocr_data
            },
            "page_bbox": page_bbox
        }

        metadata_filename_order = "metadata_order.jsonl"
        metadata_filepath_order = os.path.join(output_dirpath, metadata_filename_order)
        metadata_filename = "metadata.jsonl"
        metadata_filepath = os.path.join(output_dirpath, metadata_filename)
        metadata_filename_page = "metadata_page.jsonl"
        metadata_filepath_page = os.path.join(output_dirpath, metadata_filename_page)
        
        with open(metadata_filepath_order, "a") as fp:
            json.dump(metadata_order, fp, ensure_ascii=False)
            fp.write("\n")
        with open(metadata_filepath, "a") as fp:
            json.dump(metadata, fp, ensure_ascii=False)
            fp.write("\n")
        with open(metadata_filepath_page, "a") as fp:
            json.dump(metadata_page, fp, ensure_ascii=False)
            fp.write("\n")
                
    def end_save(self, root):
        pass

    def format_metadata(self, image_filepath: str, keys: List[str], values: List[Any]):
        """
        Fit gt_parse contents to huggingface dataset's format
        keys and values, whose lengths are equal, are used to constrcut 'gt_parse' field in 'ground_truth' field
        Args:
            keys: List of task_name
            values: List of actual gt data corresponding to each task_name
        """
        assert len(keys) == len(values), "Length does not match: keys({}), values({})".format(len(keys), len(values))

        _gt_parse_v = dict()
        for k, v in zip(keys, values):
            _gt_parse_v[k] = v
        gt_parse = {"gt_parse": _gt_parse_v}
        return gt_parse  
    
    
    
    # 返回字典而不是字符串:
    #     image = data["image"]
    #     label = data["label"]
    #     quality = data["quality"]
    #     roi = data["roi"]
    #     bboxes = data["bboxes"]
    #     #glyph_bboxes = data["char_bboxes"]

    #     # split
    #     split_idx = self.split_indexes[idx % len(self.split_indexes)]
    #     output_dirpath = os.path.join(root, self.splits[split_idx])

    #     # save image
    #     image_filename = f"image_{idx}.jpg"
    #     image_filepath = os.path.join(output_dirpath, image_filename)
    #     os.makedirs(os.path.dirname(image_filepath), exist_ok=True)
    #     image = Image.fromarray(image[..., :3].astype(np.uint8))
    #     image.save(image_filepath, quality=quality)

    #     # coords = [[x, y, x + w, y + h] for x, y, w, h in bboxes]
    #     # coords = "\t".join([",".join(map(str, map(int, coord))) for coord in coords])
    #     # print('-----coords-----',coords)
    #     # Prepare OCR data
    #     # Prepare OCR data
    #     # 将label字符串按空格分割为单词列表
    #     #labels = label.split()
    #     labels = label.splitlines()

    #     # 确保labels和bboxes长度一致
    #     if len(labels) != len(bboxes):
    #         raise ValueError("The number of labels does not match the number of bounding boxes.")

    #     ocr_data = []
    #     for bbox, text in zip(bboxes, labels):  # 每个text对应一个bbox
    #         coords = [int(bbox[0]), int(bbox[1]), int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])]
    #         ocr_item = {"coords": coords, "text": text}
    #         ocr_data.append(ocr_item)

    #     # 构建最终的metadata字典
    #     # save metadata (gt_json)
    #     metadata_filename = "metadata.jsonl"
    #     metadata_filepath = os.path.join(output_dirpath, metadata_filename)
    #     os.makedirs(os.path.dirname(metadata_filepath), exist_ok=True)
        
    #     # # 构建最终的metadata字典
    #     # metadata = {
    #     #     "img_filename": image_filename,
    #     #     "ocr": ocr_data
    #     # }
        
    #     metadata = self.format_metadata(
    #         image_filename=image_filename,
    #         keys=["text_sequence"],
    #         values=[json.dumps({"ocr": ocr_data}, ensure_ascii=False)]
    #     )
    #     #metadata = self.format_metadata(image_filename=image_filename, keys=["text_sequence"], values=[label])
    #     with open(metadata_filepath, "a") as fp:
    #         json.dump(metadata, fp, ensure_ascii=False)
    #         fp.write("\n")

    # def end_save(self, root):
    #     pass

    # def format_metadata(self, image_filename: str, keys: List[str], values: List[Any]):
    #     """
    #     Fit gt_parse contents to huggingface dataset's format
    #     keys and values, whose lengths are equal, are used to constrcut 'gt_parse' field in 'ground_truth' field
    #     Args:
    #         keys: List of task_name
    #         values: List of actual gt data corresponding to each task_name
    #     """
    #     assert len(keys) == len(values), "Length does not match: keys({}), values({})".format(len(keys), len(values))

    #     _gt_parse_v = dict()
    #     for k, v in zip(keys, values):
    #         _gt_parse_v[k] = v
    #     gt_parse = {"gt_parse": _gt_parse_v}
    #     gt_parse_str = json.dumps(gt_parse, ensure_ascii=False)
    #     metadata = {"file_name": image_filename, "ground_truth": gt_parse_str}
    #     return metadata
