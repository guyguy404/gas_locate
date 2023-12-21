import random
import math
import time
import rclpy
from sim.utils import Utils, Info

def main():

    car_1_info = [Info() for i in range (3)]
    car_2_info = [Info() for i in range (3)]

    index_1 = -1
    index_2 = -1

    con_loc = [Info() for i in range (3)]
    loc_index = 0

    def dis(inf_1,inf_2):
        return math.sqrt(((inf_1.pos[0]-inf_2.pos[0])*(inf_1.pos[0]-inf_2.pos[0])+(inf_1.pos[1]-inf_2.pos[1])*(inf_1.pos[1]-inf_2.pos[1]))) <= 0.1

    def check_con(inf_1,inf_2):
        return inf_1.gas_conc > inf_2.gas_conc

    def adjust_info_1(i):
        for i in range (i,0,-1):
            if car_1_info[i].gas_conc > car_1_info[i-1].gas_conc:
                t = car_1_info[i]
                car_1_info[i] = car_1_info[i-1]
                car_1_info[i-1] = t

    def adjust_info_2(i):
        for i in range (i,0,-1):
            if car_2_info[i].gas_conc > car_2_info[i-1].gas_conc:
                t = car_2_info[i]
                car_2_info[i] = car_2_info[i-1]
                car_2_info[i-1] = t

    def modify_car_1_info(inf): # 我记录前三大小的浓度在数组中, 并且这些位置的距离不能小于 0.1
        if index_1 == -1:
            car_1_info[0]= inf
            index_1 = 0
            return
        for i in range (index_1 - 1,-1,-1):
            if dis(inf,car_1_info[i]) and check_con(inf,car_1_info[i]):
                car_1_info[i] = inf
                adjust_info_1(i)
                return
        if index_1 <= 2:    
            car_1_info[index_1] = inf
            index_1 = index_1 + 1
        else:
            if inf.gas_conc > car_1_info[2].gas_conc:
                car_1_info[2] = inf
            adjust_info_1(2)

    def modify_car_2_info(inf):
        if index_2 == -1:
            car_2_info[0]= inf
            index_2 = 0
            return
        for i in range (index_2 - 1,-1,-1):
            if dis(inf,car_2_info[i]) and check_con(inf,car_2_info[i]):
                car_2_info[i] = inf
                adjust_info_2(i)
                return
        if index_2 <= 2:    
            car_2_info[index_2] = inf
            index_2 = index_2 + 1
        else:
            if inf.gas_conc > car_2_info[2].gas_conc:
                car_2_info[2] = inf
            adjust_info_2(2)

    def rotate_1(i):
        car_1.rotate(i*2*math.pi)
        time.sleep(1)
        car_1.rotate(0)

    def rotate_2(i):
        car_2.rotate(i*2*math.pi)
        time.sleep(1)
        car_2.rotate(0)

    def forward_1(i):
        car_1.forward(0.05)
        time.sleep(i)
        car_1.forward(0)

    def forward_2(i):
        car_2.forward(0.05)
        time.sleep(i)
        car_2.forward(0)

    def Circle_1(): #走六边形
        forward_1(0.2)
        max_info = car_1.get_info()
        num = 0
        rotate_1(1.0/6)
        for i in range (6):
            rotate_1(1.0/6)
            forward_1(0.2)
            if i == 5:
                break
            if car_1.get_info().gas_conc>max_info.gas_conc:
                max_info = car_1.get_info
                num = i + 1
        rotate_1(1.0/3)
        forward_1(0.2)
        rotate_1(0.5)
        return num

    def Circle_2(): #走六边形
        forward_2(0.2)
        max_info = car_2.get_info()
        num = 0
        rotate_2(1.0/6)
        for i in range (6):
            rotate_2(1.0/6)
            forward_2(0.2)
            if i == 5:
                break
            if car_2.get_info().gas_conc>max_info.gas_conc:
                max_info = car_2.get_info
                num = i + 1
        rotate_2(1.0/3)
        forward_2(0.2)
        rotate_2(0.5)
        return num

    def Cal_dire_1(i):
        dire_first_x = 0
        dire_first_y = 0
        if (loc_index == 1):
            k_1 = (con_loc[0].pos[1] - inf_1.pos[1])/(con_loc[0].pos[0] - inf_1.pos[0])
            theta_1 = math.atan(k_1)
            if (con_loc[0].pos[0] - inf_1.pos[0] < 0): theta_1 = math.pi + theta_1
            dire_first_x = math.cos(theta_1)
            dire_first_y = math.sin(theta_1)
        elif (loc_index == 2):
            k_1 = (con_loc[1].pos[1] - inf_1.pos[1])/(con_loc[1].pos[0] - inf_1.pos[0])
            theta_1 = math.atan(k_1)
            if (con_loc[1].pos[0] - inf_1.pos[0] < 0): theta_1 = math.pi + theta_1
            k_2 = (con_loc[0].pos[1] - inf_1.pos[1])/(con_loc[0].pos[0] - inf_1.pos[0])
            theta_2 = math.atan(k_2)
            if (con_loc[0].pos[0] - inf_1.pos[0] < 0): theta_2 = math.pi + theta_2
            dire_first_x = 0.75* math.cos(theta_1) + 0.25 * math.cos(theta_2)
            dire_first_y = 0.75* math.sin(theta_1) + 0.25 * math.sin(theta_2)
        elif (loc_index >= 3):
            k_1 = (con_loc[(loc_index - 1) % 3].pos[1] - inf_1.pos[1])/(con_loc[(loc_index - 1) % 3].pos[0] - inf_1.pos[0])
            theta_1 = math.atan(k_1)
            if (con_loc[(loc_index - 1) % 3].pos[0] - inf_1.pos[0] < 0): theta_1 = math.pi + theta_1
            k_2 = (con_loc[(loc_index - 2) % 3].pos[1] - inf_1.pos[1])/(con_loc[(loc_index - 2) % 3].pos[0] - inf_1.pos[0])
            theta_2 = math.atan(k_2)
            if (con_loc[(loc_index - 2) % 3].pos[0] - inf_1.pos[0] < 0): theta_2 = math.pi + theta_2
            k_3 = (con_loc[(loc_index - 3) % 3].pos[1] - inf_1.pos[1])/(con_loc[(loc_index - 3) % 3].pos[0] - inf_1.pos[0])
            theta_3 = math.atan(k_3)
            if (con_loc[(loc_index - 3) % 3].pos[0] - inf_1.pos[0] < 0): theta_3 = math.pi + theta_3
            dire_first_x = 0.6* math.cos(theta_1) + 0.3 * math.cos(theta_2) + 0.1 *math.cos(theta_3)
            dire_first_y = 0.6* math.sin(theta_1) + 0.3 * math.sin(theta_2) + 0.1 *math.sin(theta_3)
        
        dire_second_x = 0
        dire_second_y = 0
        if (index_1 == 0):
            k_1 = (car_1_info[0].pos[1] - inf_1.pos[1])/(car_1_info[0].pos[0] - inf_1.pos[0])
            theta_1 = math.atan(k_1)
            if (car_1_info[0].pos[0] - inf_1.pos[0] < 0): theta_1 = math.pi + theta_1
            dire_second_x = math.cos(theta_1)
            dire_second_y = math.sin(theta_1)
        elif (index_1 == 1):
            k_1 = (car_1_info[0].pos[1] - inf_1.pos[1])/(car_1_info[0].pos[0] - inf_1.pos[0])
            theta_1 = math.atan(k_1)
            if (car_1_info[0].pos[0] - inf_1.pos[0] < 0): theta_1 = math.pi + theta_1
            k_2 = (car_1_info[1].pos[1] - inf_1.pos[1])/(car_1_info[1].pos[0] - inf_1.pos[0])
            theta_2 = math.atan(k_2)
            if (car_1_info[1].pos[0] - inf_1.pos[0] < 0): theta_2 = math.pi + theta_2
            dire_second_x = 0.75 *math.cos(theta_1) + 0.25 *math.cos(theta_2)
            dire_second_y = 0.75 *math.sin(theta_1) + 0.25 *math.sin(theta_2)
        else:
            k_1 = (car_1_info[0].pos[1] - inf_1.pos[1])/(car_1_info[0].pos[0] - inf_1.pos[0])
            theta_1 = math.atan(k_1)
            if (car_1_info[0].pos[0] - inf_1.pos[0] < 0): theta_1 = math.pi + theta_1
            k_2 = (car_1_info[1].pos[1] - inf_1.pos[1])/(car_1_info[1].pos[0] - inf_1.pos[0])
            theta_2 = math.atan(k_2)
            if (car_1_info[1].pos[0] - inf_1.pos[0] < 0): theta_2 = math.pi + theta_2
            k_3 = (car_1_info[2].pos[1] - inf_1.pos[1])/(car_1_info[2].pos[0] - inf_1.pos[0])
            theta_3 = math.atan(k_3)
            if (car_1_info[2].pos[0] - inf_1.pos[0] < 0): theta_3 = math.pi + theta_3
            dire_second_x = 0.6 *math.cos(theta_1) + 0.3 *math.cos(theta_2) + 0.1*math.cos(theta_3)
            dire_second_y = 0.6 *math.sin(theta_1) + 0.3 *math.sin(theta_2) + 0.1*math.sin(theta_3)

        
        if inf_1.gas_conc < inf_2.gas_conc:
            k = (car_2_info[0].pos[1] - inf_1.pos[1])/(car_2_info[0].pos[0] - inf_1.pos[0])
            theta = math.atan(k)
            if (car_2_info[0].pos[0] - inf_1.pos[0] < 0): theta = math.pi + theta
            dire_x = 0.05 *(19 - i) * dire_first_x + 0.05 * (i + 1) * 0.5 *dire_second_x + 0.5 * 0.05 * (i + 1) *math.cos(theta)
            dire_y = 0.05 *(19 - i) * dire_first_y + 0.05 * (i + 1) * 0.5 *dire_second_y + 0.5 * 0.05 * (i + 1) *math.sin(theta)
            theta_final = math.atan(dire_y/dire_x)
            if (dire_x < 0):
                theta_final = math.pi + theta_final
            theta_final = -theta_final
            if (theta_final < 0): theta_final = 2*math.pi + theta_final
            return theta_final
        else :
            dire_x = 0.05 *(19 - i) * dire_first_x + 0.05 * (i + 1) *dire_second_x
            dire_y = 0.05 *(19 - i) * dire_first_y + 0.05 * (i + 1) *dire_second_y
            theta_final = math.atan(dire_y/dire_x)
            if (dire_x < 0):
                theta_final = math.pi + theta_final
            theta_final = -theta_final
            if (theta_final < 0): theta_final = 2*math.pi + theta_final
            return theta_final

    def Cal_dire_2(i): #计算往哪边走
        dire_first_x = 0
        dire_first_y = 0
        if (loc_index == 1):
            k_1 = (con_loc[0].pos[1] - inf_2.pos[1])/(con_loc[0].pos[0] - inf_2.pos[0])
            theta_1 = math.atan(k_1)
            if (con_loc[0].pos[0] - inf_2.pos[0] < 0): theta_1 = math.pi + theta_1
            dire_first_x = math.cos(theta_1)
            dire_first_y = math.sin(theta_1)
        elif (loc_index == 2):
            k_1 = (con_loc[1].pos[1] - inf_2.pos[1])/(con_loc[1].pos[0] - inf_2.pos[0])
            theta_1 = math.atan(k_1)
            if (con_loc[1].pos[0] - inf_2.pos[0] < 0): theta_1 = math.pi + theta_1
            k_2 = (con_loc[0].pos[1] - inf_2.pos[1])/(con_loc[0].pos[0] - inf_2.pos[0])
            theta_2 = math.atan(k_2)
            if (con_loc[0].pos[0] - inf_2.pos[0] < 0): theta_2 = math.pi + theta_2
            dire_first_x = 0.75* math.cos(theta_1) + 0.25 * math.cos(theta_2)
            dire_first_y = 0.75* math.sin(theta_1) + 0.25 * math.sin(theta_2)
        elif (loc_index >= 3):
            k_1 = (con_loc[(loc_index - 1) % 3].pos[1] - inf_2.pos[1])/(con_loc[(loc_index - 1) % 3].pos[0] - inf_2.pos[0])
            theta_1 = math.atan(k_1)
            if (con_loc[(loc_index - 1) % 3].pos[0] - inf_2.pos[0] < 0): theta_1 = math.pi + theta_1
            k_2 = (con_loc[(loc_index - 2) % 3].pos[1] - inf_2.pos[1])/(con_loc[(loc_index - 2) % 3].pos[0] - inf_2.pos[0])
            theta_2 = math.atan(k_2)
            if (con_loc[(loc_index - 2) % 3].pos[0] - inf_2.pos[0] < 0): theta_2 = math.pi + theta_2
            k_3 = (con_loc[(loc_index - 3) % 3].pos[1] - inf_2.pos[1])/(con_loc[(loc_index - 3) % 3].pos[0] - inf_2.pos[0])
            theta_3 = math.atan(k_3)
            if (con_loc[(loc_index - 3) % 3].pos[0] - inf_2.pos[0] < 0): theta_3 = math.pi + theta_3
            dire_first_x = 0.6* math.cos(theta_1) + 0.3 * math.cos(theta_2) + 0.1 *math.cos(theta_3)
            dire_first_y = 0.6* math.sin(theta_1) + 0.3 * math.sin(theta_2) + 0.1 *math.sin(theta_3)
        
        dire_second_x = 0
        dire_second_y = 0
        if (index_1 == 0):
            k_1 = (car_2_info[0].pos[1] - inf_2.pos[1])/(car_2_info[0].pos[0] - inf_2.pos[0])
            theta_1 = math.atan(k_1)
            if (car_2_info[0].pos[0] - inf_2.pos[0] < 0): theta_1 = math.pi + theta_1
            dire_second_x = math.cos(theta_1)
            dire_second_y = math.sin(theta_1)
        elif (index_1 == 1):
            k_1 = (car_2_info[0].pos[1] - inf_2.pos[1])/(car_2_info[0].pos[0] - inf_2.pos[0])
            theta_1 = math.atan(k_1)
            if (car_2_info[0].pos[0] - inf_2.pos[0] < 0): theta_1 = math.pi + theta_1
            k_2 = (car_2_info[1].pos[1] - inf_2.pos[1])/(car_2_info[1].pos[0] - inf_2.pos[0])
            theta_2 = math.atan(k_2)
            if (car_2_info[1].pos[0] - inf_2.pos[0] < 0): theta_2 = math.pi + theta_2
            dire_second_x = 0.75 *math.cos(theta_1) + 0.25 *math.cos(theta_2)
            dire_second_y = 0.75 *math.sin(theta_1) + 0.25 *math.sin(theta_2)
        else:
            k_1 = (car_2_info[0].pos[1] - inf_2.pos[1])/(car_2_info[0].pos[0] - inf_2.pos[0])
            theta_1 = math.atan(k_1)
            if (car_2_info[0].pos[0] - inf_2.pos[0] < 0): theta_1 = math.pi + theta_1
            k_2 = (car_2_info[1].pos[1] - inf_2.pos[1])/(car_2_info[1].pos[0] - inf_2.pos[0])
            theta_2 = math.atan(k_2)
            if (car_2_info[1].pos[0] - inf_2.pos[0] < 0): theta_2 = math.pi + theta_2
            k_3 = (car_2_info[2].pos[1] - inf_2.pos[1])/(car_2_info[2].pos[0] - inf_2.pos[0])
            theta_3 = math.atan(k_3)
            if (car_2_info[2].pos[0] - inf_2.pos[0] < 0): theta_3 = math.pi + theta_3
            dire_second_x = 0.6 *math.cos(theta_1) + 0.3 *math.cos(theta_2) + 0.1*math.cos(theta_3)
            dire_second_y = 0.6 *math.sin(theta_1) + 0.3 *math.sin(theta_2) + 0.1*math.sin(theta_3)

        
        if inf_1.gas_conc > inf_2.gas_conc:
            k = (car_1_info[0].pos[1] - inf_2.pos[1])/(car_1_info[0].pos[0] - inf_2.pos[0])
            theta = math.atan(k)
            if (car_1_info[0].pos[0] - inf_2.pos[0] < 0): theta = math.pi + theta
            dire_x = 0.05 *(19 - i) * dire_first_x + 0.05 * (i + 1) * 0.5 *dire_second_x + 0.5 * 0.05 * (i + 1) *math.cos(theta)
            dire_y = 0.05 *(19 - i) * dire_first_y + 0.05 * (i + 1) * 0.5 *dire_second_y + 0.5 * 0.05 * (i + 1) *math.sin(theta)
            theta_final = math.atan(dire_y/dire_x)
            if (dire_x < 0):
                theta_final = math.pi + theta_final
            theta_final = -theta_final
            if (theta_final < 0): theta_final = 2*math.pi + theta_final
            return theta_final
        else :
            dire_x = 0.05 *(19 - i) * dire_first_x + 0.05 * (i + 1) *dire_second_x
            dire_y = 0.05 *(19 - i) * dire_first_y + 0.05 * (i + 1) *dire_second_y
            theta_final = math.atan(dire_y/dire_x)
            if (dire_x < 0):
                theta_final = math.pi + theta_final
            theta_final = -theta_final
            if (theta_final < 0): theta_final = 2*math.pi + theta_final
            return theta_final


    rclpy.init(args=None)
    # if __name__=="__main__":
    car_1 = Utils()
    car_2 = Utils()
    for i in range (10): # 由于一开始生成在同一点，因此我让他随机游走 10 步
        rotate_1(random.random())
        rotate_2(random.random())
        forward_1(random.random())
        forward_2(random.random())
        modify_car_1_info(car_1.get_info())
        modify_car_2_info(car_2.get_info())
    for i in range (20):
        inf_1 = car_1.get_info()
        inf_2 = car_2.get_info()
        num_1 = Circle_1()
        num_2 = Circle_2()
        theta_1 = -(math.pi/3 * num_1 + inf_1.orien)
        theta_2 = -(math.pi/3 * num_2 + inf_2.orien)
        x = (inf_1.pos[1] - inf_2.pos[1] + math.tan(theta_2) * inf_2.pos[0] + math.tan(theta_1) * inf_1.pos[0])/(math.tan(theta_2) - math.tan(theta_1))
        y = (math.tan(theta_1) * (x - inf_1.pos[0])) + inf_1.pos[1]
        if x < 2 and x > -2 and y < 2 and y > -2 :
            con_loc[loc_index % 3].pos[0] = x
            con_loc[loc_index % 3].pos[1] = y
            loc_index = loc_index + 1
        ori_1 = Cal_dire_1(i)
        ori_2 = Cal_dire_2(i)
        if (ori_1 > inf_1.orien):
            rotate_1((ori_1-inf_1.orien)/(2*math.pi))
        else:
            rotate_1((ori_1-inf_1.orien + 2*math.pi)/(2*math.pi))
        if (ori_2 > inf_2.orien):
            rotate_2((ori_2-inf_2.orien)/(2*math.pi))
        else:
            rotate_2((ori_2-inf_2.orien + 2*math.pi)/(2*math.pi))
        forward_1(1)
        forward_2(1)
        modify_car_1_info(car_1.get_info())
        modify_car_2_info(car_2.get_info())

    loc_index = 0 # 不需要模型了
    rdm_1 = 0 #是否需要大肠杆菌随机
    rdm_2 = 0
    for i in range(20):
        inf_1 = car_1.get_info()
        inf_2 = car_2.get_info()
        ori_1 = Cal_dire_1(19) + rdm_1 * 2* (random.random()-0.5) *math.pi/6 # 不需要模型了
        ori_2 = Cal_dire_2(19) + rdm_2 * 2* (random.random()-0.5) *math.pi/6
        if (ori_1 > inf_1.orien):
            rotate_1((ori_1-inf_1.orien)/(2*math.pi))
        else:
            rotate_1((ori_1-inf_1.orien + 2*math.pi)/(2*math.pi))
        if (ori_2 > inf_2.orien):
            rotate_2((ori_2-inf_2.orien)/(2*math.pi))
        else:
            rotate_2((ori_2-inf_2.orien + 2*math.pi)/(2*math.pi))
        forward_1(1)
        forward_2(1)
        con_max_1 = car_1_info[0].gas_conc
        con_max_2 = car_2_info[0].gas_conc
        modify_car_1_info(car_1.get_info())
        modify_car_2_info(car_2.get_info())
        if (con_max_1 == car_1_info[0].gas_conc):
            rdm_1 = 1
        else:
            rdm_1 = 0
        if (con_max_2 == car_2_info[0].gas_conc):
            rdm_2 = 1
        else:
            rdm_2 = 0
    if (car_1_info[0].gas_conc > car_2_info[0].gas_conc): #输出最大的浓度坐标
        print(car_1_info[0].pos[0],car_1_info[0].pos[1])
    else:
        print(car_2_info[0].pos[0],car_2_info[0].pos[1])
    rclpy.shutdown()
