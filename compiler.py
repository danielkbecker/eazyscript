import re


class Node:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []


def tokenize(code):
    tokens = []
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),
        ('ASSIGN', r':'),
        ('ID', r'[A-Za-z]+'),
        ('STRING', r'"[^"]*"'),
        ('NEWLINE', r'\n'),
        ('SKIP', r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
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
    def parse_application(tokens):
        node = Node('APPLICATION')
        while tokens:
            token = tokens.pop(0)
            if token[0] == 'LAYOUT':
                node.children.append(parse_layout(tokens))
            elif token[0] == 'COMPONENT':
                node.children.append(parse_component(tokens))
            elif token[0] == 'VAR':
                node.children.append(parse_var(tokens))
        return node

    def parse_layout(tokens):
        node = Node('LAYOUT')
        while tokens:
            token = tokens.pop(0)
            if token[0] == 'COMPONENT':
                node.children.append(parse_component(tokens))
            elif token[0] == 'LAYOUT':
                node.children.append(parse_layout(tokens))
            elif token[0] == 'VAR':
                node.children.append(parse_var(tokens))
        return node

    def parse_component(tokens):
        node = Node('COMPONENT')
        while tokens:
            token = tokens.pop(0)
            if token[0] == 'TEXT':
                node.children.append(Node('TEXT', tokens.pop(0)[1]))
            elif token[0] == 'ONCLICK':
                node.children.append(Node('ONCLICK', tokens.pop(0)[1]))
            elif token[0] == 'CSS':
                node.children.append(parse_css(tokens))
        return node

    def parse_var(tokens):
        node = Node('VAR', tokens.pop(0)[1])
        return node

    def parse_css(tokens):
        node = Node('CSS')
        while tokens and tokens[0][0] != 'COMPONENT' and tokens[0][0] != 'LAYOUT' and tokens[0][0] != 'VAR':
            token = tokens.pop(0)
            node.children.append(Node('CSS_PROPERTY', (token[0], tokens.pop(0)[1])))
        return node

    return parse_application(tokens)


def generate_js(node):
    try:
        if node.type == 'APPLICATION':
            return '\n'.join(generate_js(child) for child in node.children)
        elif node.type == 'LAYOUT':
            return '\n'.join(generate_js(child) for child in node.children)
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
        js_code = ''
        for child in node.children:
            if child.type == 'TEXT':
                js_code += f'document.body.innerHTML += "<button>{child.value}</button>";\n'
            elif child.type == 'ONCLICK':
                js_code += f'document.querySelector("button").onclick = function() {{ alert("{child.value}"); }};\n'
            elif child.type == 'CSS':
                js_code += generate_css(child)
            else:
                raise ValueError(f"Unknown component child type: {child.type}")
        return js_code
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
        code = file.read()
    tokens = tokenize(code)
    ast = parse(tokens)
    js_code = generate_js(ast)
    with open('example.js', 'w') as file:
        file.write(js_code)
