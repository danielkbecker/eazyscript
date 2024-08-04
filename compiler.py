import re


class Node:
    def __init__(self, node_type, value=None):
        self.type = node_type
        self.value = value
        self.children = []


def tokenize(input_code):
    tokens = []
    token_spec = [
        ('NUMBER', r'\d+(\.\d*)?'),
        ('ASSIGN', r':'),
        ('ID', r'[A-Za-z]+'),
        ('STRING', r'"[^"]*"'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_spec)
    for match_obj in re.finditer(tok_regex, input_code):
        kind = match_obj.lastgroup
        value = match_obj.group()
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'STRING':
            value = value.strip('"')
        elif kind == 'ID' and value in (
                'application', 'layout', 'component', 'var', 'text', 'onClick', 'css', 'state', 'event', 'query'):
            kind = value.upper()
        elif kind == 'SKIP':
            continue
        elif kind == 'NEWLINE':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected')
        tokens.append((kind, value))
    return tokens


def parse(tokens):
    def parse_application(tokns):
        node = Node('APPLICATION')
        while tokns:
            current_token = tokns.pop(0)
            if current_token[0] == 'LAYOUT':
                node.children.append(parse_layout(tokns))
            elif current_token[0] == 'COMPONENT':
                node.children.append(parse_component(tokns))
            elif current_token[0] == 'VAR':
                node.children.append(parse_var(tokns))
        return node

    def parse_layout(tokns):
        node = Node('LAYOUT')
        while tokns:
            current_token = tokns.pop(0)
            if current_token[0] == 'COMPONENT':
                node.children.append(parse_component(tokns))
            elif current_token[0] == 'LAYOUT':
                node.children.append(parse_layout(tokns))
            elif current_token[0] == 'VAR':
                node.children.append(parse_var(tokns))
        return node

    def parse_component(tokns):
        node = Node('COMPONENT')
        while tokns:
            current_token = tokns.pop(0)
            if current_token[0] == 'TEXT':
                node.children.append(Node('TEXT', tokns.pop(0)[1]))
            elif current_token[0] == 'ONCLICK':
                node.children.append(Node('ONCLICK', tokns.pop(0)[1]))
            elif current_token[0] == 'CSS':
                node.children.append(parse_css(tokns))
        return node

    def parse_var(tokns):
        node = Node('VAR', tokns.pop(0)[1])
        return node

    def parse_css(tokns):
        node = Node('CSS')
        while tokns and tokns[0][0] != 'COMPONENT' and tokns[0][0] != 'LAYOUT' and tokns[0][0] != 'VAR':
            current_token = tokns.pop(0)
            node.children.append(Node('CSS_PROPERTY', (current_token[0], tokns.pop(0)[1])))
        return node

    return parse_application(tokens)


def generate_js_code(node):
    try:
        if node.type == 'APPLICATION':
            return '\n'.join(generate_js_code(child) for child in node.children)
        elif node.type == 'LAYOUT':
            return '\n'.join(generate_js_code(child) for child in node.children)
        elif node.type == 'COMPONENT':
            return generate_component_js(node)
        elif node.type == 'VAR':
            return f'let {node.value};\n'
        else:
            raise ValueError(f"Unknown node type: {node.type}")
    except Exception as e:
        log_error(f"Error generating JS for node {node.type}: {e}")
        return ''


def generate_component_js(node):
    try:
        js_component_code = ''
        for child in node.children:
            if child.type == 'TEXT':
                js_component_code += f'document.body.innerHTML += "<button>{child.value}</button>";\n'
            elif child.type == 'ONCLICK':
                js_component_code += (f'document.querySelector("button").onclick = function()'
                                      f' {{ alert("{child.value}"); }};\n')
            elif child.type == 'CSS':
                js_component_code += generate_css(child)
            else:
                raise ValueError(f"Unknown component child type: {child.type}")
        return js_component_code
    except Exception as e:
        log_error(f"Error generating JS for component: {e}")
        return ''


def generate_css(node):
    try:
        css_code = ''
        for child in node.children:
            if child.type == 'CSS_PROPERTY':
                property_name, property_value = child.value
                css_code += f'document.querySelector("button").style.{property_name} = "{property_value}";\n'
            else:
                raise ValueError(f"Unknown CSS child type: {child.type}")
        return css_code
    except Exception as e:
        log_error(f"Error generating CSS: {e}")
        return ''


def log_error(message):
    print(f"ERROR: {message}")


if __name__ == "__main__":
    with open('example.ez', 'r') as file:
        source_code = file.read()
    all_tokens = tokenize(source_code)
    ast = parse(all_tokens)
    final_js_code = generate_js_code(ast)
    with open('example.js', 'w') as file:
        file.write(final_js_code)
