import re

def clean_novel(input_file, output_file):
    """
    对 TXT 小说文件进行优化和整理。
    :param input_file: 输入文件路径
    :param output_file: 输出文件路径
    """
    try:
        # 尝试用 UTF-8 读取，失败后尝试 GBK
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            with open(input_file, 'r', encoding='gbk') as file:
                content = file.read()

        # 仅删除不符合特定标点符号后的换行符
        # 匹配中英文句号、省略号、引号、冒号后的换行符并保留
        # 同时保留可能是标题行的换行符（行长度短且无标点符号）
        lines = content.split('\n')
        new_content = []
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:  # 跳过空行
                continue
                
            # 判断是否要保留换行符
            # 更智能的标题行判断条件
            is_title = (
                (len(line) < 30  # 行长度较短
                and not re.search(r'[。.……\"\'“”‘’：:]$', line)  # 不以标点符号结尾
                and re.search(r'[章节回集卷部篇]', line)  # 包含常见标题关键词
                and not re.search(r'[0-9]', line)  # 不包含数字（避免误判）
                and not re.search(r'[\[\](){}<>]', line))  # 不包含特殊符号
                or (len(line) < 10  # 行长度非常短
                and not re.search(r'[。.……\"\'“”‘’：:]$', line))  # 不以标点符号结尾
            )
            if is_title:
                new_content.append('\n' + line + '\n\n')  # 标题行前后各加一个换行
            elif re.search(r'[。.……\"\'“”‘’：:]$', line):
                new_content.append(line + '\n')  # 标点结尾保留换行
            else:
                new_content.append(line)
                # 如果不是最后一行且下一行不需要换行，则加空格
                if i < len(lines)-1 and lines[i+1].strip() and \
                   not (len(lines[i+1].strip()) < 30 and not re.search(r'[。.……\"\'“”‘’：:]$', lines[i+1].strip())) and \
                   not re.search(r'[。.……\"\'“”‘’：:]$', lines[i+1].strip()):
                    new_content.append(' ')
        content = ''.join(new_content)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"小说整理完成，结果已保存到 {output_file}")

    except FileNotFoundError:
        print("错误：输入文件未找到，请检查路径。")
    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='对 TXT 小说文件进行优化和整理。')
    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('output', help='输出文件路径')
    args = parser.parse_args()
    clean_novel(args.input, args.output)