"""娜比娅偷吃事件：回合制战斗练习。"""

from __future__ import annotations
import random
import time
from typing import Literal

Action = Literal["attack", "defend", "special"]
NabiyaAction = Literal["attack", "defend"]
BattleResult = Literal["nagato", "nabiya", "draw"]

NAGATO_MAX_HP = 115
NABIYA_MAX_HP = 105
NAGATO_ATTACK_DICE = 3
NAGATO_DEFEND_DICE = 2
NABIYA_ATTACK_DICE = 3
NABIYA_DEFEND_DICE = 2
SPECIAL_ATTACK_DAMAGE = 24
SPECIAL_ATTACK_SUCCESS_RATE = 0.45
CRITICAL_HIT_THRESHOLD = 15

NAGATO_LOW_HP_THRESHOLD = 30
NABIYA_SPECIAL_HP_THRESHOLD = 20
NABIYA_DEFEND_HP_THRESHOLD = 40
MAX_BATTLE_TURNS = 50


def display_status(character_name: str, current_hp: int, max_hp: int) -> None:
    """输出角色状态，格式为：[角色名]HP: 当前生命值 / 最大生命值。"""
    if max_hp <= 0:
        raise ValueError("最大生命值必须大于零。")
    
    current_hp = max(0, min(current_hp, max_hp))
    print(f"[{character_name}]HP: {current_hp} / {max_hp}")
    # 检查最大生命值是否合法，并使用 print() 输出角色状态。


def roll_dice(num_dice: int) -> int:
    """投掷指定数量的六面骰子并返回点数总和。"""
    if num_dice < 0:
        raise ValueError("骰子数量不能为负数。")
    
    cnt = 0
    while num_dice > 0:
        num_dice -= 1
        cnt += random.randint(1, 6)
    return cnt
    # 先处理非法骰子数量，再用 while 循环调用 random.randint(1, 6)。


def choose_nagato_action(nagato_hp: int, nabiya_hp: int) -> Action:
    """根据双方生命值选择长门的行动。"""
    if nagato_hp < NAGATO_LOW_HP_THRESHOLD:
        return "defend"
    if nabiya_hp < NABIYA_SPECIAL_HP_THRESHOLD:
        return "special"
    return "attack"
    # 长门生命值低于 30 时防御，娜比娅生命值低于 20 时使用特殊攻击，
    # 其余情况进行普通攻击；注意使用 if/elif/else 保持判断顺序。


def calculate_attack_damage(num_dice: int) -> int:
    """调用 roll_dice() 计算基础攻击伤害。"""
    return roll_dice(num_dice)
    # 把骰子数量传给 roll_dice()，并返回它的结果。


def calculate_defense_value(num_dice: int) -> int:
    """调用 roll_dice() 计算本回合的防御值。"""
    return roll_dice(num_dice)
    # 把骰子数量传给 roll_dice()，并返回它的结果。


def check_critical_hit(base_damage: int) -> bool:
    """判断基础伤害是否达到暴击阈值。"""
    if base_damage >= CRITICAL_HIT_THRESHOLD:
        return True
    return False
    # 当基础伤害大于等于 CRITICAL_HIT_THRESHOLD 时返回 True。


def nabiya_ai_action(nabiya_hp: int) -> NabiyaAction:
    """根据娜比娅生命值选择她的行动。"""
    if nabiya_hp <= NABIYA_DEFEND_HP_THRESHOLD:
        return "defend"
    return "attack"
    # 娜比娅生命值小于等于 40 时防御，否则攻击。


def calculate_final_damage(base_damage: int, defense_bonus: int) -> int:
    """用防御值抵消基础伤害，并返回不会小于零的最终伤害。"""
    if base_damage < 0:
        raise ValueError("基础伤害不能为负数。")
    if defense_bonus < 0:
        raise ValueError("防御值不能为负数。")
    return max(0, base_damage - defense_bonus)
    # 拒绝负数伤害或防御值，再计算 max(0, 基础伤害 - 防御值)。


def apply_damage(current_hp: int, base_damage: int, defense_bonus: int = 0) -> int:
    """结算一次攻击并返回不会小于零的剩余生命值。"""
    damage = calculate_final_damage(base_damage, defense_bonus)
    return max(0, current_hp - damage)
    # 调用 calculate_final_damage()，再从当前生命值中扣除最终伤害。


def is_battle_over(nagato_hp: int, nabiya_hp: int) -> bool:
    """判断是否至少有一名角色的生命值归零。"""
    if nagato_hp <= 0 or nabiya_hp <= 0:
        return True
    return False
    # 只要任意一方 HP 小于等于 0，就返回 True。


def get_battle_result(nagato_hp: int, nabiya_hp: int) -> BattleResult:
    """根据双方剩余生命值返回胜者或平局。"""
    if is_battle_over(nagato_hp, nabiya_hp):
        if nagato_hp > 0:
            return "nagato"
        elif nabiya_hp > 0:
            return "nabiya"
    return "draw"
    # 仅一方存活时返回对应结果；双方同时归零或都存活时返回 draw。


def _pause(seconds: float) -> None:
    """只有调用者要求展示战斗动画时才暂停。"""
    if seconds > 0:
        time.sleep(seconds)


def main_battle_loop(pause_seconds: float = 0.0,max_turns: int = MAX_BATTLE_TURNS,) -> BattleResult:
    """运行完整战斗，并返回 nagato、nabiya 或 draw。"""
    if pause_seconds < 0:
        raise ValueError("暂停秒数不能为负数。")
    if max_turns <= 0:
        raise ValueError("最大回合数必须大于零。")
    # 先检查 pause_seconds 和 max_turns 是否合理，不合理时抛出 ValueError。

    nagato_hp = NAGATO_MAX_HP
    nabiya_hp = NABIYA_MAX_HP
    nagato_defense_bonus = 0
    nabiya_defense_bonus = 0
    turn = 1

    while nagato_hp > 0 and nabiya_hp > 0 and turn <= max_turns:
        print(f"\n=== 第 {turn} 回合 ===")
        display_status("长门", nagato_hp, NAGATO_MAX_HP)
        display_status("娜比娅", nabiya_hp, NABIYA_MAX_HP)
        
        print("\n>>> 长门的回合")
        action = choose_nagato_action(nagato_hp, nabiya_hp)
        if action == "attack":
            base_damage = calculate_attack_damage(NAGATO_ATTACK_DICE)
            if check_critical_hit(base_damage):
                base_damage *= 2
                print("触发 BIG SEVEN：造成暴击伤害！")
            nabiya_hp = apply_damage(base_damage=base_damage,current_hp=nabiya_hp,defense_bonus=nabiya_defense_bonus)
            nabiya_defense_bonus = 0
            print(f"长门造成了伤害，娜比娅剩余 {nabiya_hp} 点生命值。")

        elif action == "defend":
            nagato_defense_bonus = calculate_defense_value(NAGATO_DEFEND_DICE)
            print(f"长门进入防御姿态，获得 {nagato_defense_bonus} 点防御值。")

        elif action == "special":
            if random.random() < SPECIAL_ATTACK_SUCCESS_RATE:
                nabiya_hp = apply_damage(base_damage=SPECIAL_ATTACK_DAMAGE,current_hp=nabiya_hp,defense_bonus=nabiya_defense_bonus)
                print(f"长门使用特殊攻击成功，娜比娅剩余 {nabiya_hp} 点生命值。")
            else:
                print("长门使用特殊攻击失败。")
            nabiya_defense_bonus = 0

        if is_battle_over(nagato_hp, nabiya_hp):
            break

        _pause(pause_seconds)
    
        print("\n>>> 娜比娅的回合")
        enemy_action = nabiya_ai_action(nabiya_hp)
        if enemy_action == "attack":
            base_damage = calculate_attack_damage(NABIYA_ATTACK_DICE)
            nagato_hp = apply_damage(base_damage=base_damage,current_hp=nagato_hp,defense_bonus=nagato_defense_bonus)
            nagato_defense_bonus = 0
            print(f"娜比娅造成了伤害，长门剩余 {nagato_hp} 点生命值。")
        elif enemy_action == "defend":
            nabiya_defense_bonus = calculate_defense_value(NABIYA_DEFEND_DICE)
            print(f"娜比娅进入防御姿态，获得 {nabiya_defense_bonus} 点防御值。")

        turn += 1
        _pause(pause_seconds)
    
    result = get_battle_result(nagato_hp, nabiya_hp)
    if result == "nagato":
        print("\n=== 战斗结束：长门获胜！ ===")
    elif result == "nabiya":
        print("\n=== 战斗结束：娜比娅获胜！ ===")
    else:
        print("\n=== 战斗结束：平局！ ===")
    return result
    # 循环结束后调用 get_battle_result()，输出中文结果并返回 result。