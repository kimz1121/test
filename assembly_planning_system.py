from pprint import pprint


class AssemblyType:
    """조립부 종류를 나타내는 클래스
    
    조립부 간의 차이점과 공통점을 구분하기 위한 타입 정보를 저장합니다.
    각 AssemblyType은 main_type과 sub_type으로 구성되며,
    조립 가능 여부를 판단하는 기준이 됩니다.
    
    Attributes:
        assembled_flag (bool): 해당 타입이 조립에 사용되었는지 여부
        parent_item (Item): 이 타입을 소유한 부품 객체
        main_type (str): 주 타입 (예: 'A', 'B', 'C')
        sub_type (str): 부 타입 (예: 'm', 'f', 'i')
    """
    
    def __init__(self, main_type_arg: str, sub_type_arg: str = ""):
        """AssemblyType 초기화
        
        Args:
            main_type_arg: 주 타입 문자열
            sub_type_arg: 부 타입 문자열 (기본값: "")
        """
        self.assembled_flag = False  # 초기 상태: 조립에 미사용
        self.parent_item: 'Item' = None
        self.main_type: str = ""
        self.sub_type: str = ""
        self.set_type(main_type_arg, sub_type_arg)

    def set_type(self, main_type_arg: str, sub_type_arg: str = ""):
        """타입 설정"""
        self.main_type = main_type_arg
        self.sub_type = sub_type_arg

    def get_type(self) -> tuple[str, str]:
        """타입 정보 반환
        
        Returns:
            (main_type, sub_type) 튜플
        """
        return self.main_type, self.sub_type
    
    def set_assembled_flag(self, assembled_flag_arg: bool):
        """조립 사용 여부 플래그 설정"""
        self.assembled_flag = assembled_flag_arg

    def set_parent_item(self, parent_item_arg: 'Item'):
        """부모 아이템(부품) 설정"""
        self.parent_item = parent_item_arg
    
    def get_parent_item(self):
        """부모 아이템(부품) 반환"""
        return self.parent_item


class Item:
    """부품을 나타내는 클래스
    
    부품의 이름과 해당 부품이 가진 여러 조립부 타입(AssemblyType)을 관리합니다.
    하나의 부품은 여러 개의 조립부 타입을 가질 수 있습니다.
    
    Attributes:
        name (str): 부품 이름
        type_list (list[AssemblyType]): 부품이 가진 조립부 타입 리스트
    """
    
    static_type_dict = {}
    
    def __init__(self, name_arg: str = ""):
        """Item 초기화
        
        Args:
            name_arg: 부품 이름 (기본값: "")
        """
        self.name: str = name_arg
        self.type_list: list[AssemblyType] = []

    def set_name(self, name_arg: str):
        """부품 이름 설정"""
        self.name = name_arg

    def add_type(self, type_arg: AssemblyType):
        """조립부 타입 추가
        
        Args:
            type_arg: 추가할 AssemblyType 객체
        """
        self.type_list.append(type_arg)
        type_arg.set_parent_item(self)

    def get_type_list(self) -> list[AssemblyType]:
        """조립부 타입 리스트 반환"""
        return self.type_list


class AssemblyGroupDataBase:
    """조립 가능한 타입 그룹 정보를 저장하는 데이터베이스
    
    어떤 AssemblyType들이 서로 조립 가능한지에 대한 규칙을 저장합니다.
    matching_system은 이 데이터베이스를 조회하여 조립 가능 여부를 판단합니다.
    
    예: main_type 'A'에 대해 ['m', 'f']가 저장되어 있다면,
        A-m과 A-f 타입이 서로 조립 가능함을 의미합니다.
    
    Attributes:
        assembly_group_data (dict): {main_type: [sub_type 리스트]} 형태의 조립 그룹 데이터
    """
    
    def __init__(self):
        self.assembly_group_data = {}

    def add_assembly_type_group(self, assembly_type_group: list[AssemblyType]):
        """조립 가능한 타입 그룹 추가
        
        같은 main_type을 가진 AssemblyType들의 sub_type 목록을 저장합니다.
        
        Args:
            assembly_type_group: 조립 가능한 AssemblyType 리스트
        """
        if len(assembly_type_group) > 0:
            assembly_type = assembly_type_group[0]
            group_type, _ = assembly_type.get_type()
            sub_type_list = []
            
            for assembly_type in assembly_type_group:
                main_type, sub_type = assembly_type.get_type()
                if group_type != main_type:
                    # 타입 그룹화 오류: 서로 다른 main_type 간의 그룹화 시도
                    return
                sub_type_list.append(sub_type)
            
            self.assembly_group_data.update({group_type: sub_type_list})

    def get_assembly_group_data(self, main_type: str) -> list:
        """특정 main_type에 대한 조립 가능한 sub_type 리스트 반환
        
        Args:
            main_type: 조회할 main_type
            
        Returns:
            해당 main_type과 조립 가능한 sub_type 리스트
        """
        return self.assembly_group_data.get(main_type)

    def check_can_assemble(self, candidate_type_group: list[AssemblyType]) -> bool:
        """후보 타입 그룹이 조립 가능한지 검증
        
        주어진 AssemblyType 리스트가 데이터베이스에 정의된 
        조립 규칙을 만족하는지 확인합니다.
        
        Args:
            candidate_type_group: 검증할 AssemblyType 리스트
            
        Returns:
            조립 가능 여부 (True/False)
        """
        main_type_list: list = []
        sub_type_list: list = []
        
        for type in candidate_type_group:
            main_type, sub_type = type.get_type()
            main_type_list.append(main_type)
            sub_type_list.append(sub_type)
        
        # 모든 타입이 같은 main_type을 가지는지 확인
        if all(main_type_list):
            main_type = main_type_list[0]
            grouped_sub_type_data = self.assembly_group_data.get(main_type)

            for sub_type in grouped_sub_type_data:
                if sub_type in sub_type_list:
                    sub_type_list.remove(sub_type)
                else:
                    # 필요한 sub_type이 후보 그룹에 없음
                    return False
            
            if len(sub_type_list) == 0:
                # 필요한 sub_type을 모두 찾음: 조립 가능
                return True
            else:
                # 필요한 것보다 더 많은 sub_type이 있음: 조립 불가
                return False


class State:
    """시스템의 전체 상태를 나타내는 클래스
    
    모든 부품(Item)의 현재 상태를 하나의 객체로 관리합니다.
    Planning 시스템이 개별 아이템이 아닌 전체 상태를 기반으로 
    의사결정을 할 수 있도록 합니다.
    
    Attributes:
        item_state_list (list[Item]): 현재 상태의 부품 리스트
    """
    
    def __init__(self, item_list):
        """State 초기화
        
        Args:
            item_list: Item 객체들의 리스트
        """
        self.item_state_list: list[Item] = item_list.copy()

    def get_item_state_list(self):
        """부품 상태 리스트 반환"""
        return self.item_state_list


def check_matching(state_arg: State, assembly_data_base: AssemblyGroupDataBase) -> list[list[AssemblyType]]:
    """현재 상태에서 가능한 조립 후보들을 탐색
    
    주어진 상태(State)에서 조립 가능한 AssemblyType 조합들을 찾습니다.
    각 조합은 데이터베이스의 조립 규칙을 만족해야 합니다.
    
    Args:
        state_arg: 현재 시스템 상태
        assembly_data_base: 조립 규칙 데이터베이스
        
    Returns:
        조립 가능한 AssemblyType 조합들의 리스트
        각 조합은 [AssemblyType, AssemblyType, ...] 형태
    """
    before_check_item_list: list[Item] = state_arg.get_item_state_list().copy()
    after_check_item_list: list[Item] = []
    match_list: list[AssemblyType] = []

    while len(before_check_item_list) > 0:
        # 검사할 부품 선택
        end_item: Item = before_check_item_list.pop()
        assembly_type_list = end_item.get_type_list()
        
        for assembly_type in assembly_type_list:
            main_type, sub_type = assembly_type.get_type()
            required_sub_type_list = assembly_data_base.get_assembly_group_data(main_type)

            if required_sub_type_list is not None and sub_type in required_sub_type_list:
                # 조립 가능한 타입 그룹의 일부를 발견
                assembly_candidate: list[AssemblyType] = [assembly_type]
                acquired_sub_type_list = [sub_type]
                
                # 나머지 부품들에서 조립 가능한 타입 찾기
                for check_item in before_check_item_list:
                    check_item_type_list = check_item.get_type_list()
                    
                    for check_item_type in check_item_type_list:
                        if check_item_type.assembled_flag:
                            # 이미 조립에 사용된 타입은 건너뜀
                            continue
                        
                        check_main_type, check_sub_type = check_item_type.get_type()
                        
                        # 조립 가능 조건:
                        # 1. 같은 main_type
                        # 2. required_sub_type에 포함됨
                        # 3. 중복되지 않은 sub_type
                        if (check_main_type == main_type
                                and check_sub_type in required_sub_type_list
                                and check_sub_type not in acquired_sub_type_list):
                            assembly_candidate.append(check_item_type)
                            acquired_sub_type_list.append(check_sub_type)
                            # 한 아이템에서 하나의 타입만 추가
                            break
                
                # 완전한 조립 그룹을 찾았는지 검증
                if assembly_data_base.check_can_assemble(assembly_candidate):
                    match_list.append(assembly_candidate)

    return match_list


def execute_assemble(match_set: list[AssemblyType]):
    """조립 실행
    
    조립 가능한 타입들의 assembled_flag를 True로 설정하여
    해당 타입들이 조립에 사용되었음을 표시합니다.
    
    Args:
        match_set: 조립할 AssemblyType 리스트
    """
    for assembly_type in match_set:
        assembly_type.set_assembled_flag(True)


def search_algorithm(init_state_arg: list, goal_state_arg: list, 
                    assembly_data_base: AssemblyGroupDataBase) -> list[list[AssemblyType]]:
    """조립 계획 탐색 알고리즘
    
    초기 상태에서 목표 상태까지 도달하기 위한 조립 순서를 계획합니다.
    
    [중요: 임시 구현 상태]
    본 함수는 다른 알고리즘 모듈의 작동을 테스트하기 위한 
    단순화된 임시 버전입니다.
    
    아직 구현되지 않은 필수 기능:
    - 다양한 조립 순서 조합 탐색 (Search Algorithm)
    - 목표 상태(goal_state) 고려
    
    현재는 먼저 발견된 조립 가능한 후보부터 순서대로 조립하는
    단순한 방식으로만 동작합니다.
    이는 정식 Planning 알고리즘이 아니며, 
    향후 연구 개발을 통해 핵심 알고리즘이 구현되어야 합니다.
    
    Args:
        init_state_arg: 초기 상태
        goal_state_arg: 목표 상태 (현재 미사용)
        assembly_data_base: 조립 규칙 데이터베이스
        
    Returns:
        조립 순서를 나타내는 계획 시퀀스
        각 단계는 [AssemblyType, ...] 형태의 조립 그룹
    """
    plan_sequence: list[list[AssemblyType]] = []
    n = 1
    
    while True:
        print(f"=== [Planning Step {n}] ===")
        n += 1
        
        # 현재 상태에서 가능한 조립 후보 탐색
        match_list = check_matching(init_state_arg, assembly_data_base)
        
        print("▶ 발견된 타입 매칭 후보:")
        if len(match_list) == 0:
            print("후보 리스트가 비었음!")
            print("더 이상 조립 가능한 타입 그룹이 없으므로 Planning 종료.")
            break

        pprint([[assembly_type.get_type() for assembly_type in match] 
                for match in match_list])
        
        # 첫 번째 후보 선택 (데모 버전 단순 전략)
        print("▶ 선택된 타입 매칭 후보:")
        print([assembly_type.get_type() for assembly_type in match_list[0]])
        
        # 조립 실행 및 계획에 추가
        print("▶ 조립 실행 및 상태 갱신:")
        plan_sequence.append(match_list[0])
        execute_assemble(match_list[0])
        print("\n-----\n")

    return plan_sequence


def print_plan_sequence(plan_sequence: list[list[AssemblyType]]):
    """조립 계획 시퀀스 출력
    
    각 조립 단계별로 어떤 부품들이 어떤 타입으로 조립되는지 출력합니다.
    
    Args:
        plan_sequence: 조립 계획 시퀀스
    """
    for planning_step, match in enumerate(plan_sequence):
        print(f"[조립 단계 {planning_step + 1}]")
        for assembly_type in match:
            parent_item = assembly_type.get_parent_item()
            print("부품 이름:", parent_item.name)
            main_type, sub_type = assembly_type.get_type()
            print(f"  └─> 매칭 타입: {main_type}-{sub_type}")
        print("-----")


def main():
    """메인 함수: 조립 계획 시스템 데모"""
    
    # ========================================
    # 1. 데이터 생성 단계
    # ========================================
    
    # --- 1-1. 조립 타입 데이터 생성 ---
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

    # --- 1-2. 조립 규칙 데이터베이스 구축 ---
    # 어떤 타입들이 서로 조립 가능한지 정의
    assembly_data_base = AssemblyGroupDataBase()
    assembly_data_base.add_assembly_type_group([type_A_m, type_A_f])
    assembly_data_base.add_assembly_type_group([type_B_m, type_B_i, type_B_f])
    assembly_data_base.add_assembly_type_group([type_C_m, type_C_f])
    assembly_data_base.add_assembly_type_group([type_D_m, type_D_i, type_D_f])
    assembly_data_base.add_assembly_type_group([type_E_m, type_E_f])
    assembly_data_base.add_assembly_type_group([type_F_m, type_F_f])

    # --- 1-3. 부품 데이터 생성 ---
    item_0 = Item(name_arg="도어체커")
    item_0.add_type(type_C_m)
    item_0.add_type(type_D_i)

    item_1 = Item(name_arg="도어래치")
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

    # --- 1-4. 초기 상태 정의 ---
    init_state = State(item_list=[item_0, item_1, item_2, item_3, item_4, item_5])

    # ========================================
    # 2. 알고리즘 수행 단계
    # ========================================
    
    # --- 2-1. 조립 계획(Planning) 수행 ---
    print("---< Planning 시작 >---\n")
    plan_sequence = search_algorithm(init_state, None, assembly_data_base)
    print("\n---< Planning 종료 >---")

    # --- 2-2. 결과 출력 ---
    print("---< 결과 출력 시작 >---\n")
    print_plan_sequence(plan_sequence)
    print("\n---< 결과 출력 종료 >---")


if __name__ == "__main__":
    main()
