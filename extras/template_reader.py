from string import Template


def parse_template(file_name):
    with open('Blog/message_temp.txt', 'r', encoding='utf-8') as msg_template:
        msg_template_content = msg_template.read()
    return Template(msg_template_content)