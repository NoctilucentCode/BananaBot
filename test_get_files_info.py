from functions.get_files_info import get_files_info
def test():
    print(f"Result for current directory:")
    print(f"{get_files_info('calculator', '.')}")
    print(f"Result for 'pkg' directory:")
    print(f"{get_files_info('calculator', 'pkg')}")
    print(f"Result for '/bin' directory:")
    print(f"{get_files_info('calculator', '/bin')}")
    print("Result for '../' directory:")
    print(f"{get_files_info('calculator', '../')}")
if __name__ == "__main__":
    test()