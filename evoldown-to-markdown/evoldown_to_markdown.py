# 引入正则表达式库
import re
# 引入系统操作库
import os
# 引入lxml处理svg代码
from lxml import etree
# 引入模板引擎
from jinja2 import Template

# 定义段落类型与对应svg图标的映射关系
icon_svg_filename = {
    '#d': 'Description',
    '#e': 'Example',
    '#t': 'Transfer',
    '#c': 'Custom',
    '#v': 'Verification',
    '#a': 'Advertisement'
}

# 定义段落svg图标的参数
icon_svg_changes = {
    'fill': 'currentColor',  # 使用当前文字的颜色填充
    'width': '2em',  # 宽度是文字大小的两倍
    'height': '2em'  # 高度是文字大小的两倍
}

# 定义段落类型与对应hsl()颜色的映射关系
card_color = {
    '#d': '200 72% 50%',
    '#e': '0 72% 50%',
    '#t': '50 72% 50%',
    '#c': '0 0% 50%',
    '#v': '260 72% 50%',
    '#a': '300 72% 50%'
}


# f-string 是 Python3.6 引入的一种新的字符串格式化方式，
# 它允许在字符串中插入变量值或表达式结果，
# 使用 {} 括起来，并在字符串前面加上 f 或 F。
# 获取本项目svg文件夹里的SVG图标的源代码,并更改样式
def extract_modify_svg_content(svg_filename, svg_changes):
    """
    从SVG文件中提取并修改内容。

    Parameters:
        svg_filename (str): SVG文件名。
        svg_changes: 变化参数

    Returns:
        str_content: 修改后的SVG内容。

    """
    # 构建SVG文件的路径
    svg_path = os.path.join('svg', f'{svg_filename}.svg')
    # 打开SVG文件并读取内容
    with open(svg_path, 'r', encoding='utf-8') as svg_file:
        svg_code = svg_file.read()
    # 将 Unicode 字符串转换为字节字符串
    svg_bytes = svg_code.encode('utf-8')
    # 使用 lxml 解析 SVG 文件
    svg_root = etree.fromstring(svg_bytes)
    # 修改svg的属性
    for key, value in svg_changes.items():
        svg_root.attrib[key] = value
    # 获取 <svg> 标签内的内容
    svg_content = etree.tostring(svg_root, encoding="unicode")
    return svg_content


# 该函数的输入参数是evoldown文件的位置和输出的markdown文件位置
def convert_evoldown_to_markdown(evoldown_file, markdown_file):
    """
    将Evoldown格式转换为Markdown格式。

    Parameters:
        evoldown_file (str): 输入的Evoldown文件位置。
        markdown_file (str): 输出的Markdown文件位置。
    """
    # 以utf-8格式读取evoldown文件给file对象，然后把内容保存到evoldown_text里面，
    with open(evoldown_file, 'r', encoding='utf-8') as input_file:
        evoldown_text = input_file.read()
        # print(evoldown_text)

    # raw string 是一种特殊的字符串，它以 r 或 R 开头，并且对反斜杠 \ 不进行转义处理。
    # 正则表达式匹配：学习材料的类型，学习材料的关键词，关联的学习材料。
    pattern = r'(#[detva])( \S+)( \S+)?'
    # 正则表达式匹配：学习材料的类型、自定义的学习材料的类型、学习材料的关键词、关联的学习材料。
    pattern_c = r'(#c)( \S+)( \S+)( \S+)?'

    # 提取根据表达式提取内容
    matches = re.findall(pattern, evoldown_text)
    matches_c = re.findall(pattern_c, evoldown_text)
    dict_matches = {}
    dict_matches_c = {}
    # 遍历 matches，将关键词和材料类型添加到字典中
    for match in matches:
        material_type, keywords, associated_keyword = match
        dict_matches[keywords] = material_type
    # 遍历 matches_c，将关键词、材料类型和自定义类型添加到字典中
    for match_c in matches_c:
        material_type, custom_type, keywords, associated_keyword = match_c
        dict_matches_c[keywords] = [material_type, custom_type]

    # print(matches)
    # print(matches_c)
    # print(dict_matches)
    # print(dict_matches_c)

    def find_associated_type(key):
        # 首先在 dict_matches 中查找关键字
        if key in dict_matches:
            return [dict_matches[key], None]
        # 如果在 dict_matches 中未找到，则在 dict_matches_c 中查找
        elif key in dict_matches_c:
            return dict_matches_c[key]

    # 段落文本标记替换成HTML代码
    new_markdown_text = evoldown_text

    # 定义段落标记 HTML 模板
    tag_html_template = """
<div style="display: flex; flex-direction: row; align-items: center;">
{{ material_card }}
{{ find_associated_svg }}
{{ associated_card }}
</div>
    """
    # 定义卡片 HTML 模板
    card_html_template = """<span style="display: flex; flex-direction: row; align-items: center; color: hsl({{ color_value }}); background-color: hsl({{ color_value }}/0.08); padding: 0 0.4em; border-radius: 0.4em;; line-height: 2.5em">
<span style="display: flex; flex-direction: row; align-items: center; margin-right: 0.4em; ">
{{ svg_code }}
{% if custom_type %}
<span style="">{{ custom_type }} |</span>
{% endif %}
</span>
{{ keywords }}
</span>
    """

    # 创建 Jinja2 模板对象
    tag_template = Template(tag_html_template)
    card_template = Template(card_html_template)

    """  翻译参考
    Learning material tags, learning material types,
    learning material type cards, custom learning material types,
    learning material keywords, associated_keyword learning materials. No association found
    学习材料标记、学习材料的类型、学习材料类型卡、自定义的学习材料的类型、学习材料的关键词、关联的学习材料。未发现关联
    """
    # d、e、t、v、a类型段落标记替换成HTML代码
    for match in matches:
        # print(match)
        # 段落标签内容
        material_type, keywords, associated_keyword = match
        # 段落卡片数据
        material_card = card_template.render(
            color_value=card_color[material_type],
            svg_code=extract_modify_svg_content(icon_svg_filename[material_type], icon_svg_changes),
            keywords=keywords.strip(),
        )
        # 关联段落卡片数据
        if associated_keyword:
            associated_types = find_associated_type(associated_keyword)
            if associated_types:
                associated_type = associated_types[0]
                associated_custom_type = associated_types[1]
                associated_card = card_template.render(
                    color_value=card_color[associated_type],
                    svg_code=extract_modify_svg_content(icon_svg_filename[associated_type], icon_svg_changes),
                    custom_type=associated_custom_type,
                    keywords=associated_keyword
                )
                find_associated_svg = extract_modify_svg_content('Associated', icon_svg_changes)
            else:
                associated_card = card_template.render(
                    color_value='0 0% 70%',
                    keywords=associated_keyword
                )
                find_associated_svg = extract_modify_svg_content('NotFoundAssociated', icon_svg_changes)
        else:
            associated_card = ''
            find_associated_svg = ''

        tag_html_code = tag_template.render(
            material_card=material_card,
            find_associated_svg=find_associated_svg,
            associated_card=associated_card,
        )

        # print(tag_html_code)
        new_markdown_text = new_markdown_text.replace(
            f'\n{material_type}{keywords}{associated_keyword}\n', tag_html_code)

    # c类型段落标记替换成HTML代码
    for match_c in matches_c:
        # print(match_c)
        material_type, custom_type, keywords, associated_keyword = match_c
        # 段落卡片数据
        material_card = card_template.render(
            color_value=card_color[material_type],
            svg_code=extract_modify_svg_content(icon_svg_filename[material_type], icon_svg_changes),
            custom_type=custom_type,
            keywords=keywords.strip(),
        )
        # 关联段落卡片数据
        if associated_keyword:
            associated_types = find_associated_type(associated_keyword)
            if associated_types:
                associated_type = associated_types[0]
                associated_custom_type = associated_types[1]
                associated_card = card_template.render(
                    color_value=card_color[associated_type],
                    svg_code=extract_modify_svg_content(icon_svg_filename[associated_type], icon_svg_changes),
                    custom_type=associated_custom_type,
                    keywords=associated_keyword
                )
                find_associated_svg = extract_modify_svg_content('Associated', icon_svg_changes)
            else:
                associated_card = card_template.render(
                    color_value='0 0% 70%',
                    keywords=associated_keyword
                )
                find_associated_svg = extract_modify_svg_content('NotFoundAssociated', icon_svg_changes)
        else:
            associated_card = ''
            find_associated_svg = ''

        tag_html_code = tag_template.render(
            material_card=material_card,
            find_associated_svg=find_associated_svg,
            associated_card=associated_card,
        )
        # print(tag_html_code)
        new_markdown_text = new_markdown_text.replace(
            f'\n{material_type}{custom_type}{keywords}{associated_keyword}\n', tag_html_code)

    # print(new_markdown_text)

    # 将生成的HTML代码发送给output_file,以UTF-8格式保存到新的Markdown文件中
    with open(markdown_file, 'w', encoding='utf-8') as output_file:
        output_file.write(new_markdown_text)


# 测试
convert_evoldown_to_markdown(r'markdown\example.md', r'markdown\example_output.md')
