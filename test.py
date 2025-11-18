# 일단 파이썬 형식으로 만들고, 코드가 낮선 사람들을 위해 몇몇 부분을 간략화 하자
# data

class AssemblyType:
    """
    조립부종류(AssemblyType)를 설명하는 객체
    객체에 저장한 정보를 바탕으로 조립부 간의 차이점과 공통점을 구분한다.
    """
    def __init__(self, name_arg:str):
        self.name = name_arg
        self.assembled_flag = False# 초기 상태에서는 조립에 사용되지 않음의 뜻으로 False 상태

        self.main_type:str=""
        self.sub_type:str=""

    def set_type(self, type_arg:str, sub_type_arg:str=""):
        self.main_type = type_arg
        self.sub_type = sub_type_arg

    def get_type(self)->tuple[str, str]:
        return self.main_type, self.sub_type
    
    def set_assembled_flag(self, assembled_flag_arg:bool):
        self.assembled = assembled_flag_arg

class Item:
    """
    아이템(부품)을 정의하는 객체
    부품의 이름과, 부품의 조립부종류(AssemblyType)를 저장할 수 있다.
    """
    static_type_dict = {}
    def __init__(self, name_arg:str=""):
        self.name:str = name_arg
        self.type_list:list[AssemblyType] = []
        pass

    def set_name(self, name_arg:str):
        self.name = name_arg

    def set_type(self, type_arg:AssemblyType):
        self.type_list.append(type_arg)

    def get_type_list(self)->list:
        return self.type_list
    
class AssemblyGroupDataBase:
    """
    타입이 어떻개 묶일지 데이터를 저장해두는 데이터 베이스
    matching_system이 AssemblyGroupDataBase를 조회하여 
    Item이 가진 AssemblyType 간의 묶임(조립가능)여부를 판단한다.
    """
    assembly_group_data = {}
    def __init__(self):
        ...

    def set_bundle(cls, type_group:list[AssemblyType]):
        if len(type_group) > 0:
            assembly_type = type_group[0]
            gorup_type, _ = assembly_type.get_type()
            sub_type_list = []
            for assembly_type in type_group:
                main_type, sub_type = assembly_type.get_type()
                if gorup_type != main_type:
                    # 타입 그룹화 오류 발생, 
                    # 서로 다른 타입 간의 그룹화 발생
                    return
                sub_type_list.append(sub_type)

        cls.assembly_group_data.update({gorup_type, sub_type_list})

    def check_can_assemble(cls, type_group:list[AssemblyType]):
        main_type_list:list = []
        sub_type_list:list = []
        for type in type_group:
            main_type, sub_type = type.get_type()
            main_type_list.append(main_type)
            sub_type_list.append(sub_type)
        
        if all(main_type_list) == True:# main type이 모두 같은 값을 가졌는지 확인.
            main_type = main_type_list[0]# 그룹의 첫 번째 원소로 부터 main type을 확인.  
            sub_type_list
            group_data = cls.assembly_group_data.get(main_type)

            sub_type_list
            group_data

class State:
    def __init__(self, item_list):
        self.item_list = []
        ...

# 객체 리스트

# 매칭 탐색 함수
def check_matching(item_list_arg:list):
    """
    주어진 상태에서 가능한 matching 후보를 제안함
    (= 모델에서 가능한 Transition을 제시함.)
    """
    item_list:list = item_list_arg.copy()
    remainder_list:list = []
    assembly_candidate:list = []
    match_list:list = []

    while len(item_list) > 0:
        # 앤드아이템
        enditme = item_list.pop()
        ...

    return match_list, remainder_list

def execute_assemble(match_list):
    ...


def BFS_search_algorithm(init_state:list, target_state:list):
    # 탐색 우선순위는 BFS로 정함.

    ...

    # goal 달성/혹은 실패시 Planning 종료


def main():
    # 데이터 생성 단계
    item_list = []


if __name__ == "__main__":
    main()


