class Employee:
    __empName = "";
    __empAge = 0;

    def __init__(self,name,age):
        self.empAge = age
        self.empName = name
    def __str__(self):
        return "Employee name=%s,age=%d" % (self.empName,self.empAge)

if __name__ == '__main__':
    emp = Employee("tom",20)
    print(emp.empName,emp.empAge)