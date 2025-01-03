"""
Donut
Copyright (c) 2022-present NAVER Corp.
MIT License
"""
import numpy as np
from synthtiger import components

from elements.content_inter import Content
from elements.paper import Paper


class Document_inter:
    def __init__(self, config):
        self.fullscreen = config.get("fullscreen", 0.5)
        self.landscape = config.get("landscape", 0.5)
        self.short_size = config.get("short_size", [480, 1024])
        self.text_count_config = config.get("text_count", {"min": 2, "max": 50}) 
        self.aspect_ratio = config.get("aspect_ratio", [1, 2])
        self.paper = Paper(config.get("paper", {}))
        self.content = Content(config.get("content", {}))
        self.effect = components.Iterator(
            [
                components.Switch(components.ElasticDistortion()),
                components.Switch(components.AdditiveGaussianNoise()),
                components.Switch(
                    components.Selector(
                        [
                            components.Perspective(),
                            components.Perspective(),
                            components.Perspective(),
                            components.Perspective(),
                            components.Perspective(),
                            components.Perspective(),
                            components.Perspective(),
                            components.Perspective(),
                        ]
                    )
                ),
            ],
            **config.get("effect", {}),
        )

    def generate(self, size, num_texts=None):
        width, height = size
        fullscreen = np.random.rand() < self.fullscreen

        if not fullscreen:
            landscape = np.random.rand() < self.landscape
            max_size = width if landscape else height
            short_size = np.random.randint(
                min(width, height, self.short_size[0]),
                min(width, height, self.short_size[1]) + 1,
            )
            aspect_ratio = np.random.uniform(
                min(max_size / short_size, self.aspect_ratio[0]),
                min(max_size / short_size, self.aspect_ratio[1]),
            )
            long_size = int(short_size * aspect_ratio)
            size = (long_size, short_size) if landscape else (short_size, long_size)
        # # 如果没有提供num_texts，则根据配置随机决定文本数量
        # if num_texts is None:
        #     num_texts = np.random.randint(self.text_count_config['min'], self.text_count_config['max'] + 1)
            
        text_layers, texts = self.content.generate(size, num_texts=num_texts)
        paper_layer = self.paper.generate(size)
        self.effect.apply([*text_layers, paper_layer])

        return paper_layer, text_layers, texts
