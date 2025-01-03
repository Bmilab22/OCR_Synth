"""
Donut
Copyright (c) 2022-present NAVER Corp.
MIT License
"""
from collections import OrderedDict

import numpy as np
from synthtiger import components

from elements.textbox_inter import TextBox
from layouts import GridStack


# class TextReader:
#     def __init__(self, path, cache_size=2 ** 28, block_size=2 ** 20):
#         self.fp = open(path, "r", encoding="utf-8")
#         self.length = 0
#         self.offsets = [0]
#         self.cache = OrderedDict()
#         self.cache_size = cache_size
#         self.block_size = block_size
#         self.bucket_size = cache_size // block_size
#         self.idx = 0

#         while True:
#             text = self.fp.read(self.block_size)
#             if not text:
#                 break
#             self.length += len(text)
#             self.offsets.append(self.fp.tell())

#     def __len__(self):
#         return self.length

#     def __iter__(self):
#         return self

#     def __next__(self):
#         char = self.get()
#         self.next()
#         return char

#     def move(self, idx):
#         self.idx = idx

#     def next(self):
#         self.idx = (self.idx + 1) % self.length

#     def prev(self):
#         self.idx = (self.idx - 1) % self.length

#     def get(self):
#         key = self.idx // self.block_size

#         if key in self.cache:
#             text = self.cache[key]
#         else:
#             if len(self.cache) >= self.bucket_size:
#                 self.cache.popitem(last=False)

#             offset = self.offsets[key]
#             self.fp.seek(offset, 0)
#             text = self.fp.read(self.block_size)
#             self.cache[key] = text

#         self.cache.move_to_end(key)
#         char = text[self.idx % self.block_size]
#         return char


# class Content:
#     def __init__(self, config):
#         self.margin = config.get("margin", [0, 0.1])
#         self.reader = TextReader(**config.get("text", {}))
#         self.font = components.BaseFont(**config.get("font", {}))
#         self.layout = GridStack(config.get("layout", {}))
#         self.textbox = TextBox(config.get("textbox", {}))
#         self.textbox_color = components.Switch(components.Gray(), **config.get("textbox_color", {}))
#         self.content_color = components.Switch(components.Gray(), **config.get("content_color", {}))

#     def generate(self, size, num_texts=None):
#         width, height = size

#         layout_left = width * np.random.uniform(self.margin[0], self.margin[1])
#         layout_top = height * np.random.uniform(self.margin[0], self.margin[1])
#         layout_width = max(width - layout_left * 2, 0)
#         layout_height = max(height - layout_top * 2, 0)
#         layout_bbox = [layout_left, layout_top, layout_width, layout_height]

#         text_layers, texts = [], []
#         layouts = self.layout.generate(layout_bbox)
#         self.reader.move(np.random.randint(len(self.reader)))

#         # 如果指定了num_texts，则限制生成的文本框数量
#         if num_texts is not None:
#             layouts = list(layouts)[:num_texts]  # 只取前num_texts个布局
            
#         for layout in layouts:
#             font = self.font.sample()

#             for bbox, align in layout:
#                 if num_texts is not None and len(texts) >= num_texts:
#                     break  # 达到所需文本数量后退出循环
                
#                 x, y, w, h = bbox
#                 text_layer, text = self.textbox.generate((w, h), self.reader, font)

#                 if text_layer is None or not text.strip():
#                     continue

#                 # 确保文本框中的文本不会从单词中间开始或结束
#                 words = text.split()
#                 if words and (text.endswith('-') or not text.endswith(words[-1])):
#                     # 计算最后一个完整单词的位置，并回退到这个位置
#                     last_word = words[-1]
#                     word_start_idx = text.rfind(last_word)
#                     self.reader.move(self.reader.idx - (len(text) - word_start_idx))
#                     text_layer, text = self.textbox.generate((w, h), self.reader, font)

#                 if text_layer is None or not text.strip():
#                     continue

#                 # 确保文本框中的文本不会在单词中间被截断
#                 if not text.endswith(' ') and not text.endswith('\n'):
#                     last_space_idx = text.rfind(' ')
#                     if last_space_idx != -1:
#                         self.reader.move(self.reader.idx - (len(text) - last_space_idx))
#                         text_layer, text = self.textbox.generate((w, h), self.reader, font)

#                 if text_layer is None or not text.strip():
#                     continue

#                 text_layer.center = (x + w / 2, y + h / 2)
#                 if align == "left":
#                     text_layer.left = x
#                 elif align == "right":
#                     text_layer.right = x + w

#                 self.textbox_color.apply([text_layer])
#                 text_layers.append(text_layer)
#                 texts.append(text)

#                 if num_texts is not None and len(texts) >= num_texts:
#                     break  # 达到所需文本数量后退出循环
                    
#         self.content_color.apply(text_layers)

#         return text_layers, texts

class TextReader:
    def __init__(self, path, cache_size=2 ** 28, block_size=2 ** 20):
        self.fp = open(path, "r", encoding="utf-8")
        self.length = 0
        self.offsets = [0]
        self.cache = OrderedDict()
        self.cache_size = cache_size
        self.block_size = block_size
        self.bucket_size = cache_size // block_size
        self.idx = 0

        while True:
            text = self.fp.read(self.block_size)
            if not text:
                break
            self.length += len(text)
            self.offsets.append(self.fp.tell())

    def __len__(self):
        return self.length

    def __iter__(self):
        return self

    def __next__(self):
        char = self.get()
        self.next()
        return char

    def move(self, idx):
        self.idx = idx % self.length

    def next(self):
        self.idx = (self.idx + 1) % self.length

    def prev(self):
        self.idx = (self.idx - 1) % self.length

    def get(self):
        key = self.idx // self.block_size

        if key in self.cache:
            text = self.cache[key]
        else:
            if len(self.cache) >= self.bucket_size:
                self.cache.popitem(last=False)

            offset = self.offsets[key]
            self.fp.seek(offset, 0)
            text = self.fp.read(self.block_size)
            self.cache[key] = text

        self.cache.move_to_end(key)
        char = text[self.idx % self.block_size]
        return char

    def move_to_next_delimiter(self, delimiters):
        """Move the reader's position to the next delimiter."""
        start_idx = self.idx
        found = False
        
        while not found:
            char = self.get()
            if char in delimiters or char in "\n":  # 包括换行符作为分隔符
                found = True
            else:
                self.next()
            
            if self.idx == start_idx:  # 防止无限循环（如果文件中没有分隔符）
                break

        if not found:
            # 如果没有找到任何分隔符，则不改变位置
            self.move(start_idx)


class Content:
    def __init__(self, config):
        self.margin = config.get("margin", [0, 0.1])
        self.reader = TextReader(**config.get("text", {}))
        self.font = components.BaseFont(**config.get("font", {}))
        self.layout = GridStack(config.get("layout", {}))
        self.textbox = TextBox(config.get("textbox", {}))
        self.textbox_color = components.Switch(components.Gray(), **config.get("textbox_color", {}))
        self.content_color = components.Switch(components.Gray(), **config.get("content_color", {}))

    def generate(self, size, num_texts=None):
        width, height = size

        layout_left = width * np.random.uniform(self.margin[0], self.margin[1])
        layout_top = height * np.random.uniform(self.margin[0], self.margin[1])
        layout_width = max(width - layout_left * 2, 0)
        layout_height = max(height - layout_top * 2, 0)
        layout_bbox = [layout_left, layout_top, layout_width, layout_height]

        text_layers, texts = [], []
        layouts = self.layout.generate(layout_bbox)
        self.reader.move(np.random.randint(len(self.reader)))

        symbols = set(".,!?-:;()[]{}<>\"'`~@#$%^&*_=+|\\/ ")  # 包括空格在内的符号集合

        # 如果指定了num_texts，则限制生成的文本框数量
        if num_texts is not None:
            layouts = list(layouts)[:num_texts]  # 只取前num_texts个布局
            
        for layout in layouts:
            font = self.font.sample()

            for bbox, align in layout:
                if num_texts is not None and len(texts) >= num_texts:
                    break  # 达到所需文本数量后退出循环
                
                # 在生成新的bbox前，尝试读取字符直到遇到空格或符号
                self.reader.move_to_next_delimiter(symbols)

                x, y, w, h = bbox
                text_layer, text = self.textbox.generate((w, h), self.reader, font)

                if text_layer is None or not text.strip():
                    continue

                # 确保文本框中的文本不会从单词中间开始或结束
                words = text.split()
                if words and (text.endswith('-') or not text.endswith(words[-1])):
                    last_word = words[-1]
                    word_start_idx = text.rfind(last_word)
                    self.reader.move(self.reader.idx - (len(text) - word_start_idx))
                    text_layer, text = self.textbox.generate((w, h), self.reader, font)

                if text_layer is None or not text.strip():
                    continue

                # 确保文本框中的文本不会在单词中间被截断
                if not text.endswith(' ') and not text.endswith('\n'):
                    last_space_idx = text.rfind(' ')
                    if last_space_idx != -1:
                        self.reader.move(self.reader.idx - (len(text) - last_space_idx))
                        text_layer, text = self.textbox.generate((w, h), self.reader, font)

                if text_layer is None or not text.strip():
                    continue

                text_layer.center = (x + w / 2, y + h / 2)
                if align == "left":
                    text_layer.left = x
                elif align == "right":
                    text_layer.right = x + w

                self.textbox_color.apply([text_layer])
                text_layers.append(text_layer)
                texts.append(text)

                if num_texts is not None and len(texts) >= num_texts:
                    break  # 达到所需文本数量后退出循环
                    
        self.content_color.apply(text_layers)

        return text_layers, texts