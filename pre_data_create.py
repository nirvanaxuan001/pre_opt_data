'''
Created on 2016-6-12

@author: Xuan Zhang
'''

'''
File{
    key  path
    value {
        start create_index
        end   del_index
        length file_size
    }
}
output:
Index{
    key line_number
    value opts
}
'''
from config import *
import random,string
import numpy as np
import scipy.stats as stats



def find_all_index(arr,item):
    return [i for i,a in enumerate(arr) if a==item]
def index_check(*idx):            #Placeholder     len(idx)>=1 <=2
    if len(idx)==1:
        if index[idx[0]]!=0:
            return False
        else:
            index[idx[0]]=1
            return True
    else:
        if index[idx[0]]!=0 or index[idx[1]]!=0:
            return False
        else:
            index[idx[0]]=1
            index[idx[1]]=1
            return True
def random_file_path(name_length=8):       # name_length str
    a=list(string.ascii_letters)
    random.shuffle(a)
    return ''.join(a[:name_length])

'''
create
'''
def dir_threshold_creater():
    while True:
        dir_name = random_file_path()
        if dir_map.get(dir_name,-1)==-1:
            break
    count=5
    while True:
        if count<0:
            return 0
        count-=1
        start=random.choice(find_all_index(index, 0))
        end=random.choice(find_all_index(index, 0))
        if end-start>line_num/2 and index_check(start,end):
            break
    dir_map[dir_name]=[start,end]
    return dir_name,start,end
def file_threshold_creater(dir_name,ds,de):
    while True:
        file_name = random_file_path()
        if dir_name =="/":
            k=file_name
        else:
            k=dir_name+"/"+file_name
        if file_map.get(k,-1)==-1:
            break
    count = 5
    while True:
        if count<0:
            return 0
        count-=1
        start=random.choice([i for i in find_all_index(index, 0) if i>ds and i<de])
        end=random.choice([i for i in find_all_index(index, 0) if i>ds and i<de])
        if end-start>(ds-de)/2 and index_check(start,end):
            break
    file_map[k]=[start,end,0]
    return k,start,end
'''
rename
'''
def dir_rename(old,new):
    while True:
        rename_loc=random.randrange(dir_map[old][0],dir_map[old][1])
        if index_check(rename_loc):
            break
    end = dir_map[old][1]
    dir_map[old][1]=rename_loc-1
    dir_map[new] = [rename_loc+1,end]
    rename[rename_loc]=[old,new]
def file_rename(old,new):
    while True:
        rename_loc=random.randrange(dir_map[old][0],dir_map[old][1])
        if index_check(rename_loc):
            break
    end = file_map[old][1]
    file_map[old][1]=rename_loc-1
    file_map[new] = [rename_loc+1,end]
    rename[rename_loc]=[old,new]
'''read'''
def read_opt_creater(low,high):                          #  low = [low|loc]  high = [high|read_size]
    if type(high)!=list:
        files = [k for k in file_map if file_map[k][2]>=low]
        if files !=[]:
            count=0
            while count<10:
                file_name = random.choice(files)           
                start = file_map[file_name][0]
                end = file_map[file_name][1]
                length = file_map[file_name][2]
                locs= [i for i in find_all_index(index,0) if i>start and i<end]
                if locs !=[]:
                    loc= random.choice(locs)
                    if index_check(loc):
                        size = random.randrange(low,high)
                        read[loc] = [file_name,size]
                        file_map[file_name][2]= size
                        break
                count+=1
        else:
            print 'no fit file %d'%low
    else:
        for k in file_map:
            if file_map[k][0]<low and file_map[k][1]>low:
                if index_check(low):
                    read[low]=[k,high.pop(0)] 
                    break
'''write'''
def write_opt_creater(low,high):
    if type(high)!=list:
        file_name = random.choice(file_map_w.keys())
        start = file_map[file_name][0]
        end = file_map[file_name][1]
        length = file_map[file_name][2]
        loc = random.choice(find_all_index(index[start:end],0))
        if index_check(loc):
            size = random.randrange(low,high)
            write[loc] = [file_name,size]
            file_map[file_name][2]= size
    else:
        for k in file_map_w:
            if file_map_w[k][0]<low and file_map_w[k][1]>low:
                if index_check(low):
                    write[low]=[k,high.pop(0)] 
                    break
def read_file_init(file_name,size):
    start = file_map[file_name][0]
    end = file_map[file_name][1]
    length = file_map[file_name][2]
    count=1
    error = 1
    while count<10 :
        if index_check(start+count):
            error=0
            break
        count+=1
    if error == 0:
        write[start+count] = [file_name,size]
        file_map[file_name][2]=size
    else:
        return True
    
if __name__ == "__main__":  
    config_file_path = 'conf.ini'

    src_path = read_config(config_file_path,'common','src_path')
    line_num = int(read_config(config_file_path,'common','line_num'))
    file_num = int(read_config(config_file_path,'common','file_num'))
    r = int(read_config(config_file_path,'read','read_frequency'))
    w = int(read_config(config_file_path,'write','write_frequency'))
    order = int(read_config(config_file_path,'read','read_size_order'))
    



    file_map = {}
    file_map_w ={}
    dir_map = {}
    read ={}
    write={}
    rename = {}
    index=[0]*line_num
    
    
    
    print 'a'
    dir_num = file_num/10                                                           #create  form
    dir_map['/']=[0,line_num]
    for i in range(dir_num):
        dir_threshold_creater()
#    for i in range(random.randrange(dir_num)):
#        dir_rename(random.choice(dir_map.keys()),random_file_path())   
    count = file_num                                                                #create file               
    while(count>1):
        for k in dir_map:
            for i in range(random.randrange(count)):
                file_threshold_creater(k,dir_map[k][0],dir_map[k][1])
                count-=1
    for i in range(len(file_map.keys())*w/(w+r)):                                   #divide read and write
        name = random.choice(file_map.keys())
        file_map_w[name] = file_map.pop(name)
    print 'devide done'
    #read init
    for file_name in file_map:
        if read_file_init(file_name, 1024*pow(2,order)):
            print 'no loc'
    print 'read init done'
    print sum(index)
    # calculate probability
    x= np.arange(0,order,1)
    y = stats.lognorm.cdf(x,1)
    prob = map(lambda a,b:b-a,y[:-1],y[1:])
    num = len(find_all_index(index[find_all_index(index, 1)[1]:find_all_index(index, 1)[-1]],0))
    read_num = num*r/(w+r)
    write_num = num-read_num
    #read create
    print 'create read opt ing'
    read_size=[]
    for i in range(1,order):
        low = 1024*pow(2,i-1)
        n =int(read_num*prob[i-1])
        for j in range(n):
            read_size.append(low)
    tmp=[i for i in find_all_index(index,0) if i>find_all_index(index, 1)[1] and i<find_all_index(index, 1)[-1]]
    id=random.sample(tmp,len(read_size))
    for i in id:
        read_opt_creater(i, read_size)
    # write create
    print 'create  write opt ing'
    x= np.arange(0,order,1)
    y= stats.zipf.cdf(x,2)
    zipf = map(lambda a,b:b-a,y[:-1],y[1:])
    write_size = []
    for i in range(1,order):
        low = 1024*pow(2,i-1)
        n =int(write_num*zipf[i-1])
        for j in range(n):
            write_size.append(low)
    tmp=[i for i in find_all_index(index,0) if i>find_all_index(index, 1)[1] and i<find_all_index(index, 1)[-1]] 
    for i in tmp[:len(write_size)]:
        write_opt_creater(i, write_size)
    print 'write done'
#    print len(read)
#    print len(write)
#    print sum(index)
    print 'create all map'
    null_id=find_all_index(index,0)
    all_map  = {}
    for id in null_id:
        all_map[id] = ['create','file',random_file_path(9)]
#    for rf in rename:
#        all_map[rf] =['rename',rename[rf][0],rename[rf][1]]
    for dir in dir_map:
        start= dir_map[dir][0]
        end = dir_map[dir][1]
        all_map[start] = ['create','dir',dir]
        all_map[end] = ['del','dir',dir]
    for rf in file_map:
        start =file_map[rf][0]
        end =file_map[rf][1]
        all_map[start]= ['create','file',rf]
        all_map[end]= ['del','file',rf]
    for rf in file_map_w:
        start = file_map_w[rf][0]
        end =file_map_w[rf][1]
        all_map[start] = ['create','file',rf]
        all_map[end] = ['del','file',rf]
    for wf in write:
        all_map[wf] = ['write',write[wf][0],write[wf][1]]
    for rf in read:
        all_map[rf] = ['read',read[rf][0],read[rf][1]]
    print 'write to file'    
    f= open('out.txt','w')
    for i in all_map:
        line = ''
        for s in all_map[i]:
            line += (str(s)+'\t')
        line+='\n'
        f.write(line)
    f.close()