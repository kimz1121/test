# 일단 파이썬 형식으로 만들고, 코드가 낮선 사람들을 위해 몇몇 부분을 간략화 하자
# data

import copy

class AssemblyType:
    """
    조립부종류(AssemblyType)를 설명하는 객체
    객체에 저장한 정보를 바탕으로 조립부 간의 차이점과 공통점을 구분한다.
    """
    def __init__(self, main_type_arg:str, sub_type_arg:str=""):
        self.assembled_flag = False# 초기 상태에서는 조립에 사용되지 않음의 뜻으로 False 상태
        self.parent_item: 'Item' = None

        self.main_type:str=""
        self.sub_type:str=""
        self.set_type(main_type_arg, sub_type_arg)

    def set_type(self, main_type_arg:str, sub_type_arg:str=""):
        self.main_type = main_type_arg
        self.sub_type = sub_type_arg

    def get_type(self)->tuple[str, str]:
        return self.main_type, self.sub_type
    
    def set_assembled_flag(self, assembled_flag_arg:bool):
        self.assembled_flag = assembled_flag_arg

    def set_parent_item(self, parent_item_arg: 'Item'):
        self.parent_item = parent_item_arg
    
    def get_parent_item(self):
        return self.parent_item

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

    def add_type(self, type_arg:AssemblyType):
        self.type_list.append(type_arg)
        type_arg.set_parent_item(self)

    def get_type_list(self)->list[AssemblyType]:
        return self.type_list
    
class AssemblyGroupDataBase:
    """
    타입이 어떻개 묶일지 데이터를 저장해두는 데이터 베이스
    matching_system이 AssemblyGroupDataBase를 조회하여 
    Item이 가진 AssemblyType 간의 묶임(조립가능)여부를 판단한다.
    """
    def __init__(self):
        self.assembly_group_data = {}
        ...

    def add_assembly_type_group(self, assembly_type_group:list[AssemblyType]):
        if len(assembly_type_group) > 0:
            assembly_type = assembly_type_group[0]
            gorup_type, _ = assembly_type.get_type()
            sub_type_list = []
            for assembly_type in assembly_type_group:
                main_type, sub_type = assembly_type.get_type()
                if gorup_type != main_type:
                    # 타입 그룹화 오류 발생, 
                    # 서로 다른 타입 간의 그룹화 발생
                    return
                sub_type_list.append(sub_type)
        print(gorup_type)
        print(sub_type_list)
        self.assembly_group_data.update({gorup_type : sub_type_list})

    def get_assembly_group_data(self, main_type:str)->list:  
        return self.assembly_group_data.get(main_type)

    def check_can_assemble(self, candidate_type_group:list[AssemblyType]):
        main_type_list:list = []
        sub_type_list:list = []
        for type in candidate_type_group:
            main_type, sub_type = type.get_type()
            main_type_list.append(main_type)
            sub_type_list.append(sub_type)
        
        if all(main_type_list) == True:# main type이 모두 같은 값을 가졌는지 확인.
            main_type = main_type_list[0]# 그룹의 첫 번째 원소로 부터 main type을 확인.  
            sub_type_list
            grouped_sub_type_data = self.assembly_group_data.get(main_type)

            for sub_type in grouped_sub_type_data:
                if sub_type in sub_type_list:
                    sub_type_list.remove(sub_type)
                else:
                    return False# Group이 되기 위해 요구되는 sub_type을 candidate_type_group 내에서 찾지 못했을 경우 조립 불가함.
            
            if len(sub_type_list) == 0:
                return True# Group이 되기 위해 요구되는 sub_type을 알맞게 찾은 경우 candidate_type_group은 조립 가능함.
            else:
                return False# Group이 되기 위해 요구되는 양 보다 더 많은 sub_type이 주어진 경우 올바른 조립이 아니라서 조립 불가함.

class State:
    def __init__(self, item_list):
        self.item_state_list:list[Item] = item_list.copy()

    def get_item_state_list(self):
        return self.item_state_list

# 객체 리스트

# 매칭 탐색 함수
def check_matching(state_arg:State, assembly_data_base:AssemblyGroupDataBase)->list:
    """
    주어진 상태에서 가능한 matching 후보를 제안함
    (= 모델에서 가능한 Transition을 제시함.)
    """

    before_check_item_list:list[Item] = state_arg.get_item_state_list().copy()
    after_check_item_list:list[Item] = []
    match_list:list[AssemblyType] = []

    while len(before_check_item_list) > 0:
        # 앤드아이템
        enditme:Item = before_check_item_list.pop()
        assembly_type_list = enditme.get_type_list()
        
        for assembly_type in assembly_type_list:
            main_type, sub_type = assembly_type.get_type()
            required_sub_type_list = assembly_data_base.get_assembly_group_data(main_type)

            if required_sub_type_list is not None and sub_type in required_sub_type_list:
                # 조립 가능한 타입 그룹의 일부를 찾음
                assembly_candidate:list[AssemblyType] = [assembly_type]
                acquired_sub_type_list = [sub_type]
                for check_item in before_check_item_list:
                    check_item_type_list = check_item.get_type_list()
                    for check_item_type in check_item_type_list:
                        if check_item_type.assembled_flag == True:
                            continue# 이미 조립에 사용된 타입은 건너뜀
                        check_main_type, check_sub_type = check_item_type.get_type()
                        # 같은 main_type 이고 required_sub_type 에 포함되며, 중복된 sub_type 이 아니면 추가
                        if (check_main_type == main_type
                                and check_sub_type in required_sub_type_list
                                and check_sub_type not in acquired_sub_type_list):
                            assembly_candidate.append(check_item_type)
                            acquired_sub_type_list.append(check_sub_type)
                            # 한 아이템에서 여러 타입을 중복으로 추가하지 않기 위해 내부 루프 종료
                            break
                
                # 조립 가능한 타입 그룹의 모든 타입을 찾았는지 확인
                if assembly_data_base.check_can_assemble(assembly_candidate) == True:
                    match_list.append(assembly_candidate)
                    print("매칭 후보 발견:", main_type, acquired_sub_type_list)

    return match_list

def execute_assemble(match_set:list[AssemblyType]):
    """
    매칭 가능한 경우, 조립하여 조립된 타입의 assembled_flag를 True(조립에 사용되었음)로 설정
    """
    for assembly_type in match_set:
        assembly_type.set_assembled_flag(True)

def search_algorithm(init_state_arg:list, goal_state_arg:list, assembly_data_base:AssemblyGroupDataBase)->list[list[AssemblyType]]:
    """
    goal 달성/혹은 실패시 Planning 종료

    연구 개발을 통해 구현예정인 부분으로 아직 구현되지 않음.

    현재 데모코드에서는 
    - Search Algorithm을 통한 다양한 순서 조합 고려
    - goal state 고려 
    위 두가지 알고리즘 관련 부분을 생략하고, 단순히 먼저 발견한 매칭 가능한 후보부터 조립하는 방식으로 구현됨. 
    """
    plan_sequence:list[list[AssemblyType]] = []
    while True:
        match_list = check_matching(init_state_arg, assembly_data_base)
        if len(match_list) == 0:
            print("더 이상 조립 가능한 타입 그룹이 없음. Planning 종료.")
            break
        plan_sequence.append(match_list[0])
        execute_assemble(match_list[0])

    return plan_sequence

def main():
    # 타입 데이터 생성 단계
    # 도어레치-프론트도어
    type_A_m = AssemblyType(main_type_arg="A", sub_type_arg="m")
    type_A_f = AssemblyType(main_type_arg="A", sub_type_arg="f")

    type_B_m = AssemblyType(main_type_arg="B", sub_type_arg="m")
    type_B_i = AssemblyType(main_type_arg="B", sub_type_arg="i")
    type_B_f = AssemblyType(main_type_arg="B", sub_type_arg="f")
    
    type_C_m = AssemblyType(main_type_arg="C", sub_type_arg="m")
    type_C_f = AssemblyType(main_type_arg="C", sub_type_arg="f")

    type_D_m = AssemblyType(main_type_arg="D", sub_type_arg="m")
    type_D_i = AssemblyType(main_type_arg="D", sub_type_arg="i")
    type_D_f = AssemblyType(main_type_arg="D", sub_type_arg="f")

    type_E_m = AssemblyType(main_type_arg="E", sub_type_arg="m")
    type_E_f = AssemblyType(main_type_arg="E", sub_type_arg="f")

    type_F_m = AssemblyType(main_type_arg="F", sub_type_arg="m")
    type_F_f = AssemblyType(main_type_arg="F", sub_type_arg="f")

    # 타입간 조립 관계 데이터 베이스 저장
    assembly_data_base = AssemblyGroupDataBase()
    assembly_data_base.add_assembly_type_group([type_A_m, type_A_f])
    assembly_data_base.add_assembly_type_group([type_B_m, type_B_i, type_B_f])
    assembly_data_base.add_assembly_type_group([type_C_m, type_C_f])
    assembly_data_base.add_assembly_type_group([type_D_m, type_D_i, type_D_f])
    assembly_data_base.add_assembly_type_group([type_E_m, type_E_f])
    assembly_data_base.add_assembly_type_group([type_F_m, type_F_f])

    # 부품 데이터 생성 단계
    item_0 = Item(name_arg="도어체커")
    item_0.add_type(type_C_m)
    item_0.add_type(type_D_i)

    item_1 = Item(name_arg="도어레치")
    item_1.add_type(type_A_f)
    item_1.add_type(type_B_f)
    item_1.add_type(type_E_m)
    item_1.add_type(type_F_m)

    item_2 = Item(name_arg="프론트 도어")
    item_2.add_type(type_A_m)
    item_2.add_type(type_B_i)
    item_2.add_type(type_C_f)

    item_3 = Item(name_arg="바디")
    item_3.add_type(type_D_f)

    item_4 = Item(name_arg="볼트1")
    item_4.add_type(type_B_m)

    item_5 = Item(name_arg="볼트2")
    item_5.add_type(type_D_m)

    # State 정의 단계
    init_state = State(item_list=[item_0, item_1, item_2, item_3, item_4, item_5])

    # test
    bool = assembly_data_base.check_can_assemble([type_B_m, type_B_i, type_B_f])
    print(bool)
    bool = assembly_data_base.check_can_assemble([type_B_m, type_B_f])
    print(bool)
    bool = assembly_data_base.check_can_assemble([type_B_m, type_B_i])
    print(bool)
    bool = assembly_data_base.check_can_assemble([type_B_i, type_B_f])
    print(bool)
    bool = assembly_data_base.check_can_assemble([type_B_m])
    print(bool)
    bool = assembly_data_base.check_can_assemble([type_B_i])
    print(bool)
    bool = assembly_data_base.check_can_assemble([type_B_f])
    print(bool)
    bool = assembly_data_base.check_can_assemble([type_B_m, type_B_i, type_B_f, type_A_m, type_A_f])
    print(bool)

    plan_sequence = search_algorithm(init_state, None, assembly_data_base)
    print("-----")
    for match in plan_sequence:
        for assembly_type in match:
            parent_item = assembly_type.get_parent_item()
            print("부품 이름:", parent_item.name)
            main_type, sub_type = assembly_type.get_type()
            print(f"  └->매칭 후보 타입: {main_type}-{sub_type}")
        print("-----")

if __name__ == "__main__":
    main()


