class DoubleList:
    def __init__(self, val, prev, next_node):
        self.val = val
        self.prev = prev
        self.next = next_node

    @staticmethod
    def generate_linked_list(list1):

        # generate nodes for circular doubly linked list for player list
        node_list = [DoubleList(x, None, None) for x in list1]

        for i in range(0, len(node_list)):
            node_list[i].prev = node_list[i-1]
            if i != len(node_list)-1:
                node_list[i].next = node_list[i+1]
            else:
                node_list[i].next = node_list[0]
        return node_list[0]


