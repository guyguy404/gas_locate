import random
import math
import time
import rclpy
from sim.utils import *

car_info = [[Info() for i in range (2)] for j in range(3)]

index = [-1,-1]

con_loc = [Info() for i in range (3)] #直线重合的点
loc_index = 0

rclpy.init(args = None)

Utility = Utils()

def dis(inf_1,inf_2):
    return math.sqrt(((inf_1.pos[0]-inf_2.pos[0])*(inf_1.pos[0]-inf_2.pos[0])+(inf_1.pos[1]-inf_2.pos[1])*(inf_1.pos[1]-inf_2.pos[1]))) <= 0.1

def check_con(inf_1,inf_2):
    return inf_1.gas_conc > inf_2.gas_conc

def it(car_num): #int
    return int(car_num) - 1
def oit(car_num): #other_car_int
    if car_num == "1":
        return 1
    else: 
        return 0

def cn(car_num): #car_name
    return "car"+car_num
def ocn(car_num): #other_car_name:
    if car_num == "1":
        return "car2"
    else: 
        return "car1"

def adjust_info(i,car_num):
    for i in range (i,0,-1):
        if car_info[i][it(car_num)].gas_conc > car_info[i-1][it(car_num)].gas_conc:
            t = car_info[i][it(car_num)]
            car_info[i][it(car_num)] = car_info[i-1][it(car_num)]
            car_info[i-1][it(car_num)] = t


def modify_car_info(inf,car_num): # 我记录前三大小的浓度在数组中, 并且这些位置的距离不能小于 0.1
    if index[it(car_num)] == -1:
        car_info[0][it(car_num)]= inf
        index[it(car_num)] = 0
        return
    for i in range (index[it(car_num)] - 1,-1,-1):
        if dis(inf,car_info[i][it(car_num)]) and check_con(inf,car_info[i][it(car_num)]):
            car_info[i][it(car_num)] = inf
            adjust_info(i,car_num)
            return
    if index[it(car_num)] <= 2:    
        print
        car_info[index[it(car_num)]][it(car_num)] = inf
        index[it(car_num)] = index[it(car_num)] + 1
    else:
        if inf.gas_conc > car_info[2][it(car_num)].gas_conc:
            car_info[2][it(car_num)] = inf
        adjust_info(2,car_num)

def rotate(i,car_num):
    Utility.rotate("car"+car_num,i*2*math.pi)
    time.sleep(1)
    Utility.rotate("car"+car_num,0)

def forward(i,car_num):
    Utility.forward("car" + car_num,0.05)
    time.sleep(i)
    Utility.forward("car" + car_num,0)

def Circle(car_num): #走六边形
    forward(0.2,car_num)
    max_info = Utility.get_info()["car"+car_num]
    num = 0
    rotate(1.0/6,car_num)
    for i in range (6):
        rotate(1.0/6,car_num)
        forward(0.2,car_num)
        if i == 5:
            break
        if Utility.get_info()["car"+car_num].gas_conc>max_info.gas_conc:
            max_info = Utility.get_info()["car"+car_num]
            num = i + 1
    rotate(1.0/3,car_num)
    forward(0.2,car_num)
    rotate(0.5,car_num)
    return num

def Cal_dire(i, inf, car_num): #计算往哪边走
    global loc_index
    dire_first_x = 0
    dire_first_y = 0
    if (loc_index == 1):
        k_1 = (con_loc[0].pos[1] - inf[cn(car_num)].pos[1])/(con_loc[0].pos[0] - inf[cn(car_num)].pos[0])
        theta_1 = math.atan(k_1)
        if (con_loc[0].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_1 = math.pi + theta_1
        dire_first_x = math.cos(theta_1)
        dire_first_y = math.sin(theta_1)
    elif (loc_index == 2):
        k_1 = (con_loc[1].pos[1] - inf[cn(car_num)].pos[1])/(con_loc[1].pos[0] - inf[cn(car_num)].pos[0])
        theta_1 = math.atan(k_1)
        if (con_loc[1].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_1 = math.pi + theta_1
        k_2 = (con_loc[0].pos[1] - inf[cn(car_num)].pos[1])/(con_loc[0].pos[0] - inf[cn(car_num)].pos[0])
        theta_2 = math.atan(k_2)
        if (con_loc[0].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_2 = math.pi + theta_2
        dire_first_x = 0.75* math.cos(theta_1) + 0.25 * math.cos(theta_2)
        dire_first_y = 0.75* math.sin(theta_1) + 0.25 * math.sin(theta_2)
    elif (loc_index >= 3):
        k_1 = (con_loc[(loc_index - 1) % 3].pos[1] - inf[cn(car_num)].pos[1])/(con_loc[(loc_index - 1) % 3].pos[0] - inf[cn(car_num)].pos[0])
        theta_1 = math.atan(k_1)
        if (con_loc[(loc_index - 1) % 3].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_1 = math.pi + theta_1
        k_2 = (con_loc[(loc_index - 2) % 3].pos[1] - inf[cn(car_num)].pos[1])/(con_loc[(loc_index - 2) % 3].pos[0] - inf[cn(car_num)].pos[0])
        theta_2 = math.atan(k_2)
        if (con_loc[(loc_index - 2) % 3].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_2 = math.pi + theta_2
        k_3 = (con_loc[(loc_index - 3) % 3].pos[1] - inf[cn(car_num)].pos[1])/(con_loc[(loc_index - 3) % 3].pos[0] - inf[cn(car_num)].pos[0])
        theta_3 = math.atan(k_3)
        if (con_loc[(loc_index - 3) % 3].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_3 = math.pi + theta_3
        dire_first_x = 0.6* math.cos(theta_1) + 0.3 * math.cos(theta_2) + 0.1 *math.cos(theta_3)
        dire_first_y = 0.6* math.sin(theta_1) + 0.3 * math.sin(theta_2) + 0.1 *math.sin(theta_3)
    
    dire_second_x = 0
    dire_second_y = 0
    if (index[it(car_num)] == 0):
        k_1 = (car_info[0][it(car_num)].pos[1] - inf[cn(car_num)].pos[1])/(car_info[0][it(car_num)].pos[0] - inf[cn(car_num)].pos[0])
        theta_1 = math.atan(k_1)
        if (car_info[0][it(car_num)].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_1 = math.pi + theta_1
        dire_second_x = math.cos(theta_1)
        dire_second_y = math.sin(theta_1)
    elif (index[it(car_num)] == 1):
        k_1 = (car_info[0][it(car_num)].pos[1] - inf[cn(car_num)].pos[1])/(car_info[0][it(car_num)].pos[0] - inf[cn(car_num)].pos[0])
        theta_1 = math.atan(k_1)
        if (car_info[0][it(car_num)].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_1 = math.pi + theta_1
        k_2 = (car_info[1][it(car_num)].pos[1] - inf[cn(car_num)].pos[1])/(car_info[1][it(car_num)].pos[0] - inf[cn(car_num)].pos[0])
        theta_2 = math.atan(k_2)
        if (car_info[1][it(car_num)].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_2 = math.pi + theta_2
        dire_second_x = 0.75 *math.cos(theta_1) + 0.25 *math.cos(theta_2)
        dire_second_y = 0.75 *math.sin(theta_1) + 0.25 *math.sin(theta_2)
    else:
        k_1 = (car_info[0][it(car_num)].pos[1] - inf[cn(car_num)].pos[1])/(car_info[0][it(car_num)].pos[0] - inf[cn(car_num)].pos[0])
        theta_1 = math.atan(k_1)
        if (car_info[0][it(car_num)].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_1 = math.pi + theta_1
        k_2 = (car_info[1][it(car_num)].pos[1] - inf[cn(car_num)].pos[1])/(car_info[1][it(car_num)].pos[0] - inf[cn(car_num)].pos[0])
        theta_2 = math.atan(k_2)
        if (car_info[1][it(car_num)].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_2 = math.pi + theta_2
        k_3 = (car_info[2][it(car_num)].pos[1] - inf[cn(car_num)].pos[1])/(car_info[2][it(car_num)].pos[0] - inf[cn(car_num)].pos[0])
        theta_3 = math.atan(k_3)
        if (car_info[2][it(car_num)].pos[0] - inf[cn(car_num)].pos[0] < 0): theta_3 = math.pi + theta_3
        dire_second_x = 0.6 *math.cos(theta_1) + 0.3 *math.cos(theta_2) + 0.1*math.cos(theta_3)
        dire_second_y = 0.6 *math.sin(theta_1) + 0.3 *math.sin(theta_2) + 0.1*math.sin(theta_3)

    
    if inf[cn(car_num)].gas_conc < inf[ocn(car_num)].gas_conc:
        k = (car_info[0][oit(car_num)].pos[1] - inf[cn(car_num)].pos[1])/(car_info[0][oit(car_num)].pos[0] - inf[cn(car_num)].pos[0])
        theta = math.atan(k)
        if (car_info[0][oit(car_num)].pos[0] - inf[cn(car_num)].pos[0] < 0): theta = math.pi + theta
        dire_x = 0.25 *(3 - i) * dire_first_x + 0.25 * (i + 1) * 0.5 *dire_second_x + 0.5 * 0.25 * (i + 1) *math.cos(theta)
        dire_y = 0.25 *(3 - i) * dire_first_y + 0.25 * (i + 1) * 0.5 *dire_second_y + 0.5 * 0.25 * (i + 1) *math.sin(theta)
        theta_final = math.atan(dire_y/dire_x)
        if (dire_x < 0):
            theta_final = math.pi + theta_final
        theta_final = -theta_final
        if (theta_final < 0): theta_final = 2*math.pi + theta_final
        return theta_final
    else :
        dire_x = 0.25 *(3 - i) * dire_first_x + 0.05 * (i + 1) *dire_second_x
        dire_y = 0.25 *(3 - i) * dire_first_y + 0.05 * (i + 1) *dire_second_y
        theta_final = math.atan(dire_y/dire_x)
        if (dire_x < 0):
            theta_final = math.pi + theta_final
        theta_final = -theta_final
        if (theta_final < 0): theta_final = 2*math.pi + theta_final
        return theta_final

def main():
    global loc_index
    for i in range (1): # 由于一开始生成在同一点，因此我让他随机游走 10 步
        rotate(random.random(),"1")
        rotate(random.random(),"2")
        forward(random.random(),"1")
        forward(random.random(),"2")
        modify_car_info(Utility.get_info()["car1"],"1")
        modify_car_info(Utility.get_info()["car2"],"2")
        print("first step:"+str(i))
    print("first step finished")
    for i in range (4):
        inf_1 = Utility.get_info()["car1"]
        inf_2 = Utility.get_info()["car2"]
        inf = Utility.get_info()
        num_1 = Circle("1")
        num_2 = Circle("2")
        theta_1 = -(math.pi/3 * num_1 + inf_1.orien)
        theta_2 = -(math.pi/3 * num_2 + inf_2.orien)
        x = (inf_1.pos[1] - inf_2.pos[1] + math.tan(theta_2) * inf_2.pos[0] + math.tan(theta_1) * inf_1.pos[0])/(math.tan(theta_2) - math.tan(theta_1))
        y = (math.tan(theta_1) * (x - inf_1.pos[0])) + inf_1.pos[1]
        if x < 2 and x > -2 and y < 2 and y > -2 :
            con_loc[loc_index % 3].pos[0] = x
            con_loc[loc_index % 3].pos[1] = y
            loc_index = loc_index + 1
        ori_1 = Cal_dire(i, inf,"1")
        ori_2 = Cal_dire(i, inf,"2")
        if (ori_1 > inf_1.orien):
            rotate((ori_1-inf_1.orien)/(2*math.pi),"1")
        else:
            rotate((ori_1-inf_1.orien + 2*math.pi)/(2*math.pi),"1")
        if (ori_2 > inf_2.orien):
            rotate((ori_2-inf_2.orien)/(2*math.pi),"2")
        else:
            rotate((ori_2-inf_2.orien + 2*math.pi)/(2*math.pi),"2")
        forward(1,"1")
        forward(1,"2")
        modify_car_info(Utility.get_info()["car1"],"1")
        modify_car_info(Utility.get_info()["car2"],"2")
        print("second step:"+str(i))
    print("second step finished")
    loc_index = 0 # 不需要模型了
    rdm_1 = 0 #是否需要大肠杆菌随机
    rdm_2 = 0
    for i in range(20):
        inf_1 = Utility.get_info()["car1"]
        inf_2 = Utility.get_info()["car2"]
        inf = Utility.get_info()
        ori_1 = Cal_dire(19, inf, "1") + rdm_1 * 2* (random.random()-0.5) *math.pi/6 # 不需要模型了
        ori_2 = Cal_dire(19, inf, "2") + rdm_2 * 2* (random.random()-0.5) *math.pi/6
        if (ori_1 > inf_1.orien):
            rotate((ori_1-inf_1.orien)/(2*math.pi),"1")
        else:
            rotate((ori_1-inf_1.orien + 2*math.pi)/(2*math.pi),"2")
        if (ori_2 > inf_2.orien):
            rotate((ori_2-inf_2.orien)/(2*math.pi),"2")
        else:
            rotate((ori_2-inf_2.orien + 2*math.pi)/(2*math.pi),"2")
        forward(1,"1")
        forward(1,"2")
        con_max_1 = car_info[0][it("1")].gas_conc
        con_max_2 = car_info[0][it("2")].gas_conc
        modify_car_info(Utility.get_info()["car1"],"1")
        modify_car_info(Utility.get_info()["car2"],"2")
        if (con_max_1 == car_info[0][it("1")].gas_conc):
            rdm_1 = 1
        else:
            rdm_1 = 0
        if (con_max_2 == car_info[0][it("2")].gas_conc):
            rdm_2 = 1
        else:
            rdm_2 = 0
        print("third step:"+str(i))
    if (car_info[0][it("1")].gas_conc > car_info[0][it("2")].gas_conc): #输出最大的浓度坐标
        print(car_info[0][it("2")].pos[0],car_info[0][it("1")].pos[1])
    else:
        print(car_info[0][it("2")].pos[0],car_info[0][it("2")].pos[1])
    rclpy.shutdown()
