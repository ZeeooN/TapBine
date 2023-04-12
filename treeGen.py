# Nosaukums: TapBine - koku ģenerators
# Izstrādāja: Haralds Bikše
# Studenta apliecības numurs: 211RDB120

from main import generate_field, field_merge
from anytree import Node, RenderTree


# Funkcija, kas ģenerē lauka visas nākamās iespejamības
# arr - Spēles lauks no kura tiks izveidoti visi iespējamie nākamie gājieni
def generate_branch(arr):
    branches = []
    for i in range(len(arr) - 1):
        branches.append(field_merge(arr, i))
    return branches


# Funcija, kas uzģenerē visu spēles koku
# start_field - Spēles sākuma lauks
def generate_tree(start_field):
    # Speles koka definēšana
    tree_root = Node(start_field)

    # Speles gājienu indeksa koka definēšana
    index_tree = Node("Top")

    # Pirmā gajiena iespējamo iznākumu ģenerēšana
    start_field = generate_branch(start_field)

    # Otrā gājiena iespējamo iznākumu ģenerēšana
    temp = []
    for i in range(len(start_field)):
        temp.append(generate_branch(start_field[i]))
        Node(start_field[i], parent=tree_root)
        Node(i, parent=index_tree)
    start_field = temp

    # Trešā gajiena iespējamo iznākumu ģenerēšana
    temp = [[]]
    for i in range(len(start_field)):
        temp.append([])
        for j in range(len(start_field[i])):
            temp[i].append(generate_branch(start_field[i][j]))
            Node(start_field[i][j], parent=tree_root.children[i])
            Node(j, parent=index_tree.children[i])
    start_field = temp

    # Ceturtā gajiena iespējamo iznākumu ģenerēšana
    for i in range(len(start_field)):
        for j in range(len(start_field[i])):
            for k in range(len(start_field[i][j])):
                Node(start_field[i][j][k], parent=tree_root.children[i].children[j])
                Node(k, parent=index_tree.children[i].children[j])
    return [tree_root, index_tree]


# Heiristiskā vērtējuma koka ģenerēšana
# tree - Spēles koks ar visiem iespējamajiem gājieniem
def h_generation(tree):
    h_value_tree = tree
    l1 = []
    for i in range(4):
        l2 = []
        for j in range(3):
            l3 = []
            for k in range(2):
                get_val = str(tree.children[i].children[j].children[k].name)[1]
                h_value_tree.children[i].children[j].children[k].name = get_val
                l3.append(int(get_val))
            h_value_tree.children[i].children[j].name = max(l3)
            l2.append(max(l3))
        h_value_tree.children[i].name = min(l2)
        l1.append(min(l2))
    h_value_tree.name = max(l1)
    return h_value_tree


# No analizēt dotos datus un veikt datora gājienu, ja neviens ceļš neved uz uzvaru tiek izvēlēts pirmais ceļš
def algo_make_move(h_tree, i_tree, index_his, bot_start=False):
    if len(index_his) > 0:
        if len(index_his) == 1:
            for i in range(3):
                if (bot_start is True) and int(h_tree.children[index_his[0]].children[i].name) == 1:
                    return int(i_tree.children[index_his[0]].children[i].name)
                else:
                    if (bot_start is False) and int(h_tree.children[index_his[0]].children[i].name) == 0:
                        return int(i_tree.children[index_his[0]].children[i].name)
            return 0
        elif len(index_his) == 2:
            for i in range(2):
                if (bot_start is True) and \
                        int(h_tree.children[index_his[0]].children[index_his[1]].children[i].name) == 1:
                    return int(i_tree.children[index_his[0]].children[index_his[1]].children[i].name)
                else:
                    if (bot_start is False) and \
                            int(h_tree.children[index_his[0]].children[index_his[1]].children[i].name) == 0:
                        return int(i_tree.children[index_his[0]].children[index_his[1]].children[i].name)
            return 0
        else:
            return 0
    else:
        for i in range(4):
            if (bot_start is True) and int(h_tree.children[i].name) == 1:
                return int(i_tree.children[i].name)
            else:
                if (bot_start is False) and int(h_tree.children[i].name) == 0:
                    return int(i_tree.children[i].name)
        return 0


if __name__ == '__main__':
    # Šī faila dāļa ir domāta, lai notestētu spēles koka ģenerēšanu
    # Tiek izpildīts tikai tādā gadījumā, ja tieši šis fails tiek palaist
    test_field = generate_field()
    game_tree = generate_tree(test_field)
    for pre, fill, node in RenderTree(game_tree[0]):
        print("%s%s" % (pre, node.name))
    print("------------------------------")
    for pre, fill, node in RenderTree(game_tree[1]):
        print("%s%s" % (pre, node.name))

    h_values_tree = h_generation(game_tree[0])

    print("------------------------------")
    for pre, fill, node in RenderTree(h_values_tree):
        print("%s%s" % (pre, node.name))
    print("------------------------------")
