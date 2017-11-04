class Node:
    def __init__(self, i, p):
        self.index = i
        self.parent = p
        self.children = []


# prints the given graph
def print_nodes(nodes):
    print len(nodes)
    for node in nodes:
        line = ""
        line += str(len(node.children))
        for c in node.children:
            line += " " + str(c)
        print line


# searches the node's ancestry.
def is_parent(node, candidate, nodes):
    if node.parent is None:
        return False
    if node.parent == candidate:
        return True
    return is_parent(nodes[node.parent], candidate, nodes)


# searches the node's offspring.
def is_child(node, candidate, nodes, visited):
    visited.append(node.index)
    if len(node.children) == 0:
        return False
    if candidate in node.children:
        return True
    for child in node.children:
        if child not in visited:
            result = is_child(nodes[child], candidate, nodes, visited)
            if result:
                return result
    return False


# search for an available node to make a back edge
def back_edge_search(nodes):
    for node in nodes:
        for candidate in nodes:
            if is_parent(node, candidate.index, nodes) and candidate.index != node.index and candidate.index not in node.children:
                return [node.index, candidate.index]
    return None


# searches for available nodes to make a forward edge.
def dfs_f(node, children, parent, nodes):
    if len(children) == 0:
        return None
    real_children = []
    for child in children:
        if nodes[child].parent == parent:
            real_children.append(child)
    for child in real_children:
        for grandson in nodes[child].children:
            if grandson not in node.children and nodes[grandson].parent == child:
                return [node.index, grandson]
        result = dfs_f(node, nodes[child].children, child, nodes)
        if result is not None:
            return result
        result = dfs_f(nodes[child], nodes[child].children, child, nodes)
        if result is not None:
            return result
    return None


edge_input = raw_input("tree edge, back edge, forward edge and cross edge: ")
edge_input = edge_input.strip().split()

t = int(edge_input[0])    # tree edge
b = int(edge_input[1])    # back edge
f = int(edge_input[2])    # forward edge
c = int(edge_input[3])    # cross edge

iterator = 0

# Adds a base node
nodes = [Node(iterator, None)]

iterator += 1
edge_index = 0

while b > 0 or f > 0 or c > 0:

    edge_index += 1
    if edge_index == 4:
        edge_index = 1

    # back edge
    if edge_index == 1 and b > 0:
        if len(nodes) < 2:  # case where we only have one node, it creates another.
            n = Node(iterator, nodes[-1].index)
            n.children.append(nodes[-1].index)
            nodes[-1].children.append(n.index)

            nodes.append(n)

            iterator += 1
            t -= 1
            b -= 1

        else:  # case where is more than one node
            ancestors = []
            visited = []
            result = back_edge_search(nodes)   # searches for an available node to make a back edge.
            if result is None:  # case where there is no node available, it creates another attached to the last node.
                parent = nodes[-1]
                node = Node(iterator, parent.index)
                node.children.append(parent.index)
                parent.children.append(node.index)
                nodes.append(node)

                iterator += 1
                t -= 1
                b -= 1

            else:  # it connects the nodes.
                parent = nodes[result[0]]
                child_index = result[1]
                parent.children.append(child_index)

                b -= 1

    # forward edge
    if edge_index == 2 and f > 0:
        if len(nodes) == 1:  # case when there is only one node, we create another
            node = Node(iterator, nodes[-1].index)
            nodes[-1].children.append(iterator)
            nodes.append(node)

            iterator += 1
            t -= 1

        # case where there are 2 nodes. We create another and connect the first one with the new one.
        if len(nodes) == 2:
            parent = nodes[-1]
            grandparent = nodes[parent.parent]
            node = Node(iterator, parent.index)
            parent.children.append(iterator)
            nodes.append(node)
            grandparent.children.append(node.index)

            iterator += 1
            t -= 1
            f -= 1

        else:
            result = dfs_f(nodes[0], nodes[0].children, nodes[0].index, nodes)
            if result is None:
                parent = nodes[-1]
                grandparent = nodes[parent.parent]
                node = Node(iterator, parent.index)
                parent.children.append(iterator)
                nodes.append(node)
                grandparent.children.append(iterator)

                iterator += 1
                t -= 1
                f -= 1

            else:
                parent_index = result[0]
                child_index = result[1]

                nodes[parent_index].children.append(child_index)

                f -= 1

    # cross edge
    if edge_index == 3 and c > 0:
        if len(nodes) == 1:
            parent = nodes[0]
            node = Node(iterator, parent.index)
            parent.children.append(node.index)
            nodes.append(node)

            iterator += 1
            t -= 1

        if len(nodes) == 2:
            parent = nodes[0]
            node = Node(iterator, parent.index)
            parent.children.append(node.index)
            nodes.append(node)

            cousin_index = parent.children[0]
            node.children.append(cousin_index)

            iterator += 1
            t -= 1
            c -= 1

        found = False
        for node in nodes:
            if found:
                break
            for candidate in nodes:
                if found:
                    break
                visited = []
                if not is_parent(node, candidate.index, nodes) and not is_child(node, candidate.index, nodes, visited) \
                        and candidate.index < node.index:
                    node.children.append(candidate.index)
                    c -= 1
                    found = True

        if not found:
            parent = nodes[0]
            node = Node(iterator, parent.index)
            parent.children.append(iterator)
            nodes.append(node)
            cousin_index = parent.children[0]
            node.children.append(cousin_index)

            iterator += 1
            t -= 1
            c -= 1

while t > 0:
    parent = nodes[-1]
    node = Node(iterator, parent.index)
    parent.children.append(node.index)
    nodes.append(node)

    iterator += 1
    t -= 1

print_nodes(nodes)
