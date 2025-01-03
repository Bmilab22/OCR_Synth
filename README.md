# 合成OCR数据

## 数据介绍

数据构成：
- 图片可选：ImageNet, COCO(2017，2014)。
- 文字可选：万卷(大规模)，wiki，自定义词典。
- 案例生成采用：文档(A4空白文档)，场景OCR采用COCO train2017，文本采用自定义词典和wiki数据。
- 大规模训练：文档(A4空白文档)，场景OCR采用COCO train2017，文本采用万卷数据，小语种采用多语言文本数据。

数据类型: Image-Text pair，共八种合成数据类型
- 场景文本样例(标准英文) 
- 场景文本特殊样例(多行英文)  
- 单栏，双栏，混合文档(英文)  
- 场景文本样例(标准中文)  
- 场景文本特殊样例(多行中文)   
- 单栏，双栏，混合文档(中文) 
- 小语种 (七种语言)
- 单栏，双栏，混合文档(中英文混合) 
结果jsonl文件：包含图像路径，图像中每个text对应bboxs，阅读顺序(order)，页面(page_bbox)。

方法和质量控制：
1. 图像背景生成：利用imageNet和COCO的img文件作为background以保证背景的多样性
     背景策略：background,document和paper模块
2. 场景文本生成：使用万卷，wiki以及自定义文本数据集以保证文本的多样性
     文本策略：textbox，layout和content生成控制模块
3. 质量控制
- 文本框和文本字符数量控制。
- 增加文字变形功能，包含波浪形，弧形以及随机曲线几何变换。
- 增加随机文字旋转，模糊生成。
- 改进文字密度(增大文字框填充比例，文字数量)，固定分辨率，减少内容效果的强度，修改文字生成逻辑(之前缺少对于空格和OCR结果分割的处理)。
- 改良单词截断算法，主要用于场景文本OCR(英文)生成。
4. 合成模板
template_ori，template_special和template_paper分别用于生成场景文本的标准数据，生成场景文本的特殊情况数据以及生成场景文本的文档数据。

数据生产速度：对于每种类型在S集群上单卡速度约 0.5M/24h。

## 数据生产代码

1. 配置[Synthdog](https://github.com/wangbinDL/SynthDog_SmarkDoc)的环境,或者配置synthtiger(pip install synthtiger)。

2. 构建划分好的数据路径文件夹list 如WebText-zh-list-split(00-05)

3. 运行数据合成脚本
```shell
conda activate Synthdog
srun -p bigdata_alg  --cpus-per-task=32 --mem=1000000 bash run_en_paper.sh WebText-en-list-split01.txt    #示例运行代码-单栏，双栏，混合文档(英文)  
srun -p bigdata_alg  --cpus-per-task=32 --mem=1000000 bash run_zh_paper.sh WebText-zh-list-split01.txt    #示例运行代码-单栏，双栏，混合文档(中文) 
```
模型的子结果保存在对应生成的子文件夹下，包含metadata.jsonl，metadata_order.jsonl和metadata_page.jsonl的结果，其中metadata_page包含了页面和阅读顺序信息。

4. 数据处理
- json_tool_merge.py脚本，用于合并不同数据路径文件的metadata_page.jsonl结果，保存全部数据的最终jsonl结果。

```shell
python json_tool_merge.py
```

- merge_en_cn.py脚本，用于生成中英文混合的TxT合成文件。
```shell
python merge_en_cn.py
```

5. 数据可视化检查

数据可视化检查的测试代码在`draw_bbox.py`中。

```shell
python draw_bbox.py
```


