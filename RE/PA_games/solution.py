memory_hex_str = "ff ff ff ff 01 00 00 00 05 15 41 40 01 00 00 00 75 75 7d 5f 01 00 00 00 41 40 14 15 01 00 00 00 f7 5d 77 f5 01 00 00 00 05 11 15 10 01 00 00 00 d5 77 55 5d 01 00 00 00 51 41 44 45 01 00 00 00 77 f7 d7 77 01 00 00 00 41 14 54 51 01 00 00 00 7d df 5d 5d 01 00 00 00 11 40 00 50 01 00 00 00 55 dd fd 5d 01 00 00 00 55 11 11 54 01 00 00 00 7d 77 7f 55 01 00 00 00 15 14 54 41 01 00 00 00 55 dd d7 5d 01 00 00 00 55 51 51 51 01 00 00 00 55 77 57 5f 01 00 00 00 41 41 00 40 01 00 00 00 ff ff ff ff 01 00 00 00"  # 这个字符串应该包含所有的内存数据。
memory_bytes = bytes.fromhex(memory_hex_str.replace(' ', ''))

# 将这个字节列表转换为一个长整型的列表，每8个字节转换为一个长整型。
memory = []
for i in range(0, len(memory_bytes), 8):
    # 假设是小端序，所以需要反转每8个字节
    memory_value = int.from_bytes(memory_bytes[i:i+8], 'little')
    memory.append(memory_value)

# 定义检查函数，基于游戏的FUN_00101403逻辑
def check_memory(param1, param2):
    if param2 < 0 or param2 >= len(memory):
        return True  # 如果param2超出范围，假定失败。
    memory_value = memory[param2]
    # 右移并检查最低位
    return (memory_value >> (param1 & 0x3f)) & 1

# 尝试寻找正确的输入字符串
def find_solution():
    for param2 in range(len(memory)):  # 假设param2是在数组长度范围内
        for param1 in range(64):  # param1只能右移0到63位
            if not check_memory(param1, param2):  # 如果检查通过
                # 找到一个可能的通关点，尝试构建字符串
                path = reconstruct_path(param1, param2)
                if path:  # 如果确实有一条路径
                    return path
    return "No solution found"

# 根据param1和param2反向推导出输入字符串
def reconstruct_path(param1, param2):
    # 这里需要一个算法来根据结束的param1和param2反向工作出输入字符串
    # 这可能涉及到创建一个状态空间搜索问题，比如使用BFS或DFS
    pass

# 执行函数找到解决方案
solution = find_solution()
print("Solution:", solution)