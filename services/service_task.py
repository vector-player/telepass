# -*- coding: UTF-8 -*-



class Task_tool:
    
    @staticmethod
    def clear_port(port:int):        
        
        import os
        import re
 
        # port = 8080
    
    
        ret = os.popen("netstat -nao|findstr " + str(port))
        
        ## Be adviced: decode in 'gbk' as the same as CMD to avoid messy code.
        # str_list = ret.read().decode('gbk')  ## Error in Python3, str already decoded
        str_list = ret.read().encode().decode('gbk') ## fit for boths python2 | 3
        # str_list = ret.read()  
        if str_list == "" : return      
        print('Clearing port:', str_list)
        ret_list = re.split(' ', str_list)
        print('Clearing port:', ret_list)
        try:
            # process_pid = list(ret_list[0].split())[-1]
            process_pid = ret_list[-1].split('\n')[0]
            os.popen('taskkill /pid ' + str(process_pid) + ' /F')
            # print("port is already released.")
            print('Clearing task:', process_pid, 'has been terminated.')
            print('Clearing port:', port,'has been released.')
        except Exception as e:
            # print("port is not using.")
            print('Clearing port:', port, 'is not using.')
            print('More detail:',e)
            
            
    if __name__ == '__main__':
        clear_port(18861)
    
    # output1 = os.popen('ipconfig')
    # print output1.read().decode('gbk')