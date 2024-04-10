studentEmail = []
studentName = []
password_string = "0123456789"
passwords = []

def createEmailsNames():
    for i in range(0,10):
        studentEmail.append("S3987749"+str(i)+"@student.rmit.edu.au")
        studentName.append("Ajahn Tundla"+str(i))

def createPasswords():
    for x in range(0,10):
        passwords.append(password_string[0:6])
        init_letter = password_string[0]
        password_string = password_string[1:]
        password_string = password_string+init_letter


# print(passwords)
# print(studentEmail)
# print(studentName)