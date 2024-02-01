import networkx as net
import matplotlib.pyplot as matplt



def file_cleaning():
    data = open("webisalod-pairs.txt", 'r', encoding='utf8')
    dict_all = {}
    for line in data.readlines():
        comps = line.rstrip().split(";")

        entity = comps[0]
        entity_c1 = entity.replace('_', ' ')
        entity_c2 = entity_c1.replace('+', ' ')
        entity_c3 = entity_c2.strip()

        type_confi = comps[1]
        con = type_confi.rstrip().split("\t")
        type = con[0]
        type_c1 = type.replace('_', ' ')
        type_c2 = type_c1.replace('+', ' ')
        type_c3 = type_c2.strip()

        confi = float(con[1])
        confi_r = round(confi, 2)

        if entity_c3 not in dict_all:
            dict_all[entity_c3] = {type_c3: confi_r}
        else:
            dict_all_3 = dict_all[entity_c3]
            dict_all_3[type_c3] = confi_r

    return dict_all


def level_1():
    vertices_1 = []
    edge = []
    input_1 = open("input-1.txt", 'r', encoding='utf8')
    for line1 in input_1:
        vertices_1.append(line1.strip())
    vertices_2 = []
    vertices_2.extend(vertices_1)
    dict_all = file_cleaning()
    for v in vertices_1:
        if v in dict_all:
            vertex_value = dict_all[v]
            vertex_value_f = max(vertex_value, key=vertex_value.get)
            vertices_2.append(vertex_value_f)
            edge.append((v, vertex_value_f))
    return vertices_2, edge

def level_2():
    vertices_2nd = []
    edge_2nd = []
    vertices_2nd, edge_2nd = level_1()
    v1 = []
    dict_all = file_cleaning()
    input_1 = open("input-1.txt", 'r', encoding='utf8')
    for line1 in input_1:
        v1.append(line1.strip())
    length_vertices_1= len(v1)
    vertices_3 = []
    vertices_3.extend(v1)
    for v in vertices_2nd[(length_vertices_1 -1):]:
        if v in dict_all:
            vertex_value1 = dict_all[v]
            vertex_value_f1 = max(vertex_value1, key= vertex_value1.get())
            vertices_3
        edge_2nd.append((v, 'entity'))
    return vertices_2nd, edge_2nd

def draw():
    gFinal = net.DiGraph()
    vertices, edge = level_2()
    gFinal.add_nodes_from(vertices[::-1])
    gFinal.add_edges_from(edge[::-1])
    net.draw(gFinal, with_labels=True)
    matplt.show()
'''
main function
'''
if __name__ == '__main__':
    #level_2()
    draw()
