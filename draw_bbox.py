# from PIL import Image, ImageDraw, ImageFont
# import json
# import os

# def draw_bboxes_on_image(image_filepath, ocr_data, page_bbox=None, output_filepath=None):
#     # Load the image
#     image = Image.open(image_filepath)
#     draw = ImageDraw.Draw(image)

#     # Define a font for the text (you may need to adjust the path and size according to your system)
#     try:
#         font = ImageFont.truetype("/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/resources/font/cn_en/经典宋体简.TTF", 20)  # Adjust the path if necessary
#     except IOError:
#         font = ImageFont.load_default()  # Use default font if specified font is not available

#     # Draw each bbox and its corresponding text
#     for item in ocr_data:
#         coords = item['coords']
#         text = item['text']
#         order = item.get('order', '')  # Get the order if it exists

#         # Draw the rectangle
#         draw.rectangle(coords, outline="red", width=2)

#         # Draw the text next to or above the rectangle
#         text_position = (coords[0], coords[1] - 25) if coords[1] > 25 else (coords[0], coords[3])
#         draw.text(text_position, f"{order}: {text}", fill="blue", font=font)

#     # If provided, draw the page_bbox as well
#     if page_bbox:
#         # Ensure page_bbox values are integers
#         page_bbox_int = [int(coord) for coord in page_bbox]
#         draw.rectangle(page_bbox_int, outline="green", width=4)  # Use green color and thicker line for page_bbox

#         # Optionally, add a label to indicate this is the page_bbox
#         draw.text((page_bbox_int[0], page_bbox_int[1] - 25), "Page BBox", fill="green", font=font)

#     # Save the modified image
#     if output_filepath is None:
#         output_filepath = os.path.join(os.path.dirname(image_filepath), "annotated_" + os.path.basename(image_filepath))
    
#     image.save(output_filepath)
#     print(f"Annotated image saved to: {output_filepath}")

# # Provided JSON string with corrected format
# json_string = 

# # Extract OCR data and page_bbox from the provided JSON structure
# ocr_data = json_string['ground_truth']['ocr']
# page_bbox = json_string.get('page_bbox')

# # Set the correct image file path
# image_filepath = json_string['image_filepath']

# # Call the function to draw bboxes on the image including the page_bbox
# draw_bboxes_on_image(image_filepath, ocr_data, page_bbox)

from PIL import Image, ImageDraw, ImageFont
import json
import os
def draw_bboxes_on_image(image_filepath, ocr_data, page_bbox=None, output_filepath=None):
    # Load the image
    image = Image.open(image_filepath)
    draw = ImageDraw.Draw(image)

    # Define a font for the text (you may need to adjust the path and size according to your system)
    try:
        font = ImageFont.truetype("/mnt/petrelfs/zhujiawei/Projects/donut-master/synthdog/resources/font/cn_en/经典宋体简.TTF", 20)  # Adjust the path if necessary
    except IOError:
        font = ImageFont.load_default()  # Use default font if specified font is not available

    # Draw each bbox and its corresponding text
    for item in ocr_data:
        coords = item['coords']
        text = item['text']
        order = item.get('order', '')  # Get the order if it exists

        # Draw the rectangle
        draw.rectangle(coords, outline="red", width=2)

        # Draw the text next to or above the rectangle
        text_position = (coords[0], coords[1] - 25) if coords[1] > 25 else (coords[0], coords[3])
        draw.text(text_position, f"{order}: {text}", fill="blue", font=font)

    # If provided, draw the page_bbox as well
    if page_bbox:
        # Ensure page_bbox values are integers
        page_bbox_int = [int(coord) for coord in page_bbox]
        draw.rectangle(page_bbox_int, outline="green", width=4)  # Use green color and thicker line for page_bbox

        # Optionally, add a label to indicate this is the page_bbox
        draw.text((page_bbox_int[0], page_bbox_int[1] - 25), "Page BBox", fill="green", font=font)

    # Save the modified image
    if output_filepath is None:
        output_filepath = os.path.join(os.path.dirname(image_filepath), "annotated_" + os.path.basename(image_filepath))
    
    image.save(output_filepath)
    print(f"Annotated image saved to: {output_filepath}")

# Provided JSON string with corrected format
json_string = '{"ground_truth": "{\"gt_parse\": {\"text_sequence\": {\"ocr\": [{\"coords\": [29, 45, 219, 77], \"text\": \"面积：10700平方米\"}, {\"coords\": [29, 77, 385, 109], \"text\": \":A-Level地址：东莞市南城街道蛤地\"}, {\"coords\": [29, 143, 225, 175], \"text\": \"东莞市海德双语学校\"}, {\"coords\": [467, 212, 641, 244], \"text\": \"学校档案占地面积\"}, {\"coords\": [334, 270, 654, 291], \"text\": \"学位：可提供约5000个学位 开设课程：A-Level/DP\"}]}}}", "image_filepath": "./outputs_zh/part-000036-4fcc5597/image_10.jpg"}'

# Parse the JSON string
data = json.loads(json_string)

# Extract OCR data from the provided JSON structure
# The ground_truth field contains an escaped JSON string, so we need to parse it again.
ground_truth = json.loads(data['ground_truth'])
ocr_data = ground_truth['gt_parse']['text_sequence']['ocr']

# Set the correct image file path
image_filepath = data['image_filepath']

# Set the output file path
output_filepath = os.path.join(os.path.dirname(image_filepath), "annotated_" + os.path.basename(image_filepath))

# Call the function to draw bboxes on the image
draw_bboxes_on_image(image_filepath, ocr_data, output_filepath=output_filepath)

# import json

# # 原始JSON字符串
# json_string = '{"image_filepath": "./outputs_en_cn_paper/image_3.jpg", "ground_truth": "{"gt_parse": {"text_sequence": "{\\"ocr\\": [{\\"coords\\": [99, 152, 527, 193], \\"text\\": \\"er sites, and must sign a\\", \\"order\\": 1},                                cccccccccccccccccccccc {\\"coords\\": [640, 1464, 1344, 1505], \\"text\\": \\"展PB业务发展机遇,\\", \\"order\\": 66}]}}"}'

# # 第一步：解析最外层的JSON字符串
# data = json.loads(json_string)

# # 第二步：解析'ground_truth'中的JSON字符串，同时修正转义字符问题
# ground_truth = json.loads(data['ground_truth'])

# # 第三步：解析'text_sequence'中的JSON字符串，同样修正转义字符问题
# text_sequence = json.loads(ground_truth['gt_parse']['text_sequence'])

# # 将解析后的数据放回原位置
# ground_truth['gt_parse']['text_sequence'] = text_sequence['ocr']
# data['ground_truth'] = ground_truth

# # 打印出处理后的数据结构，确认是否符合预期
# print(json.dumps(data, ensure_ascii=False, indent=2))

# from PIL import Image, ImageDraw, ImageFont
# import json
# import os

# def draw_bboxes_on_image(image_filepath, ocr_data, output_filepath):
#     # Load the image
#     image = Image.open(image_filepath)
#     draw = ImageDraw.Draw(image)

#     # Define a font for the text (you may need to adjust the path and size according to your system)
#     try:
#         font = ImageFont.truetype("arial.ttf", 20)  # Adjust the path if necessary
#     except IOError:
#         font = ImageFont.load_default()  # Use default font if Arial is not available

#     # Draw each bbox and its corresponding text
#     for item in ocr_data:
#         coords = item['coords']
#         text = item['text']
#         order = item.get('order', '')  # Get the order if it exists

#         # Draw the rectangle
#         draw.rectangle(coords, outline="red", width=2)

#         # Draw the text next to the rectangle or above it
#         text_position = (coords[0], coords[1] - 25) if coords[1] > 25 else (coords[0], coords[3])  # Above or next to the bbox
#         draw.text(text_position, f"{order}: {text}", fill="blue", font=font)

#     # Save the modified image
#     image.save(output_filepath)

# # Provided JSON object with corrected format
# json_object = {"image_filepath": "./outputs_en_cn_paper/image_4.jpg", "ground_truth": {"ocr": [{"coords": [57, 187, 935, 255], "text": "||$219.99||$219.99| Copy the following string", "order": 1}, {"coords": [60, 229, 895, 307], "text": "into an e-mail to support@ultrarob.com to", "order": 2}, {"coords": [61, 278, 854, 352], "text": "request support.11月8日，威尼斯官网招标受", "order": 3}, {"coords": [63, 326, 832, 397], "text": "邀到昆明钢铁集团有限责任公司进行《中华人", "order": 4}, {"coords": [64, 370, 829, 445], "text": "民共和国招标投标法实施条例（2019年修订）", "order": 5}, {"coords": [66, 421, 880, 487], "text": "》的法律法规专题培训授课。 省建设工程招标投", "order": 6}, {"coords": [67, 468, 822, 529], "text": "标行业协会专家委员会委员、威尼斯官网招标", "order": 7}, {"coords": [1018, 220, 1238, 275], "text": "总工程师杨斌", "order": 8}, {"coords": [1014, 267, 1268, 321], "text": "从法律法规层面", "order": 9}, {"coords": [1009, 313, 1262, 366], "text": "、典型案例分析", "order": 10}, {"coords": [1005, 358, 1256, 410], "text": "的角度，对新修", "order": 11}, {"coords": [1000, 403, 1215, 452], "text": "订的《招标投", "order": 12}, {"coords": [996, 448, 1209, 494], "text": "标法实施条例", "order": 13}, {"coords": [992, 491, 1204, 538], "text": "》内容进行了", "order": 14}, {"coords": [71, 588, 1095, 646], "text": "深度剖析和细致讲解。昆钢集团领导对本次培训内容及讲解分析", "order": 15}, {"coords": [72, 632, 1225, 689], "text": "给予了高度评价，并要求把培训的内容切实运用到实际工作中，依法依规", "order": 16}, {"coords": [73, 676, 1203, 729], "text": "做好各项招采工作。 本次培训，威尼斯官网招标向昆钢集团展现了公司", "order": 17}, {"coords": [75, 720, 1115, 769], "text": "在招标投标领域的专业性、系统性。同时，也展示了威澳门尼斯人", "order": 18}, {"coords": [76, 763, 1059, 808], "text": "娱乐场在招采管理过程中的严谨性、科学性和高效性。 威尼斯", "order": 19}, {"coords": [77, 805, 1171, 847], "text": "官网招标在做好市场化服务和集团内基础协同、降本增效、监督抓手作", "order": 20}, {"coords": [79, 846, 1133, 887], "text": "用功能平台的同时，通过提供专业培训，展现了公司的良好形象，扩", "order": 21}, {"coords": [80, 887, 1193, 928], "text": "大了公司的影响力，也为公司向全过程工程咨询服务转型、由单一业务经", "order": 22}, {"coords": [81, 925, 976, 969], "text": "营向服务链前后延伸、价值服务提供了有力宣传。 昆钢集", "order": 23}, {"coords": [83, 964, 1118, 1005], "text": "团领导班子、本部全体中层管理人员、直属机关科级管理人员以及各", "order": 24}, {"coords": [84, 1000, 1113, 1048], "text": "二级单位领导班子和党群纪检部门负责人参加培训，采取视频现场连", "order": 25}, {"coords": [85, 1036, 1157, 1087], "text": "线方式，共计1000余人参加培训。Bayshore Community Hospital, Holm", "order": 26}, {"coords": [86, 1074, 1057, 1125], "text": "del, has announced Carol Hundsrucker, RN, has been named", "order": 27}, {"coords": [87, 1110, 1069, 1163], "text": "the winner of the 2003 Nurse of the Year Award. Hundsrucke", "order": 28}, {"coords": [91, 1224, 1074, 1285], "text": "r is nursing care coordinator for the endoscopy unit. S", "order": 29}, {"coords": [96, 1407, 347, 1436], "text": "he was nominated by Jacqu", "order": 30}, {"coords": [402, 1384, 997, 1425], "text": "eline Earle, CNN nursing technician, and commented she never wa", "order": 31}, {"coords": [101, 1555, 331, 1582], "text": "nted to be anything other than a nu", "order": 32}, {"coords": [366, 1527, 987, 1570], "text": "rse. "I strongly urge anyone interested in this field to follow their instincts, follow their dream,", "order": 33}]}}


# # Extract OCR data from the provided JSON structure
# ocr_data = json_object['ground_truth']['ocr']

# # Set the correct image file path
# image_filepath = json_object['image_filepath']

# # Set the output file path
# output_filepath = os.path.join(os.path.dirname(image_filepath), "annotated_" + os.path.basename(image_filepath))

# # Call the function to draw bboxes on the image
# draw_bboxes_on_image(image_filepath, ocr_data, output_filepath)

# print(f"Annotated image saved to: {output_filepath}")