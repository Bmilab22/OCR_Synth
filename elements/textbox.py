"""
Donut
Copyright (c) 2022-present NAVER Corp.
MIT License
"""
import numpy as np
from synthtiger import layers


class TextBox:
    def __init__(self, config):
        self.fill = config.get("fill", [1, 1])

    def generate(self, size, text, font):
        width, height = size

        char_layers, chars = [], []
        fill = np.random.uniform(self.fill[0], self.fill[1])
        width = np.clip(width * fill, height, width)
        font = {**font, "size": int(height)}
        left, top = 0, 0

        for char in text:
            if char in "\r\n":
                continue

            char_layer = layers.TextLayer(char, **font)
            char_scale = height / char_layer.height
            char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
            if char_layer.right > width:
                break

            char_layers.append(char_layer)
            chars.append(char)
            left = char_layer.right

        text = "".join(chars).strip()
        if len(char_layers) == 0 or len(text) == 0:
            return None, None

        text_layer = layers.Group(char_layers).merge()

        return text_layer, text

# # 单词截断
# import numpy as np
# from synthtiger import layers

# class TextBox:
#     def __init__(self, config):
#         self.fill = config.get("fill", [1, 1])
#         self.space_prob = config.get("space_prob", 0.00)  # 新增参数：空格插入的概率
#     def generate(self, size, reader, font):
#         width, height = size

#         char_layers, chars = [], []
#         fill = np.random.uniform(self.fill[0], self.fill[1])
#         effective_width = np.clip(width * fill, height, width)
#         font = {**font, "size": int(height)}
#         left, top = 0, 0
#         text_buffer = []

#         # 定义符号集合，用于判断是否到达符号
#         symbols = set(".,!?-:;()[]{}<>\"'`~@#$%^&*_=+|\\/")

#         while True:
#             char = next(reader, None)

#             if char is None or char in "\r\n":
#                 break

#             text_buffer.append(char)

#             # 创建临时文本层来测量当前缓冲区中的文本是否能适应文本框
#             temp_text = ''.join(text_buffer).strip()
#             if temp_text:
#                 temp_layer = layers.TextLayer(temp_text, **font)
#                 char_scale = height / temp_layer.height
#                 temp_layer.bbox = [left, top, *(temp_layer.size * char_scale)]

#                 # 如果文本超出了文本框宽度，则尝试找到最近的空格或符号
#                 if temp_layer.right > width:
#                     for i in reversed(range(len(text_buffer))):
#                         if text_buffer[i] == ' ' or (i < len(text_buffer) - 1 and text_buffer[i] in symbols):
#                             # 包含分割点字符（空格或符号），并确保不是纯空白
#                             text = ''.join(text_buffer[:i + 1]).strip()
#                             if text:
#                                 char_layer = layers.TextLayer(text, **font)
#                                 char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
#                                 char_layers.append(char_layer)
#                                 chars.append(text)
#                                 left = char_layer.right
#                                 text_buffer = text_buffer[i + 1:]
#                             break
#                     else:  # 如果没有找到合适的分割点，则整个文本作为一块添加
#                         text = ''.join(text_buffer).strip()
#                         if text:
#                             char_layer = layers.TextLayer(text, **font)
#                             char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
#                             char_layers.append(char_layer)
#                             chars.append(text)
#                             left = char_layer.right
#                             text_buffer.clear()
#                     break  # 超出宽度后退出循环

#             # 如果当前字符是空格或者符号，并且后面还有内容，检查是否需要开始新的文本块
#             elif char in ' ' or char in symbols:
#                 temp_text = ''.join(text_buffer).strip()
#                 if temp_text:
#                     temp_layer = layers.TextLayer(temp_text, **font)
#                     char_scale = height / temp_layer.height
#                     temp_layer.bbox = [left, top, *(temp_layer.size * char_scale)]

#                     if temp_layer.right <= width:
#                         char_layers.append(temp_layer)
#                         chars.append(temp_text.strip())
#                         left = temp_layer.right
#                         text_buffer.clear()

#         # 处理剩余的文本
#         if text_buffer:
#             text = ''.join(text_buffer).strip()
#             if text:
#                 char_layer = layers.TextLayer(text, **font)
#                 char_scale = height / char_layer.height
#                 char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
#                 if char_layer.right <= width:
#                     char_layers.append(char_layer)
#                     chars.append(text)

#         if not char_layers:
#             return None, None

#         text_layer = layers.Group(char_layers).merge()

#         return text_layer, "".join(chars)