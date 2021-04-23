import pymysql
import IPy
import queue
import threading
import getopt
import sys


class MysqlScanner(object):
    def __init__(self):
        self.q = queue.Queue()
        self.lock = threading.Lock()

        self.port = port
        self.thread = thread
        self.timeout = timeout
        self.outfile = savefile

    def getIpList(self, ipcmd):
        errMsg = '\n参数格式错误，请参照以下用法:\n' \
                 '-h 192.168.1.1   单个地址\n' \
                 '-h 192.168.1.1/16    掩码网段地址\n' \
                 '-h ip.txt    地址文件\n'
        ip_list = []
        if ".txt" in ipcmd:
            try:
                ip_file = open(ipcmd, "r", encoding="utf8")
                for ip in ip_file:
                    ip_list.append(ip.strip())
                ip_file.close()
            except FileNotFoundError:
                print("\nIP地址文件 %s 不存在！\n" % ipcmd)
                exit()
        elif '/' in ipcmd:
            ips = IPy.IP(ipcmd)
            for ip in ips:
                ip_list.append(ip)
        else:
            if "." in ipcmd:
                if len(ipcmd.split('.')) == 4:
                    ip_list.append(ipcmd)
                else:
                    print(errMsg)
                    exit()
            else:
                print(errMsg)
                exit()

        return ip_list

    def getUserList(self, usercmd):
        user_list = []
        if ".txt" in usercmd:
            try:
                user_file = open(usercmd, "r", encoding="utf8")
                for user in user_file:
                    user_list.append(user.strip())
                user_file.close()
            except FileNotFoundError:
                print("\n用户名文件 %s 不存在！\n" % usercmd)
                exit()
        else:
            user_list.append(usercmd)

        return user_list

    def getPassList(self, passcmd):
        pass_list = []
        if ".txt" in passcmd:
            try:
                pass_file = open(passcmd, "r", encoding="utf8")
                for pwd in pass_file:
                    if pwd.strip() == "空":
                        pass_list.append(' ')  # 添加空密码
                    else:
                        pass_list.append(pwd.strip())
                pass_file.close()
            except FileNotFoundError:
                print("\n密码文件 %s 不存在！\n" % passcmd)
                exit()
        else:
            pass_list.append(passcmd)

        return pass_list

    def prepareQueue(self, users, pwds):
        for user in users:
            for pwd in pwds:
                self.q.put(user + ":" + pwd)

    def connect(self, ip):
        while not self.q.empty():
            username, password = self.q.get().split(':')

            try:
                pymysql.connect(host=ip, user=username, passwd=password, port=self.port, connect_timeout=0.1)
                self.lock.acquire()
                print("----- Success connected. (IP: %s, User: %s, Pass: %s)" % (ip, username, password))
                with open(self.outfile, 'a') as f:
                    f.write(ip + ":" + str(port) + "\t" + username + "\t" + password + "\n")
                self.lock.release()
            except Exception as e:
                if printall:
                    self.lock.acquire()
                    print("Failed connected. (IP: %s, User: %s, Pass: %s)" % (ip, username, password))
                    self.lock.release()
                else:
                    pass

    def scanner(self, ip):
        t_wait = []
        for i in range(self.thread):
            t = threading.Thread(target=self.connect, args=(ip,))
            t_wait.append(t)
            t.setDaemon(True)
            t.start()

        for t in t_wait:
            t.join()


if __name__ == '__main__':

    ipcmd = "ip.txt"
    port = 3306
    usercmd = "user.txt"
    passcmd = "pass.txt"

    thread = 12
    timeout = 1.0
    savefile = "result.txt"
    printall = 0

    opts, args = getopt.getopt(sys.argv[1:], "hH:u:p:P:T:t:s:a:")
    for opt, arg in opts:
        if opt == '-h':
            print("""
    __  ___                 _______                                 
   /  |/  /_  ___________ _/ / ___/_________ _____  ____  ___  _____
  / /|_/ / / / / ___/ __ `/ /\__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
 / /  / / /_/ (__  ) /_/ / /___/ / /__/ /_/ / / / / / / /  __/ /    
/_/  /_/\__, /____/\__, /_//____/\___/\__,_/_/ /_/_/ /_/\___/_/     
       /____/        /_/    

\t -H\t 主机地址，有以下三种方式：
\t \t 192.168.1.1   单个地址
\t \t 192.168.1.1/16    掩码网段地址
\t \t ip.txt    地址文件
\t -u\t 用户文件或单个用户 [默认：user.txt] 
\t -p\t 密码文件或单个密码 [默认：pass.txt] 
\t -P\t 端口号 [默认：3306] 
\t -T\t 线程数量 [默认：12] 
\t -t\t 连接超时 [默认：1.0s] 
\t -s\t 保存结果 [默认：result.txt] 
\t -a\t 打印模式 [默认：0 不显示失败结果]
""")
            exit()
        elif opt == '-H':
            ipcmd = arg
        elif opt == '-u':
            usercmd = arg
        elif opt == '-p':
            passcmd = arg
        elif opt == '-P':
            port = int(arg)
        elif opt == '-T':
            thread = int(arg)
        elif opt == '-t':
            timeout = float(arg)
        elif opt == '-s':
            savefile = arg
        elif opt == '-a':
            printall = int(arg)

    ms = MysqlScanner()
    ips = ms.getIpList(ipcmd)
    users = ms.getUserList(usercmd)
    pwds = ms.getPassList(passcmd)

    for ip in ips:
        ms.prepareQueue(users, pwds)
        ms.scanner(ip)