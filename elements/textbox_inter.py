"""
Donut
Copyright (c) 2022-present NAVER Corp.
MIT License
"""
# import numpy as np
# from synthtiger import layers


# class TextBox:
#     def __init__(self, config):
#         self.fill = config.get("fill", [1, 1])

#     def generate(self, size, text, font):
#         width, height = size

#         char_layers, chars = [], []
#         fill = np.random.uniform(self.fill[0], self.fill[1])
#         width = np.clip(width * fill, height, width)
#         font = {**font, "size": int(height)}
#         left, top = 0, 0

#         for char in text:
#             if char in "\r\n":
#                 continue

#             char_layer = layers.TextLayer(char, **font)
#             char_scale = height / char_layer.height
#             char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
#             if char_layer.right > width:
#                 break

#             char_layers.append(char_layer)
#             chars.append(char)
#             left = char_layer.right

#         text = "".join(chars).strip()
#         if len(char_layers) == 0 or len(text) == 0:
#             return None, None

#         text_layer = layers.Group(char_layers).merge()

#         return text_layer, text

import numpy as np
from synthtiger import layers

# class TextBox:
#     def __init__(self, config):
#         self.fill = config.get("fill", [1, 1])
#         self.space_prob = config.get("space_prob", 0.0)  # 新增参数：空格插入的概率开始

#     @staticmethod
#     def is_word_boundary(char):
#         symbols = set(".,!?-:;()[]{}<>\"'`~@#$%^&*_=+|\\/")
#         return char == ' ' or char in symbols

#     def flush_text(self, char_layers, chars, left, top, width, height, text_buffer):
#         if text_buffer:
#             text = ''.join(text_buffer).strip()
#             if text:
#                 char_layer = layers.TextLayer(text, **{"size": int(height)})
#                 char_scale = height / char_layer.height
#                 char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
#                 if char_layer.right <= width:
#                     char_layers.append(char_layer)
#                     chars.append(text)
#                     left = char_layer.right
#         text_buffer.clear()
#         return left

#     def generate(self, size, reader, font):
#         width, height = size
#         char_layers, chars = [], []
#         fill = np.random.uniform(self.fill[0], self.fill[1])
#         effective_width = np.clip(width * fill, height, width)
#         font = {**font, "size": int(height)}
#         left, top = 0, 0
#         text_buffer = []

#         while True:
#             char = next(reader, None)

#             if char is None or char in "\r\n":
#                 break

#             text_buffer.append(char)

#             temp_text = ''.join(text_buffer).strip()
#             if temp_text:
#                 temp_layer = layers.TextLayer(temp_text, **font)
#                 char_scale = height / temp_layer.height
#                 temp_layer.bbox = [left, top, *(temp_layer.size * char_scale)]

#                 if temp_layer.right > effective_width:
#                     for i in reversed(range(len(text_buffer))):
#                         if self.is_word_boundary(text_buffer[i]):
#                             left = self.flush_text(char_layers, chars, left, top, width, height, text_buffer[:i + 1])
#                             text_buffer = text_buffer[i + 1:]
#                             break
#                     else:
#                         left = self.flush_text(char_layers, chars, left, top, width, height, text_buffer)
#                     break

#         self.flush_text(char_layers, chars, left, top, width, height, text_buffer)

#         if not char_layers:
#             return None, None

#         text_layer = layers.Group(char_layers).merge()

#         return text_layer, "".join(chars)
    

    # def generate(self, size, text, font):
    #     width, height = size

    #     char_layers, chars = [], []
    #     fill = np.random.uniform(self.fill[0], self.fill[1])
    #     width = np.clip(width * fill, height, width)
    #     font = {**font, "size": int(height)}
    #     left, top = 0, 0
    #     text_buffer = []
        
    #     for char in text:
    #         if char in "\r\n":
    #             continue

    #         if char == " ":
    #             # 如果是空格，直接添加空格并更新left位置
    #             chars.append(char)
    #             left += font["size"] * 0.5  # 假设空格宽度为字体大小的一半
    #             continue

    #         char_layer = layers.TextLayer(char, **font)
    #         char_scale = height / char_layer.height
    #         char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #         if char_layer.right > width:
    #             break

    #         char_layers.append(char_layer)
    #         chars.append(char)
    #         left = char_layer.right

    #         # 随机决定是否插入空格 暂时不加
    #         if np.random.rand() < self.space_prob:
    #             chars.append(" ")
    #             left += font["size"] * 0.5  # 更新left位置以留出空格空间

    #     text = "".join(chars).strip()
    #     if len(char_layers) == 0 or len(text) == 0:
    #         return None, None

    #     text_layer = layers.Group(char_layers).merge()

    #     return text_layer, text
    
    # def generate(self, size, reader, font):
    #     width, height = size

    #     char_layers, chars = [], []
    #     fill = np.random.uniform(self.fill[0], self.fill[1])
    #     width = np.clip(width * fill, height, width)
    #     font = {**font, "size": int(height)}
    #     left, top = 0, 0
    #     text_buffer = []

    #     while True:
    #         char = next(reader, None)
    #         if char is None or char in "\r\n" or char == ' ' or left + font["size"] > width:
    #             if char == ' ' or left + font["size"] > width:  # 如果是空格或超出宽度
    #                 if text_buffer:  # 如果有缓冲区中的文本
    #                     text = ''.join(text_buffer).strip()
    #                     if text:  # 如果文本非空
    #                         char_layer = layers.TextLayer(text, **font)
    #                         char_scale = height / char_layer.height
    #                         char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #                         if char_layer.right <= width:  # 检查是否适合宽度
    #                             char_layers.append(char_layer)
    #                             chars.append(text)
    #                             left = char_layer.right
    #                         else:  # 如果不适合，跳出循环
    #                             break
    #                     text_buffer.clear()  # 清空缓冲区
    #             if char is None or left + font["size"] > width:  # 如果达到末尾或超出宽度，跳出循环
    #                 break
    #             elif char == ' ':  # 如果是空格，直接跳过
    #                 continue
    #         else:
    #             text_buffer.append(char)

    #     text = "".join(chars).strip()
    #     if len(char_layers) == 0 or len(text) == 0:
    #         return None, None

    #     text_layer = layers.Group(char_layers).merge()

    #     return text_layer, text
class TextBox:
    def __init__(self, config):
        self.fill = config.get("fill", [1, 1])
        self.space_prob = config.get("space_prob", 0.00)  # 新增参数：空格插入的概率
    # def generate(self, size, reader, font):
    #     width, height = size

    #     char_layers, chars = [], []
    #     fill = np.random.uniform(self.fill[0], self.fill[1])
    #     effective_width = np.clip(width * fill, height, width)
    #     font = {**font, "size": int(height)}
    #     left, top = 0, 0
    #     text_buffer = []

    #     # 定义符号集合，用于判断是否到达符号
    #     symbols = set(".,!?-:;()[]{}<>\"'`~@#$%^&*_=+|\\/")
        
    #     while True:
    #         char = next(reader, None)

    #         if char is None or char in "\r\n":
    #             break

    #         text_buffer.append(char)

    #         # 创建临时文本层来测量当前缓冲区中的文本是否能适应文本框
    #         temp_text = ''.join(text_buffer).strip()
    #         if temp_text:
    #             temp_layer = layers.TextLayer(temp_text, **font)
    #             char_scale = height / temp_layer.height
    #             temp_layer.bbox = [left, top, *(temp_layer.size * char_scale)]

    #             # 如果文本超出了文本框宽度，则尝试找到最近的空格或符号
    #             if temp_layer.right > width:
    #                 for i in reversed(range(len(text_buffer))):
    #                     if text_buffer[i] == ' ' or text_buffer[i] in symbols:
    #                         text = ''.join(text_buffer[:i + 1]).strip()
    #                         if text:
    #                             char_layer = layers.TextLayer(text, **font)
    #                             char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #                             char_layers.append(char_layer)
    #                             chars.append(text)
    #                             left = char_layer.right
    #                             text_buffer = text_buffer[i + 1:]
    #                         break
    #                 else:  # 如果没有找到合适的分割点，则整个文本作为一块添加
    #                     text = ''.join(text_buffer).strip()
    #                     if text:
    #                         char_layer = layers.TextLayer(text, **font)
    #                         char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #                         char_layers.append(char_layer)
    #                         chars.append(text)
    #                         left = char_layer.right
    #                         text_buffer.clear()
    #                 break  # 超出宽度后退出循环

    #     # 处理剩余的文本
    #     if text_buffer:
    #         text = ''.join(text_buffer).strip()
    #         if text:
    #             char_layer = layers.TextLayer(text, **font)
    #             char_scale = height / char_layer.height
    #             char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #             if char_layer.right <= width:
    #                 char_layers.append(char_layer)
    #                 chars.append(text)

    #     if not char_layers:
    #         return None, None

    #     text_layer = layers.Group(char_layers).merge()

    #     return text_layer, "".join(chars)
    
    # def generate(self, size, reader, font):
    #     width, height = size

    #     char_layers, chars = [], []
    #     fill = np.random.uniform(self.fill[0], self.fill[1])
    #     effective_width = np.clip(width * fill, height, width)
    #     font = {**font, "size": int(height)}
    #     left, top = 0, 0
    #     text_buffer = []

    #     # 定义符号集合，用于判断是否到达符号
    #     symbols = set(".,!?-:;()[]{}<>\"'`~@#$%^&*_=+|\\/")
        
    #     # 跳过非字母字符，直到找到一个单词的开头
    #     while True:
    #         char = next(reader, None)
    #         if char is None or char.isalpha():
    #             break
    #         elif char in "\r\n":
    #             return None, None  # 如果遇到换行符，直接返回
        
    #     # 开始读取单词
    #     while True:
    #         if char is None or char in "\r\n":
    #             break
            
    #         text_buffer.append(char)

    #         # 创建临时文本层来测量当前缓冲区中的文本是否能适应文本框
    #         temp_text = ''.join(text_buffer).strip()
    #         if temp_text:
    #             temp_layer = layers.TextLayer(temp_text, **font)
    #             char_scale = height / temp_layer.height
    #             temp_layer.bbox = [left, top, *(temp_layer.size * char_scale)]

    #             # 如果文本超出了文本框宽度，则尝试找到最近的空格或符号
    #             if temp_layer.right > width:
    #                 for i in reversed(range(len(text_buffer))):
    #                     if i == 0 or text_buffer[i] == ' ' or text_buffer[i] in symbols:
    #                         text = ''.join(text_buffer[:i + 1]).strip()
    #                         if text:
    #                             char_layer = layers.TextLayer(text, **font)
    #                             char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #                             char_layers.append(char_layer)
    #                             chars.append(text)
    #                             left = char_layer.right
    #                             text_buffer = text_buffer[i + 1:]
    #                         break
    #                 else:  # 如果没有找到合适的分割点，则整个文本作为一块添加
    #                     text = ''.join(text_buffer).strip()
    #                     if text:
    #                         char_layer = layers.TextLayer(text, **font)
    #                         char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #                         char_layers.append(char_layer)
    #                         chars.append(text)
    #                         left = char_layer.right
    #                         text_buffer.clear()
    #                 break  # 超出宽度后退出循环

    #         # 继续读取下一个字符
    #         char = next(reader, None)

    #     # 处理剩余的文本
    #     if text_buffer:
    #         text = ''.join(text_buffer).strip()
    #         if text:
    #             char_layer = layers.TextLayer(text, **font)
    #             char_scale = height / char_layer.height
    #             char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #             if char_layer.right <= width:
    #                 char_layers.append(char_layer)
    #                 chars.append(text)

    #     if not char_layers:
    #         return None, None

    #     text_layer = layers.Group(char_layers).merge()

    #     return text_layer, "".join(chars)
    # def generate(self, size, reader, font):
    #     width, height = size

    #     char_layers, chars = [], []
    #     fill = np.random.uniform(self.fill[0], self.fill[1])
    #     effective_width = np.clip(width * fill, height, width)
    #     font = {**font, "size": int(height)}
    #     left, top = 0, 0
    #     text_buffer = []

    #     # 定义符号集合，用于判断是否到达符号
    #     symbols = set(".,!?-:;()[]{}<>\"'`~@#$%^&*_=+|\\/")

    #     while True:
    #         char = next(reader, None)

    #         if char is None or char in "\r\n":
    #             break

    #         text_buffer.append(char)

    #         # 创建临时文本层来测量当前缓冲区中的文本是否能适应文本框
    #         temp_text = ''.join(text_buffer).strip()
    #         if temp_text:
    #             temp_layer = layers.TextLayer(temp_text, **font)
    #             char_scale = height / temp_layer.height
    #             temp_layer.bbox = [left, top, *(temp_layer.size * char_scale)]

    #             # 如果文本超出了文本框宽度，则尝试找到最近的空格或符号
    #             if temp_layer.right > width:
    #                 for i in reversed(range(len(text_buffer))):
    #                     if text_buffer[i] == ' ' or (i < len(text_buffer) - 1 and text_buffer[i] in symbols):
    #                         text = ''.join(text_buffer[:i + 1])  # 包含分割点字符（空格或符号）
    #                         if text.strip():  # 确保不是纯空白
    #                             char_layer = layers.TextLayer(text, **font)
    #                             char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #                             char_layers.append(char_layer)
    #                             chars.append(text)
    #                             left = char_layer.right
    #                             text_buffer = text_buffer[i + 1:]
    #                         break
    #                 else:  # 如果没有找到合适的分割点，则整个文本作为一块添加
    #                     text = ''.join(text_buffer)
    #                     if text.strip():
    #                         char_layer = layers.TextLayer(text, **font)
    #                         char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #                         char_layers.append(char_layer)
    #                         chars.append(text)
    #                         left = char_layer.right
    #                         text_buffer.clear()
    #                 break  # 超出宽度后退出循环

    #         # 如果当前字符是空格或者符号，并且后面还有内容，检查是否需要开始新的文本块
    #         if char in ' ' or char in symbols:
    #             temp_text = ''.join(text_buffer)
    #             if temp_text:
    #                 temp_layer = layers.TextLayer(temp_text, **font)
    #                 char_scale = height / temp_layer.height
    #                 temp_layer.bbox = [left, top, *(temp_layer.size * char_scale)]

    #                 if temp_layer.right <= width:
    #                     char_layers.append(temp_layer)
    #                     chars.append(temp_text)
    #                     left = temp_layer.right
    #                     text_buffer.clear()

    #     # 处理剩余的文本
    #     if text_buffer:
    #         text = ''.join(text_buffer)
    #         if text.strip():
    #             char_layer = layers.TextLayer(text, **font)
    #             char_scale = height / char_layer.height
    #             char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
    #             if char_layer.right <= width:
    #                 char_layers.append(char_layer)
    #                 chars.append(text)

    #     if not char_layers:
    #         return None, None

    #     text_layer = layers.Group(char_layers).merge()

    #     return text_layer, "".join(chars)
    def generate(self, size, reader, font):
        width, height = size

        char_layers, chars = [], []
        fill = np.random.uniform(self.fill[0], self.fill[1])
        effective_width = np.clip(width * fill, height, width)
        font = {**font, "size": int(height)}
        left, top = 0, 0
        text_buffer = []

        # 定义符号集合，用于判断是否到达符号
        symbols = set(".,!?-:;()[]{}<>\"'`~@#$%^&*_=+|\\/")

        while True:
            char = next(reader, None)

            if char is None or char in "\r\n":
                break

            text_buffer.append(char)

            # 创建临时文本层来测量当前缓冲区中的文本是否能适应文本框
            temp_text = ''.join(text_buffer).strip()
            if temp_text:
                temp_layer = layers.TextLayer(temp_text, **font)
                char_scale = height / temp_layer.height
                temp_layer.bbox = [left, top, *(temp_layer.size * char_scale)]

                # 如果文本超出了文本框宽度，则尝试找到最近的空格或符号
                if temp_layer.right > width:
                    for i in reversed(range(len(text_buffer))):
                        if text_buffer[i] == ' ' or (i < len(text_buffer) - 1 and text_buffer[i] in symbols):
                            # 包含分割点字符（空格或符号），并确保不是纯空白
                            text = ''.join(text_buffer[:i + 1]).strip()
                            if text:
                                char_layer = layers.TextLayer(text, **font)
                                char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
                                char_layers.append(char_layer)
                                chars.append(text)
                                left = char_layer.right
                                text_buffer = text_buffer[i + 1:]
                            break
                    else:  # 如果没有找到合适的分割点，则整个文本作为一块添加
                        text = ''.join(text_buffer).strip()
                        if text:
                            char_layer = layers.TextLayer(text, **font)
                            char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
                            char_layers.append(char_layer)
                            chars.append(text)
                            left = char_layer.right
                            text_buffer.clear()
                    break  # 超出宽度后退出循环

            # 如果当前字符是空格或者符号，并且后面还有内容，检查是否需要开始新的文本块
            elif char in ' ' or char in symbols:
                temp_text = ''.join(text_buffer).strip()
                if temp_text:
                    temp_layer = layers.TextLayer(temp_text, **font)
                    char_scale = height / temp_layer.height
                    temp_layer.bbox = [left, top, *(temp_layer.size * char_scale)]

                    if temp_layer.right <= width:
                        char_layers.append(temp_layer)
                        chars.append(temp_text.strip())
                        left = temp_layer.right
                        text_buffer.clear()

        # 处理剩余的文本
        if text_buffer:
            text = ''.join(text_buffer).strip()
            if text:
                char_layer = layers.TextLayer(text, **font)
                char_scale = height / char_layer.height
                char_layer.bbox = [left, top, *(char_layer.size * char_scale)]
                if char_layer.right <= width:
                    char_layers.append(char_layer)
                    chars.append(text)

        if not char_layers:
            return None, None

        text_layer = layers.Group(char_layers).merge()

        return text_layer, "".join(chars)
    
# import numpy as np
# from synthtiger import layers
# import re


# class TextBox:
#     def __init__(self, config):
#         self.fill = config.get("fill", [1, 1])

#     def generate(self, size, text, font):
#         width, height = size

#         char_layers, chars = [], []
#         fill = np.random.uniform(self.fill[0], self.fill[1])
#         adjusted_width = np.clip(width * fill, height, width)
#         font = {**font, "size": int(height)}
#         left, top = 0, 0

#         words = re.findall(r'\S+|\s+', text)  # 按照单词和空格分隔符分割文本

#         for word in words:
#             if word.isspace():
#                 # 如果是空格，直接添加空格并更新left位置
#                 chars.append(word)
#                 left += font["size"] * 0.5  # 假设空格宽度为字体大小的一半
#                 continue

#             word_layer = layers.TextLayer(word, **font)
#             word_scale = height / word_layer.height
#             word_layer.bbox = [left, top, *(word_layer.size * word_scale)]

#             if word_layer.right > adjusted_width:
#                 break  # 如果当前单词超出宽度限制，则停止添加字符

#             char_layers.append(word_layer)
#             chars.append(word)
#             left = word_layer.right

#         text = "".join(chars).strip()
#         if len(char_layers) == 0 or len(text) == 0:
#             return None, None

#         text_layer = layers.Group(char_layers).merge()

#         return text_layer, text