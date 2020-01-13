from graphviz import Digraph

def outline():
    dot = Digraph(comment='Outline')
    dot.attr('node', shape='rectangle')
    dot.attr(rankdir='LR')

    with dot.subgraph() as c:
        c.attr(rank='same')
        c.node('1', 'Bokeh', fontsize='30', color='green', fontcolor='green')
        c.node('1a', 'The Bokeh Model')
        c.edge('1', '1a')
    with dot.subgraph() as c:
        c.attr(rank='same')
        c.node('2', 'Holoviews', fontsize='30', color='purple', fontcolor='purple')
        c.node('2a', 'Test')
        c.edge('2', '2a')
    with dot.subgraph() as c:
        c.attr(rank='same')
        c.node('3', 'Other')
    dot.edges(['12', '23'])
    dot.format = 'svg'
    return dot

def bokeh_model(): 
    dot = Digraph(comment='The Bokeh Model')
    dot.attr('node', shape='rectangle')
    dot.attr(rankdir='LR')
    with dot.subgraph(name='cluster_0') as c:
        c.attr(style='filled', color='lightgrey')
        c.node_attr.update(style='filled', color='white')
        c.node('A', 'Python Objects')
        c.attr(label='Bokeh')
    dot.node('B', 'JSON')

    with dot.subgraph(name='cluster_1') as c:
        c.attr(style='filled', color='lightgrey')
        c.node_attr.update(style='filled', color='white')
        c.node('C', 'JavaScript Objects')
        c.attr(label='BokehJS')
    dot.node('D', 'HTML/SVG Output')
    dot.edges(['AB', 'BC', 'CD'])
    dot.format = 'svg'
    return dot

def bokeh_server():
    dot = Digraph(comment='Bokeh Server')
    dot.attr('node', shape='rectangle')
    dot.attr(rankdir='LR')

    dot.node('BS', 'Bokeh Server')
    dot.node('App', 'Application')
    for i in [0, 1]:
        with dot.subgraph(name=f'cluster_{i}') as c:
            c.attr(style='filled', color='lightgrey')
            c.node_attr.update(style='filled', color='white')
            c.node(f'A{i}', 'Python Objects', group=str(i))
            c.attr(label='User Session')
            c.node(f'W1{i}', 'WebSocket', shape='oval')
            c.node(f'B{i}', 'JSON', group=str(i))
            c.node(f'W2{i}', 'WebSocket', shape='oval')
            c.node(f'C{i}', 'JavaScript Objects', group=str(i))
        dot.node(f'D{i}', 'HTML Canvas/SVG Output')
        dot.edges([
            [f'A{i}', f'B{i}'],
            [f'B{i}', f'C{i}'],
            [f'C{i}', f'D{i}'],
            [f'A{i}', f'W1{i}'],
            [f'W1{i}', f'C{i}'],
        ])
        dot.edge(f'A{i}', f'W2{i}', dir='back')
        dot.edge(f'W2{i}', f'C{i}', dir='back')

    dot.edge('BS', 'App')
    dot.edge('App', 'A0')
    dot.edge('App', 'A1')
    dot.format = 'svg'
    return dot
