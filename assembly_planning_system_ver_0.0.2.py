import copy
from pprint import pprint
import uuid
from uuid import UUID

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
    # uuid_list:list[UUID] = []# 고유 ID 할당 시, 기존 ID 리스트를 확인하여 중복 방지
    def __init__(self, name_arg: str = ""):
        """Item 초기화
        
        Args:
            name_arg: 부품 이름 (기본값: "")
        """
        self.uuid:UUID = None# 고유 구분자
        self.name: str = name_arg
        self.type_list: list[AssemblyType] = []

        self.uuid = uuid.uuid4()
        # self.uuid = self.generate_uuid()
        # Item.uuid_list.append(self.uuid)

    # def __del__(self):
    #     Item.uuid_list.remove(self.uuid)

    # def generate_uuid(self):
    #     n = 0
    #     while True:
    #         n =+ 1 
    #         sampled_uuid = uuid.uuid4()
    #         if sampled_uuid not in Item.uuid_list:
    #             break
    #         if n >= 10:
    #             assert 0, "failed to generate uuid"
    #             break
    #     return sampled_uuid
    
    def get_uuid(self):
        return self.uuid

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
    
    def get_type_by_index(self, index)->AssemblyType:
        return self.type_list[index]


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

# 기존까지의 조립 과정을 로깅하는 기능 추가 필요
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
        self.action_sequence_log: list[tuple[UUID, int]] = []

    def get_item_state_list(self):
        """부품 상태 리스트 반환"""
        return self.item_state_list

    def loging_action_sequence(self, match_set_info:list[tuple[UUID, int]]):
        self.action_sequence_log.append(match_set_info)

    def get_action_sequence_log(self)->list[tuple[UUID, int]]:
        return self.action_sequence_log

def check_candidate_match(state_arg: State, assembly_data_base: AssemblyGroupDataBase) -> list[list[tuple[UUID, int]]]:
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
    before_visit_item_list: list[Item] = state_arg.get_item_state_list().copy()
    candidate_match_list: list[list[tuple[UUID, int]]] = []# item uuid와 assembly_type_index 를 통해 조립을 표현 

    while len(before_visit_item_list) > 0:
        # 검사할 부품 선택
        anchor_item: Item = before_visit_item_list.pop()
        anchor_item_uuid = anchor_item.get_uuid()
        anchor_assembly_type_list = anchor_item.get_type_list()
        
        for anchor_assembly_type_index, anchor_assembly_type in enumerate(anchor_assembly_type_list):
            anchor_main_type, sub_type = anchor_assembly_type.get_type()
            required_sub_type_list = assembly_data_base.get_assembly_group_data(anchor_main_type)

            if required_sub_type_list is not None and sub_type in required_sub_type_list:
                # 조립 가능한 타입 그룹의 일부를 발견
                candidate_assembly_info_list: list[tuple[UUID, int]] = [(anchor_item_uuid, anchor_assembly_type_index)]
                acquired_sub_type_list = [sub_type]
                
                # 나머지 부품들에서 조립 가능한 타입 찾기
                for visiting_item in before_visit_item_list:
                    visiting_item_uuid = visiting_item.get_uuid()
                    visiting_item_assembly_type_list = visiting_item.get_type_list()
                    
                    for visiting_assembly_type_index, visiting_item_assembly_type in enumerate(visiting_item_assembly_type_list):
                        if visiting_item_assembly_type.assembled_flag:
                            # 이미 조립에 사용된 타입은 건너뜀
                            continue
                        
                        visiting_main_type, visiting_sub_type = visiting_item_assembly_type.get_type()
                        
                        # 조립 가능 조건:
                        # 1. 같은 main_type
                        # 2. required_sub_type에 포함됨
                        # 3. 중복되지 않은 sub_type
                        if (visiting_main_type == anchor_main_type
                                and visiting_sub_type in required_sub_type_list
                                and visiting_sub_type not in acquired_sub_type_list):
                            
                            candidate_assembly_info_list.append((visiting_item_uuid, visiting_assembly_type_index))
                            acquired_sub_type_list.append(visiting_sub_type)
                            # 한 아이템에서 하나의 타입만 추가
                            break
                
                # 완전한 조립 그룹을 찾았는지 검증
                candidate_assembly_type_list = []
                for candidate_item_uuid, candidate_assembly_type_index in candidate_assembly_info_list:
                    for item in state_arg.get_item_state_list():
                        if item.get_uuid() == candidate_item_uuid:
                            candidate_item = item
                    candidate_assembly_type_list.append(candidate_item.get_type_by_index(candidate_assembly_type_index))

                if assembly_data_base.check_can_assemble(candidate_assembly_type_list):
                    candidate_match_list.append(candidate_assembly_info_list)

    return candidate_match_list

def execute_assemble(state_arg:State, match_set_info_arg: list[tuple[UUID, int]])->State:
    """조립 실행
    
    조립 가능한 타입들의 assembled_flag를 True로 설정하여
    해당 타입들이 조립에 사용되었음을 표시합니다.
    
    Args:
        match_set: 조립할 AssemblyType 리스트
    """
    state_copy = copy.deepcopy(state_arg)
    for item_uuid, assembly_type_index in match_set_info_arg:
        for item in state_copy.get_item_state_list():
            if item.get_uuid() == item_uuid:
                assembly_type = item.get_type_by_index(assembly_type_index)
                assembly_type.set_assembled_flag(True)
    state_copy.loging_action_sequence(match_set_info=match_set_info_arg)

    return state_copy


def search_algorithm_temp_demo(init_state_arg: list, goal_state_arg: list, 
                    assembly_data_base: AssemblyGroupDataBase) -> list[State]:
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
    n = 1
    iteration_limit = 10000
    state = init_state_arg
    while True:
        print(f"=== [Planning Step {n}] ===")
        n += 1
        if n >= iteration_limit:
            break
        # 현재 상태에서 가능한 조립 후보 탐색
        candidate_match_list = check_candidate_match(state, assembly_data_base)
        print("▶ 발견된 타입 매칭 후보:")
        if len(candidate_match_list) == 0:
            print("후보 리스트가 비었음!")
            print("더 이상 조립 가능한 타입 그룹이 없으므로 Planning 종료.")
            break
        
        print_match_info_list(state, candidate_match_list)
        
        # 첫 번째 후보 선택 (데모 버전 단순 전략)
        print("▶ 선택된 타입 매칭 후보:")
        elected_assembly_action = candidate_match_list[0]
        print_match_info(state, elected_assembly_action)
        
        # 조립 실행 및 계획에 추가
        print("▶ 조립 실행 및 상태 갱신:")
        state = execute_assemble(state, candidate_match_list[0])
        print_state_action_sequence_log(state)
        print("\n-----\n")

    return [state]# plan은 1가지가 아닐 수 있으므로 리스트의 형태로 반환


def search_algorithm_BFS(init_state_arg: list, assembly_data_base: AssemblyGroupDataBase) -> list[State]:
    """
    각 개별 State 객체에 action_sequence_log로서 최종 상태까지의 plan이 담기게 된다.
    BFS 방법을 통해 State 가 갱신되는 모든 경우를 candidate_match_list에서 선택해본다.

    그리고 더이상 조립을 진행할 수 없는 말단 상태의 State들을 한번에 묶어 반환한다.
    그리고 이것은 우리 시스템에서 가능한 모든 plan의 경우의 수를 순회한 것과 같다.
    """
    final_state_list:list[State] = []
    return 
    

def print_state_action_sequence_log(state:State):
    """조립 계획 시퀀스 출력
    
    각 조립 단계별로 어떤 부품들이 어떤 타입으로 조립되는지 출력합니다.
    
    Args:
        plan_sequence: 조립 계획 시퀀스
    """
    action_sequence_log = state.get_action_sequence_log()
    item_list = state.get_item_state_list()
    for planning_step, match in enumerate(action_sequence_log):
        print(f"[조립 단계 {planning_step + 1}]")
        for item_uuid, assembly_type_index in match:
            for item in item_list:
                if item.get_uuid() == item_uuid:
                    print("부품 이름:", item.name)
                    assembly_type = item.get_type_by_index(assembly_type_index)
                    main_type, sub_type = assembly_type.get_type()
                    print(f"  └─> 매칭 타입: {main_type}-{sub_type}")
        print("-----")
        
def print_match_info_list(state:State, match_info_list:list[tuple[UUID, int]]):
    for match_index, match_set in enumerate(match_info_list):
        print("--매칭[{}]--".format(match_index))
        for uuid, index in match_set:
            for item in state.get_item_state_list():
                if item.get_uuid() == uuid:
                    candidate_item = item
            assembly_type = candidate_item.get_type_by_index(index)
            print("item: {:15}, assembly_main_type: {}, assembly_sub_type: {}".format(candidate_item.name, assembly_type.main_type, assembly_type.sub_type)) 

def print_match_info(state:State, match_info:list[tuple[UUID, int]]):
    for uuid, index in match_info:
        for item in state.get_item_state_list():
            if item.get_uuid() == uuid:
                candidate_item = item
        assembly_type = candidate_item.get_type_by_index(index)
        print("item: {:15}, assembly_main_type: {}, assembly_sub_type: {}".format(candidate_item.name, assembly_type.main_type, assembly_type.sub_type)) 

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
    item_0 = Item(name_arg="door checker")
    item_0.add_type(type_C_m)
    item_0.add_type(type_D_i)

    item_1 = Item(name_arg="door latch")
    item_1.add_type(type_A_f)
    item_1.add_type(type_B_f)
    item_1.add_type(type_E_m)
    item_1.add_type(type_F_m)

    item_2 = Item(name_arg="front door")
    item_2.add_type(type_A_m)
    item_2.add_type(type_B_i)
    item_2.add_type(type_C_f)

    item_3 = Item(name_arg="body")
    item_3.add_type(type_D_f)

    item_4 = Item(name_arg="bolt1")
    item_4.add_type(type_B_m)

    item_5 = Item(name_arg="bolt2")
    item_5.add_type(type_D_m)

    # --- 1-4. 초기 상태 정의 ---
    init_state = State(item_list=[item_0, item_1, item_2, item_3, item_4, item_5])

    # ========================================
    # 2. 알고리즘 수행 단계
    # ========================================
    
    # --- 2-1. 조립 계획(Planning) 수행 ---
    print("---< Planning 시작 >---\n")
    final_state_list = search_algorithm_temp_demo(init_state, None, assembly_data_base)
    print("\n---< Planning 종료 >---")

    # --- 2-2. 결과 출력 ---
    print("---< 결과 출력 시작 >---\n")
    for final_state in final_state_list:
        print_state_action_sequence_log(final_state)
    print("\n---< 결과 출력 종료 >---")

if __name__ == "__main__":
    main()
