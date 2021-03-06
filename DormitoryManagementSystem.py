"""
学生信息包括
学号（唯一）  姓名  性别  年龄  寝室（一间寝室最多安排4人）
寝室编号 男生（100 101 102） 女生（200 201 202）

功能包括：
1. 可以录入学生信息
2. 录入过程中可以为其分配寝室（可选自动分配或手动分配，手动分配的话如果选择的寝室人员已满，提示重新分配）
3. 可以打印各寝室人员列表（做到表格打印是加分项）
4. 可以用学号索引打印特定学生信息，可以打印所有学生信息（做到表格打印是加分项）
5. 可以为学生调整寝室（一人调整到其他寝室，两人交换寝室等，自由发挥）
6. 可以将所有信息存入文件（json格式）
7. 程序启动时，将文件中的学生信息自动导入系统
"""
# -*- coding: UTF-8 -*-
import json

# 系统主菜单选项宏
RECORD_INFO = '1'
DELETE_INFO = '2'
FIND_INFO = '3'
SHOW_INFO = '4'
CHANGE_ROOM = '5'
QUIT_SYSTEM = '0'

# query_student_id函数mode宏
ID_EXISTS = 1
DELETE_ID = 2
INFO_RETURN = 3

# 学生信息打印的统一开头
print_info = '''
============================================================
学号\t\t姓名\t\t性别\t\t年龄\t\t寝室号
------------------------------------------------------------'''


# 加载json文件中的学生信息
def load_json_file():
    with open("information.json", "r", encoding='utf-8') as file:       # 加载保存json文件的编码都为utf-8
        return json.load(file)      # 将导入的学生信息返回到全局变量student_info_dict（字典类型）


# 将学生信息保存在json文件
def save_json_file():
    with open("information.json", "w", encoding='utf-8') as file:
        json.dump(room_info_dict, file, ensure_ascii=False)  # 传入文件描述符，和dumps一样的结果，关闭默认以ASCII码存入json


# 根据学号遍历、调整学生信息
def query_student_id(query_id, mode):
    for room in room_info_dict.values():
        for stu_info in room["student"]:
            if query_id == stu_info["student_id"]:
                if mode == ID_EXISTS:
                    return True
                elif mode == DELETE_ID:
                    room["student"].pop(room["student"].index(stu_info))  # 删除寝室字典里面的该生信息
                    room["count"] -= 1
                    return True
                else:
                    return room["student"][room["student"].index(stu_info)]      # 按学号搜索学生的学生信息
    return False


# 录入学生信息
def record_student_info():
    new_student_info = {"student_id": "", "name": "", "sex": "", "age": 0, "room": ""}       # 新增学生的个人信息集

    # 判断输入学号是否合法
    while True:     # 由于学号格式为整型，所以加了异常和格式转换，阻止了输入为1.1和1、1之类的情况
        try:
            new_student_info["student_id"] = str(int(input("请输入要录入学生的学号:\n")))
            if query_student_id(new_student_info["student_id"], 1):      # 学号是否唯一
                print("您输入的学号已存在(提示：有效数字之前的零无效)，请重新输入")
            elif new_student_info["student_id"] == '0':
                print("抱歉，学号不能为零，请重新输入")
            else:
                break
        except ValueError:
            print("您输入学生学号格式有误，请重新输入")

    # 判断输入姓名是否合法
    while not new_student_info["name"]:     # 姓名仅做了输入为空判断
        new_student_info["name"] = input("请输入学生姓名（不能为空哦）:\n")

    # 判断输入性别是否合法
    while new_student_info["sex"] not in ("男", "女"):        # 判断性别输入是否为（男/女）
        new_student_info["sex"] = input("请输入性别（男/女）:\n")

    # 判断年龄输入是否合法
    while True:     # 由于输入格式为整型，所以加了异常和格式转换，阻止了输入为.和、之类的情况
        try:
            new_student_info["age"] = int(input("请输入年龄，范围(6-48):\n"))
            if int(new_student_info["age"]) not in range(6, 48):      # 判断年龄输入是否合法
                print("您输入的年龄范围不符合规定，请重新输入")
            else:
                break
        except ValueError:
            print("您输入的年龄格式有误，请重新输入")

    k = 1  # k = 1，默认为女生
    if new_student_info["sex"] == "男":      # 提前用k值标识性别，方便后面为其分配对应的寝室
        k = 0       # k = 0为男生

    while True:
        info = """========================寝室分配============================
        1.自动分配
        2.手动分配
        """
        print(info)
        choice1 = input("请选择你需要进行的操作:\n")
        if choice1 == "1":      # 自动分配
            for i in (100 + 100*k, 101 + 100*k, 102 + 100*k):       # 顺序遍历每一间寝室
                i = str(i)
                if concreteness_allot_step(room_info_dict[i], new_student_info, i):     # 寝室分配函数，寝室已满会分配失败，返回False
                    break
                if i >= str(102 + 100*k):
                    print("抱歉，所有符合规定的寝室已住满")
                    break
            break

        elif choice1 == "2":        # 手动分配
            while True:
                room_id = input("请输入要分配的寝室号:\n")
                if int(room_id) not in (100 + 100*k, 101 + 100*k, 102 + 100*k):
                    print("您输入的寝室号不符合规定，请重新输入:")
                elif not concreteness_allot_step(room_info_dict[room_id], new_student_info, room_id):
                    print("您输入的寝室号对应的寝室已住满，请重新输入:")
                else:
                    break
            break

        else:
            print("请按照提示输入选项对应的数字:\n")

    save_json_file()
    print("新增学生信息录入成功")


# 删除学生信息
def delete_student_info():
    delete_id = '0'
    while not query_student_id(delete_id, ID_EXISTS):  # 判断输入的学号是否存在
        delete_id = input("请输入要删除学生的学号（要确保学生信息存在哦）:\n")     # 输入要删除学生的学号

    query_student_id(delete_id, DELETE_ID)      # 删除寝室字典里面的该生信息

    save_json_file()
    print("已删除学号{}的学生信息".format(delete_id))


# 显示寝室信息
def show_room_info():
    print("按寝室显示学生信息:", end="")
    print(print_info)
    for room_id in room_info_dict:
        print("{}号寝室，人员如下:".format(room_id))
        for stu_info in room_info_dict[room_id]["student"]:
            print("{}\t\t{}\t\t{}\t\t{}\t\t{}"
                  .format(stu_info["student_id"], stu_info["name"], stu_info["sex"], stu_info["age"], stu_info["room"]))


# 按学号搜索并显示学生信息
def show_student_info():
    find_id = input("请你输入想要查找的学号:\n")
    find_info = query_student_id(find_id, INFO_RETURN)
    if find_info:
        print("{}号学生信息如下:".format(find_id), end="")
        print(print_info)
        print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format(
            find_info["student_id"], find_info["name"], find_info["sex"], find_info["age"], find_info["room"]))
    else:
        print("系统未录入此学号的学生")


# 具体分配步骤
def concreteness_allot_step(room_info, student_info, room_id):
    if student_info["room"] == room_id:  # 在学生个人信息中备注其寝室号
        print("该生已在此寝室")
        room_info["student"].append(student_info)        # 将学生信息添加到寝室信息字典中，抵消后续的删除操作
        room_info["count"] += 1
        return True
    if room_info["count"] < 4:      # 判断寝室是否未住满
        student_info["room"] = room_id      # 在学生个人信息中备注其寝室号
        room_info["student"].append(student_info)        # 将学生信息添加到寝室信息字典中
        room_info["count"] += 1
        print("分配成功")
        return True
    else:
        return False


# 调整学生宿舍
def change_student_room():      # 可将学生调整到空余寝室，或者和其他学生互换寝室
    while True:
        info = """========================调整寝室============================
        1.一人调整寝室
        2.两人互换寝室
        """
        print(info)
        choice1 = input("请选择你需要进行的操作:\n")
        if choice1 == "1":      # 一人调整寝室
            change_id = '0'
            while not query_student_id(change_id, ID_EXISTS):  # 判断输入的学号是否存在
                change_id = input("请输入要调整学生的学号（要确保学生信息存在哦）:\n")  # 输入调整学生的学号

            change_info = query_student_id(change_id, INFO_RETURN)
            k = 1  # k = 1，默认为女生
            if change_info["sex"] == "男":  # 用k值标识性别，方便后面为其分配对应的寝室
                k = 0  # k = 0为男

            change_room = 0
            # 判断输入寝室号是否合法
            while True:  # 由于寝室号格式转换为整型，所以加了异常和格式转换，阻止了输入为1.1和1、1之类的情况
                try:
                    if change_room not in (100 + 100 * k, 101 + 100 * k, 102 + 100 * k):  # 寝室号是否合法
                        change_room = int(input("请输入要调整的寝室号（男女生要分配到与其对应的寝室哦）:\n"))
                    else:
                        break
                except ValueError:
                    print("您输入的寝室号格式有误，请重新输入")

            change_room = str(change_room)
            if not concreteness_allot_step(room_info_dict[change_room], change_info, change_room):
                print("{}号寝室已满，人员如下:".format(change_room))
                print(print_info)
                for stu_info in room_info_dict[change_room]["student"]:
                    print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format(
                        stu_info["student_id"], stu_info["name"], stu_info["sex"], stu_info["age"], stu_info["room"]))

                if 'y' == input("是否与其中一人交换宿舍(y/n)"):
                    another_change_id = input("请输入与之交换寝室的学生学号")  # 输入被交换学生的学号
                    another_change_info = query_student_id(another_change_id, INFO_RETURN)  # 获取被交换学生的信息
                    another_change_room = change_info["room"]  # 获取交换学生原有宿舍

                    # 删除学生原来的宿舍信息
                    query_student_id(change_id, DELETE_ID)
                    query_student_id(another_change_id, DELETE_ID)
                    # 更新被交换学生宿舍信息
                    concreteness_allot_step(room_info_dict[another_change_room], another_change_info,
                                            another_change_room)
                    # 更新交换学生宿舍信息
                    concreteness_allot_step(room_info_dict[change_room], change_info, change_room)
                    break

            else:
                query_student_id(change_id, DELETE_ID)
                break

        elif choice1 == "2":        # 两人互换寝室
            one_change_id = '0'
            while not query_student_id(one_change_id, ID_EXISTS):  # 判断输入的学号是否存在
                one_change_id = input("请输入第一个要交换学生的学号（要确保学生信息存在哦）:\n")  # 输入第一个交换学生的学号
            one_change_info = query_student_id(one_change_id, INFO_RETURN)  # 获取第一个交换学生的信息
            one_change_room = one_change_info["room"]  # 获取第一个交换学生原有宿舍

            two_change_id = '0'
            while not query_student_id(two_change_id, ID_EXISTS):  # 判断输入的学号是否存在
                two_change_id = input("请输入另一个要交换学生的学号（要确保学生信息存在哦）:\n")  # 输入另一个交换学生的学号
            two_change_info = query_student_id(two_change_id, INFO_RETURN)  # 获取另一个交换学生的信息
            two_change_room = two_change_info["room"]  # 获取第一个交换学生原有宿舍

            # 删除学生原来的宿舍信息
            query_student_id(one_change_id, DELETE_ID)
            query_student_id(two_change_id, DELETE_ID)
            # 更新第一个交换学生宿舍信息
            concreteness_allot_step(room_info_dict[two_change_room], one_change_info, two_change_room)
            # 更新另一个交换学生宿舍信息
            concreteness_allot_step(room_info_dict[one_change_room], two_change_info, one_change_room)
            break

        else:
            print("请按照提示输入选项对应的数字:\n")

    save_json_file()
    print("调整学生寝室成功")


# 系统功能菜单
def show_menu():
    while True:
        info = """
欢迎使用[寝室管理系统]:
            1.录入学生信息
            2.删除学生信息
            3.搜索学生信息
            4.显示学生信息
            5.调整学生宿舍
            0.退出管理系统
               """
        print(info)
        choice = input("请输入你想进行的操作是:\n")

        if choice == RECORD_INFO:        # 1.录入学生信息
            record_student_info()

        elif choice == DELETE_INFO:      # 2.删除学生信息
            delete_student_info()

        elif choice == FIND_INFO:      # 3.搜索学生信息
            show_student_info()

        elif choice == SHOW_INFO:      # 4.显示学生信息
            show_room_info()

        elif choice == CHANGE_ROOM:      # 5.调整学生宿舍
            change_student_room()

        elif choice == QUIT_SYSTEM:      # 0.退出管理系统
            print("欢迎再次使用学生管理系统！")
            break

        else:
            print("您的输入有误，请您输入操作相对应的数字:")

        print("按enter键继续...")
        input()


if __name__ == "__main__":
    room_info_dict = load_json_file()        # 加载json文件的学生信息到字典中

    show_menu()     # 显示系统主菜单，并在其中循环

    save_json_file()        # 将学生信息保存在json文件
